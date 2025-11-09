"""
Assembly System
Automatically aligns, checks fit, and assembles aircraft components
"""

import logging
from typing import Dict, Any, List, Tuple, Optional
import numpy as np
import cadquery as cq
from app.core.config import settings

logger = logging.getLogger(__name__)


class Assembler:
    """Assemble aircraft components with automatic alignment"""

    def __init__(self):
        self.tolerance_mm = settings.ASSEMBLY_TOLERANCE_MM

    async def create_assembly(
        self,
        components: List[Dict[str, Any]]
    ) -> Tuple[cq.Assembly, Dict[str, Any]]:
        """
        Create assembly from components

        Args:
            components: List of components with models and metadata

        Returns:
            Tuple of (Assembly, results)
        """
        logger.info(f"Creating assembly from {len(components)} components")

        assembly = cq.Assembly()
        results = {
            "success": True,
            "components_added": 0,
            "interferences": [],
            "warnings": [],
            "metadata": {}
        }

        try:
            # Organize components by type
            organized = self._organize_components(components)

            # Add fuselage first (reference)
            if "fuselage" in organized:
                fuselage = organized["fuselage"][0]
                assembly.add(
                    fuselage["model"],
                    name="fuselage",
                    color=cq.Color("lightgray")
                )
                results["components_added"] += 1

            # Attach wings
            if "wing" in organized:
                for idx, wing in enumerate(organized["wing"]):
                    position = await self._calculate_wing_position(
                        wing, organized.get("fuselage", [{}])[0]
                    )
                    assembly.add(
                        wing["model"],
                        name=f"wing_{idx}",
                        loc=cq.Location(cq.Vector(*position)),
                        color=cq.Color("blue")
                    )
                    results["components_added"] += 1

            # Attach tail
            if "tail" in organized:
                for idx, tail in enumerate(organized["tail"]):
                    position = await self._calculate_tail_position(
                        tail, organized.get("fuselage", [{}])[0]
                    )
                    assembly.add(
                        tail["model"],
                        name=f"tail_{idx}",
                        loc=cq.Location(cq.Vector(*position)),
                        color=cq.Color("red")
                    )
                    results["components_added"] += 1

            # Attach engines
            if "engine_nacelle" in organized:
                for idx, engine in enumerate(organized["engine_nacelle"]):
                    position = await self._calculate_engine_position(
                        engine, organized.get("wing", [{}])[0], idx
                    )
                    assembly.add(
                        engine["model"],
                        name=f"engine_{idx}",
                        loc=cq.Location(cq.Vector(*position)),
                        color=cq.Color("gray")
                    )
                    results["components_added"] += 1

            # Attach landing gear
            if "landing_gear" in organized:
                for idx, gear in enumerate(organized["landing_gear"]):
                    position = await self._calculate_landing_gear_position(
                        gear, organized.get("fuselage", [{}])[0], idx
                    )
                    assembly.add(
                        gear["model"],
                        name=f"landing_gear_{idx}",
                        loc=cq.Location(cq.Vector(*position)),
                        color=cq.Color("black")
                    )
                    results["components_added"] += 1

            # Check for interferences
            interferences = await self._check_interferences(assembly)
            results["interferences"] = interferences
            results["has_interferences"] = len(interferences) > 0

            if results["has_interferences"]:
                results["warnings"].append(
                    f"Found {len(interferences)} interference(s)"
                )

            logger.info(
                f"Assembly created: {results['components_added']} components, "
                f"{len(interferences)} interferences"
            )

            return assembly, results

        except Exception as e:
            logger.error(f"Error creating assembly: {e}")
            results["success"] = False
            results["error"] = str(e)
            return assembly, results

    def _organize_components(
        self,
        components: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Organize components by type"""
        organized = {}
        for component in components:
            comp_type = component.get("component_type", "unknown")
            if comp_type not in organized:
                organized[comp_type] = []
            organized[comp_type].append(component)
        return organized

    async def _calculate_wing_position(
        self,
        wing: Dict[str, Any],
        fuselage: Dict[str, Any]
    ) -> Tuple[float, float, float]:
        """Calculate wing mounting position on fuselage"""
        # Default: mid-fuselage, top-mounted
        fuselage_params = fuselage.get("parameters", {})
        wing_params = wing.get("parameters", {})

        # X: typically 30-40% of fuselage length from nose
        fuselage_length = fuselage_params.get("length_m", 20.0) * 1000
        x_pos = fuselage_length * 0.35

        # Y: centered
        y_pos = 0.0

        # Z: on top of fuselage
        fuselage_diameter = fuselage_params.get("diameter_m", 3.0) * 1000
        z_pos = fuselage_diameter / 2

        # Check for wing mounting type
        wing_mount = wing_params.get("mounting", "high")  # high, mid, low
        if wing_mount == "mid":
            z_pos = 0
        elif wing_mount == "low":
            z_pos = -fuselage_diameter / 2

        logger.info(f"Wing position: ({x_pos}, {y_pos}, {z_pos})")
        return (x_pos, y_pos, z_pos)

    async def _calculate_tail_position(
        self,
        tail: Dict[str, Any],
        fuselage: Dict[str, Any]
    ) -> Tuple[float, float, float]:
        """Calculate tail mounting position"""
        fuselage_params = fuselage.get("parameters", {})

        # X: at rear of fuselage
        fuselage_length = fuselage_params.get("length_m", 20.0) * 1000
        x_pos = fuselage_length * 0.9

        # Y: centered
        y_pos = 0.0

        # Z: depends on tail type
        tail_type = tail.get("parameters", {}).get("type", "conventional")
        fuselage_diameter = fuselage_params.get("diameter_m", 3.0) * 1000

        if tail_type == "T-tail":
            z_pos = fuselage_diameter  # High mounted
        else:
            z_pos = fuselage_diameter / 4  # Slightly above fuselage centerline

        logger.info(f"Tail position: ({x_pos}, {y_pos}, {z_pos})")
        return (x_pos, y_pos, z_pos)

    async def _calculate_engine_position(
        self,
        engine: Dict[str, Any],
        wing: Dict[str, Any],
        engine_index: int
    ) -> Tuple[float, float, float]:
        """Calculate engine mounting position"""
        wing_params = wing.get("parameters", {})
        engine_params = engine.get("parameters", {})

        # Get engine mounting type
        mount_type = engine_params.get("mounting", "underwing")  # underwing, wing, fuselage

        wingspan = wing_params.get("wingspan_m", 10.0) * 1000
        root_chord = wing_params.get("root_chord_m", 2.0) * 1000

        # X: typically at 40% chord
        x_pos = root_chord * 0.4

        # Y: position along span (symmetric)
        # For twin engines: ±40% semi-span
        semi_span = wingspan / 2
        y_offset = semi_span * 0.4
        y_pos = y_offset if engine_index == 0 else -y_offset

        # Z: below wing
        z_pos = -1000  # 1m below wing

        logger.info(f"Engine {engine_index} position: ({x_pos}, {y_pos}, {z_pos})")
        return (x_pos, y_pos, z_pos)

    async def _calculate_landing_gear_position(
        self,
        gear: Dict[str, Any],
        fuselage: Dict[str, Any],
        gear_index: int
    ) -> Tuple[float, float, float]:
        """Calculate landing gear position"""
        fuselage_params = fuselage.get("parameters", {})
        gear_params = gear.get("parameters", {})

        fuselage_length = fuselage_params.get("length_m", 20.0) * 1000
        fuselage_diameter = fuselage_params.get("diameter_m", 3.0) * 1000
        gear_type = gear_params.get("gear_type", "tricycle")

        if gear_type == "tricycle":
            if gear_index == 0:  # Nose gear
                x_pos = fuselage_length * 0.1
                y_pos = 0
                z_pos = -fuselage_diameter / 2 - 2000  # Below fuselage
            else:  # Main gear
                x_pos = fuselage_length * 0.5
                y_offset = fuselage_diameter * 1.5
                y_pos = y_offset if gear_index == 1 else -y_offset
                z_pos = -fuselage_diameter / 2 - 2000
        else:  # Tail dragger
            if gear_index == 0:  # Tail wheel
                x_pos = fuselage_length * 0.95
                y_pos = 0
                z_pos = -fuselage_diameter / 2 - 500
            else:  # Main gear
                x_pos = fuselage_length * 0.4
                y_offset = fuselage_diameter * 1.5
                y_pos = y_offset if gear_index == 1 else -y_offset
                z_pos = -fuselage_diameter / 2 - 2000

        logger.info(f"Landing gear {gear_index} position: ({x_pos}, {y_pos}, {z_pos})")
        return (x_pos, y_pos, z_pos)

    async def _check_interferences(
        self,
        assembly: cq.Assembly
    ) -> List[Dict[str, Any]]:
        """
        Check for component interferences

        Returns:
            List of interference reports
        """
        logger.info("Checking for component interferences")
        interferences = []

        # This would use actual collision detection
        # For now, return empty list
        # TODO: Implement proper interference checking using:
        # - Bounding box overlap
        # - Mesh intersection
        # - Volume calculation

        return interferences

    async def optimize_assembly(
        self,
        assembly: cq.Assembly,
        constraints: Dict[str, Any]
    ) -> cq.Assembly:
        """
        Optimize assembly based on constraints

        Args:
            assembly: Current assembly
            constraints: Optimization constraints (CG position, balance, etc.)

        Returns:
            Optimized assembly
        """
        logger.info("Optimizing assembly")

        # Would implement optimization here:
        # - Adjust component positions for optimal CG
        # - Balance weight distribution
        # - Minimize interference
        # - Satisfy aerodynamic constraints

        return assembly

    async def generate_assembly_instructions(
        self,
        assembly: cq.Assembly
    ) -> List[Dict[str, Any]]:
        """Generate step-by-step assembly instructions"""
        instructions = []

        # Extract assembly sequence
        # Generate installation steps
        # Include torque specs, fasteners, etc.

        return instructions
