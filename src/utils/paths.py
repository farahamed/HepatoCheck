"""
Path Utilities
"""

import os
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Data paths
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SAMPLE_INPUTS_DIR = DATA_DIR / "sample_inputs"

# Model paths
MODELS_DIR = PROJECT_ROOT / "models"

# Output paths
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
REPORTS_DIR = OUTPUTS_DIR / "reports"
PREDICTIONS_DIR = OUTPUTS_DIR / "predictions"

# Source paths
SRC_DIR = PROJECT_ROOT / "src"
