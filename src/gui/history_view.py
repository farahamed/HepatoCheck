"""
Screening History Page
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from src.gui.styles import FONTS


class HistoryView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        ttk.Label(
            self,
            text="Screening History",
            font=FONTS["title"],
        ).grid(row=0, column=0, sticky="w", pady=(0, 10))

        button_frame = ttk.Frame(self)
        button_frame.grid(row=1, column=0, sticky="w", pady=(0, 10))

        ttk.Button(
            button_frame,
            text="Refresh History",
            command=self.refresh,
        ).grid(row=0, column=0, padx=(0, 10))

        ttk.Button(
            button_frame,
            text="Export History to TXT",
            command=self.export_txt,
        ).grid(row=0, column=1)

        columns = ["timestamp", "age", "sex", "prediction", "confidence"]

        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=18,
        )

        self.tree.heading("timestamp", text="Time")
        self.tree.heading("age", text="Age")
        self.tree.heading("sex", text="Sex")
        self.tree.heading("prediction", text="Prediction")
        self.tree.heading("confidence", text="Confidence")

        for col in columns:
            self.tree.column(col, width=150, anchor="center")

        self.tree.grid(row=2, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=2, column=1, sticky="ns")

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        history = self.controller.get_history()

        for item in history:
            patient_input = item["input"]
            result = item["result"]

            self.tree.insert(
                "",
                tk.END,
                values=[
                    item["timestamp"],
                    patient_input.get("Age", ""),
                    patient_input.get("Sex", ""),
                    result.get("prediction_label", ""),
                    result.get("confidence", ""),
                ],
            )

    def export_txt(self):
        filepath = filedialog.asksaveasfilename(
            title="Save History",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
        )

        if not filepath:
            return

        try:
            self.controller.export_history_to_txt(filepath)
            messagebox.showinfo("Exported", "History exported successfully.")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))