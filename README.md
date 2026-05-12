# HepatoCheck

## Overview
HepatoCheck is a machine learning application for predicting Hepatitis C infection status based on clinical and demographic features.

## Project Structure
```
HepatoCheck/
├── main.py                    # Application entry point
├── README.md                  # Project documentation
├── requirements.txt           # Python dependencies
├── data/                      # Data files
│   ├── raw/                  # Raw datasets
│   ├── processed/            # Processed datasets
│   └── sample_inputs/        # Sample input files
├── models/                   # Trained models and artifacts
├── src/                      # Source code
│   ├── gui/                  # GUI components
│   ├── app/                  # Application controller
│   ├── ml/                   # Machine learning modules
│   ├── data/                 # Data processing modules
│   └── utils/                # Utility functions
├── outputs/                  # Generated outputs
│   ├── reports/             # Generated reports
│   └── predictions/         # Prediction results
├── tests/                    # Test files
└── docs/                     # Documentation
```

## Installation
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
Run the application:
```
python main.py
```

## Team Structure
- **Teammate**: Data processing, ML models, training pipeline
- **Partner**: GUI development, application controller
- **Shared**: Testing, documentation, utilities

## Contributing
See `docs/contribution_matrix.md` for contribution guidelines.
