import numpy as np

from src.utils.constants import FEATURE_NAMES
from src.ml import predict as predict_module


class _IdentityScaler:
    def transform(self, X):
        return np.asarray(X)


class _FakeModel:
    feature_importances_ = np.array([0.1] * len(FEATURE_NAMES))

    def predict(self, X):
        return np.array([0])

    def predict_proba(self, X):
        return np.array([[0.82, 0.18]])


def test_predict_liver_risk_contract(monkeypatch):
    dummy_patient = {
        "Age": 57,
        "Sex": "Male",
        "ALB": 40.0,
        "ALP": 80.0,
        "ALT": 20.0,
        "AST": 25.0,
        "BIL": 0.8,
        "CHE": 8.0,
        "CHOL": 5.0,
        "CREA": 0.9,
        "GGT": 30.0,
        "PROT": 72.0,
    }

    monkeypatch.setattr(predict_module, "load_feature_names", lambda path=None: FEATURE_NAMES)

    result = predict_module.predict_liver_risk(
        dummy_patient,
        model=_FakeModel(),
        scaler=_IdentityScaler(),
    )

    assert isinstance(result, dict)
    assert "prediction_label" in result
    assert "confidence" in result
    assert "key_markers" in result
    assert "recommendation" in result
    assert result["prediction_label"] in {"Low Risk", "Possible Risk"}
    assert 0.0 <= float(result["confidence"]) <= 1.0
