"""
AI Model Manager
Manages Vertex AI and Gemini models for prompt-to-CAD conversion
"""

import logging
from typing import Dict, Any, Optional, List
import google.generativeai as genai
from vertexai.language_models import TextGenerationModel
from vertexai.language_models import TextEmbeddingModel
import vertexai
import json
from app.core.config import settings

logger = logging.getLogger(__name__)


class ModelManager:
    """Manages AI models for the application"""

    def __init__(self):
        self.gemini_model = None
        self.vertex_text_model = None
        self.embedding_model = None
        self.initialized = False

    async def initialize(self):
        """Initialize AI models"""
        try:
            # Initialize Vertex AI
            if settings.GCP_PROJECT_ID:
                vertexai.init(
                    project=settings.GCP_PROJECT_ID,
                    location=settings.VERTEX_AI_LOCATION
                )
                logger.info(f"Vertex AI initialized for project: {settings.GCP_PROJECT_ID}")

            # Initialize Gemini
            if settings.GEMINI_API_KEY:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self.gemini_model = genai.GenerativeModel(settings.GEMINI_MODEL)
                logger.info(f"Gemini model loaded: {settings.GEMINI_MODEL}")

            # Initialize Vertex AI text model
            try:
                self.vertex_text_model = TextGenerationModel.from_pretrained(
                    settings.VERTEX_AI_MODEL
                )
                logger.info(f"Vertex text model loaded: {settings.VERTEX_AI_MODEL}")
            except Exception as e:
                logger.warning(f"Could not load Vertex text model: {e}")

            # Initialize embedding model
            try:
                self.embedding_model = TextEmbeddingModel.from_pretrained(
                    settings.EMBEDDING_MODEL
                )
                logger.info(f"Embedding model loaded: {settings.EMBEDDING_MODEL}")
            except Exception as e:
                logger.warning(f"Could not load embedding model: {e}")

            self.initialized = True
            logger.info("Model Manager initialized successfully")

        except Exception as e:
            logger.error(f"Error initializing Model Manager: {e}")
            raise

    async def parse_prompt(self, prompt: str, component_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Parse natural language prompt into structured CAD parameters

        Args:
            prompt: Natural language description
            component_type: Type of component (wing, fuselage, etc.)

        Returns:
            Dict with extracted parameters
        """
        if not self.initialized:
            await self.initialize()

        try:
            # Create system prompt for parameter extraction
            system_prompt = self._get_parameter_extraction_prompt(component_type)

            # Use Gemini for prompt parsing
            if self.gemini_model:
                response = await self._gemini_parse(system_prompt, prompt)
            elif self.vertex_text_model:
                response = await self._vertex_parse(system_prompt, prompt)
            else:
                # Fallback to rule-based parsing
                response = self._fallback_parse(prompt, component_type)

            logger.info(f"Prompt parsed successfully: {prompt[:50]}...")
            return response

        except Exception as e:
            logger.error(f"Error parsing prompt: {e}")
            # Return basic structure on error
            return {
                "component_type": component_type or "unknown",
                "parameters": {},
                "error": str(e)
            }

    async def _gemini_parse(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """Parse using Gemini"""
        try:
            full_prompt = f"{system_prompt}\n\nUser prompt: {user_prompt}\n\nExtract parameters as JSON:"

            response = self.gemini_model.generate_content(
                full_prompt,
                generation_config={
                    "temperature": settings.TEMPERATURE,
                    "max_output_tokens": settings.MAX_TOKENS,
                }
            )

            # Parse JSON response
            result_text = response.text.strip()

            # Extract JSON from markdown code blocks if present
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()

            parameters = json.loads(result_text)
            return parameters

        except Exception as e:
            logger.error(f"Gemini parsing error: {e}")
            raise

    async def _vertex_parse(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """Parse using Vertex AI"""
        try:
            full_prompt = f"{system_prompt}\n\nUser prompt: {user_prompt}"

            response = self.vertex_text_model.predict(
                full_prompt,
                temperature=settings.TEMPERATURE,
                max_output_tokens=settings.MAX_TOKENS,
            )

            # Parse JSON response
            result_text = response.text.strip()
            parameters = json.loads(result_text)
            return parameters

        except Exception as e:
            logger.error(f"Vertex parsing error: {e}")
            raise

    def _fallback_parse(self, prompt: str, component_type: Optional[str]) -> Dict[str, Any]:
        """Fallback rule-based parsing"""
        import re

        prompt_lower = prompt.lower()
        parameters = {}

        # Detect component type if not specified
        if not component_type:
            if "wing" in prompt_lower:
                component_type = "wing"
            elif "fuselage" in prompt_lower:
                component_type = "fuselage"
            elif "tail" in prompt_lower or "stabilizer" in prompt_lower:
                component_type = "tail"
            else:
                component_type = "unknown"

        # Extract numbers with units
        # Wingspan/span
        wingspan_match = re.search(r'(\d+\.?\d*)\s*m?\s*(?:wing)?span', prompt_lower)
        if wingspan_match:
            parameters["wingspan_m"] = float(wingspan_match.group(1))

        # Chord
        chord_match = re.search(r'(\d+\.?\d*)\s*m?\s*chord', prompt_lower)
        if chord_match:
            parameters["chord_m"] = float(chord_match.group(1))

        # Airfoil
        airfoil_match = re.search(r'naca\s*(\d{4,5})', prompt_lower)
        if airfoil_match:
            parameters["airfoil"] = f"NACA{airfoil_match.group(1)}"

        # Dihedral angle
        dihedral_match = re.search(r'(\d+\.?\d*)\s*(?:deg|°|degree)?\s*dihedral', prompt_lower)
        if dihedral_match:
            parameters["dihedral_deg"] = float(dihedral_match.group(1))

        # Sweep angle
        sweep_match = re.search(r'(\d+\.?\d*)\s*(?:deg|°|degree)?\s*sweep', prompt_lower)
        if sweep_match:
            parameters["sweep_deg"] = float(sweep_match.group(1))

        # Fuselage length
        length_match = re.search(r'(\d+\.?\d*)\s*m?\s*long', prompt_lower)
        if length_match:
            parameters["length_m"] = float(length_match.group(1))

        # Fuselage diameter
        diameter_match = re.search(r'(\d+\.?\d*)\s*m?\s*diameter', prompt_lower)
        if diameter_match:
            parameters["diameter_m"] = float(diameter_match.group(1))

        return {
            "component_type": component_type,
            "parameters": parameters,
            "prompt": prompt
        }

    def _get_parameter_extraction_prompt(self, component_type: Optional[str]) -> str:
        """Get system prompt for parameter extraction"""

        base_prompt = """You are an expert aerospace engineer and CAD system. Extract design parameters from natural language prompts.

Return a JSON object with the following structure:
{
  "component_type": "wing|fuselage|tail|engine|landing_gear|control_surface",
  "parameters": {
    // Component-specific parameters
  },
  "assembly_instructions": {
    // Optional assembly information
  }
}
"""

        if component_type == "wing":
            return base_prompt + """
For wings, extract:
- wingspan_m: total wingspan in meters
- root_chord_m: root chord length
- tip_chord_m: tip chord length
- airfoil: airfoil designation (e.g., NACA2412)
- sweep_deg: leading edge sweep angle
- dihedral_deg: dihedral angle
- twist_deg: wing twist
- taper_ratio: tip_chord / root_chord
- aspect_ratio: wingspan^2 / wing_area
- has_winglets: boolean
- winglet_cant_angle_deg: if has_winglets
"""
        elif component_type == "fuselage":
            return base_prompt + """
For fuselage, extract:
- length_m: total length
- diameter_m or width_m/height_m: cross-section dimensions
- nose_length_m: nose cone length
- tail_length_m: tail cone length
- cross_section_shape: circular, elliptical, rectangular
- num_seats: passenger capacity
- has_cockpit: boolean
- has_cargo_hold: boolean
"""
        elif component_type == "tail":
            return base_prompt + """
For tail (empennage), extract:
- type: conventional, T-tail, V-tail, cruciform
- horizontal_span_m: horizontal stabilizer span
- vertical_height_m: vertical stabilizer height
- horizontal_area_m2: horizontal stabilizer area
- vertical_area_m2: vertical stabilizer area
"""
        else:
            return base_prompt + """
Extract all relevant aerodynamic and geometric parameters.
Be specific about dimensions, angles, airfoil profiles, and configuration.
"""

    async def get_embedding(self, text: str) -> List[float]:
        """Generate embedding vector for text"""
        if not self.embedding_model:
            logger.warning("Embedding model not available, returning empty vector")
            return []

        try:
            embeddings = self.embedding_model.get_embeddings([text])
            return embeddings[0].values
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return []

    async def find_similar_designs(
        self,
        parameters: Dict[str, Any],
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find similar designs from dataset based on parameters

        Args:
            parameters: Design parameters
            limit: Number of similar designs to return

        Returns:
            List of similar designs
        """
        # This would query the database for similar designs
        # For now, return empty list
        # TODO: Implement vector similarity search
        return []

    async def enhance_parameters(
        self,
        parameters: Dict[str, Any],
        similar_designs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Enhance parameters based on similar designs and engineering rules

        Args:
            parameters: Extracted parameters
            similar_designs: Similar designs from dataset

        Returns:
            Enhanced parameters
        """
        enhanced = parameters.copy()

        # Apply engineering rules
        if "wing" in parameters.get("component_type", ""):
            # Calculate derived parameters
            if "wingspan_m" in parameters and "chord_m" in parameters:
                wing_area = parameters["wingspan_m"] * parameters["chord_m"]
                enhanced["wing_area_m2"] = wing_area
                enhanced["aspect_ratio"] = parameters["wingspan_m"] ** 2 / wing_area

            # Set defaults from similar designs if available
            if similar_designs:
                # Use average values from similar designs
                pass

        return enhanced
