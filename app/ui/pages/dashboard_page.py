"""
AI Piano Coach - Dashboard Page
Premium modern landing page with polished status cards and quick actions.
"""
import customtkinter as ctk
from app.ui.base_page import BasePage
from app.design_system import (
    get_light_colors, adjust_color,
    RADIUS_MD, RADIUS_SM, RADIUS_LG, RADIUS_FULL,
    SECTION_GAP, CARD_GAP, CARD_PADDING,
)


class DashboardPage(BasePage):
    """Dashboard with premium welcome and status overview."""

    def __init__(self, parent, app_controller):
        super().__init__(
            parent, app_controller,
            "Dashboard",
            "Selamat datang di AI Piano Coach"
        )
        self._create_content()

    def _create_content(self):
        """Create dashboard content inside scrollable frame."""
        # Scrollable container so nothing clips on small windows
        scroll = self.scrollable_frame(self.content_frame)
        scroll.pack(fill="both", expand=True)

        # Welcome hero card
        self._create_welcome_card(scroll)

        # Status overview row - device status cards
        self._create_status_row(scroll)

        # Quick actions
        self._create_actions_row(scroll)

        # Tips card
        self._create_tips_card(scroll)

    def _create_welcome_card(self, parent):
        """Create premium welcome hero card."""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors["accent_light"],
            border_color=self.colors["info_border"],
            border_width=1,
            corner_radius=RADIUS_LG,
        )
        card.pack(fill="x", pady=(0, SECTION_GAP))

        # Hero content
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=CARD_PADDING + 8, pady=CARD_PADDING + 8)

        # Left side - description
        left = ctk.CTkFrame(content, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True)

        title_lbl = ctk.CTkLabel(
            left,
            text="Selamat Datang di AI Piano Coach",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=self.colors["accent_hover"],
            anchor="w",
        )
        title_lbl.pack(anchor="w")

        desc_lbl = ctk.CTkLabel(
            left,
            text="Asisten cerdas untuk berlatih piano dengan deteksi postur tangan dan analisis MIDI real-time. "
                 "Mulai setup untuk menghubungkan perangkat Anda.",
            font=ctk.CTkFont(size=14),
            text_color=self.colors["text_secondary"],
            justify="left",
            wraplength=600,
            anchor="w",
        )
        desc_lbl.pack(anchor="w", pady=(8, 0))

        # Right side - quick setup CTA
        right = ctk.CTkFrame(content, fg_color="transparent")
        right.pack(side="right", padx=(20, 0))

        cta_btn = self.btn_cta(
            right,
            text="Mulai Setup →",
            command=lambda: self.app.show_page("setup"),
            width=180,
        )
        cta_btn.pack(pady=8)

    def _create_status_row(self, parent):
        """Create status overview row with device status cards using grid."""
        # Section label
        section_lbl = ctk.CTkLabel(
            parent,
            text="STATUS PERANGKAT",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.colors["text_muted"],
            anchor="w",
        )
        section_lbl.pack(anchor="w", pady=(0, 8))

        # Grid container for 4 equal-width cards
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=(0, SECTION_GAP))
        for col in range(4):
            row.grid_columnconfigure(col, weight=1, uniform="status")

        # Camera status
        self.camera_card = self.device_status_card(
            row, "Kamera", "Belum Dipilih", "info", hint="Pilih kamera di Setup"
        )
        self.camera_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=0)

        # MIDI status
        self.midi_card = self.device_status_card(
            row, "MIDI Input", "Belum Dipilih", "info", hint="Pilih device di Setup"
        )
        self.midi_card.grid(row=0, column=1, sticky="nsew", padx=(4, 8), pady=0)

        # Keyboard status
        self.keyboard_card = self.device_status_card(
            row, "Keyboard", "61 Keys", "info", hint="Ukuran keyboard"
        )
        self.keyboard_card.grid(row=0, column=2, sticky="nsew", padx=(4, 8), pady=0)

        # MIDI guide status
        self.guide_card = self.device_status_card(
            row, "MIDI Guide", "Tidak Ada", "info", hint="Free Play mode"
        )
        self.guide_card.grid(row=0, column=3, sticky="nsew", padx=(4, 0), pady=0)

    def _create_actions_row(self, parent):
        """Create quick action buttons row using grid."""
        # Section label
        section_lbl = ctk.CTkLabel(
            parent,
            text="AKSI CEPAT",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.colors["text_muted"],
            anchor="w",
        )
        section_lbl.pack(anchor="w", pady=(0, 8))

        actions = [
            ("Setup", "Konfigurasi perangkat keras", "setup", "⚙"),
            ("Kalibrasi", "Tandai area keyboard", "calibration", "◎"),
            ("Latihan", "Mulai berlatih piano", "practice", "▶"),
            ("Panduan", "Pelajari cara pakai", "panduan", "?"),
        ]

        # Grid row for actions
        actions_row = ctk.CTkFrame(parent, fg_color="transparent")
        actions_row.pack(fill="x", pady=(0, SECTION_GAP))
        for col in range(4):
            actions_row.grid_columnconfigure(col, weight=1, uniform="action")

        for i, (text, desc, page, icon) in enumerate(actions):
            btn_frame = self._make_action_card(actions_row, text, desc, page, icon)
            padx_left = 0 if i == 0 else 4
            padx_right = 0 if i == 3 else 8
            btn_frame.grid(row=0, column=i, sticky="nsew", padx=(padx_left, padx_right), pady=0)

    def _make_action_card(self, parent, text: str, description: str, page: str, icon: str):
        """Make a premium action card."""
        btn = ctk.CTkFrame(
            parent,
            fg_color=self.colors["bg_secondary"],
            border_color=self.colors["border"],
            border_width=1,
            corner_radius=RADIUS_MD,
            cursor="hand2",
        )

        # Inner content
        inner = ctk.CTkFrame(btn, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=16, pady=14)

        # Icon
        icon_frame = ctk.CTkFrame(
            inner,
            fg_color=self.colors["accent_light"],
            corner_radius=RADIUS_SM,
            width=36,
            height=36,
        )
        icon_frame.pack(anchor="w", pady=(0, 10))
        icon_frame.pack_propagate(False)

        icon_lbl = ctk.CTkLabel(
            icon_frame,
            text=icon,
            font=ctk.CTkFont(size=16),
            text_color=self.colors["accent"],
        )
        icon_lbl.pack(expand=True)

        # Title
        title_lbl = ctk.CTkLabel(
            inner,
            text=text,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["text_primary"],
            anchor="w",
        )
        title_lbl.pack(anchor="w")

        # Description with wraplength
        desc_lbl = ctk.CTkLabel(
            inner,
            text=description,
            font=ctk.CTkFont(size=11),
            text_color=self.colors["text_secondary"],
            anchor="w",
            wraplength=200,
        )
        desc_lbl.pack(anchor="w", pady=(2, 0))

        # Click binding on all widgets
        def on_click(e, p=page):
            self.app.show_page(p)

        for widget in [btn, inner, icon_frame, icon_lbl, title_lbl, desc_lbl]:
            widget.bind("<Button-1>", on_click)

        # Hover effect
        def on_enter(e, b=btn):
            b.configure(border_color=self.colors["accent"], fg_color=self.colors["bg_hover"])

        def on_leave(e, b=btn):
            b.configure(border_color=self.colors["border"], fg_color=self.colors["bg_secondary"])

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        return btn

    def _create_tips_card(self, parent):
        """Create tips/next steps card."""
        # Section label
        section_lbl = ctk.CTkLabel(
            parent,
            text="LANGKAH SELANJUTNYA",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.colors["text_muted"],
            anchor="w",
        )
        section_lbl.pack(anchor="w", pady=(0, 8))

        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors["bg_secondary"],
            border_color=self.colors["border"],
            border_width=1,
            corner_radius=RADIUS_LG,
        )
        card.pack(fill="x", pady=(0, CARD_GAP))

        tips = [
            ("1", "Hubungkan keyboard MIDI ke komputer via USB"),
            ("2", "Pilih kamera yang mengarah ke keyboard piano"),
            ("3", "Lakukan kalibrasi 4 titik pada halaman Kalibrasi"),
            ("4", "Tekan Mulai Latihan pada halaman Latihan untuk memulai sesi"),
        ]

        for num, text in tips:
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=CARD_PADDING, pady=6)

            # Number badge
            badge = ctk.CTkFrame(
                row,
                fg_color=self.colors["accent"],
                corner_radius=RADIUS_FULL,
                width=26,
                height=26,
            )
            badge.pack(side="left", padx=(0, 14))
            badge.pack_propagate(False)

            badge_lbl = ctk.CTkLabel(
                badge,
                text=num,
                text_color=self.colors["text_on_accent"],
                font=ctk.CTkFont(size=12, weight="bold"),
            )
            badge_lbl.pack(expand=True)

            # Tip text with wraplength
            tip_lbl = ctk.CTkLabel(
                row,
                text=text,
                font=ctk.CTkFont(size=13),
                text_color=self.colors["text_secondary"],
                anchor="w",
                wraplength=600,
            )
            tip_lbl.pack(side="left", fill="x", expand=True)

        # Bottom padding
        ctk.CTkFrame(card, fg_color="transparent", height=8).pack()

    def on_appear(self):
        """Refresh status when page appears."""
        self._update_status()

    def _update_status(self):
        """Update status cards."""
        config = self.app.config.config

        # Camera status
        if self.app.camera_manager and self.app.camera_manager.is_opened:
            self._update_device_card(
                self.camera_card, "Kamera",
                f"Camera {config.camera_index}", "success", "Tersambung"
            )
        else:
            self._update_device_card(
                self.camera_card, "Kamera",
                "Belum Dipilih", "info", "Pilih di Setup"
            )

        # MIDI status
        if self.app.midi_manager and self.app.midi_manager.is_connected:
            name = config.midi_input_name or "Terhubung"
            short_name = name[:20] + "..." if len(name) > 20 else name
            self._update_device_card(
                self.midi_card, "MIDI Input",
                short_name, "success", "Device aktif"
            )
        else:
            self._update_device_card(
                self.midi_card, "MIDI Input",
                "Belum Dipilih", "info", "Pilih di Setup"
            )

        # Keyboard
        self._update_device_card(
            self.keyboard_card, "Keyboard",
            f"{config.keyboard_size} Keys", "info", "Ukuran keyboard"
        )

        # Guide file
        if config.midi_file_path:
            filename = config.midi_file_path.split("/")[-1].split("\\")[-1]
            short_name = filename[:18] + "..." if len(filename) > 18 else filename
            self._update_device_card(
                self.guide_card, "MIDI Guide",
                short_name, "success", "Guide aktif"
            )
        else:
            self._update_device_card(
                self.guide_card, "MIDI Guide",
                "Free Play", "info", "Tanpa guide"
            )

    def _update_device_card(self, card, title, value, status, hint):
        """Update a device status card by finding labels in the card hierarchy."""
        colors_map = {
            "success": (self.colors["success"], self.colors["success_light"], self.colors["success_text"]),
            "warning": (self.colors["warning"], self.colors["warning_light"], self.colors["warning_text"]),
            "error": (self.colors["error"], self.colors["error_light"], self.colors["error_text"]),
            "info": (self.colors["info"], self.colors["info_light"], self.colors["info_text"]),
        }
        color, bg, text_color = colors_map.get(status, colors_map["info"])

        card.configure(fg_color=bg)

        # Walk the widget tree to find and update labels
        self._update_card_labels(card, title, value, hint, color, text_color)

    def _update_card_labels(self, widget, title, value, hint, color, text_color):
        """Recursively find and update labels in a device status card."""
        for child in widget.winfo_children():
            if isinstance(child, ctk.CTkLabel):
                current_text = child.cget("text")
                current_font = child.cget("font")
                # Identify by font characteristics
                if hasattr(current_font, 'cget'):
                    pass  # CTkFont doesn't expose cget easily
                # Use heuristic: title is small bold, value is large bold, hint is small
                # We'll match by checking if text matches any of the expected values
            elif isinstance(child, ctk.CTkFrame):
                # Check if it's the dot frame (small, colored)
                try:
                    w = child.cget("width")
                    h = child.cget("height")
                    if w <= 10 and h <= 10:
                        child.configure(fg_color=color)
                        continue
                except Exception:
                    pass
                self._update_card_labels(child, title, value, hint, color, text_color)

        # Simpler approach: find all CTkLabel children recursively
        all_labels = self._find_all_labels(widget)
        if len(all_labels) >= 2:
            # First label is title, second is value, third (if exists) is hint
            all_labels[0].configure(text_color=text_color)
            all_labels[1].configure(text=value, text_color=text_color)
            if len(all_labels) >= 3:
                all_labels[2].configure(text=hint, text_color=self.colors["text_secondary"])

    def _find_all_labels(self, widget):
        """Find all CTkLabel widgets recursively."""
        labels = []
        for child in widget.winfo_children():
            if isinstance(child, ctk.CTkLabel):
                labels.append(child)
            elif isinstance(child, ctk.CTkFrame):
                labels.extend(self._find_all_labels(child))
        return labels