"""
Main Tkinter Window for HepatoCheck
"""

import tkinter as tk
from tkinter import ttk

from src.app.app_controller import AppController
from src.gui.styles import APP_TITLE, COLORS, FONTS
from src.gui.input_form import PatientInputForm
from src.gui.result_view import ResultView
from src.gui.batch_upload_view import BatchUploadView
from src.gui.history_view import HistoryView
from src.gui.disclaimer_view import DisclaimerView


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry("1100x700")
        self.root.minsize(950, 600)

        self.controller = AppController()

        self.setup_style()
        self.build_layout()
        self.show_home()

    def setup_style(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "TFrame",
            background=COLORS["bg"],
        )

        style.configure(
            "TLabel",
            background=COLORS["bg"],
            foreground=COLORS["text"],
            font=FONTS["body"],
        )

        style.configure(
            "TButton",
            font=FONTS["button"],
            padding=8,
        )

        style.configure(
            "Sidebar.TFrame",
            background=COLORS["sidebar"],
        )

        style.configure(
            "Sidebar.TButton",
            background=COLORS["sidebar_button"],
            foreground=COLORS["white"],
            font=FONTS["button"],
            padding=10,
        )

        style.map(
            "Sidebar.TButton",
            background=[("active", COLORS["sidebar_button_active"])],
        )

    def build_layout(self):
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.sidebar = ttk.Frame(
            self.root,
            width=230,
            style="Sidebar.TFrame",
            padding=15,
        )
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)

        self.content = ttk.Frame(
            self.root,
            padding=25,
        )
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.columnconfigure(0, weight=1)
        self.content.rowconfigure(0, weight=1)

        title = tk.Label(
            self.sidebar,
            text="HepatoCheck",
            bg=COLORS["sidebar"],
            fg=COLORS["white"],
            font=("Segoe UI", 18, "bold"),
        )
        title.pack(anchor="w", pady=(0, 25))

        nav_buttons = [
            ("Home", self.show_home),
            ("Patient Input", self.show_input_form),
            ("Batch Upload", self.show_batch_upload),
            ("History", self.show_history),
            ("Disclaimer", self.show_disclaimer),
        ]

        for text, command in nav_buttons:
            btn = ttk.Button(
                self.sidebar,
                text=text,
                command=command,
                style="Sidebar.TButton",
            )
            btn.pack(fill="x", pady=5)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_content()

        frame = ttk.Frame(self.content)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.columnconfigure(0, weight=1)

        ttk.Label(
            frame,
            text="Welcome to HepatoCheck",
            font=FONTS["title"],
        ).grid(row=0, column=0, sticky="w", pady=(0, 15))

        description = """
HepatoCheck is a liver risk screening application.

It allows healthcare users to enter patient laboratory data, analyze it using a trained machine learning model, and receive a clear risk classification.

You can use the app in two ways:

1. Single Patient Screening:
   Enter one patient's lab values manually and receive an immediate prediction.

2. Batch CSV Screening:
   Upload a CSV file containing multiple patient records and export the prediction results.

The app also keeps a temporary screening history during the current session.
"""

        ttk.Label(
            frame,
            text=description.strip(),
            font=FONTS["body"],
            wraplength=850,
            justify="left",
        ).grid(row=1, column=0, sticky="w", pady=(0, 25))

        ttk.Button(
            frame,
            text="Start Single Patient Screening",
            command=self.show_input_form,
        ).grid(row=2, column=0, sticky="w", pady=5)

        ttk.Button(
            frame,
            text="Upload Batch CSV",
            command=self.show_batch_upload,
        ).grid(row=3, column=0, sticky="w", pady=5)

    def show_input_form(self):
        self.clear_content()

        form = PatientInputForm(
            self.content,
            controller=self.controller,
            on_prediction_success=self.show_result,
        )
        form.grid(row=0, column=0, sticky="nsew")

    def show_result(self, result: dict):
        self.clear_content()

        result_view = ResultView(self.content)
        result_view.grid(row=0, column=0, sticky="nsew")
        result_view.show_result(result)

    def show_batch_upload(self):
        self.clear_content()

        batch_view = BatchUploadView(
            self.content,
            controller=self.controller,
        )
        batch_view.grid(row=0, column=0, sticky="nsew")

    def show_history(self):
        self.clear_content()

        history_view = HistoryView(
            self.content,
            controller=self.controller,
        )
        history_view.grid(row=0, column=0, sticky="nsew")
        history_view.refresh()

    def show_disclaimer(self):
        self.clear_content()

        disclaimer = DisclaimerView(self.content)
        disclaimer.grid(row=0, column=0, sticky="nsew")

    def run(self):
        self.root.mainloop()