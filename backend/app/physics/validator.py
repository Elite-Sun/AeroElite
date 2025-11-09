"""
Physics Validator
Performs lightweight aerodynamic and structural validation
"""

import logging
from typing import Dict, Any, List, Tuple
import numpy as np
from app.core.config import settings

logger = logging.getLogger(__name__)


class PhysicsValidator:
    """Validate aircraft designs for basic physics and engineering constraints"""

    def __init__(self):
        self.air_density = 1.225  # kg/m^3 at sea level
        self.gravity = 9.81  # m/s^2

    async def validate_design(
        self,
        component_type: str,
        parameters: Dict[str, Any],
        conditions: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Validate design parameters

        Args:
            component_type: Type of component
            parameters: Design parameters
            conditions: Flight conditions (optional)

        Returns:
            Validation results with warnings and errors
        """
        logger.info(f"Validating {component_type} design")

        results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "analysis": {}
        }

        try:
            if component_type == "wing":
                results = await self._validate_wing(parameters, conditions)
            elif component_type == "fuselage":
                results = await self._validate_fuselage(parameters)
            elif component_type == "tail":
                results = await self._validate_tail(parameters)
            else:
                results["warnings"].append(f"No validation available for {component_type}")

            # Set overall validity
            results["valid"] = len(results["errors"]) == 0

            logger.info(f"Validation complete: {results['valid']}")
            return results

        except Exception as e:
            logger.error(f"Validation error: {e}")
            results["errors"].append(str(e))
            results["valid"] = False
            return results

    async def _validate_wing(
        self,
        params: Dict[str, Any],
        conditions: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Validate wing design"""
        results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "analysis": {}
        }

        # Extract parameters
        wingspan = params.get("wingspan_m", 0)
        root_chord = params.get("root_chord_m", 0)
        tip_chord = params.get("tip_chord_m", root_chord)
        sweep_deg = params.get("sweep_deg", 0)
        dihedral_deg = params.get("dihedral_deg", 0)
        airfoil = params.get("airfoil", "")

        # Basic parameter validation
        if wingspan <= 0:
            results["errors"].append("Wingspan must be positive")
        elif wingspan > 100:
            results["warnings"].append("Very large wingspan (>100m) - verify units")

        if root_chord <= 0:
            results["errors"].append("Root chord must be positive")

        if tip_chord > root_chord:
            results["warnings"].append("Tip chord larger than root chord (negative taper)")

        # Calculate wing area and aspect ratio
        wing_area = (root_chord + tip_chord) / 2 * wingspan  # Simplified trapezoidal
        aspect_ratio = wingspan ** 2 / wing_area if wing_area > 0 else 0

        results["analysis"]["wing_area_m2"] = round(wing_area, 2)
        results["analysis"]["aspect_ratio"] = round(aspect_ratio, 2)
        results["analysis"]["taper_ratio"] = round(tip_chord / root_chord, 3) if root_chord > 0 else 0

        # Aspect ratio checks
        if aspect_ratio < 4:
            results["warnings"].append("Low aspect ratio (<4) - may have high induced drag")
        elif aspect_ratio > 15:
            results["warnings"].append("High aspect ratio (>15) - verify structural strength")

        # Sweep angle checks
        if abs(sweep_deg) > 45:
            results["warnings"].append("High sweep angle may cause spanwise flow and tip stall")

        # Dihedral checks
        if abs(dihedral_deg) > 10:
            results["warnings"].append("Large dihedral angle - verify roll stability")

        # Aerodynamic analysis
        if conditions:
            aero_analysis = await self._analyze_wing_aerodynamics(
                params, conditions
            )
            results["analysis"].update(aero_analysis)

        # Structural checks
        structural_analysis = await self._check_wing_structure(params)
        results["analysis"].update(structural_analysis)
        results["warnings"].extend(structural_analysis.get("warnings", []))

        return results

    async def _analyze_wing_aerodynamics(
        self,
        params: Dict[str, Any],
        conditions: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze wing aerodynamics"""
        analysis = {}

        # Get flight conditions
        velocity = conditions.get("velocity_ms", 50.0)  # m/s
        altitude = conditions.get("altitude_m", 0.0)
        angle_of_attack = conditions.get("angle_of_attack_deg", 5.0)

        # Calculate air density at altitude
        rho = self.air_density * (1 - 0.0065 * altitude / 288.15) ** 4.256

        # Wing parameters
        wingspan = params.get("wingspan_m", 10.0)
        root_chord = params.get("root_chord_m", 2.0)
        tip_chord = params.get("tip_chord_m", 1.0)
        wing_area = (root_chord + tip_chord) / 2 * wingspan

        # Estimate lift coefficient (simplified)
        # For NACA airfoils, approximate Cl = 2π * α (in radians)
        cl_alpha = 2 * np.pi / 57.3  # per degree
        cl = cl_alpha * angle_of_attack

        # Lift force
        lift = 0.5 * rho * velocity ** 2 * wing_area * cl

        # Induced drag coefficient
        aspect_ratio = wingspan ** 2 / wing_area
        e = 0.8  # Oswald efficiency factor (typical)
        cd_induced = cl ** 2 / (np.pi * aspect_ratio * e)

        # Parasitic drag (very rough estimate)
        cd_parasitic = 0.02  # Typical for smooth wing

        # Total drag
        cd = cd_induced + cd_parasitic
        drag = 0.5 * rho * velocity ** 2 * wing_area * cd

        # Lift-to-drag ratio
        ld_ratio = cl / cd if cd > 0 else 0

        analysis["lift_coefficient"] = round(cl, 3)
        analysis["drag_coefficient"] = round(cd, 4)
        analysis["lift_force_N"] = round(lift, 1)
        analysis["drag_force_N"] = round(drag, 1)
        analysis["lift_to_drag_ratio"] = round(ld_ratio, 1)

        # Checks
        if cl > settings.MIN_LIFT_COEFFICIENT:
            analysis["lift_status"] = "adequate"
        else:
            analysis["lift_status"] = "insufficient"
            analysis["warnings"] = [f"Low lift coefficient: {cl:.3f}"]

        if cl > 1.5:
            analysis.setdefault("warnings", []).append("High Cl - near stall region")

        return analysis

    async def _check_wing_structure(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Check wing structural integrity (simplified)"""
        analysis = {"warnings": []}

        wingspan = params.get("wingspan_m", 10.0)
        root_chord = params.get("root_chord_m", 2.0)
        aspect_ratio = wingspan ** 2 / ((root_chord + params.get("tip_chord_m", root_chord)) / 2 * wingspan)

        # Estimate bending moment at root (very simplified)
        # Assume uniform load distribution
        wing_area = (root_chord + params.get("tip_chord_m", root_chord)) / 2 * wingspan
        weight_per_area = 50  # kg/m^2 (typical for light aircraft wing)
        wing_weight = wing_area * weight_per_area

        # Max bending moment at root (simplified cantilever)
        max_moment = wing_weight * self.gravity * wingspan / 4  # N⋅m

        # Estimate required spar size (very rough)
        # σ = M * c / I, assume allowable stress 400 MPa (aluminum)
        allowable_stress = settings.MAX_STRESS_MPA * 1e6  # Pa
        required_section_modulus = max_moment / allowable_stress  # m^3

        analysis["estimated_bending_moment_Nm"] = round(max_moment, 1)
        analysis["required_section_modulus_m3"] = f"{required_section_modulus:.6f}"

        # Deflection check (simplified)
        # δ = (w * L^4) / (8 * E * I)
        # Assume aluminum E = 70 GPa
        E = 70e9  # Pa
        # Rough estimate of moment of inertia
        I = required_section_modulus * root_chord / 2  # Very rough
        deflection = (wing_weight * self.gravity * wingspan ** 4) / (8 * E * I)  # m

        analysis["estimated_tip_deflection_mm"] = round(deflection * 1000, 1)

        if deflection * 1000 > settings.MAX_DEFLECTION_MM:
            analysis["warnings"].append(
                f"High estimated deflection: {deflection*1000:.1f}mm - verify wing structure"
            )

        # Aspect ratio vs structural weight
        if aspect_ratio > 12:
            analysis["warnings"].append(
                "High aspect ratio may require additional structural reinforcement"
            )

        return analysis

    async def _validate_fuselage(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate fuselage design"""
        results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "analysis": {}
        }

        length = params.get("length_m", 0)
        diameter = params.get("diameter_m", 0)
        num_seats = params.get("num_seats", 0)

        # Basic validation
        if length <= 0:
            results["errors"].append("Fuselage length must be positive")
        elif length > 100:
            results["warnings"].append("Very long fuselage (>100m) - verify units")

        if diameter <= 0:
            results["errors"].append("Fuselage diameter must be positive")

        # Fineness ratio (length/diameter)
        fineness_ratio = length / diameter if diameter > 0 else 0
        results["analysis"]["fineness_ratio"] = round(fineness_ratio, 2)

        if fineness_ratio < 3:
            results["warnings"].append("Low fineness ratio - high drag expected")
        elif fineness_ratio > 15:
            results["warnings"].append("High fineness ratio - may have stability issues")

        # Seating capacity check
        if num_seats > 0:
            # Estimate required cabin volume
            volume_per_passenger = 1.5  # m^3 per passenger (rough estimate)
            required_volume = num_seats * volume_per_passenger

            # Actual fuselage volume (simplified cylinder)
            fuselage_volume = np.pi * (diameter / 2) ** 2 * length * 0.6  # 60% usable

            results["analysis"]["cabin_volume_m3"] = round(fuselage_volume, 1)
            results["analysis"]["required_volume_m3"] = round(required_volume, 1)

            if fuselage_volume < required_volume:
                results["warnings"].append(
                    f"Insufficient cabin volume for {num_seats} seats"
                )

        return results

    async def _validate_tail(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate tail design"""
        results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "analysis": {}
        }

        # Similar validation to wing
        # Check horizontal and vertical stabilizer sizes relative to wing
        # Tail volume coefficients, etc.

        h_span = params.get("horizontal_span_m", 0)
        v_height = params.get("vertical_height_m", 0)

        if h_span <= 0:
            results["errors"].append("Horizontal stabilizer span must be positive")

        if v_height <= 0:
            results["errors"].append("Vertical stabilizer height must be positive")

        return results

    async def validate_assembly(
        self,
        components: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Validate complete aircraft assembly"""
        results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "analysis": {}
        }

        # Check center of gravity
        # Check stability (static margin)
        # Check weight balance
        # Check thrust-to-weight ratio

        logger.info("Validating assembly")

        # Extract component types
        has_wing = any(c.get("component_type") == "wing" for c in components)
        has_fuselage = any(c.get("component_type") == "fuselage" for c in components)
        has_tail = any(c.get("component_type") == "tail" for c in components)

        if not has_wing:
            results["errors"].append("Assembly missing wing")

        if not has_fuselage:
            results["warnings"].append("Assembly missing fuselage")

        if not has_tail:
            results["warnings"].append("Assembly missing tail - may be unstable")

        # Calculate total weight (rough estimate)
        total_weight = sum(
            c.get("parameters", {}).get("weight_kg", 0)
            for c in components
        )

        results["analysis"]["total_weight_kg"] = round(total_weight, 1)

        return results
