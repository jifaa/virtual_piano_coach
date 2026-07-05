"""
AI Piano Coach - Diagnostics Page
Premium diagnostic monitoring page with clean status panels.
"""
import customtkinter as ctk
from app.ui.base_page import BasePage
from app.design_system import (
    get_light_colors,
    RADIUS_MD, RADIUS_LG,
    SECTION_GAP, CARD_GAP, CARD_PADDING,
)


class DiagnosticsPage(BasePage):
    """Diagnostics monitoring page with premium styling."""

    def __init__(self, parent, app_controller):
        self.refresh_id = None
        self.colors = get_light_colors()
        super().__init__(
            parent, app_controller,
            "Diagnostik",
            "Monitor status hardware dan debug informasi"
        )
        self._create_content()

    def _create_content(self):
        """Create diagnostics content."""
        # Status cards row
        self._status_cards()

        # Info panels in scrollable frame
        scroll = self.scrollable_frame(self.content_frame)
        scroll.pack(fill="both", expand=True)

        self._camera_panel(scroll)
        self._midi_panel(scroll)
        self._config_panel(scroll)
        self._calib_panel(scroll)

        # Action buttons
        self._action_bar()

    def _status_cards(self):
        """Top status overview cards with proper grid column weights."""
        row = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        row.pack(fill="x", pady=(0, SECTION_GAP))

        # Configure 4 equal columns
        for col in range(4):
            row.grid_columnconfigure(col, weight=1, uniform="diag_status")

        cards = [
            ("Kamera", "Memuat...", self.colors["text_secondary"]),
            ("MIDI", "Memuat...", self.colors["text_secondary"]),
            ("Kalibrasi", "Memuat...", self.colors["text_secondary"]),
            ("Note Aktif", "--", self.colors["text_muted"]),
        ]
        self.status_widgets = {}
        for i, (title, value, color) in enumerate(cards):
            self._mini_card(row, i, title, value, color)

    def _mini_card(self, parent, index, title, value, color):
        """Small status card with proper grid placement."""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors["bg_secondary"],
            border_color=self.colors["border"],
            border_width=1,
            corner_radius=RADIUS_MD,
        )
        padx = (0, 8) if index < 3 else (0, 0)
        card.grid(row=0, column=index, sticky="nsew", padx=padx)

        # Status indicator dot
        dot = ctk.CTkFrame(
            card,
            fg_color=color,
            corner_radius=4,
            width=8,
            height=8,
        )
        dot.pack(anchor="center", pady=(12, 0))
        dot.pack_propagate(False)

        value_lbl = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=color,
            wraplength=140,
        )
        value_lbl.pack(padx=14, pady=(6, 4))

        title_lbl = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=11),
            text_color=self.colors["text_secondary"],
        )
        title_lbl.pack(padx=14, pady=(0, 12))

        key = title.lower().replace(" ", "_")
        self.status_widgets[key] = value_lbl

    def _panel(self, parent, title):
        """Info panel card with terminal-style display."""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors["bg_secondary"],
            border_color=self.colors["border"],
            border_width=1,
            corner_radius=RADIUS_LG,
        )
        card.pack(fill="x", pady=(0, CARD_GAP))

        # Panel header with macOS-style dots
        hdr = ctk.CTkFrame(card, fg_color=self.colors["bg_tertiary"])
        hdr.pack(fill="x")
        hdr.configure(height=38)
        hdr.pack_propagate(False)

        hdr_inner = ctk.CTkFrame(hdr, fg_color="transparent")
        hdr_inner.pack(fill="x", padx=16, pady=0)

        # Traffic lights
        dots_frame = ctk.CTkFrame(hdr_inner, fg_color="transparent")
        dots_frame.pack(side="left", pady=8)

        for color in ["#EF4444", "#F59E0B", "#10B981"]:
            dot = ctk.CTkFrame(
                dots_frame,
                fg_color=color,
                corner_radius=5,
                width=10,
                height=10,
            )
            dot.pack(side="left", padx=2)
            dot.pack_propagate(False)

        # Title
        lbl = ctk.CTkLabel(
            hdr_inner,
            text=title,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.colors["text_secondary"],
        )
        lbl.pack(side="left", padx=(12, 0), pady=8)

        # Content with wraplength
        info = ctk.CTkLabel(
            card,
            text="Memuat...",
            font=ctk.CTkFont(size=12, family="Consolas"),
            text_color=self.colors["text_primary"],
            justify="left",
            anchor="nw",
            wraplength=700,
        )
        info.pack(fill="both", expand=True, padx=16, pady=12)
        return info

    def _camera_panel(self, parent):
        """Camera info panel."""
        self.camera_info = self._panel(parent, "Kamera")

    def _midi_panel(self, parent):
        """MIDI info panel."""
        self.midi_info = self._panel(parent, "MIDI Input")

    def _config_panel(self, parent):
        """Config info panel."""
        self.config_info = self._panel(parent, "Konfigurasi")

    def _calib_panel(self, parent):
        """Calibration info panel."""
        self.calib_info = self._panel(parent, "Kalibrasi")

    def _action_bar(self):
        """Action buttons."""
        row = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        row.pack(fill="x", pady=(8, 0))

        refresh = ctk.CTkButton(
            row,
            text="↻ Refresh",
            command=self._refresh,
            width=160,
            height=48,
            corner_radius=RADIUS_LG,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            text_color=self.colors["text_on_accent"],
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        refresh.pack(side="left", padx=(0, 14))

        setup = ctk.CTkButton(
            row,
            text="⚙ Buka Setup",
            command=lambda: self.app.show_page("setup"),
            width=160,
            height=48,
            corner_radius=RADIUS_LG,
            fg_color=self.colors["bg_tertiary"],
            hover_color=self.colors["bg_hover"],
            text_color=self.colors["text_primary"],
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        setup.pack(side="left")

    def _refresh(self):
        """Refresh all info."""
        self._update_camera()
        self._update_midi()
        self._update_config()
        self._update_calib()
        self._update_status_cards()

    def _update_status_cards(self):
        """Update status cards."""
        cam = self.app.camera_manager
        midi = self.app.midi_manager
        calib = self.app.config.calibration

        # Camera
        cam_w = self.status_widgets.get("kamera")
        if cam_w:
            if cam.is_opened:
                cam_w.configure(
                    text=f"Camera {cam.camera_index}",
                    text_color=self.colors["success"]
                )
            else:
                cam_w.configure(
                    text="Tidak Terbuka",
                    text_color=self.colors["error"]
                )

        # MIDI
        midi_w = self.status_widgets.get("midi")
        if midi_w:
            if midi.is_connected:
                name = midi.port_name or "Terhubung"
                short = name[:14] + "..." if len(name) > 14 else name
                midi_w.configure(
                    text=short,
                    text_color=self.colors["success"]
                )
            else:
                midi_w.configure(
                    text="Tidak Terhubung",
                    text_color=self.colors["error"]
                )

        # Calibration
        calib_w = self.status_widgets.get("kalibrasi")
        if calib_w:
            if calib.is_complete():
                calib_w.configure(
                    text=f"{len(calib.points)}/4 Titik",
                    text_color=self.colors["success"]
                )
            else:
                calib_w.configure(
                    text=f"{len(calib.points)}/4 Titik",
                    text_color=self.colors["warning"]
                )

        # Active notes
        notes_w = self.status_widgets.get("note_aktif")
        active = midi.get_active_notes()
        if notes_w:
            if active:
                notes_w.configure(
                    text=f"{len(active)} Aktif",
                    text_color=self.colors["accent"]
                )
            else:
                notes_w.configure(
                    text="--",
                    text_color=self.colors["text_muted"]
                )

    def _update_camera(self):
        """Update camera info."""
        cam = self.app.camera_manager
        lines = [
            f"Index    : {cam.camera_index}",
            f"Status   : {'Terbuka' if cam.is_opened else 'Tertutup'}",
            f"FPS      : {cam.fps:.1f}",
        ]
        if cam.error_message:
            lines.append(f"Error    : {cam.error_message}")
        available = cam.detect_cameras()
        lines.append(f"Terdeteksi: {len(available)} device")
        for idx, name in available:
            lines.append(f"  [{idx}] {name}")
        self.camera_info.configure(text="\n".join(lines))

    def _update_midi(self):
        """Update MIDI info."""
        midi = self.app.midi_manager
        lines = []
        if midi.is_connected:
            lines.append(f"Status   : Terhubung")
            lines.append(f"Port     : {midi.port_name or '-'}")
        else:
            lines.append("Status   : Tidak Terhubung")
            lines.append("Port     : -")
        inputs = midi.detect_inputs()
        lines.append(f"Terdeteksi: {len(inputs)} device")
        for name in inputs:
            lines.append(f"  - {name}")
        if midi.error_message:
            lines.append(f"Error    : {midi.error_message}")
        self.midi_info.configure(text="\n".join(lines))

    def _update_config(self):
        """Update config info."""
        cfg = self.app.config.config
        lines = [
            f"Camera      : {cfg.camera_index}",
            f"MIDI        : {cfg.midi_input_name or '-'}",
            f"Keyboard    : {cfg.keyboard_size} Keys",
            f"MIDI File   : {cfg.midi_file_path or 'Tidak ada'}",
            f"Mode        : {cfg.appearance_mode}",
            f"Tema        : {cfg.color_theme}",
            f"Mirror      : {'Ya' if cfg.camera_mirror else 'Tidak'}",
            f"Finger Lbl  : {'Ya' if cfg.show_finger_labels else 'Tidak'}",
            f"Posture     : {'Ya' if cfg.show_posture_feedback else 'Tidak'}",
            f"Split Note  : {cfg.hand_split_note}",
        ]
        self.config_info.configure(text="\n".join(lines))

    def _update_calib(self):
        """Update calibration info."""
        calib = self.app.config.calibration
        lines = []
        if calib.is_complete():
            lines.append("Status    : Selesai")
            lines.append(f"Titik     : {len(calib.points)}/4")
            lines.append(f"Keyboard  : {calib.keyboard_size} Keys")
            lines.append(f"Kamera    : {calib.camera_index}")
            lines.append(f"Tuts      : {len(calib.tuts_rects)}")
            for i, pt in enumerate(calib.points):
                lines.append(f"T{i+1}      : ({pt[0]:.0f}, {pt[1]:.0f})")
        else:
            lines.append("Status    : Belum Lengkap")
            lines.append(f"Titik     : {len(calib.points)}/4")
        self.calib_info.configure(text="\n".join(lines))

    def on_appear(self):
        """On page appear."""
        self._refresh()

    def on_disappear(self):
        """On page disappear."""
        pass