"""
Batch CSV Upload Page
"""

import csv
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from src.ml.predict import FEATURE_REQUEST_ORDER
from src.gui.styles import FONTS


class BatchUploadView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.batch_results = []

        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

        ttk.Label(
            self,
            text="Batch CSV Prediction",
            font=FONTS["title"],
        ).grid(row=0, column=0, sticky="w", pady=(0, 10))

        ttk.Label(
            self,
            text="Upload a CSV file containing the required patient features.",
            font=FONTS["subtitle"],
        ).grid(row=1, column=0, sticky="w", pady=(0, 15))

        required_text = "Required columns: " + ", ".join(FEATURE_REQUEST_ORDER)
        ttk.Label(
            self,
            text=required_text,
            font=FONTS["small"],
            wraplength=800,
        ).grid(row=2, column=0, sticky="w", pady=(0, 15))

        button_frame = ttk.Frame(self)
        button_frame.grid(row=3, column=0, sticky="ew", pady=(0, 10))

        ttk.Button(
            button_frame,
            text="Upload CSV",
            command=self.upload_csv,
        ).grid(row=0, column=0, padx=(0, 10))

        ttk.Button(
            button_frame,
            text="Export Results to CSV",
            command=self.export_csv,
        ).grid(row=0, column=1, padx=(0, 10))

        ttk.Button(
            button_frame,
            text="Clear Table",
            command=self.clear_table,
        ).grid(row=0, column=2)

        table_frame = ttk.Frame(self)
        table_frame.grid(row=4, column=0, sticky="nsew")
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        columns = [
            "Age", "Sex", "ALB", "ALP", "ALT", "AST", "BIL",
            "CHE", "CHOL", "CREA", "GGT", "PROT",
            "prediction_label", "confidence",
            "probability_low_risk", "probability_possible_risk",
        ]

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15,
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)

        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

    def upload_csv(self):
        filepath = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV Files", "*.csv")],
        )

        if not filepath:
            return

        try:
            with open(filepath, "r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                records = list(reader)

            if not records:
                messagebox.showerror("Empty File", "The selected CSV file is empty.")
                return

            missing_columns = [
                col for col in FEATURE_REQUEST_ORDER
                if col not in records[0]
            ]

            if missing_columns:
                messagebox.showerror(
                    "Missing Columns",
                    "Missing required columns:\n" + "\n".join(missing_columns),
                )
                return

            results, errors = self.controller.predict_csv_records(records)
            self.batch_results = results
            self.populate_table(results)

            if errors:
                messagebox.showwarning(
                    "Some Rows Were Skipped",
                    "\n".join(errors[:10]) +
                    ("\n\nMore errors exist..." if len(errors) > 10 else ""),
                )
            else:
                messagebox.showinfo("Success", "Batch prediction completed successfully.")

        except Exception as e:
            messagebox.showerror("Upload Failed", str(e))

    def populate_table(self, rows: list[dict]):
        self.clear_table()

        for row in rows:
            values = [
                row.get("Age", ""),
                row.get("Sex", ""),
                row.get("ALB", ""),
                row.get("ALP", ""),
                row.get("ALT", ""),
                row.get("AST", ""),
                row.get("BIL", ""),
                row.get("CHE", ""),
                row.get("CHOL", ""),
                row.get("CREA", ""),
                row.get("GGT", ""),
                row.get("PROT", ""),
                row.get("prediction_label", ""),
                row.get("confidence", ""),
                row.get("probability_low_risk", ""),
                row.get("probability_possible_risk", ""),
            ]

            self.tree.insert("", tk.END, values=values)

    def clear_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def export_csv(self):
        if not self.batch_results:
            messagebox.showerror("No Results", "There are no batch results to export.")
            return

        filepath = filedialog.asksaveasfilename(
            title="Save Results",
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
        )

        if not filepath:
            return

        try:
            self.controller.export_results_to_csv(self.batch_results, filepath)
            messagebox.showinfo("Exported", "Results exported successfully.")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))