"""
AI Piano Coach - Settings Page
Premium settings page with grouped sections and polished controls.
"""
import customtkinter as ctk
from app.ui.base_page import BasePage
from app.design_system import (
    get_light_colors, adjust_color,
    RADIUS_MD, RADIUS_SM, RADIUS_LG,
    SECTION_GAP, CARD_GAP, CARD_PADDING,
)


class SettingsPage(BasePage):
    """Settings with premium grouped sections and modern controls."""

    def __init__(self, parent, app_controller):
        self.colors = get_light_colors()
        self.appearance_var = ctk.StringVar(value="light")
        self.theme_var = ctk.StringVar(value="blue")
        self.opacity_var = ctk.DoubleVar(value=0.8)
        self.mirror_var = ctk.BooleanVar(value=False)
        self.finger_var = ctk.BooleanVar(value=True)
        self.posture_var = ctk.BooleanVar(value=True)
        self.note_num_var = ctk.BooleanVar(value=False)
        self.wrong_note_var = ctk.BooleanVar(value=True)
        self.split_var = ctk.IntVar(value=60)
        super().__init__(
            parent, app_controller,
            "Settings",
            "Konfigurasi tampilan dan fitur aplikasi"
        )
        self._create_content()

    def _create_content(self):
        """Create settings content."""
        scroll = self.scrollable_frame(self.content_frame)
        scroll.pack(fill="both", expand=True)

        # Appearance section
        self._appearance_section(scroll)

        # Overlay section
        self._overlay_section(scroll)

        # Feedback section
        self._feedback_section(scroll)

        # Advanced section
        self._advanced_section(scroll)

        # Actions
        self._action_section(scroll)

    def _section_card(self, parent, title: str, subtitle: str = None, icon: str = None):
        """Create a premium section card."""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors["bg_secondary"],
            border_color=self.colors["border"],
            border_width=1,
            corner_radius=RADIUS_LG,
        )
        card.pack(fill="x", pady=(0, CARD_GAP))

        # Header
        hdr = ctk.CTkFrame(card, fg_color="transparent")
        hdr.pack(fill="x", padx=CARD_PADDING, pady=(18, 8))

        # Icon
        if icon:
            icon_frame = ctk.CTkFrame(
                hdr,
                fg_color=self.colors["accent_light"],
                corner_radius=RADIUS_SM,
                width=28,
                height=28,
            )
            icon_frame.pack(side="left", padx=(0, 12))
            icon_frame.pack_propagate(False)

            icon_lbl = ctk.CTkLabel(
                icon_frame,
                text=icon,
                font=ctk.CTkFont(size=14),
                text_color=self.colors["accent"],
            )
            icon_lbl.pack(expand=True)

        # Title
        t = ctk.CTkLabel(
            hdr,
            text=title,
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=self.colors["text_primary"],
            anchor="w",
        )
        t.pack(side="left")

        # Subtitle
        if subtitle:
            sep = ctk.CTkLabel(
                hdr,
                text="•",
                font=ctk.CTkFont(size=12),
                text_color=self.colors["text_muted"],
            )
            sep.pack(side="left", padx=(10, 10))
            s = ctk.CTkLabel(
                hdr,
                text=subtitle,
                font=ctk.CTkFont(size=12),
                text_color=self.colors["text_secondary"],
                anchor="w",
                wraplength=400,
            )
            s.pack(side="left")

        return card

    def _appearance_section(self, parent):
        """Appearance settings."""
        card = self._section_card(
            parent,
            "Tampilan",
            "Atur tema dan tampilan aplikasi",
            icon="◈"
        )

        # Mode row
        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=CARD_PADDING, pady=(0, 12))

        lbl = ctk.CTkLabel(
            row,
            text="Mode:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["text_primary"],
        )
        lbl.pack(side="left", padx=(0, 16))

        # Light/Dark/System using grid for equal sizing
        modes_container = ctk.CTkFrame(row, fg_color="transparent")
        modes_container.pack(side="left", fill="x", expand=True)

        modes = [
            ("Light", "light", "☀"),
            ("Dark", "dark", "☾"),
            ("System", "system", "⊙"),
        ]

        for i, (label, value, icon) in enumerate(modes):
            opt = ctk.CTkFrame(
                modes_container,
                fg_color=self.colors["bg_tertiary"],
                border_color=self.colors["border"],
                border_width=1,
                corner_radius=RADIUS_MD,
                cursor="hand2",
            )
            opt.pack(side="left", padx=(0, 10) if i < 2 else (0, 0), fill="x", expand=True)

            r = ctk.CTkRadioButton(
                opt,
                text=f"{icon} {label}",
                variable=self.appearance_var,
                value=value,
                command=self._on_appearance,
                border_color=self.colors["accent"],
                fg_color=self.colors["accent"],
                font=ctk.CTkFont(size=13),
            )
            r.pack(padx=14, pady=10)

            # Hover effects
            def on_enter(e, o=opt):
                o.configure(border_color=self.colors["accent"])
            def on_leave(e, o=opt, v=value):
                if self.appearance_var.get() != v:
                    o.configure(border_color=self.colors["border"])
            opt.bind("<Enter>", on_enter)
            opt.bind("<Leave>", on_leave)

        # Theme row
        row2 = ctk.CTkFrame(card, fg_color="transparent")
        row2.pack(fill="x", padx=CARD_PADDING, pady=(0, 16))

        lbl2 = ctk.CTkLabel(
            row2,
            text="Tema:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["text_primary"],
        )
        lbl2.pack(side="left", padx=(0, 16))

        themes = [
            ("Blue", "blue", "#3B82F6"),
            ("Green", "green", "#10B981"),
        ]

        for i, (label, value, color) in enumerate(themes):
            opt = ctk.CTkFrame(
                row2,
                fg_color=self.colors["bg_tertiary"],
                border_color=self.colors["border"],
                border_width=1,
                corner_radius=RADIUS_MD,
                cursor="hand2",
            )
            opt.pack(side="left", padx=(0, 10) if i == 0 else (0, 0))

            r = ctk.CTkRadioButton(
                opt,
                text=label,
                variable=self.theme_var,
                value=value,
                border_color=color,
                fg_color=color,
                font=ctk.CTkFont(size=13),
            )
            r.pack(padx=14, pady=10)

            # Hover effects
            def on_enter(e, o=opt, c=color):
                o.configure(border_color=c)
            def on_leave(e, o=opt, v=value):
                if self.theme_var.get() != v:
                    o.configure(border_color=self.colors["border"])
            opt.bind("<Enter>", on_enter)
            opt.bind("<Leave>", on_leave)

            # Click forwarding
            def on_click(e, v=value):
                self.theme_var.set(v)
            for w in [opt, r]:
                w.bind("<Button-1>", on_click)

    def _overlay_section(self, parent):
        """Overlay settings."""
        card = self._section_card(
            parent,
            "Overlay",
            "Tampilan overlay piano pada kamera",
            icon="◉"
        )

        # Opacity slider
        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=CARD_PADDING, pady=(0, 4))

        lbl = ctk.CTkLabel(
            row,
            text="Opasitas Overlay:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["text_primary"],
        )
        lbl.pack(side="left")

        self.opacity_val = ctk.CTkLabel(
            row,
            text="80%",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["accent"],
        )
        self.opacity_val.pack(side="right")

        # Slider fills available width
        slider = ctk.CTkSlider(
            card,
            from_=0.3,
            to=1.0,
            variable=self.opacity_var,
            button_color=self.colors["accent"],
            progress_color=self.colors["accent"],
        )
        slider.pack(fill="x", padx=CARD_PADDING, pady=(0, 12))
        slider.configure(
            command=lambda v: self.opacity_val.configure(
                text=f"{int(float(v) * 100)}%"
            )
        )

        # Mirror switch
        row2 = ctk.CTkFrame(card, fg_color="transparent")
        row2.pack(fill="x", padx=CARD_PADDING, pady=(0, 16))

        sw = ctk.CTkSwitch(
            row2,
            text="Mirror Kamera (balik kiri-kanan)",
            variable=self.mirror_var,
            font=ctk.CTkFont(size=14),
            progress_color=self.colors["accent"],
        )
        sw.pack(side="left")

    def _feedback_section(self, parent):
        """Feedback settings."""
        card = self._section_card(
            parent,
            "Feedback",
            "Feedback visual dan informasi postur",
            icon="ℹ"
        )

        # Switches with wraplength on hints
        switches = [
            ("Tampilkan Label Jari", self.finger_var, "Label nama jari pada overlay"),
            ("Tampilkan Postur Tangan", self.posture_var, "Feedback postur tangan kiri/kanan"),
            ("Tampilkan Nomor Note", self.note_num_var, "Nomor MIDI note pada setiap tuts"),
            ("Feedback Note Salah", self.wrong_note_var, "Tampilkan warna merah untuk note salah"),
        ]

        for label, var, hint in switches:
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=CARD_PADDING, pady=8)

            sw = ctk.CTkSwitch(
                row,
                text=label,
                variable=var,
                font=ctk.CTkFont(size=14),
                progress_color=self.colors["accent"],
            )
            sw.pack(side="left")

            hint_lbl = ctk.CTkLabel(
                row,
                text=f"• {hint}",
                font=ctk.CTkFont(size=11),
                text_color=self.colors["text_muted"],
                anchor="e",
                wraplength=250,
            )
            hint_lbl.pack(side="right")

        ctk.CTkLabel(card, text="").pack(pady=4)

    def _advanced_section(self, parent):
        """Advanced settings."""
        card = self._section_card(
            parent,
            "Lanjutan",
            "Parameter teknis untuk tracking",
            icon="⚙"
        )

        # Split note slider
        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=CARD_PADDING, pady=(0, 4))

        lbl = ctk.CTkLabel(
            row,
            text="Titik Bagi Tangan:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["text_primary"],
        )
        lbl.pack(side="left")

        self.split_lbl = ctk.CTkLabel(
            row,
            text="C4 (60)",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["accent"],
        )
        self.split_lbl.pack(side="right")

        # Slider fills available width
        slider = ctk.CTkSlider(
            card,
            from_=40,
            to=80,
            variable=self.split_var,
            button_color=self.colors["accent"],
            progress_color=self.colors["accent"],
        )
        slider.pack(fill="x", padx=CARD_PADDING, pady=(0, 8))
        slider.configure(command=lambda v: self._update_split(int(v)))

        info = ctk.CTkLabel(
            card,
            text="Note < bagi = tangan kiri  |  Note > bagi = tangan kanan",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_secondary"],
            anchor="w",
            wraplength=500,
        )
        info.pack(fill="x", padx=CARD_PADDING, pady=(0, 16))

    def _action_section(self, parent):
        """Action buttons."""
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=(8, 0))

        save = ctk.CTkButton(
            row,
            text="✓ Simpan Pengaturan",
            command=self._save,
            width=200,
            height=54,
            corner_radius=RADIUS_LG,
            fg_color=self.colors["success"],
            hover_color=adjust_color(self.colors["success"], -15),
            text_color=self.colors["text_on_accent"],
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        save.pack(side="left", padx=(0, 16))

        reset = ctk.CTkButton(
            row,
            text="↺ Reset Default",
            command=self._reset,
            width=160,
            height=48,
            corner_radius=RADIUS_MD,
            fg_color=self.colors["bg_tertiary"],
            hover_color=self.colors["bg_hover"],
            text_color=self.colors["text_primary"],
            font=ctk.CTkFont(size=14),
        )
        reset.pack(side="left")

    def _on_appearance(self):
        """On appearance mode change."""
        self.app.set_appearance_mode(self.appearance_var.get())

    def _update_split(self, note):
        """Update split label."""
        names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        octave = (note // 12) - 1
        name = names[note % 12]
        self.split_lbl.configure(text=f"{name}{octave} ({note})")

    def _save(self):
        """Save settings."""
        cfg = self.app.config.config
        cfg.appearance_mode = self.appearance_var.get()
        cfg.color_theme = self.theme_var.get()
        cfg.overlay_opacity = self.opacity_var.get()
        cfg.camera_mirror = self.mirror_var.get()
        cfg.show_finger_labels = self.finger_var.get()
        cfg.show_posture_feedback = self.posture_var.get()
        cfg.show_note_numbers = self.note_num_var.get()
        cfg.wrong_note_feedback = self.wrong_note_var.get()
        cfg.hand_split_note = self.split_var.get()
        self.app.config.save()
        if self.app.overlay_renderer:
            self.app.overlay_renderer.show_finger_labels = cfg.show_finger_labels
            self.app.overlay_renderer.show_posture = cfg.show_posture_feedback
            self.app.overlay_renderer.show_note_numbers = cfg.show_note_numbers
            self.app.overlay_renderer.hand_split_note = cfg.hand_split_note
        from tkinter import messagebox
        messagebox.showinfo("Sukses", "Pengaturan berhasil disimpan!")

    def _reset(self):
        """Reset settings."""
        from tkinter import messagebox
        if messagebox.askyesno("Reset", "Reset semua pengaturan ke default?"):
            self.appearance_var.set("light")
            self.theme_var.set("blue")
            self.opacity_var.set(0.8)
            self.mirror_var.set(False)
            self.finger_var.set(True)
            self.posture_var.set(True)
            self.note_num_var.set(False)
            self.wrong_note_var.set(True)
            self.split_var.set(60)
            self.split_lbl.configure(text="C4 (60)")
            self.opacity_val.configure(text="80%")
            self._save()

    def on_appear(self):
        """Load settings."""
        cfg = self.app.config.config
        self.appearance_var.set(cfg.appearance_mode)
        self.theme_var.set(cfg.color_theme)
        self.opacity_var.set(cfg.overlay_opacity)
        self.mirror_var.set(cfg.camera_mirror)
        self.finger_var.set(cfg.show_finger_labels)
        self.posture_var.set(cfg.show_posture_feedback)
        self.note_num_var.set(cfg.show_note_numbers)
        self.wrong_note_var.set(cfg.wrong_note_feedback)
        self.split_var.set(cfg.hand_split_note)
        self.opacity_val.configure(text=f"{int(cfg.overlay_opacity * 100)}%")
        self.split_lbl.configure(text=self._note_name(cfg.hand_split_note))

    def _note_name(self, note):
        names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        octave = (note // 12) - 1
        return f"{names[note % 12]}{octave} ({note})"