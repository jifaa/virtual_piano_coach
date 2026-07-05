"""
AI Piano Coach - Calibration Page
Premium calibration page with polished 4-point keyboard calibration.
"""
import cv2
from PIL import Image, ImageTk
import customtkinter as ctk
from app.ui.base_page import BasePage
from app.design_system import (
    get_light_colors, adjust_color,
    RADIUS_MD, RADIUS_LG, RADIUS_SM, RADIUS_FULL,
    SECTION_GAP, CARD_GAP, CARD_PADDING,
)


class CalibrationPage(BasePage):
    """Calibration with premium 4-point instruction and visual feedback."""

    def __init__(self, parent, app_controller):
        self.colors = get_light_colors()
        self.points = []
        self.preview_running = False
        self.preview_id = None
        self.canvas_image = None  # Inisialisasi untuk menghindari bug
        self._canvas_width = 640
        self._canvas_height = 480
        super().__init__(
            parent, app_controller,
            "Kalibrasi Keyboard",
            "Tandai 4 sudut keyboard pada preview kamera"
        )
        self._create_content()

    def _create_content(self):
        """Create calibration content with grid-based split layout."""
        # Main grid layout: left panel (fixed) + right panel (expanding)
        main = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        main.pack(fill="both", expand=True)
        main.grid_columnconfigure(0, weight=0, minsize=280)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(0, weight=1)

        # Left: Controls panel (fixed width)
        left = ctk.CTkFrame(
            main,
            fg_color=self.colors["bg_secondary"],
            border_color=self.colors["border"],
            border_width=1,
            corner_radius=RADIUS_LG,
        )
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        # Left content in scrollable area
        left_scroll = ctk.CTkScrollableFrame(left, fg_color="transparent")
        left_scroll.pack(fill="both", expand=True)

        # Left header
        hdr = ctk.CTkLabel(
            left_scroll,
            text="Kontrol Kalibrasi",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors["text_primary"],
        )
        hdr.pack(anchor="w", padx=CARD_PADDING, pady=(18, 12))

        # Instructions card
        self._instructions_card(left_scroll)

        # Point progress indicators
        self._point_indicators(left_scroll)

        # Control buttons
        self._control_buttons(left_scroll)

        # Right: Camera preview (expanding)
        right = ctk.CTkFrame(
            main,
            fg_color=self.colors["bg_secondary"],
            border_color=self.colors["border"],
            border_width=1,
            corner_radius=RADIUS_LG,
        )
        right.grid(row=0, column=1, sticky="nsew")

        # Camera header
        cam_hdr = ctk.CTkFrame(
            right,
            fg_color=self.colors["bg_tertiary"],
            corner_radius=0,
        )
        cam_hdr.pack(fill="x")
        cam_hdr.configure(height=42)
        cam_hdr.pack_propagate(False)

        cam_hdr_inner = ctk.CTkFrame(cam_hdr, fg_color="transparent")
        cam_hdr_inner.pack(fill="x", padx=16, pady=10)

        cam_title = ctk.CTkLabel(
            cam_hdr_inner,
            text="Preview Kamera",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["text_primary"],
        )
        cam_title.pack(side="left")

        self.point_count_lbl = ctk.CTkLabel(
            cam_hdr_inner,
            text="(0/4 titik)",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_muted"],
        )
        self.point_count_lbl.pack(side="left", padx=(8, 0))

        # Camera canvas container - allows canvas to resize
        self._canvas_container = ctk.CTkFrame(right, fg_color="transparent")
        self._canvas_container.pack(fill="both", expand=True, padx=12, pady=12)

        self.canvas = ctk.CTkCanvas(
            self._canvas_container,
            width=640,
            height=480,
            bg=self.colors["canvas_bg"],
            highlightthickness=0,
            cursor="crosshair",
        )
        self.canvas.pack(fill="both", expand=True)

        # Draw initial placeholder
        self.after(100, self._stop_preview)

        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<Configure>", self._on_canvas_resize)

    def _on_canvas_resize(self, event):
        """Handle canvas resize to update render dimensions."""
        self._canvas_width = max(320, event.width)
        self._canvas_height = max(240, event.height)

    def _instructions_card(self, parent):
        """Instructions card with numbered steps."""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors["accent_light"],
            corner_radius=RADIUS_MD,
            border_color=self.colors["accent"],
            border_width=1,
        )
        card.pack(fill="x", padx=16, pady=(0, CARD_GAP))

        title = ctk.CTkLabel(
            card,
            text="Cara Kalibrasi",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.colors["accent"],
        )
        title.pack(anchor="w", padx=14, pady=(12, 10))

        steps = [
            ("1", "Klik [Mulai Preview]"),
            ("2", "Atur posisi kamera"),
            ("3", "Klik 4 sudut keyboard:"),
            ("", "  Kiri-atas → Kanan-atas"),
            ("", "  Kanan-bawah → Kiri-bawah"),
            ("4", "Klik [Simpan Kalibrasi]"),
        ]

        for num, text in steps:
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=2)

            if num:
                badge = ctk.CTkFrame(
                    row,
                    fg_color=self.colors["accent"],
                    corner_radius=10,
                    width=20,
                    height=20,
                )
                badge.pack(side="left", padx=(0, 8))
                badge.pack_propagate(False)

                badge_lbl = ctk.CTkLabel(
                    badge,
                    text=num,
                    text_color=self.colors["text_on_accent"],
                    font=ctk.CTkFont(size=10, weight="bold"),
                )
                badge_lbl.pack(expand=True)

            txt = ctk.CTkLabel(
                row,
                text=text,
                font=ctk.CTkFont(size=11),
                text_color=self.colors["text_secondary"] if num else self.colors["text_muted"],
                anchor="w",
                wraplength=200,
            )
            txt.pack(side="left", fill="x", expand=True)

        ctk.CTkFrame(card, fg_color="transparent", height=8).pack()

    def _point_indicators(self, parent):
        """Point progress indicators with visual feedback."""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors["bg_tertiary"],
            corner_radius=RADIUS_MD,
        )
        card.pack(fill="x", padx=16, pady=(0, CARD_GAP))

        title = ctk.CTkLabel(
            card,
            text="Progress Titik Kalibrasi",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.colors["text_primary"],
        )
        title.pack(anchor="w", padx=14, pady=(12, 10))

        # 4 point indicators in a grid row
        points_row = ctk.CTkFrame(card, fg_color="transparent")
        points_row.pack(fill="x", padx=14, pady=(0, 8))
        for col in range(4):
            points_row.grid_columnconfigure(col, weight=1, uniform="pt")

        self.indicators = []
        for i in range(4):
            ind = ctk.CTkFrame(
                points_row,
                fg_color=self.colors["bg_secondary"],
                border_color=self.colors["border"],
                border_width=1,
                corner_radius=RADIUS_SM,
            )
            padx = (0, 4) if i < 3 else (0, 0)
            ind.grid(row=0, column=i, sticky="nsew", padx=padx)

            # Point label
            num_lbl = ctk.CTkLabel(
                ind,
                text=f"T{i+1}",
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=self.colors["text_muted"],
            )
            num_lbl.pack(pady=(8, 2))

            # Status indicator
            status_lbl = ctk.CTkLabel(
                ind,
                text="—",
                font=ctk.CTkFont(size=18),
                text_color=self.colors["text_muted"],
            )
            status_lbl.pack(pady=(0, 8))

            self.indicators.append(status_lbl)

        # Status text
        self.status_lbl = ctk.CTkLabel(
            card,
            text="Tekan Mulai Preview untuk memulai",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_secondary"],
            wraplength=220,
        )
        self.status_lbl.pack(padx=14, pady=(0, 12))

    def _control_buttons(self, parent):
        """Control buttons with premium styling."""
        btns = ctk.CTkFrame(parent, fg_color="transparent")
        btns.pack(fill="x", padx=16, pady=(0, 16))

        self.btn_preview = ctk.CTkButton(
            btns,
            text="Mulai Preview",
            command=self._toggle_preview,
            height=46,
            corner_radius=RADIUS_MD,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            text_color=self.colors["text_on_accent"],
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.btn_preview.pack(fill="x", pady=(0, 10))

        reset_btn = ctk.CTkButton(
            btns,
            text="Reset Titik",
            command=self._reset,
            height=40,
            corner_radius=RADIUS_MD,
            fg_color=self.colors["bg_tertiary"],
            hover_color=self.colors["bg_hover"],
            text_color=self.colors["text_primary"],
            font=ctk.CTkFont(size=14),
        )
        reset_btn.pack(fill="x", pady=(0, 10))

        save_btn = ctk.CTkButton(
            btns,
            text="Simpan Kalibrasi",
            command=self._save,
            height=54,
            corner_radius=RADIUS_LG,
            fg_color=self.colors["success"],
            hover_color=adjust_color(self.colors["success"], -15),
            text_color=self.colors["text_on_accent"],
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        save_btn.pack(fill="x", pady=(0, 10))

        # Skip button if already calibrated
        if self.app.config.is_calibration_complete():
            skip_btn = ctk.CTkButton(
                btns,
                text="Skip - Ke Latihan →",
                command=lambda: self.app.show_page("practice"),
                height=40,
                corner_radius=RADIUS_MD,
                fg_color=self.colors["bg_tertiary"],
                hover_color=self.colors["bg_hover"],
                text_color=self.colors["text_primary"],
                font=ctk.CTkFont(size=14),
            )
            skip_btn.pack(fill="x")

    def _toggle_preview(self):
        """Toggle preview on/off."""
        if self.preview_running:
            self._stop_preview()
        else:
            self._start_preview()

    def _start_preview(self):
        """Start camera preview."""
        idx = self.app.config.config.camera_index
        if not self.app.camera_manager.open(idx):
            self.status_lbl.configure(
                text=f"✗ Gagal membuka kamera {idx}. Pastikan kamera di-setup.",
                text_color=self.colors["error"]
            )
            return

        self.preview_running = True
        self.btn_preview.configure(
            text="Hentikan Preview",
            fg_color=self.colors["error"],
        )
        self.canvas.delete("all")
        self.canvas_image = None
        self._update_preview()

    def _stop_preview(self):
        """Stop preview."""
        self.preview_running = False
        self.btn_preview.configure(
            text="Mulai Preview",
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
        )
        if self.preview_id:
            self.canvas.after_cancel(self.preview_id)
            self.preview_id = None
        self.canvas.delete("all")
        # Penting: reset canvas_image agar tidak reference stale canvas item
        self.canvas_image = None
        
        # Draw a beautiful placeholder
        w = max(320, self._canvas_width)
        h = max(240, self._canvas_height)
        cx, cy = w // 2, h // 2
        
        # Center box
        box_w, box_h = 300, 160
        x1, y1 = cx - box_w//2, cy - box_h//2
        x2, y2 = cx + box_w//2, cy + box_h//2
        
        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            outline=self.colors["border"],
            width=2,
            dash=(6, 4),
            fill=self.colors["bg_secondary"]
        )
        
        self.canvas.create_text(
            cx, cy - 15,
            text="📷",
            fill=self.colors["text_muted"],
            font=("TkDefaultFont", 32),
            justify="center",
        )

        self.canvas.create_text(
            cx, cy + 25,
            text="Kamera belum aktif",
            fill=self.colors["text_primary"],
            font=("TkDefaultFont", 16, "bold"),
            justify="center",
        )

        self.canvas.create_text(
            cx, cy + 50,
            text="Klik [Mulai Preview] untuk melihat\ndan menandai area keyboard",
            fill=self.colors["text_secondary"],
            font=("TkDefaultFont", 13),
            justify="center",
        )

    def _update_preview(self):
        """Update preview frame."""
        if not self.preview_running:
            return

        frame = self.app.camera_manager.read_frame()
        if frame is not None:
            # Simpan dimensi asli untuk konversi titik kalibrasi
            self._orig_frame_w = frame.shape[1]
            self._orig_frame_h = frame.shape[0]

            # Draw points
            for i, pt in enumerate(self.points):
                cv2.circle(frame, pt, 12, (0, 255, 0), -1)
                cv2.putText(
                    frame,
                    str(i + 1),
                    (pt[0] - 5, pt[1] + 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 0, 0),
                    2
                )

            # Draw prompt bar
            cv2.rectangle(frame, (10, 10), (350, 48), (0, 0, 0), -1)
            cv2.putText(
                frame,
                f"Klik 4 sudut keyboard ({len(self.points)}/4)",
                (15, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
            )

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cw = max(320, self._canvas_width)
            ch = max(240, self._canvas_height)
            
            # Resize while preserving aspect ratio
            h_img, w_img = rgb.shape[:2]
            scale = min(cw / w_img, ch / h_img)
            new_w = int(w_img * scale)
            new_h = int(h_img * scale)
            
            pil = Image.fromarray(rgb).resize((new_w, new_h))
            photo = ImageTk.PhotoImage(pil)

            cx = cw // 2
            cy = ch // 2
            
            # Save drawing metadata for accurate click mapping
            self._drawn_w = new_w
            self._drawn_h = new_h
            self._drawn_cx = cx
            self._drawn_cy = cy
            if self.canvas_image:
                self.canvas.itemconfig(self.canvas_image, image=photo)
                self.canvas.coords(self.canvas_image, cx, cy)
            else:
                self.canvas_image = self.canvas.create_image(cx, cy, image=photo)
            self.photo = photo

        self._update_indicators()
        self.preview_id = self.canvas.after(33, self._update_preview)

    def _update_indicators(self):
        """Update point indicators."""
        for i, lbl in enumerate(self.indicators):
            if i < len(self.points):
                lbl.configure(text="✓", text_color=self.colors["success"])
            else:
                lbl.configure(text="—", text_color=self.colors["text_muted"])

        count = len(self.points)
        self.point_count_lbl.configure(text=f"({count}/4 titik)")

        if count == 0:
            self.status_lbl.configure(
                text="Klik pada preview untuk menandai titik pertama",
                text_color=self.colors["text_secondary"]
            )
        elif count < 4:
            self.status_lbl.configure(
                text=f"✓ Titik {count} ditandai. Klik titik berikutnya.",
                text_color=self.colors["info"]
            )
        else:
            self.status_lbl.configure(
                text="✓ Kalibrasi lengkap! Klik Simpan Kalibrasi.",
                text_color=self.colors["success"]
            )

    def _on_click(self, event):
        """Handle canvas click."""
        if not self.preview_running:
            self.status_lbl.configure(
                text="⚠ Klik [Mulai Preview] terlebih dahulu",
                text_color=self.colors["warning"]
            )
            return
        if len(self.points) >= 4:
            self.status_lbl.configure(
                text="⚠ Sudah 4 titik. Klik Reset untuk mengulang.",
                text_color=self.colors["warning"]
            )
            return

        if not hasattr(self, '_orig_frame_w') or not hasattr(self, '_drawn_w'):
            return

        # Determine the top-left coordinates of the drawn image on the canvas
        drawn_x0 = self._drawn_cx - (self._drawn_w // 2)
        drawn_y0 = self._drawn_cy - (self._drawn_h // 2)
        
        # Check if the click is outside the image bounds
        if not (drawn_x0 <= event.x <= drawn_x0 + self._drawn_w and
                drawn_y0 <= event.y <= drawn_y0 + self._drawn_h):
            return  # Ignore clicks outside the image

        # Translate click to the image's coordinate space
        img_x = event.x - drawn_x0
        img_y = event.y - drawn_y0

        # Scale back to original frame coordinates
        orig_x = int(img_x * self._orig_frame_w / self._drawn_w)
        orig_y = int(img_y * self._orig_frame_h / self._drawn_h)

        self.points.append((orig_x, orig_y))
        self._update_indicators()

    def _reset(self):
        """Reset points."""
        self.points = []
        self._update_indicators()
        self.point_count_lbl.configure(text="(0/4 titik)")
        self.status_lbl.configure(
            text="✓ Titik direset. Klik pada preview untuk memulai.",
            text_color=self.colors["text_secondary"]
        )

    def _save(self):
        """Save calibration."""
        if len(self.points) != 4:
            from tkinter import messagebox
            messagebox.showwarning(
                "Belum Lengkap",
                f"Harus 4 titik. Sekarang: {len(self.points)}"
            )
            return

        self.app.keyboard_mapper.set_calibration_points(self.points)
        self.app.config.calibration.points = self.points
        self.app.config.calibration.keyboard_size = self.app.config.config.keyboard_size
        self.app.config.calibration.tuts_rects = {
            k: list(v) for k, v in self.app.keyboard_mapper.get_all_key_rects().items()
        }
        self.app.config.save_calibration(self.app.config.calibration)

        from tkinter import messagebox
        messagebox.showinfo("Berhasil", "Kalibrasi disimpan!\nLanjut ke halaman Latihan.")
        self.app.show_page("practice")

    def on_appear(self):
        """On page appear."""
        if self.app.config.is_calibration_complete():
            pts = self.app.config.calibration.points
            if pts:
                self.points = [(int(a), int(b)) for a, b in pts]
                self._update_indicators()
                self.status_lbl.configure(
                    text="✓ Kalibrasi tersimpan. Klik Preview untuk melihat.",
                    text_color=self.colors["success"]
                )

    def on_disappear(self):
        """On page disappear."""
        self._stop_preview()