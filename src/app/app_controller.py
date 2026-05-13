"""
Application Controller

Connects the GUI with the ML prediction layer.
Handles validation, single prediction, batch prediction, history, and exports.
"""

import csv
from datetime import datetime
from pathlib import Path

from src.ml.predict import predict_liver_risk, predict_batch, FEATURE_REQUEST_ORDER
from src.utils.paths import PREDICTIONS_DIR


class AppController:
    """Main application controller."""

    def __init__(self):
        self.history = []

    def validate_patient_input(self, data: dict) -> tuple[bool, list[str]]:
        """
        Validate one patient input dictionary before sending it to the model.
        Returns:
        - True/False
        - list of error messages
        """
        errors = []

        for feature in FEATURE_REQUEST_ORDER:
            if feature not in data or str(data[feature]).strip() == "":
                errors.append(f"{feature} is required.")

        if errors:
            return False, errors

        try:
            age = float(data["Age"])
            if age <= 0 or age > 120:
                errors.append("Age must be between 1 and 120.")
        except ValueError:
            errors.append("Age must be a number.")

        sex = str(data["Sex"]).strip().lower()
        if sex not in {"m", "f", "male", "female"}:
            errors.append("Sex must be Male or Female.")

        numeric_features = [
            "ALB", "ALP", "ALT", "AST", "BIL",
            "CHE", "CHOL", "CREA", "GGT", "PROT"
        ]

        for feature in numeric_features:
            try:
                value = float(data[feature])
                if value < 0:
                    errors.append(f"{feature} cannot be negative.")
            except ValueError:
                errors.append(f"{feature} must be a number.")

        return len(errors) == 0, errors

    def prepare_patient_input(self, data: dict) -> dict:
        """
        Convert validated GUI/CSV string input into model-ready values.

        Tkinter Entry and CSV values arrive as strings.
        This method converts numeric fields to floats and normalizes Sex.
        It also rebuilds the dictionary using FEATURE_REQUEST_ORDER so the
        order matches the model/backend expectation.
        """
        prepared = {}

        for feature in FEATURE_REQUEST_ORDER:
            value = data[feature]

            if feature == "Sex":
                sex = str(value).strip().lower()

                if sex in {"male", "m"}:
                    prepared[feature] = "m"
                elif sex in {"female", "f"}:
                    prepared[feature] = "f"
                else:
                    prepared[feature] = sex

            else:
                prepared[feature] = float(value)

        return prepared

    def predict(self, data: dict) -> dict:
        """
        Validate input, run prediction, save to history, and return result.
        """
        is_valid, errors = self.validate_patient_input(data)

        if not is_valid:
            return {
                "success": False,
                "errors": errors,
                "result": None,
            }

        try:
            prepared_data = self.prepare_patient_input(data)

            result = predict_liver_risk(prepared_data)

            record = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "input": prepared_data,
                "result": result,
            }

            self.history.append(record)

            return {
                "success": True,
                "errors": [],
                "result": result,
            }

        except Exception as e:
            return {
                "success": False,
                "errors": [f"Prediction failed: {str(e)}"],
                "result": None,
            }

    def predict_csv_records(self, records: list[dict]) -> tuple[list[dict], list[str]]:
        """
        Validate and predict a list of CSV records.
        Returns:
        - results list
        - errors list
        """
        results = []
        errors = []

        for index, record in enumerate(records, start=1):
            is_valid, row_errors = self.validate_patient_input(record)

            if not is_valid:
                errors.append(f"Row {index}: " + " | ".join(row_errors))
                continue

            try:
                prepared_record = self.prepare_patient_input(record)

                prediction = predict_liver_risk(prepared_record)

                output_row = {
                    **prepared_record,
                    "prediction_label": prediction.get("prediction_label"),
                    "confidence": prediction.get("confidence"),
                    "recommendation": prediction.get("recommendation"),
                }

                results.append(output_row)

                self.history.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "input": prepared_record,
                    "result": prediction,
                })

            except Exception as e:
                errors.append(f"Row {index}: Prediction failed: {str(e)}")

        return results, errors

    def get_history(self) -> list[dict]:
        return self.history

    def export_results_to_csv(self, rows: list[dict], filepath: str) -> None:
        """
        Export batch results or flattened history to CSV.
        """
        if not rows:
            raise ValueError("No results to export.")

        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)

        fieldnames = list(rows[0].keys())

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def export_history_to_txt(self, filepath: str) -> None:
        """
        Export screening history to readable TXT.
        """
        if not self.history:
            raise ValueError("No history to export.")

        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            for index, item in enumerate(self.history, start=1):
                f.write(f"Screening #{index}\n")
                f.write(f"Time: {item['timestamp']}\n")
                f.write("Input:\n")

                for key, value in item["input"].items():
                    f.write(f"  {key}: {value}\n")

                f.write("Result:\n")
                for key, value in item["result"].items():
                    if key not in {"feature_importance"}:
                        f.write(f"  {key}: {value}\n")

                f.write("-" * 50 + "\n")