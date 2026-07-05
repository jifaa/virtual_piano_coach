"""
AI Piano Coach - UI Pages Package
Berisi halaman-halaman UI aplikasi.
"""
from app.ui.pages.dashboard_page import DashboardPage
from app.ui.pages.setup_page import SetupPage
from app.ui.pages.calibration_page import CalibrationPage
from app.ui.pages.practice_page import PracticePage
from app.ui.pages.guide_page import GuidePage
from app.ui.pages.settings_page import SettingsPage
from app.ui.pages.diagnostics_page import DiagnosticsPage

__all__ = [
    "DashboardPage",
    "SetupPage",
    "CalibrationPage",
    "PracticePage",
    "GuidePage",
    "SettingsPage",
    "DiagnosticsPage",
]