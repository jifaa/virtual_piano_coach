"""
AI Piano Coach - Main Application
Premium modern light theme UI with polished navigation.
"""
import customtkinter as ctk
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import ConfigManager
from app.constants import WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT, WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT, SIDEBAR_WIDTH
from app.design_system import get_light_colors, adjust_color, RADIUS_SM, RADIUS_MD, RADIUS_LG


class AIPianoCoachApp(ctk.CTk):
    """Main application class with premium light theme."""

    def __init__(self):
        super().__init__()

        # Window config
        self.title("AI Piano Coach")
        self.geometry(f"{WINDOW_DEFAULT_WIDTH}x{WINDOW_DEFAULT_HEIGHT}")
        self.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        # Use light theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Load config
        self.config = ConfigManager()
        self.config.load()

        # Use premium light theme colors
        self.colors = get_light_colors()

        # Initialize core managers
        self.camera_manager = None
        self.midi_manager = None
        self.keyboard_mapper = None
        self.hand_tracker = None
        self.song_player = None
        self.overlay_renderer = None

        # Initialize core components
        self._init_core_components()

        # UI state
        self.pages = {}
        self.current_page = None

        # Create UI
        self._create_ui()

        # Show dashboard
        self.show_page("dashboard")

        # Protocol for closing
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _init_core_components(self):
        """Initialize core components."""
        from app.core import (
            CameraManager,
            MidiInputManager,
            KeyboardMapper,
            HandTracker,
            MidiSongPlayer,
            OverlayRenderer,
        )

        self.camera_manager = CameraManager()
        self.midi_manager = MidiInputManager()
        keyboard_config = self.config.config.get_keyboard_config()
        self.keyboard_mapper = KeyboardMapper(
            total_keys=keyboard_config.total_keys,
            base_midi=keyboard_config.base_midi,
        )

        if self.config.is_calibration_complete():
            calib = self.config.calibration
            if calib.points and len(calib.points) == 4:
                points = [(int(x), int(y)) for x, y in calib.points]
                self.keyboard_mapper.set_calibration_points(points)

        self.hand_tracker = HandTracker()
        self.song_player = MidiSongPlayer()
        self.overlay_renderer = OverlayRenderer(self.keyboard_mapper)

        self.overlay_renderer.show_finger_labels = self.config.config.show_finger_labels
        self.overlay_renderer.show_posture = self.config.config.show_posture_feedback
        self.overlay_renderer.show_note_numbers = self.config.config.show_note_numbers
        self.overlay_renderer.hand_split_note = self.config.config.hand_split_note

        midi_name = self.config.config.midi_input_name
        if midi_name:
            try:
                if self.midi_manager.connect(midi_name):
                    print(f"[App] MIDI connected to {midi_name}")
            except Exception as e:
                print(f"[App] MIDI connection failed: {e}")
                self.midi_manager.is_connected = False

    def _create_ui(self):
        """Create the main UI layout with proper grid weights."""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0, minsize=SIDEBAR_WIDTH)
        self.grid_columnconfigure(1, weight=1)

        self._create_sidebar()
        self._create_page_container()
        self._create_pages()

    def _create_sidebar(self):
        """Create a premium polished sidebar."""
        # Sidebar frame with subtle border
        sidebar = ctk.CTkFrame(
            self,
            fg_color=self.colors["sidebar_bg"],
            border_color=self.colors["border"],
            border_width=1,
            width=SIDEBAR_WIDTH,
        )
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.pack_propagate(False)

        # App branding header
        brand = ctk.CTkFrame(sidebar, fg_color="transparent")
        brand.pack(fill="x", padx=16, pady=(20, 16))

        # App icon (rounded accent square)
        icon_frame = ctk.CTkFrame(
            brand,
            fg_color=self.colors["accent"],
            corner_radius=RADIUS_SM,
            width=36,
            height=36,
        )
        icon_frame.pack(side="left", padx=(0, 12))
        icon_frame.pack_propagate(False)

        # Piano keys icon
        icon_inner = ctk.CTkFrame(icon_frame, fg_color="transparent")
        icon_inner.pack(expand=True)
        for i, color in enumerate(["#FFFFFF", "#FFFFFF", "#FFFFFF", "#334155"]):
            key = ctk.CTkFrame(icon_inner, fg_color=color, corner_radius=1, width=6, height=12)
            key.pack(side="left", padx=1)

        # App name and subtitle
        name_frame = ctk.CTkFrame(brand, fg_color="transparent")
        name_frame.pack(side="left", fill="x", expand=True)

        app_name = ctk.CTkLabel(
            name_frame,
            text="AI Piano Coach",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors["text_primary"],
        )
        app_name.pack(anchor="w")

        app_sub = ctk.CTkLabel(
            name_frame,
            text="Computer Vision + MIDI",
            font=ctk.CTkFont(size=10),
            text_color=self.colors["text_muted"],
        )
        app_sub.pack(anchor="w")

        # Separator line
        sep = ctk.CTkFrame(sidebar, fg_color=self.colors["border"], height=1)
        sep.pack(fill="x", padx=12, pady=(0, 12))

        # Navigation label
        nav_label = ctk.CTkLabel(
            sidebar,
            text="NAVIGASI",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=self.colors["text_muted"],
        )
        nav_label.pack(anchor="w", padx=20, pady=(0, 8))

        # Navigation items - premium styled buttons
        nav_items = [
            ("dashboard", "Dashboard", "Home"),
            ("setup", "Setup", "Config"),
            ("calibration", "Kalibrasi", "Calibrate"),
            ("practice", "Latihan", "Play"),
            ("panduan", "Panduan", "Guide"),
            ("settings", "Settings", "Settings"),
            ("diagnostics", "Diagnostik", "Info"),
        ]

        self.nav_buttons = {}
        self.nav_icons = {}
        self.nav_labels = {}
        self.nav_pills = {}

        for page_name, label, icon_text in nav_items:
            # Create nav button frame
            nav_btn = ctk.CTkButton(
                sidebar,
                text="",
                fg_color="transparent",
                hover_color=self.colors["nav_hover"],
                corner_radius=RADIUS_MD,
                height=44,
                border_width=0,
                command=lambda pn=page_name: self.show_page(pn),
            )
            nav_btn.pack(fill="x", padx=10, pady=2)
            nav_btn.pack_propagate(False)

            # Inner content frame
            inner = ctk.CTkFrame(nav_btn, fg_color="transparent")
            inner.pack(fill="both", expand=True)
            # Pass clicks through to the button
            inner.bind("<Button-1>", lambda e, pn=page_name: self.show_page(pn))

            # Active indicator pill (hidden by default)
            pill = ctk.CTkFrame(
                inner,
                fg_color="transparent",
                width=4,
                corner_radius=2,
            )
            pill.pack(side="left", fill="y", pady=8, padx=(4, 0))
            pill.pack_propagate(False)
            self.nav_pills[page_name] = pill

            # Icon circle
            icon_bg = ctk.CTkFrame(
                inner,
                fg_color=self.colors["bg_tertiary"],
                corner_radius=RADIUS_SM,
                width=28,
                height=28,
            )
            icon_bg.pack(side="left", padx=(8, 10), pady=8)
            icon_bg.pack_propagate(False)
            icon_bg.bind("<Button-1>", lambda e, pn=page_name: self.show_page(pn))

            icon_lbl = ctk.CTkLabel(
                icon_bg,
                text=self._get_nav_icon(page_name),
                font=ctk.CTkFont(size=13),
                text_color=self.colors["text_muted"],
            )
            icon_lbl.pack(expand=True)
            icon_lbl.bind("<Button-1>", lambda e, pn=page_name: self.show_page(pn))
            self.nav_icons[page_name] = icon_lbl

            # Label
            lbl = ctk.CTkLabel(
                inner,
                text=label,
                font=ctk.CTkFont(size=14, weight="normal"),
                text_color=self.colors["text_secondary"],
                anchor="w",
            )
            lbl.pack(side="left", fill="x", expand=True)
            lbl.bind("<Button-1>", lambda e, pn=page_name: self.show_page(pn))

            # Store reference
            self.nav_buttons[page_name] = nav_btn
            self.nav_labels[page_name] = lbl

        # Bottom spacer
        spacer = ctk.CTkFrame(sidebar, fg_color="transparent")
        spacer.pack(fill="both", expand=True)

        # Status footer card
        footer = ctk.CTkFrame(
            sidebar,
            fg_color=self.colors["bg_tertiary"],
            corner_radius=RADIUS_MD,
        )
        footer.pack(fill="x", padx=12, pady=(0, 16))

        # Footer inner layout
        footer_inner = ctk.CTkFrame(footer, fg_color="transparent")
        footer_inner.pack(fill="x", padx=14, pady=12)

        # Status indicator dot - using pack, no place()
        status_dot = ctk.CTkFrame(
            footer_inner,
            fg_color=self.colors["success"],
            corner_radius=5,
            width=10,
            height=10,
        )
        status_dot.pack(side="left", padx=(0, 10))
        status_dot.pack_propagate(False)

        # Status text area
        status_content = ctk.CTkFrame(footer_inner, fg_color="transparent")
        status_content.pack(side="left", fill="x", expand=True)

        self.status_label = ctk.CTkLabel(
            status_content,
            text="Ready",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.colors["text_primary"],
            anchor="w",
        )
        self.status_label.pack(anchor="w")

        status_sub = ctk.CTkLabel(
            status_content,
            text="Sistem aktif",
            font=ctk.CTkFont(size=10),
            text_color=self.colors["text_muted"],
            anchor="w",
        )
        status_sub.pack(anchor="w")

        self.sidebar = sidebar

    def _get_nav_icon(self, page_name: str) -> str:
        """Get text icon for navigation item."""
        icons = {
            "dashboard": "◈",
            "setup": "⚙",
            "calibration": "◎",
            "practice": "▶",
            "panduan": "?",
            "settings": "≡",
            "diagnostics": "ℹ",
        }
        return icons.get(page_name, "○")

    def _create_page_container(self):
        """Create page container."""
        self.page_container = ctk.CTkFrame(
            self,
            fg_color=self.colors["bg_primary"],
        )
        self.page_container.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)

    def _create_pages(self):
        """Create all page instances."""
        from app.ui.pages import (
            DashboardPage, SetupPage, CalibrationPage,
            PracticePage, GuidePage, SettingsPage, DiagnosticsPage,
        )

        page_classes = {
            "dashboard": DashboardPage,
            "setup": SetupPage,
            "calibration": CalibrationPage,
            "practice": PracticePage,
            "panduan": GuidePage,
            "settings": SettingsPage,
            "diagnostics": DiagnosticsPage,
        }

        for page_name, PageClass in page_classes.items():
            page = PageClass(self.page_container, self)
            page.pack(fill="both", expand=True)
            page.pack_forget()
            self.pages[page_name] = page

    def show_page(self, page_name: str):
        """Show a specific page with navigation highlight update."""
        if self.current_page and self.current_page in self.pages:
            self.pages[self.current_page].pack_forget()
            self.pages[self.current_page].on_disappear()

        if page_name in self.pages:
            self.pages[page_name].on_appear()
            self.pages[page_name].pack(fill="both", expand=True)
            self.current_page = page_name
            self._update_nav_buttons(page_name)

    def _update_nav_buttons(self, active_page: str):
        """Update navigation button states."""
        for page_name, nav_btn in self.nav_buttons.items():
            icon_lbl = self.nav_icons[page_name]
            text_lbl = self.nav_labels[page_name]
            pill = self.nav_pills[page_name]

            if page_name == active_page:
                # Active state - accent background
                nav_btn.configure(
                    fg_color=self.colors["nav_active_bg"],
                    hover_color=self.colors["nav_active_bg"],
                )
                pill.configure(fg_color=self.colors["accent"])
                icon_lbl.configure(text_color=self.colors["accent"])
                text_lbl.configure(
                    text_color=self.colors["accent"],
                    font=ctk.CTkFont(size=14, weight="bold"),
                )
            else:
                # Default state
                nav_btn.configure(
                    fg_color="transparent",
                    hover_color=self.colors["nav_hover"],
                )
                pill.configure(fg_color="transparent")
                icon_lbl.configure(text_color=self.colors["text_muted"])
                text_lbl.configure(
                    text_color=self.colors["text_secondary"],
                    font=ctk.CTkFont(size=14, weight="normal"),
                )

    def set_appearance_mode(self, mode: str):
        """Set appearance mode."""
        ctk.set_appearance_mode(mode)

    def create_keyboard_mapper(self, keyboard_config):
        """Create a keyboard mapper."""
        return self.keyboard_mapper.__class__(
            total_keys=keyboard_config.total_keys,
            base_midi=keyboard_config.base_midi,
        )

    def update_status(self, text: str, status: str = "idle"):
        """Update status label in sidebar footer."""
        status_colors = {
            "success": self.colors["success"],
            "warning": self.colors["warning"],
            "error": self.colors["error"],
            "info": self.colors["info"],
            "idle": self.colors["text_secondary"],
        }
        color = status_colors.get(status, self.colors["text_secondary"])
        self.status_label.configure(text=text, text_color=color)

    def _on_close(self):
        """Handle window close."""
        print("[App] Closing application...")

        if hasattr(self, 'practice_engine') and self.practice_engine:
            self.practice_engine.close()
        if self.camera_manager:
            self.camera_manager.close()
        if self.midi_manager:
            self.midi_manager.disconnect()
        if self.hand_tracker:
            self.hand_tracker.close()
        if self.song_player:
            self.song_player.unload()

        self.destroy()