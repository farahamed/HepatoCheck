# Contribution Matrix

## Team Members
- **You (Teammate)**: Data processing, ML models, training
- **Partner**: GUI development, application controller

## Responsibility Matrix

| Component | You | Partner | Shared |
|-----------|-----|---------|--------|
| **GUI Components** | | ✓ | |
| **Input Form** | | ✓ | |
| **Result View** | | ✓ | |
| **Batch Upload** | | ✓ | |
| **History View** | | ✓ | |
| **App Controller** | ✓ | ✓ | ✓ |
| **ML Training** | ✓ | | |
| **Preprocessing** | ✓ | | |
| **Prediction** | ✓ | | |
| **Evaluation** | ✓ | | |
| **Explainability** | ✓ | | |
| **Data Loading** | ✓ | | |
| **Data Cleaning** | ✓ | | |
| **Validation** | ✓ | | |
| **Utils** | ✓ | ✓ | ✓ |
| **Testing** | ✓ | ✓ | ✓ |
| **Documentation** | ✓ | ✓ | ✓ |

## File Ownership
- You handle: `src/ml/`, `src/data/`, `tests/test_prediction.py`, `tests/test_validation.py`
- Partner handles: `src/gui/`, styling
- Shared: `src/app/`, `src/utils/`, `tests/`, `docs/`, root files
