"""
AI Piano Coach - Setup Page
Premium wizard-style configuration page with step-by-step setup.
"""
import customtkinter as ctk
from tkinter import filedialog
from app.ui.base_page import BasePage
from app.design_system import (
    get_light_colors, adjust_color,
    RADIUS_MD, RADIUS_SM, RADIUS_LG,
    SECTION_GAP, CARD_GAP, CARD_PADDING,
)


class SetupPage(BasePage):
    """Setup page with premium step-by-step configuration."""

    def __init__(self, parent, app_controller):
        self.camera_var = ctk.StringVar(value="Memuat...")
        self.midi_var = ctk.StringVar(value="Memuat...")
        self.keyboard_var = ctk.StringVar(value="61")
        self.colors = get_light_colors()
        super().__init__(parent, app_controller, "Setup", "Konfigurasi hardware dan software")
        self._create_content()

    def _create_content(self):
        """Create setup content."""
        scroll = self.scrollable_frame(self.content_frame)
        scroll.pack(fill="both", expand=True)

        # Step indicator
        steps = ["Kamera", "MIDI Input", "Ukuran Keyboard", "File MIDI"]
        self._step_indicator(scroll, steps)

        # Spacer
        self.spacer(scroll, 16).pack()

        # Step 1: Camera section
        self._camera_section(scroll)

        # Step 2: MIDI section
        self._midi_section(scroll)

        # Step 3: Keyboard section
        self._keyboard_section(scroll)

        # Step 4: MIDI file section
        self._midi_file_section(scroll)

        # Action buttons
        self._action_section(scroll)

    def _step_indicator(self, parent, steps: list):
        """Create step progress indicator with proper alignment."""
        container = ctk.CTkFrame(
            parent,
            fg_color=self.colors["bg_secondary"],
            corner_radius=RADIUS_MD,
            border_color=self.colors["border"],
            border_width=1,
        )
        container.pack(fill="x", pady=(0, SECTION_GAP))

        inner = ctk.CTkFrame(container, fg_color="transparent")
        inner.pack(fill="x", padx=CARD_PADDING, pady=16)

        # Use grid for even spacing of steps
        for col in range(len(steps)):
            inner.grid_columnconfigure(col, weight=1)

        self._step_dots = []
        for i, step in enumerate(steps):
            step_frame = ctk.CTkFrame(inner, fg_color="transparent")
            step_frame.grid(row=0, column=i, sticky="nsew")

            # Circle
            circle = ctk.CTkFrame(
                step_frame,
                fg_color=self.colors["accent"] if i == 0 else self.colors["bg_tertiary"],
                corner_radius=14,
                width=28,
                height=28,
            )
            circle.pack(pady=(0, 6))
            circle.pack_propagate(False)

            circle_lbl = ctk.CTkLabel(
                circle,
                text=str(i + 1),
                text_color=self.colors["text_on_accent"] if i == 0 else self.colors["text_muted"],
                font=ctk.CTkFont(size=12, weight="bold"),
            )
            circle_lbl.pack(expand=True)
            self._step_dots.append((circle, circle_lbl))

            # Label
            lbl = ctk.CTkLabel(
                step_frame,
                text=step,
                font=ctk.CTkFont(size=11, weight="bold" if i == 0 else "normal"),
                text_color=self.colors["accent"] if i == 0 else self.colors["text_secondary"],
            )
            lbl.pack()

    def _camera_section(self, parent):
        """Camera configuration section."""
        card = self.section_card(
            parent,
            "1. Konfigurasi Kamera",
            "Pilih kamera yang mengarah ke keyboard piano Anda"
        )

        # Dropdown row
        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=CARD_PADDING, pady=(0, 12))

        lbl = ctk.CTkLabel(
            row,
            text="Pilih Kamera:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["text_primary"],
        )
        lbl.pack(side="left", padx=(0, 12))

        self.camera_dropdown = ctk.CTkOptionMenu(
            row,
            variable=self.camera_var,
            values=["Memuat..."],
            command=self._on_camera_selected,
            height=40,
            corner_radius=RADIUS_MD,
            fg_color=self.colors["bg_tertiary"],
            button_color=self.colors["accent"],
            button_hover_color=self.colors["accent_hover"],
            dropdown_fg_color=self.colors["bg_secondary"],
            dropdown_hover_color=self.colors["bg_hover"],
        )
        self.camera_dropdown.pack(side="left", fill="x", expand=True, padx=(0, 10))

        refresh_btn = ctk.CTkButton(
            row,
            text="Refresh",
            command=self._refresh_cameras,
            width=100,
            height=40,
            corner_radius=RADIUS_MD,
            fg_color=self.colors["bg_tertiary"],
            hover_color=self.colors["bg_hover"],
            text_color=self.colors["text_primary"],
            font=ctk.CTkFont(size=13, weight="bold"),
        )
        refresh_btn.pack(side="left")

        # Test button row
        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(fill="x", padx=CARD_PADDING, pady=(0, 12))

        test_btn = ctk.CTkButton(
            btn_row,
            text="Test Kamera",
            command=self._test_camera,
            width=160,
            height=42,
            corner_radius=RADIUS_MD,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            text_color=self.colors["text_on_accent"],
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        test_btn.pack(side="left", padx=(0, 12))

        self.camera_status = ctk.CTkLabel(
            btn_row,
            text="Klik Test Kamera untuk memastikan kamera berfungsi",
            font=ctk.CTkFont(size=13),
            text_color=self.colors["text_secondary"],
            anchor="w",
            wraplength=400,
        )
        self.camera_status.pack(side="left", fill="x", expand=True, pady=8)

    def _midi_section(self, parent):
        """MIDI configuration section."""
        card = self.section_card(
            parent,
            "2. Konfigurasi MIDI Input",
            "Pilih keyboard MIDI Anda. Pastikan sudah terhubung via USB."
        )

        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=CARD_PADDING, pady=(0, 12))

        lbl = ctk.CTkLabel(
            row,
            text="Pilih MIDI:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["text_primary"],
        )
        lbl.pack(side="left", padx=(0, 12))

        self.midi_dropdown = ctk.CTkOptionMenu(
            row,
            variable=self.midi_var,
            values=["Memuat..."],
            command=self._on_midi_selected,
            height=40,
            corner_radius=RADIUS_MD,
            fg_color=self.colors["bg_tertiary"],
            button_color=self.colors["accent"],
            button_hover_color=self.colors["accent_hover"],
            dropdown_fg_color=self.colors["bg_secondary"],
            dropdown_hover_color=self.colors["bg_hover"],
        )
        self.midi_dropdown.pack(side="left", fill="x", expand=True, padx=(0, 10))

        refresh_btn = ctk.CTkButton(
            row,
            text="Refresh",
            command=self._refresh_midi,
            width=100,
            height=40,
            corner_radius=RADIUS_MD,
            fg_color=self.colors["bg_tertiary"],
            hover_color=self.colors["bg_hover"],
            text_color=self.colors["text_primary"],
            font=ctk.CTkFont(size=13, weight="bold"),
        )
        refresh_btn.pack(side="left")

        self.midi_status = ctk.CTkLabel(
            card,
            text="Klik Refresh jika keyboard tidak muncul. Pastikan keyboard MIDI terhubung via USB.",
            font=ctk.CTkFont(size=13),
            text_color=self.colors["text_secondary"],
            anchor="w",
            wraplength=600,
        )
        self.midi_status.pack(anchor="w", padx=CARD_PADDING, pady=(0, 16))

    def _keyboard_section(self, parent):
        """Keyboard size selection using grid for equal widths."""
        card = self.section_card(
            parent,
            "3. Ukuran Keyboard",
            "Pilih jumlah tuts keyboard fisik Anda"
        )

        options = [
            ("61 Keys", "Roland E-X10 dan keyboard portable", "61"),
            ("88 Keys", "Piano full-size / grand digital", "88"),
        ]

        # Use grid for equal-width radio cards
        radio_row = ctk.CTkFrame(card, fg_color="transparent")
        radio_row.pack(fill="x", padx=CARD_PADDING, pady=(0, 16))
        radio_row.grid_columnconfigure(0, weight=1, uniform="kb")
        radio_row.grid_columnconfigure(1, weight=1, uniform="kb")

        # Store references to cards for styling
        self._keyboard_cards = {}

        for i, (title, desc, value) in enumerate(options):
            opt = ctk.CTkFrame(
                radio_row,
                fg_color=self.colors["bg_tertiary"],
                border_color=self.colors["border"],
                border_width=2,
                corner_radius=RADIUS_MD,
                cursor="hand2",
            )
            padx = (0, 8) if i == 0 else (8, 0)
            opt.grid(row=0, column=i, sticky="nsew", padx=padx)
            self._keyboard_cards[value] = opt

            inner = ctk.CTkFrame(opt, fg_color="transparent")
            inner.pack(fill="both", expand=True, padx=16, pady=14)

            # Radio button
            radio = ctk.CTkRadioButton(
                inner,
                text="",
                variable=self.keyboard_var,
                value=value,
                command=self._on_keyboard_changed,
                border_color=self.colors["border"],
                fg_color=self.colors["accent"],
                hover_color=self.colors["accent_hover"],
            )
            radio.pack(side="left", padx=(0, 12))

            # Content
            txt = ctk.CTkFrame(inner, fg_color="transparent")
            txt.pack(side="left", fill="both", expand=True)

            t_lbl = ctk.CTkLabel(
                txt,
                text=title,
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color=self.colors["text_primary"],
                anchor="w",
            )
            t_lbl.pack(anchor="w")

            d_lbl = ctk.CTkLabel(
                txt,
                text=desc,
                font=ctk.CTkFont(size=12),
                text_color=self.colors["text_secondary"],
                anchor="w",
                wraplength=250,
            )
            d_lbl.pack(anchor="w")

            # Click forwarding
            def on_click(e, v=value):
                self.keyboard_var.set(v)
                self._on_keyboard_changed()
            
            for w in [opt, inner, txt, t_lbl, d_lbl]:
                w.bind("<Button-1>", on_click)

            # Hover effects
            def on_enter(e, o=opt, v=value):
                if self.keyboard_var.get() != v:
                    o.configure(border_color=self.colors["border_hover"])
            def on_leave(e, o=opt, v=value):
                if self.keyboard_var.get() != v:
                    o.configure(border_color=self.colors["border"])
            opt.bind("<Enter>", on_enter)
            opt.bind("<Leave>", on_leave)

        # Initialize selection styling
        self.after(100, self._on_keyboard_changed)

    def _midi_file_section(self, parent):
        """MIDI guide file section."""
        card = self.section_card(
            parent,
            "4. File MIDI Guide (Opsional)",
            "Pilih file .mid/.midi untuk latihan terpandu. Kosongkan untuk free play."
        )

        # File info
        file_row = ctk.CTkFrame(card, fg_color="transparent")
        file_row.pack(fill="x", padx=CARD_PADDING, pady=(0, 12))

        # File icon placeholder
        icon_frame = ctk.CTkFrame(
            file_row,
            fg_color=self.colors["bg_tertiary"],
            corner_radius=RADIUS_SM,
            width=40,
            height=40,
        )
        icon_frame.pack(side="left", padx=(0, 12))
        icon_frame.pack_propagate(False)

        icon_lbl = ctk.CTkLabel(
            icon_frame,
            text="♫",
            font=ctk.CTkFont(size=20),
            text_color=self.colors["text_muted"],
        )
        icon_lbl.pack(expand=True)

        # File label with wraplength
        self.midi_file_lbl = ctk.CTkLabel(
            file_row,
            text="Belum ada file dipilih - Mode Free Play",
            font=ctk.CTkFont(size=14),
            text_color=self.colors["text_secondary"],
            wraplength=500,
            anchor="w",
        )
        self.midi_file_lbl.pack(side="left", fill="x", expand=True)

        # Buttons
        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(anchor="w", padx=CARD_PADDING, pady=(0, 16))

        select_btn = ctk.CTkButton(
            btn_row,
            text="Pilih File MIDI",
            command=self._select_midi_file,
            width=160,
            height=42,
            corner_radius=RADIUS_MD,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            text_color=self.colors["text_on_accent"],
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        select_btn.pack(side="left", padx=(0, 12))

        clear_btn = ctk.CTkButton(
            btn_row,
            text="Hapus",
            command=self._clear_midi_file,
            width=100,
            height=42,
            corner_radius=RADIUS_MD,
            fg_color=self.colors["bg_tertiary"],
            hover_color=self.colors["bg_hover"],
            text_color=self.colors["text_primary"],
            font=ctk.CTkFont(size=14),
        )
        clear_btn.pack(side="left")

    def _action_section(self, parent):
        """Action buttons."""
        # Hint banner
        hint = self.info_banner(
            parent,
            "💡 Setelah menyimpan setup, lanjut ke halaman Kalibrasi untuk menandai area keyboard.",
            "info"
        )
        hint.pack(fill="x", pady=(0, SECTION_GAP))

        # Buttons
        btn_row = ctk.CTkFrame(parent, fg_color="transparent")
        btn_row.pack(fill="x")

        save_btn = ctk.CTkButton(
            btn_row,
            text="Simpan Setup",
            command=self._save_setup,
            width=180,
            height=46,
            corner_radius=RADIUS_MD,
            fg_color=self.colors["success"],
            hover_color=adjust_color(self.colors["success"], -15),
            text_color=self.colors["text_on_accent"],
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        save_btn.pack(side="left", padx=(0, 16))

        next_btn = self.btn_cta(
            btn_row,
            text="Lanjut ke Kalibrasi →",
            command=lambda: self.app.show_page("calibration"),
            width=220,
        )
        next_btn.pack(side="left")

    # --- Event handlers ---
    def _refresh_cameras(self):
        """Refresh camera list."""
        cameras = self.app.camera_manager.detect_cameras()
        if cameras:
            names = [f"Camera {idx}" for idx, name in cameras]
            self.camera_dropdown.configure(values=names)
            saved = self.app.config.config.camera_index
            for i, (idx, _) in enumerate(cameras):
                if idx == saved:
                    self.camera_var.set(names[i])
                    break
            else:
                self.camera_var.set(names[0])
            self.camera_status.configure(
                text=f"✓ Ditemukan {len(cameras)} kamera",
                text_color=self.colors["success"]
            )
        else:
            self.camera_dropdown.configure(values=["Tidak ada kamera"])
            self.camera_var.set("Tidak ada kamera")
            self.camera_status.configure(
                text="⚠ Tidak ada kamera terdeteksi. Pastikan webcam terhubung.",
                text_color=self.colors["warning"]
            )

    def _refresh_midi(self):
        """Refresh MIDI list."""
        inputs = self.app.midi_manager.detect_inputs()
        if inputs:
            self.midi_dropdown.configure(values=inputs)
            saved = self.app.config.config.midi_input_name
            if saved and saved in inputs:
                self.midi_var.set(saved)
            else:
                for name in inputs:
                    if 'Roland' in name or 'E-X' in name:
                        self.midi_var.set(name)
                        break
                else:
                    self.midi_var.set(inputs[0])
            self.midi_status.configure(
                text=f"✓ Ditemukan {len(inputs)} device MIDI. {inputs[0]}",
                text_color=self.colors["success"]
            )
        else:
            self.midi_dropdown.configure(values=["Tidak ada device MIDI"])
            self.midi_var.set("Tidak ada device MIDI")
            self.midi_status.configure(
                text="⚠ Tidak ada device MIDI terdeteksi. Cek koneksi USB dan restart keyboard.",
                text_color=self.colors["warning"]
            )

    def _on_camera_selected(self, value):
        """Camera selected."""
        try:
            index = int(value.split()[1])
            self.app.config.config.camera_index = index
        except Exception:
            pass

    def _on_midi_selected(self, value):
        """MIDI selected."""
        self.app.config.config.midi_input_name = value

    def _on_keyboard_changed(self):
        """Keyboard size changed."""
        selected = self.keyboard_var.get()
        self.app.config.config.keyboard_size = selected
        
        # Update card visual states
        if hasattr(self, '_keyboard_cards'):
            for value, card in self._keyboard_cards.items():
                if value == selected:
                    card.configure(
                        border_color=self.colors["accent"],
                        fg_color=self.colors["bg_hover"],
                        border_width=2
                    )
                else:
                    card.configure(
                        border_color=self.colors["border"],
                        fg_color=self.colors["bg_tertiary"],
                        border_width=2
                    )

    def _test_camera(self):
        """Test camera."""
        try:
            index = int(self.camera_var.get().split()[1])
        except Exception:
            self.camera_status.configure(
                text="⚠ Pilih kamera yang valid terlebih dahulu",
                text_color=self.colors["error"]
            )
            return

        success = self.app.camera_manager.open(index)
        if success:
            self.camera_status.configure(
                text=f"✓ Kamera {index} berhasil dibuka! Preview ditampilkan...",
                text_color=self.colors["success"]
            )
            self._show_preview(index)
        else:
            self.camera_status.configure(
                text=f"✗ Gagal membuka kamera {index}. Coba index lain.",
                text_color=self.colors["error"]
            )

    def _show_preview(self, camera_index):
        """Show camera preview popup."""
        import cv2
        from PIL import Image, ImageTk

        win = ctk.CTkToplevel(self.app)
        win.title(f"Preview Kamera {camera_index}")
        win.geometry("680x560")
        win.resizable(False, False)
        win.attributes("-topmost", True)

        # Title bar
        title = ctk.CTkLabel(
            win,
            text=f"Preview Kamera {camera_index}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors["text_primary"],
        )
        title.pack(pady=(16, 8))

        # Canvas
        canvas = ctk.CTkCanvas(
            win,
            width=640,
            height=480,
            bg=self.colors["canvas_bg"],
            highlightthickness=0,
        )
        canvas.pack(padx=16, pady=8)

        # Close button
        close_btn = ctk.CTkButton(
            win,
            text="Tutup Preview",
            command=win.destroy,
            width=200,
            height=40,
            corner_radius=RADIUS_MD,
            fg_color=self.colors["error"],
            hover_color=adjust_color(self.colors["error"], -15),
            text_color=self.colors["text_on_accent"],
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        close_btn.pack(pady=(8, 16))

        state = {"running": True, "item": None}

        def update():
            if not state["running"]:
                return
            if not win.winfo_exists():
                return
            frame = self.app.camera_manager.read_frame()
            if frame is not None:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil = Image.fromarray(rgb).resize((640, 480))
                photo = ImageTk.PhotoImage(pil)
                if state["item"]:
                    canvas.itemconfig(state["item"], image=photo)
                else:
                    state["item"] = canvas.create_image(320, 240, image=photo)
                state["photo"] = photo
            canvas.after(33, update)

        def on_close():
            state["running"] = False
            win.destroy()

        win.protocol("WM_DELETE_WINDOW", on_close)
        update()

    def _select_midi_file(self):
        """Select MIDI file."""
        filename = filedialog.askopenfilename(
            title="Pilih File MIDI",
            filetypes=[("MIDI files", "*.mid *.midi"), ("All files", "*.*")],
        )
        if filename:
            self.app.config.config.midi_file_path = filename
            display_name = filename.split("/")[-1].split("\\")[-1]
            self.midi_file_lbl.configure(
                text=f"♪ {display_name}",
                text_color=self.colors["success"]
            )

    def _clear_midi_file(self):
        """Clear MIDI file."""
        self.app.config.config.midi_file_path = None
        self.midi_file_lbl.configure(
            text="Belum ada file dipilih - Mode Free Play",
            text_color=self.colors["text_secondary"]
        )

    def _save_setup(self):
        """Save setup."""
        self.app.config.save()
        kb_cfg = self.app.config.config.get_keyboard_config()
        self.app.keyboard_mapper = self.app.create_keyboard_mapper(kb_cfg)
        if not self.app.camera_manager.is_opened:
            self.app.camera_manager.open(self.app.config.config.camera_index)
        midi_name = self.app.config.config.midi_input_name
        if midi_name and not self.app.midi_manager.is_connected:
            self.app.midi_manager.connect(midi_name)

        from tkinter import messagebox
        messagebox.showinfo("Sukses", "Setup berhasil disimpan!\nLanjut ke halaman Kalibrasi.")

    def on_appear(self):
        """Refresh data on appear."""
        self._refresh_cameras()
        self._refresh_midi()
        self._load_config()

    def _load_config(self):
        """Load saved config."""
        cfg = self.app.config.config
        self.keyboard_var.set(cfg.keyboard_size)
        if cfg.midi_file_path:
            name = cfg.midi_file_path.split("/")[-1].split("\\")[-1]
            self.midi_file_lbl.configure(
                text=f"♪ {name}",
                text_color=self.colors["success"]
            )
        else:
            self.midi_file_lbl.configure(
                text="Belum ada file dipilih - Mode Free Play",
                text_color=self.colors["text_secondary"]
            )