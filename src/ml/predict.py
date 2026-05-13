import joblib
from typing import Any

try:
    from src.ml.preprocess import load_scaler, load_feature_names, preprocess_single_input
    from src.utils.helpers import label_from_prediction, flag_abnormal_values
    from src.utils.paths import MODEL_PATH, SCALER_PATH, FEATURE_NAMES_PATH
    from src.utils.constants import NORMAL_RANGES
except ModuleNotFoundError:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parents[2]))
    from src.ml.preprocess import load_scaler, load_feature_names, preprocess_single_input
    from src.utils.helpers import label_from_prediction, flag_abnormal_values
    from src.utils.paths import MODEL_PATH, SCALER_PATH, FEATURE_NAMES_PATH
    from src.utils.constants import NORMAL_RANGES

FEATURE_REQUEST_ORDER = [
    "Age",
    "Sex",
    "ALB",
    "ALP",
    "ALT",
    "AST",
    "BIL",
    "CHE",
    "CHOL",
    "CREA",
    "GGT",
    "PROT",
]

def load_model(path=MODEL_PATH):
    if not path.exists():
        raise FileNotFoundError(f"Model not found at {path}. Run train_model.py first.")
    return joblib.load(path)


def _ensure_prediction_artifacts_exist() -> None:
    required_paths = {
        "model": MODEL_PATH,
        "scaler": SCALER_PATH,
        "feature_names": FEATURE_NAMES_PATH,
    }
    missing = [f"{name}: {path}" for name, path in required_paths.items() if not path.exists()]
    if missing:
        missing_list = "\n".join(missing)
        raise FileNotFoundError(
            "Missing prediction artifacts. Run src/ml/train_model.py first to generate them:\n"
            f"{missing_list}"
        )


def _normalize_patient_data(patient_data: dict[str, Any]) -> dict[str, Any]:
    normalized = {}
    for feature in FEATURE_REQUEST_ORDER:
        if feature not in patient_data:
            raise KeyError(f"Missing required feature: {feature}")
        value = patient_data[feature]
        if feature == "Sex":
            sex_value = str(value).strip().lower()
            if sex_value in {"male", "m"}:
                value = "m"
            elif sex_value in {"female", "f"}:
                value = "f"
        normalized[feature] = value
    return normalized


def predict_liver_risk(patient_data: dict) -> dict:
    """Predict liver risk for one patient.

    Expected input keys:
    - Age, Sex, ALB, ALP, ALT, AST, BIL, CHE, CHOL, CREA, GGT, PROT

    Sex accepts: "m", "f", "male", "female" (case-insensitive).

    Returns a dictionary with both teammate-friendly fields and backwards-compatible fields.
    """
    # enforce exact required keys
    required_keys = set(FEATURE_REQUEST_ORDER)
    input_keys = set(patient_data.keys())
    if input_keys != required_keys:
        missing = required_keys - input_keys
        extra = input_keys - required_keys
        msg_parts = []
        if missing:
            msg_parts.append(f"missing: {sorted(missing)}")
        if extra:
            msg_parts.append(f"extra: {sorted(extra)}")
        raise KeyError("Invalid patient_data keys: " + "; ".join(msg_parts))

    normalized_patient = _normalize_patient_data(patient_data)

    # Try to load artifacts; if missing, return a dummy response (GUI-safe)
    try:
        model = load_model()
        scaler = load_scaler()
        feature_names = load_feature_names()
        model_loaded = True
    except Exception:
        model = None
        scaler = None
        feature_names = None
        model_loaded = False

    abnormal_flags = flag_abnormal_values(normalized_patient)

    def _key_markers_from_flags(flags: dict) -> list:
        markers = []
        for feat, is_ab in flags.items():
            if not is_ab:
                continue
            try:
                val = float(normalized_patient.get(feat))
                low, high = NORMAL_RANGES.get(feat, (None, None))
                if low is None or high is None:
                    markers.append(f"{feat} abnormal")
                else:
                    if val > high:
                        markers.append(f"{feat} elevated")
                    else:
                        markers.append(f"{feat} low")
            except Exception:
                markers.append(f"{feat} abnormal")
        return markers

    if not model_loaded:
        # dummy response per contract
        return {
            "prediction_label": "Possible liver disease risk",
            "confidence": 0.75,
            "key_markers": [m + " (dummy)" for m in _key_markers_from_flags(abnormal_flags)] or ["ALT elevated (dummy)"],
            "recommendation": "Dummy response - model not loaded yet",
            # backward-compatible optional fields
            "prediction": 1,
            "label": "Possible Risk",
            "top_features": [],
            "feature_importance": {},
            "abnormal_flags": abnormal_flags,
        }

    # real model path
    X = preprocess_single_input(normalized_patient, scaler)
    pred_label = int(model.predict(X)[0])
    proba = model.predict_proba(X)[0]

    try:
        importance_vals = getattr(model, "feature_importances_", None)
        if importance_vals is not None and feature_names is not None:
            feature_importance = dict(zip(feature_names, importance_vals.tolist()))
            sorted_feats = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
            top_features = [k for k, v in sorted_feats[:5]]
        else:
            feature_importance = {}
            top_features = []
    except Exception:
        feature_importance = {}
        top_features = []

    confidence = round(float(max(proba)), 4)

    # Map labels to teammate-friendly wording
    label_map_full = {0: "Low liver disease risk", 1: "Possible liver disease risk"}

    return {
        "prediction_label": label_map_full.get(pred_label, label_from_prediction(pred_label)),
        "confidence": confidence,
        "key_markers": _key_markers_from_flags(abnormal_flags),
        "recommendation": "Clinical follow-up recommended",
        # backward-compatible optional fields
        "prediction": pred_label,
        "label": label_from_prediction(pred_label),
        "top_features": top_features,
        "feature_importance": feature_importance,
        "abnormal_flags": abnormal_flags,
    }

def predict_batch(records: list[dict], model=None, scaler=None) -> list[dict]:
    return [predict_liver_risk(r) for r in records]