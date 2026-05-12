"""
HepatoCheck - Main Entry Point
Hepatitis C Prediction Application
"""

import sys
from src.gui.main_window import MainWindow


def main():
    """Initialize and run the application."""
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
