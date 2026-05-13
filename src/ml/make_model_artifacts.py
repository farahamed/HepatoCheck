"""
Create standard model artifact files expected by the GUI:
- models/trained_model.pkl
- models/scaler.pkl
- models/feature_names.pkl
- models/model_metrics.json

Strategy:
- Prefer `models/best_pipeline.pkl` if available and extract `scaler` and `clf`.
- Otherwise fall back to existing `models/trained_model.pkl` and `models/scaler.pkl` if present.
- Populate `feature_names.pkl` from existing file or from `src.utils.constants.FEATURE_NAMES`.
- Populate `model_metrics.json` from existing tuning or metrics files if available, otherwise write a minimal placeholder.
"""

import json
import joblib
from pathlib import Path

try:
    from src.utils.paths import MODELS_DIR, MODEL_PATH, SCALER_PATH, FEATURE_NAMES_PATH, METRICS_PATH
    from src.utils.paths import PROJECT_ROOT
    from src.utils.constants import FEATURE_NAMES
except Exception:
    import sys
    from pathlib import Path as P
    sys.path.append(str(P(__file__).resolve().parents[2]))
    from src.utils.paths import MODELS_DIR, MODEL_PATH, SCALER_PATH, FEATURE_NAMES_PATH, METRICS_PATH
    from src.utils.constants import FEATURE_NAMES

MODELS_DIR.mkdir(parents=True, exist_ok=True)

BEST_PIPELINE = MODELS_DIR / "best_pipeline.pkl"
TRAINED_MODEL = MODELS_DIR / "trained_model.pkl"
SCALER = SCALER_PATH
FEATURE_NAMES_FILE = FEATURE_NAMES_PATH
METRICS = METRICS_PATH


def main():
    made = []

    if BEST_PIPELINE.exists():
        pipeline = joblib.load(BEST_PIPELINE)
        # Try to extract scaler and classifier
        if hasattr(pipeline, 'named_steps'):
            steps = pipeline.named_steps
            if 'clf' in steps:
                clf = steps['clf']
                joblib.dump(clf, TRAINED_MODEL)
                made.append(str(TRAINED_MODEL))
            if 'scaler' in steps:
                scaler = steps['scaler']
                joblib.dump(scaler, SCALER)
                made.append(str(SCALER))
        else:
            # pipeline is a raw estimator
            joblib.dump(pipeline, TRAINED_MODEL)
            made.append(str(TRAINED_MODEL))

    else:
        # If trained_model exists already, nothing to do for model
        if TRAINED_MODEL.exists():
            made.append(str(TRAINED_MODEL))
        else:
            print("No best_pipeline.pkl or trained_model.pkl found — cannot create model artifact")

        if not SCALER.exists():
            print("No scaler.pkl found — scaler will remain missing unless created from training pipeline")

    # Feature names
    if FEATURE_NAMES_FILE.exists():
        made.append(str(FEATURE_NAMES_FILE))
    else:
        try:
            joblib.dump(FEATURE_NAMES, FEATURE_NAMES_FILE)
            made.append(str(FEATURE_NAMES_FILE))
        except Exception as e:
            print(f"Could not save feature names: {e}")

    # Metrics
    if METRICS.exists():
        made.append(str(METRICS))
    else:
        placeholder = {
            'note': 'Auto-generated placeholder metrics',
            'roc_auc': None
        }
        try:
            with open(METRICS, 'w', encoding='utf-8') as f:
                json.dump(placeholder, f, indent=2)
            made.append(str(METRICS))
        except Exception as e:
            print(f"Could not write metrics file: {e}")

    print('Artifacts created/verified:')
    for p in made:
        print(' -', p)

if __name__ == '__main__':
    main()
