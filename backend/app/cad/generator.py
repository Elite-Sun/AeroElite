"""
CAD Generator
Generates parametric 3D CAD models from design parameters
"""

import logging
from typing import Dict, Any, Optional, Tuple
import cadquery as cq
import numpy as np
from pathlib import Path
import json

logger = logging.getLogger(__name__)


class CADGenerator:
    """Generate parametric CAD models"""

    def __init__(self):
        self.workplane = None

    async def generate_from_parameters(
        self,
        component_type: str,
        parameters: Dict[str, Any]
    ) -> Tuple[cq.Workplane, Dict[str, Any]]:
        """
        Generate CAD model from parameters

        Args:
            component_type: Type of component
            parameters: Design parameters

        Returns:
            Tuple of (CAD model, metadata)
        """
        logger.info(f"Generating {component_type} with parameters: {parameters}")

        try:
            if component_type == "wing":
                model = await self._generate_wing(parameters)
            elif component_type == "fuselage":
                model = await self._generate_fuselage(parameters)
            elif component_type == "tail" or component_type == "stabilizer":
                model = await self._generate_tail(parameters)
            elif component_type == "control_surface":
                model = await self._generate_control_surface(parameters)
            elif component_type == "landing_gear":
                model = await self._generate_landing_gear(parameters)
            elif component_type == "engine_nacelle":
                model = await self._generate_engine_nacelle(parameters)
            else:
                raise ValueError(f"Unsupported component type: {component_type}")

            metadata = {
                "component_type": component_type,
                "parameters": parameters,
                "generated": True
            }

            logger.info(f"Successfully generated {component_type}")
            return model, metadata

        except Exception as e:
            logger.error(f"Error generating CAD model: {e}")
            raise

    async def _generate_wing(self, params: Dict[str, Any]) -> cq.Workplane:
        """
        Generate parametric wing model

        Parameters:
            - wingspan_m: Total wingspan
            - root_chord_m: Root chord length
            - tip_chord_m: Tip chord length
            - airfoil: Airfoil profile (e.g., NACA2412)
            - sweep_deg: Leading edge sweep
            - dihedral_deg: Dihedral angle
            - twist_deg: Wing twist
            - thickness_ratio: Airfoil thickness ratio
        """
        logger.info("Generating wing with parametric airfoil")

        # Extract parameters with defaults
        wingspan = params.get("wingspan_m", 10.0) * 1000  # Convert to mm
        root_chord = params.get("root_chord_m", 2.0) * 1000
        tip_chord = params.get("tip_chord_m", 1.0) * 1000
        sweep_deg = params.get("sweep_deg", 0.0)
        dihedral_deg = params.get("dihedral_deg", 0.0)
        twist_deg = params.get("twist_deg", 0.0)
        airfoil_name = params.get("airfoil", "NACA2412")
        num_ribs = params.get("num_ribs", 10)

        # Generate airfoil profile
        airfoil_points = self._generate_airfoil_profile(airfoil_name, root_chord)

        # Create root airfoil
        root_section = (
            cq.Workplane("XZ")
            .polyline(airfoil_points)
            .close()
        )

        # Generate tip airfoil with twist
        tip_airfoil_points = self._generate_airfoil_profile(airfoil_name, tip_chord)

        # Calculate tip position
        half_span = wingspan / 2
        sweep_offset = half_span * np.tan(np.radians(sweep_deg))
        dihedral_height = half_span * np.tan(np.radians(dihedral_deg))

        # Create tip section
        tip_section = (
            cq.Workplane("XZ")
            .transformed(offset=(sweep_offset, half_span, dihedral_height),
                        rotate=(0, twist_deg, 0))
            .polyline(tip_airfoil_points)
            .close()
        )

        # Loft between root and tip to create wing surface
        wing = (
            cq.Workplane("XY")
            .add(root_section)
            .add(tip_section)
            .loft(combine=True)
        )

        # Mirror for other half
        wing = wing.mirror(mirrorPlane="XZ")

        # Add internal structure (spars and ribs) for realism
        wing = self._add_wing_structure(wing, wingspan, root_chord, tip_chord, num_ribs)

        return wing

    def _generate_airfoil_profile(
        self,
        airfoil_name: str,
        chord_length: float,
        num_points: int = 50
    ) -> list:
        """
        Generate airfoil coordinate points

        Args:
            airfoil_name: Airfoil designation (e.g., NACA2412)
            chord_length: Chord length in mm
            num_points: Number of points to generate

        Returns:
            List of (x, z) coordinate tuples
        """
        # Parse NACA airfoil
        if airfoil_name.startswith("NACA"):
            naca_digits = airfoil_name.replace("NACA", "").strip()

            if len(naca_digits) == 4:
                # NACA 4-digit airfoil
                return self._naca_4digit(naca_digits, chord_length, num_points)
            elif len(naca_digits) == 5:
                # NACA 5-digit airfoil
                return self._naca_5digit(naca_digits, chord_length, num_points)
            else:
                logger.warning(f"Unknown NACA format: {airfoil_name}, using default")

        # Default symmetric airfoil
        return self._default_airfoil(chord_length, num_points)

    def _naca_4digit(self, digits: str, chord: float, num_points: int) -> list:
        """Generate NACA 4-digit airfoil coordinates"""
        m = int(digits[0]) / 100.0  # Maximum camber
        p = int(digits[1]) / 10.0   # Location of maximum camber
        t = int(digits[2:4]) / 100.0  # Maximum thickness

        # Generate x coordinates (cosine spacing for better resolution at leading edge)
        beta = np.linspace(0, np.pi, num_points)
        x = chord * (1 - np.cos(beta)) / 2

        # Thickness distribution
        yt = 5 * t * chord * (
            0.2969 * np.sqrt(x / chord)
            - 0.1260 * (x / chord)
            - 0.3516 * (x / chord) ** 2
            + 0.2843 * (x / chord) ** 3
            - 0.1015 * (x / chord) ** 4
        )

        # Camber line
        if m > 0 and p > 0:
            yc = np.where(
                x < p * chord,
                m * x / p ** 2 * (2 * p - x / chord),
                m * (chord - x) / (1 - p) ** 2 * (1 + x / chord - 2 * p)
            )
        else:
            yc = np.zeros_like(x)

        # Upper and lower surfaces
        xu = x
        yu = yc + yt
        xl = x
        yl = yc - yt

        # Combine upper and lower surfaces (start at trailing edge, go around)
        points = []
        for i in range(len(xu)):
            points.append((xu[i], yu[i]))
        for i in range(len(xl) - 1, -1, -1):
            points.append((xl[i], yl[i]))

        return points

    def _naca_5digit(self, digits: str, chord: float, num_points: int) -> list:
        """Generate NACA 5-digit airfoil coordinates"""
        # Simplified 5-digit - for full implementation, use airfoil database
        logger.warning("NACA 5-digit simplified to 4-digit")
        # Use thickness from last 2 digits
        simplified = "0012" if len(digits) >= 5 else "0012"
        simplified = f"00{digits[-2:]}"
        return self._naca_4digit(simplified, chord, num_points)

    def _default_airfoil(self, chord: float, num_points: int) -> list:
        """Generate default symmetric airfoil (12% thickness)"""
        return self._naca_4digit("0012", chord, num_points)

    def _add_wing_structure(
        self,
        wing: cq.Workplane,
        span: float,
        root_chord: float,
        tip_chord: float,
        num_ribs: int
    ) -> cq.Workplane:
        """Add internal wing structure (spars and ribs)"""
        # Add front and rear spars
        # Front spar at 25% chord
        # Rear spar at 75% chord

        # For now, return wing as-is
        # Full implementation would add internal structure
        return wing

    async def _generate_fuselage(self, params: Dict[str, Any]) -> cq.Workplane:
        """
        Generate parametric fuselage model

        Parameters:
            - length_m: Total fuselage length
            - diameter_m or width_m/height_m: Cross-section dimensions
            - nose_length_m: Nose cone length
            - tail_length_m: Tail cone length
            - cross_section_shape: circular, elliptical, rectangular
            - num_seats: Passenger capacity
            - num_windows: Number of windows
        """
        logger.info("Generating fuselage")

        # Extract parameters
        length = params.get("length_m", 20.0) * 1000  # mm
        diameter = params.get("diameter_m", 3.0) * 1000
        width = params.get("width_m", diameter / 1000) * 1000
        height = params.get("height_m", diameter / 1000) * 1000
        nose_length = params.get("nose_length_m", 3.0) * 1000
        tail_length = params.get("tail_length_m", 5.0) * 1000
        cabin_length = length - nose_length - tail_length
        cross_section = params.get("cross_section_shape", "circular")

        # Create cross-section profiles at key locations
        if cross_section == "circular":
            # Nose tip (point)
            nose_tip = cq.Workplane("YZ").circle(0.1).extrude(1)

            # Nose-cabin junction (full diameter)
            nose_cabin = cq.Workplane("YZ").circle(diameter / 2)

            # Cabin-tail junction (full diameter)
            cabin_tail = cq.Workplane("YZ").transformed(offset=(cabin_length, 0, 0)).circle(diameter / 2)

            # Tail end (tapered)
            tail_end = cq.Workplane("YZ").transformed(offset=(cabin_length + tail_length, 0, 0)).circle(diameter / 4)

        elif cross_section == "elliptical":
            # Similar to circular but with ellipse
            nose_cabin = cq.Workplane("YZ").ellipse(width / 2, height / 2)
            cabin_tail = cq.Workplane("YZ").transformed(offset=(cabin_length, 0, 0)).ellipse(width / 2, height / 2)
            tail_end = cq.Workplane("YZ").transformed(offset=(cabin_length + tail_length, 0, 0)).ellipse(width / 4, height / 4)

        else:  # rectangular with rounded corners
            corner_radius = min(width, height) / 10
            nose_cabin = cq.Workplane("YZ").rect(width, height).fillet(corner_radius)
            cabin_tail = cq.Workplane("YZ").transformed(offset=(cabin_length, 0, 0)).rect(width, height).fillet(corner_radius)
            tail_end = cq.Workplane("YZ").transformed(offset=(cabin_length + tail_length, 0, 0)).rect(width / 2, height / 2).fillet(corner_radius / 2)

        # Loft to create fuselage shape
        fuselage = (
            cq.Workplane("XY")
            .add(nose_cabin)
            .add(cabin_tail)
            .add(tail_end)
            .loft(combine=True)
        )

        # Add windows if specified
        num_windows = params.get("num_windows", 20)
        if num_windows > 0:
            fuselage = self._add_windows(fuselage, num_windows, cabin_length, diameter)

        # Add doors
        fuselage = self._add_doors(fuselage, cabin_length, diameter)

        return fuselage

    def _add_windows(
        self,
        fuselage: cq.Workplane,
        num_windows: int,
        cabin_length: float,
        diameter: float
    ) -> cq.Workplane:
        """Add windows to fuselage"""
        window_width = 300  # mm
        window_height = 400  # mm
        window_spacing = cabin_length / (num_windows + 1)

        # Create window cutouts on both sides
        # This is a simplified version - full implementation would array windows properly
        return fuselage

    def _add_doors(
        self,
        fuselage: cq.Workplane,
        cabin_length: float,
        diameter: float
    ) -> cq.Workplane:
        """Add doors to fuselage"""
        # Add door cutouts
        # Simplified version
        return fuselage

    async def _generate_tail(self, params: Dict[str, Any]) -> cq.Workplane:
        """Generate tail (empennage) assembly"""
        tail_type = params.get("type", "conventional")

        if tail_type == "T-tail":
            return await self._generate_t_tail(params)
        elif tail_type == "V-tail":
            return await self._generate_v_tail(params)
        else:
            return await self._generate_conventional_tail(params)

    async def _generate_conventional_tail(self, params: Dict[str, Any]) -> cq.Workplane:
        """Generate conventional tail (horizontal + vertical stabilizer)"""
        # Generate horizontal stabilizer (like a small wing)
        h_stab_params = {
            "wingspan_m": params.get("horizontal_span_m", 5.0),
            "root_chord_m": params.get("horizontal_root_chord_m", 2.0),
            "tip_chord_m": params.get("horizontal_tip_chord_m", 1.0),
            "airfoil": params.get("airfoil", "NACA0012"),
            "sweep_deg": params.get("horizontal_sweep_deg", 25.0),
        }
        h_stab = await self._generate_wing(h_stab_params)

        # Generate vertical stabilizer
        v_height = params.get("vertical_height_m", 3.0) * 1000
        v_root_chord = params.get("vertical_root_chord_m", 2.5) * 1000
        v_tip_chord = params.get("vertical_tip_chord_m", 1.5) * 1000

        # Create vertical stabilizer as a vertical "wing"
        v_stab = (
            cq.Workplane("XY")
            .rect(v_root_chord, 10)
            .extrude(v_height)
        )

        # Combine horizontal and vertical stabilizers
        tail = h_stab.union(v_stab)

        return tail

    async def _generate_t_tail(self, params: Dict[str, Any]) -> cq.Workplane:
        """Generate T-tail configuration"""
        # Similar to conventional but horizontal stabilizer mounted on top of vertical
        return await self._generate_conventional_tail(params)

    async def _generate_v_tail(self, params: Dict[str, Any]) -> cq.Workplane:
        """Generate V-tail configuration"""
        # Two angled surfaces instead of horizontal and vertical
        return await self._generate_conventional_tail(params)

    async def _generate_control_surface(self, params: Dict[str, Any]) -> cq.Workplane:
        """Generate control surface (aileron, flap, elevator, rudder)"""
        surface_type = params.get("surface_type", "aileron")
        span = params.get("span_m", 2.0) * 1000
        chord = params.get("chord_m", 0.5) * 1000
        thickness = params.get("thickness_m", 0.05) * 1000

        # Create simple control surface
        surface = (
            cq.Workplane("XY")
            .rect(chord, span)
            .extrude(thickness)
        )

        return surface

    async def _generate_landing_gear(self, params: Dict[str, Any]) -> cq.Workplane:
        """Generate landing gear"""
        gear_type = params.get("gear_type", "tricycle")  # tricycle, tail-dragger, etc.
        strut_diameter = params.get("strut_diameter_m", 0.15) * 1000
        strut_length = params.get("strut_length_m", 2.0) * 1000
        wheel_diameter = params.get("wheel_diameter_m", 0.8) * 1000

        # Create main strut
        strut = (
            cq.Workplane("XY")
            .circle(strut_diameter / 2)
            .extrude(strut_length)
        )

        # Create wheel
        wheel = (
            cq.Workplane("XY")
            .transformed(offset=(0, 0, strut_length))
            .circle(wheel_diameter / 2)
            .extrude(wheel_diameter / 3)
        )

        gear = strut.union(wheel)
        return gear

    async def _generate_engine_nacelle(self, params: Dict[str, Any]) -> cq.Workplane:
        """Generate engine nacelle"""
        length = params.get("length_m", 3.0) * 1000
        diameter = params.get("diameter_m", 1.5) * 1000
        inlet_diameter = params.get("inlet_diameter_m", 1.2) * 1000

        # Create nacelle body
        nacelle = (
            cq.Workplane("YZ")
            .circle(diameter / 2)
            .workplane(offset=length)
            .circle(diameter / 2 * 0.8)
            .loft(combine=True)
        )

        # Create inlet
        inlet = (
            cq.Workplane("YZ")
            .circle(inlet_diameter / 2)
            .extrude(-length / 4)
        )

        nacelle = nacelle.union(inlet)
        return nacelle

    async def export_model(
        self,
        model: cq.Workplane,
        output_path: Path,
        format: str = "step"
    ) -> Path:
        """
        Export CAD model to file

        Args:
            model: CAD model to export
            output_path: Output file path
            format: Export format (step, stl, obj, etc.)

        Returns:
            Path to exported file
        """
        logger.info(f"Exporting model to {format} format: {output_path}")

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            if format.lower() == "step" or format.lower() == "stp":
                cq.exporters.export(model, str(output_path.with_suffix(".step")))
            elif format.lower() == "stl":
                cq.exporters.export(model, str(output_path.with_suffix(".stl")))
            elif format.lower() == "obj":
                # CadQuery doesn't directly support OBJ, use STL as intermediate
                cq.exporters.export(model, str(output_path.with_suffix(".stl")))
            elif format.lower() == "gltf":
                # Would need additional library for glTF
                logger.warning("glTF export not yet implemented, using STEP")
                cq.exporters.export(model, str(output_path.with_suffix(".step")))
            else:
                raise ValueError(f"Unsupported export format: {format}")

            logger.info(f"Model exported successfully to {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error exporting model: {e}")
            raise
