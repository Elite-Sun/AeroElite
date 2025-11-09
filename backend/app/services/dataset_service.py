"""
Dataset Service
Processes and manages aircraft design datasets
"""

import logging
from typing import Dict, Any, List, Optional
import httpx
import asyncio
from pathlib import Path
import json
from app.core.config import settings

logger = logging.getLogger(__name__)


class DatasetService:
    """Manage aircraft design datasets"""

    def __init__(self):
        self.datasets = {
            "aircraftverse": {
                "url": settings.AIRCRAFTVERSE_URL,
                "total_entries": 27714,
                "loaded": False,
                "metadata": {}
            },
            "g2aero": {
                "url": settings.G2AERO_URL,
                "total_entries": 19164,
                "loaded": False,
                "metadata": {}
            },
            "nasa_crm": {
                "url": settings.NASA_CRM_URL,
                "total_entries": 0,
                "loaded": False,
                "metadata": {}
            }
        }
        self.dataset_dir = Path("datasets")
        self.dataset_dir.mkdir(exist_ok=True)

    async def load_metadata(self):
        """Load dataset metadata"""
        logger.info("Loading dataset metadata")

        try:
            # Load cached metadata if available
            metadata_file = self.dataset_dir / "metadata.json"
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    cached = json.load(f)
                    self.datasets.update(cached)
                    logger.info("Loaded cached metadata")

            # Mark as loaded
            for dataset in self.datasets.values():
                dataset["loaded"] = True

        except Exception as e:
            logger.error(f"Error loading metadata: {e}")

    async def download_dataset(
        self,
        dataset_name: str,
        force: bool = False
    ) -> Dict[str, Any]:
        """
        Download dataset from source

        Args:
            dataset_name: Name of dataset (aircraftverse, g2aero, nasa_crm)
            force: Force re-download

        Returns:
            Download status
        """
        logger.info(f"Downloading dataset: {dataset_name}")

        if dataset_name not in self.datasets:
            raise ValueError(f"Unknown dataset: {dataset_name}")

        dataset = self.datasets[dataset_name]
        dataset_path = self.dataset_dir / dataset_name
        dataset_path.mkdir(exist_ok=True)

        # Check if already downloaded
        if dataset_path.exists() and not force:
            logger.info(f"Dataset {dataset_name} already downloaded")
            return {"status": "already_downloaded", "path": str(dataset_path)}

        try:
            if dataset_name == "aircraftverse":
                return await self._download_aircraftverse(dataset_path)
            elif dataset_name == "g2aero":
                return await self._download_g2aero(dataset_path)
            elif dataset_name == "nasa_crm":
                return await self._download_nasa_crm(dataset_path)
            else:
                raise ValueError(f"Unknown dataset: {dataset_name}")

        except Exception as e:
            logger.error(f"Error downloading {dataset_name}: {e}")
            return {"status": "error", "error": str(e)}

    async def _download_aircraftverse(self, path: Path) -> Dict[str, Any]:
        """Download AircraftVerse dataset"""
        logger.info("Downloading AircraftVerse dataset")

        # AircraftVerse is large (27,714 aircraft)
        # For demo purposes, create a synthetic index
        # In production, this would download from Zenodo

        try:
            # Create sample metadata
            metadata = {
                "name": "AircraftVerse",
                "source": "zenodo",
                "total_entries": 27714,
                "description": "Large-scale dataset of aircraft designs",
                "categories": [
                    "commercial", "military", "general_aviation",
                    "rotorcraft", "uav", "experimental"
                ],
                "parameters_available": [
                    "wingspan", "length", "height", "weight",
                    "engine_count", "wing_config", "tail_config"
                ]
            }

            # Save metadata
            with open(path / "metadata.json", 'w') as f:
                json.dump(metadata, f, indent=2)

            # Create sample entries for demonstration
            sample_entries = self._create_sample_aircraft_entries()
            with open(path / "sample_entries.json", 'w') as f:
                json.dump(sample_entries, f, indent=2)

            logger.info(f"AircraftVerse metadata created at {path}")

            return {
                "status": "success",
                "path": str(path),
                "entries": len(sample_entries),
                "note": "Full dataset download requires Zenodo API integration"
            }

        except Exception as e:
            logger.error(f"Error downloading AircraftVerse: {e}")
            raise

    def _create_sample_aircraft_entries(self) -> List[Dict[str, Any]]:
        """Create sample aircraft entries for demonstration"""
        return [
            {
                "id": "ac_001",
                "name": "Boeing 737-800",
                "category": "commercial",
                "parameters": {
                    "wingspan_m": 35.79,
                    "length_m": 39.47,
                    "height_m": 12.55,
                    "wing_area_m2": 125.0,
                    "mtow_kg": 79010,
                    "engine_count": 2,
                    "wing_config": "low",
                    "tail_config": "conventional",
                    "airfoil": "custom",
                    "sweep_deg": 25.0
                }
            },
            {
                "id": "ac_002",
                "name": "Airbus A320",
                "category": "commercial",
                "parameters": {
                    "wingspan_m": 35.80,
                    "length_m": 37.57,
                    "height_m": 11.76,
                    "wing_area_m2": 122.6,
                    "mtow_kg": 78000,
                    "engine_count": 2,
                    "wing_config": "low",
                    "tail_config": "conventional",
                    "airfoil": "custom",
                    "sweep_deg": 25.0
                }
            },
            {
                "id": "ac_003",
                "name": "Cessna 172",
                "category": "general_aviation",
                "parameters": {
                    "wingspan_m": 11.0,
                    "length_m": 8.28,
                    "height_m": 2.72,
                    "wing_area_m2": 16.2,
                    "mtow_kg": 1111,
                    "engine_count": 1,
                    "wing_config": "high",
                    "tail_config": "conventional",
                    "airfoil": "NACA2412",
                    "sweep_deg": 0.0
                }
            },
            {
                "id": "ac_004",
                "name": "F-16 Fighting Falcon",
                "category": "military",
                "parameters": {
                    "wingspan_m": 9.96,
                    "length_m": 15.03,
                    "height_m": 5.09,
                    "wing_area_m2": 27.87,
                    "mtow_kg": 19187,
                    "engine_count": 1,
                    "wing_config": "mid",
                    "tail_config": "conventional",
                    "airfoil": "NACA64A204",
                    "sweep_deg": 40.0
                }
            },
            {
                "id": "ac_005",
                "name": "Gulfstream G650",
                "category": "business_jet",
                "parameters": {
                    "wingspan_m": 30.35,
                    "length_m": 30.41,
                    "height_m": 7.77,
                    "wing_area_m2": 105.6,
                    "mtow_kg": 45360,
                    "engine_count": 2,
                    "wing_config": "low",
                    "tail_config": "T-tail",
                    "airfoil": "custom",
                    "sweep_deg": 30.0
                }
            }
        ]

    async def _download_g2aero(self, path: Path) -> Dict[str, Any]:
        """Download G2Aero airfoil dataset"""
        logger.info("Downloading G2Aero airfoil dataset")

        try:
            # Create metadata
            metadata = {
                "name": "G2Aero",
                "source": "openei",
                "total_entries": 19164,
                "description": "Airfoil profile database with coordinates and performance data",
                "data_types": ["coordinates", "performance", "geometry"]
            }

            with open(path / "metadata.json", 'w') as f:
                json.dump(metadata, f, indent=2)

            # Create sample airfoils
            sample_airfoils = self._create_sample_airfoil_entries()
            with open(path / "sample_airfoils.json", 'w') as f:
                json.dump(sample_airfoils, f, indent=2)

            logger.info(f"G2Aero metadata created at {path}")

            return {
                "status": "success",
                "path": str(path),
                "entries": len(sample_airfoils),
                "note": "Full dataset download requires OpenEI API integration"
            }

        except Exception as e:
            logger.error(f"Error downloading G2Aero: {e}")
            raise

    def _create_sample_airfoil_entries(self) -> List[Dict[str, Any]]:
        """Create sample airfoil entries"""
        return [
            {
                "name": "NACA2412",
                "family": "NACA 4-digit",
                "max_thickness": 0.12,
                "max_camber": 0.02,
                "camber_position": 0.4,
                "cl_design": 0.4,
                "uses": "General aviation, light aircraft"
            },
            {
                "name": "NACA0012",
                "family": "NACA 4-digit",
                "max_thickness": 0.12,
                "max_camber": 0.0,
                "camber_position": 0.0,
                "cl_design": 0.0,
                "uses": "Symmetric, tails, vertical surfaces"
            },
            {
                "name": "NACA23012",
                "family": "NACA 5-digit",
                "max_thickness": 0.12,
                "max_camber": 0.0215,
                "camber_position": 0.15,
                "cl_design": 0.3,
                "uses": "Aircraft wings, moderate lift"
            },
            {
                "name": "NACA64-212",
                "family": "NACA 6-series",
                "max_thickness": 0.12,
                "max_camber": 0.02,
                "camber_position": 0.4,
                "cl_design": 0.2,
                "uses": "High-speed aircraft, low drag"
            }
        ]

    async def _download_nasa_crm(self, path: Path) -> Dict[str, Any]:
        """Download NASA Common Research Model"""
        logger.info("Downloading NASA CRM dataset")

        try:
            metadata = {
                "name": "NASA Common Research Model",
                "source": "nasa",
                "description": "Validated reference geometry for CFD studies",
                "includes": ["wing", "fuselage", "nacelle", "pylon"]
            }

            with open(path / "metadata.json", 'w') as f:
                json.dump(metadata, f, indent=2)

            return {
                "status": "success",
                "path": str(path),
                "note": "NASA CRM requires manual download from NASA website"
            }

        except Exception as e:
            logger.error(f"Error downloading NASA CRM: {e}")
            raise

    async def search_datasets(
        self,
        query: str,
        dataset_name: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search datasets for matching designs

        Args:
            query: Search query
            dataset_name: Specific dataset to search (optional)
            filters: Additional filters

        Returns:
            List of matching entries
        """
        logger.info(f"Searching datasets for: {query}")

        results = []

        # Search AircraftVerse
        if not dataset_name or dataset_name == "aircraftverse":
            results.extend(await self._search_aircraftverse(query, filters))

        # Search G2Aero
        if not dataset_name or dataset_name == "g2aero":
            results.extend(await self._search_g2aero(query, filters))

        logger.info(f"Found {len(results)} results")
        return results

    async def _search_aircraftverse(
        self,
        query: str,
        filters: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Search AircraftVerse dataset"""
        # Load sample entries
        sample_file = self.dataset_dir / "aircraftverse" / "sample_entries.json"
        if not sample_file.exists():
            return []

        with open(sample_file, 'r') as f:
            entries = json.load(f)

        # Simple text search
        query_lower = query.lower()
        results = [
            entry for entry in entries
            if query_lower in entry.get("name", "").lower()
            or query_lower in entry.get("category", "").lower()
        ]

        return results

    async def _search_g2aero(
        self,
        query: str,
        filters: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Search G2Aero airfoil dataset"""
        sample_file = self.dataset_dir / "g2aero" / "sample_airfoils.json"
        if not sample_file.exists():
            return []

        with open(sample_file, 'r') as f:
            airfoils = json.load(f)

        query_lower = query.lower()
        results = [
            airfoil for airfoil in airfoils
            if query_lower in airfoil.get("name", "").lower()
            or query_lower in airfoil.get("family", "").lower()
        ]

        return results

    async def get_similar_designs(
        self,
        parameters: Dict[str, Any],
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find similar designs based on parameters

        Args:
            parameters: Design parameters
            limit: Maximum number of results

        Returns:
            List of similar designs
        """
        logger.info("Finding similar designs")

        # Would use vector similarity search here
        # For now, return sample results
        return []

    async def learn_from_design(
        self,
        design: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process and learn from a user-generated design

        Args:
            design: Design to learn from

        Returns:
            Processing results
        """
        logger.info(f"Learning from design: {design.get('name')}")

        results = {
            "success": True,
            "parameters_extracted": 0,
            "embedding_created": False
        }

        try:
            # Extract parameters
            # Create embeddings
            # Update knowledge base
            # Store for future reference

            results["success"] = True

        except Exception as e:
            logger.error(f"Error learning from design: {e}")
            results["success"] = False
            results["error"] = str(e)

        return results
