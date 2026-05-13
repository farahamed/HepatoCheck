"""
Result Display Page
"""

import tkinter as tk
from tkinter import ttk

from src.gui.styles import COLORS, FONTS


class ResultView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.result_data = None

        self.columnconfigure(0, weight=1)

        self.title_label = ttk.Label(
            self,
            text="Prediction Result",
            font=FONTS["title"],
        )
        self.title_label.grid(row=0, column=0, sticky="w", pady=(0, 15))

        self.result_card = ttk.Frame(self, padding=20)
        self.result_card.grid(row=1, column=0, sticky="nsew")
        self.result_card.columnconfigure(0, weight=1)

        self.label_var = tk.StringVar(value="No prediction yet.")
        self.confidence_var = tk.StringVar(value="")
        self.recommendation_var = tk.StringVar(value="")
        self.probability_var = tk.StringVar(value="")

        ttk.Label(
            self.result_card,
            textvariable=self.label_var,
            font=("Segoe UI", 20, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 10))

        ttk.Label(
            self.result_card,
            textvariable=self.confidence_var,
            font=FONTS["heading"],
        ).grid(row=1, column=0, sticky="w", pady=5)

        ttk.Label(
            self.result_card,
            textvariable=self.probability_var,
            font=FONTS["body"],
        ).grid(row=2, column=0, sticky="w", pady=5)

        ttk.Label(
            self.result_card,
            text="Recommendation:",
            font=FONTS["heading"],
        ).grid(row=3, column=0, sticky="w", pady=(20, 5))

        ttk.Label(
            self.result_card,
            textvariable=self.recommendation_var,
            font=FONTS["body"],
            wraplength=650,
        ).grid(row=4, column=0, sticky="w")

        ttk.Label(
            self.result_card,
            text="Abnormal Lab Flags:",
            font=FONTS["heading"],
        ).grid(row=5, column=0, sticky="w", pady=(20, 5))

        self.flags_text = tk.Text(
            self.result_card,
            height=8,
            wrap="word",
            font=FONTS["body"],
        )
        self.flags_text.grid(row=6, column=0, sticky="ew")

        ttk.Label(
            self.result_card,
            text="Top Important Features:",
            font=FONTS["heading"],
        ).grid(row=7, column=0, sticky="w", pady=(20, 5))

        self.features_text = tk.Text(
            self.result_card,
            height=8,
            wrap="word",
            font=FONTS["body"],
        )
        self.features_text.grid(row=8, column=0, sticky="ew")

    def show_result(self, result: dict):
        self.result_data = result

        label = result.get("prediction_label", "Unknown")
        confidence = result.get("confidence", 0)
        low_prob = result.get("probability_low_risk", "N/A")
        risk_prob = result.get("probability_possible_risk", "N/A")
        recommendation = result.get("recommendation", "No recommendation available.")

        self.label_var.set(f"Risk Classification: {label}")
        self.confidence_var.set(f"Model Confidence: {confidence}")
        self.probability_var.set(
            f"Low Risk Probability: {low_prob} | Possible Risk Probability: {risk_prob}"
        )
        self.recommendation_var.set(recommendation)

        self.flags_text.delete("1.0", tk.END)
        abnormal_flags = result.get("abnormal_flags", {})

        if abnormal_flags:
            for feature, is_abnormal in abnormal_flags.items():
                status = "Abnormal" if is_abnormal else "Normal"
                self.flags_text.insert(tk.END, f"{feature}: {status}\n")
        else:
            self.flags_text.insert(tk.END, "No abnormal flag data available.")

        self.features_text.delete("1.0", tk.END)
        top_features = result.get("top_features") or result.get("key_markers") or {}

        if top_features:
            for feature, importance in top_features.items():
                self.features_text.insert(tk.END, f"{feature}: {importance}\n")
        else:
            self.features_text.insert(tk.END, "No feature importance data available.")