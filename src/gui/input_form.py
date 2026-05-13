"""
Patient Input Form Page
"""

import tkinter as tk
from tkinter import ttk, messagebox

from src.ml.predict import FEATURE_REQUEST_ORDER
from src.gui.styles import FONTS, INPUT_WIDTH


FIELD_LABELS = {
    "Age": "Age",
    "Sex": "Sex",
    "ALB": "Albumin (ALB)",
    "ALP": "Alkaline Phosphatase (ALP)",
    "ALT": "Alanine Aminotransferase (ALT)",
    "AST": "Aspartate Aminotransferase (AST)",
    "BIL": "Bilirubin (BIL)",
    "CHE": "Cholinesterase (CHE)",
    "CHOL": "Cholesterol (CHOL)",
    "CREA": "Creatinine (CREA)",
    "GGT": "Gamma-GT (GGT)",
    "PROT": "Total Protein (PROT)",
}


class PatientInputForm(ttk.Frame):
    def __init__(self, parent, controller, on_prediction_success):
        super().__init__(parent)

        self.controller = controller
        self.on_prediction_success = on_prediction_success
        self.entries = {}

        self.columnconfigure(0, weight=1)

        ttk.Label(
            self,
            text="Single Patient Screening",
            font=FONTS["title"],
        ).grid(row=0, column=0, sticky="w", pady=(0, 10))

        ttk.Label(
            self,
            text="Enter the patient laboratory values below, then run the liver risk prediction.",
            font=FONTS["subtitle"],
        ).grid(row=1, column=0, sticky="w", pady=(0, 20))

        form_frame = ttk.Frame(self)
        form_frame.grid(row=2, column=0, sticky="nw")

        for index, feature in enumerate(FEATURE_REQUEST_ORDER):
            row = index // 2
            col = (index % 2) * 2

            ttk.Label(
                form_frame,
                text=FIELD_LABELS.get(feature, feature),
                font=FONTS["body"],
            ).grid(row=row, column=col, sticky="w", padx=(0, 8), pady=8)

            if feature == "Sex":
                var = tk.StringVar(value="m")
                input_widget = ttk.Combobox(
                    form_frame,
                    textvariable=var,
                    values=["m", "f"],
                    width=INPUT_WIDTH,
                    state="readonly",
                )
                input_widget.var = var
            else:
                input_widget = ttk.Entry(form_frame, width=INPUT_WIDTH)

            input_widget.grid(row=row, column=col + 1, sticky="w", padx=(0, 30), pady=8)
            self.entries[feature] = input_widget

        button_frame = ttk.Frame(self)
        button_frame.grid(row=3, column=0, sticky="w", pady=25)

        ttk.Button(
            button_frame,
            text="Run Prediction",
            command=self.handle_predict,
        ).grid(row=0, column=0, padx=(0, 10))

        ttk.Button(
            button_frame,
            text="Clear Form",
            command=self.clear_form,
        ).grid(row=0, column=1)

        self.fill_sample_button = ttk.Button(
            button_frame,
            text="Fill Sample Input",
            command=self.fill_sample_input,
        )
        self.fill_sample_button.grid(row=0, column=2, padx=(10, 0))

    def get_form_data(self) -> dict:
        data = {}

        for feature, widget in self.entries.items():
            if feature == "Sex":
                data[feature] = widget.var.get()
            else:
                data[feature] = widget.get().strip()

        return data

    def handle_predict(self):
        data = self.get_form_data()
        response = self.controller.predict(data)

        if not response["success"]:
            messagebox.showerror(
                "Invalid Input",
                "\n".join(response["errors"]),
            )
            return

        self.on_prediction_success(response["result"])

    def clear_form(self):
        for feature, widget in self.entries.items():
            if feature == "Sex":
                widget.var.set("m")
            else:
                widget.delete(0, tk.END)

    def fill_sample_input(self):
        sample = {
            "Age": "45",
            "Sex": "m",
            "ALB": "42",
            "ALP": "85",
            "ALT": "30",
            "AST": "28",
            "BIL": "0.8",
            "CHE": "8.5",
            "CHOL": "4.8",
            "CREA": "0.9",
            "GGT": "35",
            "PROT": "72",
        }

        self.clear_form()

        for feature, value in sample.items():
            widget = self.entries[feature]
            if feature == "Sex":
                widget.var.set(value)
            else:
                widget.insert(0, value)