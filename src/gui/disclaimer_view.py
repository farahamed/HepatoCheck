"""
Medical Disclaimer Page
"""

from tkinter import ttk

from src.gui.styles import FONTS


class DisclaimerView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)

        ttk.Label(
            self,
            text="Medical Disclaimer",
            font=FONTS["title"],
        ).grid(row=0, column=0, sticky="w", pady=(0, 20))

        disclaimer_text = """
HepatoCheck is an educational medical data analytics application.

The prediction shown by this application is based on a machine learning model trained on a public dataset. It is intended to support screening and learning purposes only.

This application does not provide a medical diagnosis.

A “Possible Risk” result does not confirm liver disease, hepatitis, fibrosis, or cirrhosis. A “Low Risk” result does not guarantee that the patient is healthy.

Patients should always consult a licensed clinician for proper diagnosis, medical interpretation, and treatment decisions.

Clinical laboratory results must be interpreted together with symptoms, physical examination, medical history, imaging, and additional confirmatory tests.
"""

        ttk.Label(
            self,
            text=disclaimer_text.strip(),
            font=FONTS["body"],
            wraplength=800,
            justify="left",
        ).grid(row=1, column=0, sticky="w")