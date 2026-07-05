"""
AI Piano Coach - Practice Page
Premium practice page with large camera preview and polished controls.
"""
import cv2
import threading
from PIL import Image, ImageTk
import customtkinter as ctk
from app.ui.base_page import BasePage
from app.design_system import (
    get_light_colors, adjust_color,
    RADIUS_MD, RADIUS_LG, RADIUS_SM,
    SECTION_GAP, CARD_GAP, CARD_PADDING,
)


class PracticePage(BasePage):
    """Practice page with premium camera preview and practice controls."""

    def __init__(self, parent, app_controller):
        self.preview_running = False
        self.preview_id = None
        self.canvas_item = None
        self.photo = None
        self.running = False
        self.lock = threading.Lock()
        self.latest_frame = None
        self.latest_fps = 0.0
        self.latest_notes = set()
        self.latest_left = None
        self.latest_right = None
        self.frame_ready = False
        self._canvas_width = 640
        self._canvas_height = 480
        super().__init__(
            parent, app_controller,
            "Latihan Piano",
            "Monitor dan latihan piano dengan visual feedback real-time"
        )
        self._create_content()

    def _create_content(self):
        """Create practice layout with grid-based split view."""
        # Main grid layout
        main = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        main.pack(fill="both", expand=True)
        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=0, minsize=300)
        main.grid_rowconfigure(0, weight=1)

        # Left: Camera preview area (expanding)
        preview_card = self._create_preview_card(main)
        preview_card.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        # Right: Controls panel (fixed width)
        right = ctk.CTkScrollableFrame(
            main,
            fg_color="transparent",
            width=300,
        )
        right.grid(row=0, column=1, sticky="nsew")

        # System status card
        self._status_card(right)

        # Notes card
        self._notes_card(right)

        # Posture card
        self._posture_card(right)

        # Controls card
        self._controls_card(right)

    def _create_preview_card(self, parent):
        """Create the camera preview card."""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors["bg_secondary"],
            border_color=self.colors["border"],
            border_width=1,
            corner_radius=RADIUS_LG,
        )

        # Header bar with mode indicator
        hdr = ctk.CTkFrame(
            card,
            fg_color=self.colors["bg_tertiary"],
            corner_radius=0,
        )
        hdr.pack(fill="x")
        hdr.configure(height=48)
        hdr.pack_propagate(False)

        hdr_inner = ctk.CTkFrame(hdr, fg_color="transparent")
        hdr_inner.pack(fill="x", padx=18, pady=10)

        # Left: Camera icon and title
        left_hdr = ctk.CTkFrame(hdr_inner, fg_color="transparent")
        left_hdr.pack(side="left")

        cam_icon = ctk.CTkFrame(
            left_hdr,
            fg_color=self.colors["accent_light"],
            corner_radius=RADIUS_SM,
            width=28,
            height=28,
        )
        cam_icon.pack(side="left", padx=(0, 10))
        cam_icon.pack_propagate(False)

        icon_lbl = ctk.CTkLabel(
            cam_icon,
            text="◉",
            font=ctk.CTkFont(size=14),
            text_color=self.colors["accent"],
        )
        icon_lbl.pack(expand=True)

        cam_lbl = ctk.CTkLabel(
            left_hdr,
            text="Live Camera & Piano Overlay",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["text_primary"],
        )
        cam_lbl.pack(side="left")

        # Right: Mode indicator
        right_hdr = ctk.CTkFrame(hdr_inner, fg_color="transparent")
        right_hdr.pack(side="right")

        self.mode_badge = ctk.CTkFrame(
            right_hdr,
            fg_color=self.colors["accent_light"],
            corner_radius=RADIUS_SM,
        )
        self.mode_badge.pack(padx=0, pady=0)

        self.mode_lbl = ctk.CTkLabel(
            self.mode_badge,
            text="FREE PLAY",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.colors["accent"],
        )
        self.mode_lbl.pack(padx=10, pady=4)

        # Camera canvas - responsive
        self._canvas_container = ctk.CTkFrame(card, fg_color="transparent")
        self._canvas_container.pack(fill="both", expand=True, padx=12, pady=12)

        self.canvas = ctk.CTkCanvas(
            self._canvas_container,
            width=640,
            height=480,
            bg=self.colors["canvas_bg"],
            highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True)

        # Beautiful empty state placeholder
        w, h = 640, 480
        cx, cy = w // 2, h // 2
        box_w, box_h = 340, 160
        x1, y1 = cx - box_w//2, cy - box_h//2
        x2, y2 = cx + box_w//2, cy + box_h//2
        
        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            outline=self.colors["border"],
            width=2,
            dash=(6, 4),
            fill=self.colors["bg_secondary"],
            tags="placeholder"
        )
        self.canvas.create_text(
            cx, cy - 15,
            text="🎹",
            fill=self.colors["text_muted"],
            font=ctk.CTkFont(size=32),
            justify="center",
            tags="placeholder"
        )
        self.canvas.create_text(
            cx, cy + 25,
            text="Latihan Belum Dimulai",
            fill=self.colors["text_primary"],
            font=ctk.CTkFont(size=16, weight="bold"),
            justify="center",
            tags="placeholder"
        )
        self.canvas.create_text(
            cx, cy + 50,
            text="Tekan [Mulai Latihan] untuk memulai\ndengan live camera preview",
            fill=self.colors["text_secondary"],
            font=ctk.CTkFont(size=13),
            justify="center",
            tags="placeholder"
        )

        self.canvas.bind("<Configure>", self._on_canvas_resize)

        # Footer with FPS
        footer = ctk.CTkFrame(
            card,
            fg_color=self.colors["bg_tertiary"],
            corner_radius=0,
            height=36,
        )
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        fps_frame = ctk.CTkFrame(footer, fg_color="transparent")
        fps_frame.pack(fill="x", padx=18, pady=6)

        self.fps_lbl = ctk.CTkLabel(
            fps_frame,
            text="FPS: --",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_muted"],
            anchor="w",
        )
        self.fps_lbl.pack(side="left")

        self.detection_lbl = ctk.CTkLabel(
            fps_frame,
            text="• Hands: --",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_muted"],
            anchor="w",
        )
        self.detection_lbl.pack(side="left", padx=(20, 0))

        return card

    def _on_canvas_resize(self, event):
        """Handle canvas resize."""
        self._canvas_width = max(320, event.width)
        self._canvas_height = max(240, event.height)

    def _status_card(self, parent):
        """System status card with device indicators."""
        card = self.card_with_header(
            parent,
            "Status Sistem",
            icon="◈",
            pady=CARD_GAP
        )

        # Status items
        items = [
            ("Kamera", "Memuat..."),
            ("MIDI", "Memuat..."),
            ("Kalibrasi", "Memuat..."),
        ]

        self.status_items = {}
        for label, value in items:
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=16, pady=4)

            # Status dot
            dot = ctk.CTkFrame(
                row,
                fg_color=self.colors["text_muted"],
                corner_radius=4,
                width=8,
                height=8,
            )
            dot.pack(side="left", padx=(0, 10), pady=8)
            dot.pack_propagate(False)

            # Label
            lbl = ctk.CTkLabel(
                row,
                text=f"{label}:",
                font=ctk.CTkFont(size=13),
                text_color=self.colors["text_secondary"],
                anchor="w",
            )
            lbl.pack(side="left")

            # Value
            val_lbl = ctk.CTkLabel(
                row,
                text=value,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=self.colors["text_muted"],
                anchor="e",
                wraplength=150,
            )
            val_lbl.pack(side="right")
            self.status_items[label] = (val_lbl, dot)

        ctk.CTkLabel(card, text="").pack(pady=4)

    def _notes_card(self, parent):
        """Active notes card."""
        card = self.card_with_header(
            parent,
            "Note Aktif",
            icon="♪",
            pady=CARD_GAP
        )

        self.left_notes_lbl = None
        self.right_notes_lbl = None

        for hand, key in [("KIRI", "left"), ("KANAN", "right")]:
            row = ctk.CTkFrame(
                card,
                fg_color=self.colors["bg_tertiary"],
                corner_radius=RADIUS_SM,
            )
            row.pack(fill="x", padx=16, pady=3)

            # Hand label
            lbl = ctk.CTkLabel(
                row,
                text=hand,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=self.colors["text_muted"],
                width=50,
            )
            lbl.pack(side="left", padx=10, pady=8)

            # Value label
            val_lbl = ctk.CTkLabel(
                row,
                text="—",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=self.colors["text_secondary"],
                anchor="w",
            )
            val_lbl.pack(side="left", fill="x", expand=True, padx=(0, 10))

            if key == "left":
                self.left_notes_lbl = val_lbl
            else:
                self.right_notes_lbl = val_lbl

        ctk.CTkLabel(card, text="").pack(pady=2)

    def _posture_card(self, parent):
        """Posture feedback card."""
        card = self.card_with_header(
            parent,
            "Postur Tangan",
            icon="✋",
            pady=CARD_GAP
        )

        for hand, key in [("KIRI", "left"), ("KANAN", "right")]:
            row = ctk.CTkFrame(
                card,
                fg_color=self.colors["bg_tertiary"],
                corner_radius=RADIUS_SM,
            )
            row.pack(fill="x", padx=16, pady=3)

            # Hand label
            lbl = ctk.CTkLabel(
                row,
                text=hand,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=self.colors["text_muted"],
                width=50,
            )
            lbl.pack(side="left", padx=10, pady=8)

            # Status
            val_lbl = ctk.CTkLabel(
                row,
                text="—",
                font=ctk.CTkFont(size=13),
                text_color=self.colors["text_secondary"],
                anchor="w",
                wraplength=180,
            )
            val_lbl.pack(side="left", fill="x", expand=True, pady=8)
            setattr(self, f"posture_{key}_lbl", val_lbl)

        ctk.CTkLabel(card, text="").pack(pady=4)

    def _controls_card(self, parent):
        """Practice controls."""
        card = self.card_with_header(
            parent,
            "Kontrol",
            icon="⚙",
            pady=CARD_GAP
        )

        # Start/Stop button - fill width
        self.start_btn = ctk.CTkButton(
            card,
            text="▶ Mulai Latihan",
            command=self._toggle,
            height=54,
            corner_radius=RADIUS_LG,
            fg_color=self.colors["success"],
            hover_color=adjust_color(self.colors["success"], -15),
            text_color=self.colors["text_on_accent"],
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.start_btn.pack(fill="x", padx=16, pady=(0, 10))

        # Reset calibration button
        reset_btn = ctk.CTkButton(
            card,
            text="↺ Reset Kalibrasi",
            command=self._reset_calib,
            height=38,
            corner_radius=RADIUS_MD,
            fg_color=self.colors["bg_tertiary"],
            hover_color=self.colors["bg_hover"],
            text_color=self.colors["text_primary"],
            font=ctk.CTkFont(size=13),
        )
        reset_btn.pack(fill="x", padx=16, pady=(0, 12))

        # Mode info
        cfg = self.app.config.config
        
        self.guided_mode_var = ctk.BooleanVar(value=bool(cfg.midi_file_path))
        
        mode_frame = ctk.CTkFrame(
            card,
            fg_color=self.colors["bg_tertiary"] if not cfg.midi_file_path else self.colors["info_light"],
            corner_radius=RADIUS_SM,
        )
        mode_frame.pack(fill="x", padx=16, pady=(0, 12))

        if cfg.midi_file_path:
            name = cfg.midi_file_path.split("/")[-1].split("\\")[-1]
            short_name = name[:20] + "..." if len(name) > 20 else name
            
            info_lbl = ctk.CTkLabel(
                mode_frame,
                text=f"♪ {short_name}",
                font=ctk.CTkFont(size=12),
                text_color=self.colors["info_text"],
                anchor="w",
            )
            info_lbl.pack(side="left", padx=(12, 5), pady=8, expand=True, fill="x")
            
            self.guided_switch = ctk.CTkSwitch(
                mode_frame,
                text="Guide",
                variable=self.guided_mode_var,
                command=self._on_guide_toggled,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=self.colors["info_text"],
                progress_color=self.colors["success"],
                width=50,
            )
            self.guided_switch.pack(side="right", padx=(0, 12))
        else:
            info_lbl = ctk.CTkLabel(
                mode_frame,
                text="● Mode: Free Play (tanpa guide)",
                font=ctk.CTkFont(size=12),
                text_color=self.colors["text_secondary"],
                anchor="w",
            )
            info_lbl.pack(padx=12, pady=8)

    def _on_guide_toggled(self):
        """Handle guide toggle switch."""
        if not self.running:
            return
            
        if self.guided_mode_var.get() and self.app.config.config.midi_file_path:
            self.mode_lbl.configure(text="GUIDED PRACTICE", text_color=self.colors["warning"])
            self.mode_badge.configure(fg_color=self.colors["warning_light"])
            self.app.song_player.start_playback(
                base_midi=self.app.keyboard_mapper.base_midi,
                total_keys=self.app.keyboard_mapper.total_keys,
                active_notes_getter=self.app.midi_manager.get_active_notes,
            )
        else:
            self.mode_lbl.configure(text="FREE PLAY", text_color=self.colors["success"])
            self.mode_badge.configure(fg_color=self.colors["success_light"])
            self.app.song_player.stop()

    def _toggle(self):
        """Toggle practice on/off."""
        if self.running:
            self._stop()
        else:
            self._start()

    def _start(self):
        """Start practice session."""
        self.running = True
        self.preview_running = True
        self.start_btn.configure(
            text="■ Hentikan Latihan",
            fg_color=self.colors["error"],
        )

        # Update mode indicator
        if self.guided_mode_var.get() and self.app.config.config.midi_file_path:
            self.mode_lbl.configure(text="GUIDED PRACTICE", text_color=self.colors["warning"])
            self.mode_badge.configure(fg_color=self.colors["warning_light"])
        else:
            self.mode_lbl.configure(text="FREE PLAY", text_color=self.colors["success"])
            self.mode_badge.configure(fg_color=self.colors["success_light"])

        # Open camera handle moved to background thread to prevent DirectShow COM deadlock

        # Load calibration
        if self.app.config.is_calibration_complete():
            pts = self.app.config.calibration.points
            if pts:
                self.app.keyboard_mapper.set_calibration_points(
                    [(int(a), int(b)) for a, b in pts]
                )

        # Connect MIDI
        if not self.app.midi_manager.is_connected:
            name = self.app.config.config.midi_input_name
            if name:
                self.app.midi_manager.connect(name)
            else:
                ports = self.app.midi_manager.detect_inputs()
                if ports:
                    self.app.midi_manager.connect(ports[0])

        # Load MIDI file if available
        if self.app.config.config.midi_file_path:
            self.app.song_player.load_file(
                self.app.config.config.midi_file_path,
                base_midi=self.app.keyboard_mapper.base_midi,
                total_keys=self.app.keyboard_mapper.total_keys,
            )
            if self.guided_mode_var.get():
                self.app.song_player.start_playback(
                    base_midi=self.app.keyboard_mapper.base_midi,
                    total_keys=self.app.keyboard_mapper.total_keys,
                    active_notes_getter=self.app.midi_manager.get_active_notes,
                )

        # Clear placeholder
        self.canvas.delete("all")
        self.canvas_item = None  # Reset agar referensi bersih saat start

        # Start preview thread
        thread = threading.Thread(target=self._preview_loop, daemon=True)
        thread.start()

    def _preview_loop(self):
        """Background camera + overlay loop."""
        # Open camera on the background thread to avoid Windows DirectShow deadlocks
        self.app.camera_manager.close()
        self.app.camera_manager.open(self.app.config.config.camera_index)

        while self.running:
            t0 = cv2.getTickCount()
            frame = self.app.camera_manager.read_frame()
            if frame is None:
                import time
                time.sleep(0.01)
                continue

            # Poll MIDI
            self.app.midi_manager.poll_messages()
            notes = self.app.midi_manager.get_active_notes()

            # Hand tracking
            hands = self.app.hand_tracker.process_frame(frame)
            tips = []
            left_post = None
            right_post = None
            for h in hands:
                tips.extend(h["finger_tips"])
                p = h["posture"]
                if p.hand == "L":
                    left_post = p
                else:
                    right_post = p

            # Overlay rendering
            guided = (
                self.guided_mode_var.get()
                and self.app.config.config.midi_file_path
                and self.app.song_player.is_playing
            )
            self.app.overlay_renderer.update_state(
                active_notes=notes,
                target_notes=self.app.song_player.active_target_notes,
                waiting_notes=self.app.song_player.waiting_notes,
                is_guided=guided,
            )
            self.app.overlay_renderer.update_hands(tips, left_post, right_post)

            out = self.app.overlay_renderer.render(frame)
            out = self.app.overlay_renderer.render_info_panel(out)

            # Calculate FPS
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - t0 + 1e-6)

            # Store for UI update - resize to current canvas dimensions while preserving aspect ratio
            rgb = cv2.cvtColor(out, cv2.COLOR_BGR2RGB)
            cw = max(320, self._canvas_width)
            ch = max(240, self._canvas_height)
            
            h_img, w_img = rgb.shape[:2]
            scale = min(cw / w_img, ch / h_img)
            new_w = int(w_img * scale)
            new_h = int(h_img * scale)
            
            rgb_small = cv2.resize(rgb, (new_w, new_h))
            pil = Image.fromarray(rgb_small)

            with self.lock:
                self.latest_frame = pil
                self.latest_notes = notes
                self.latest_note_fingers = self.app.overlay_renderer.current_note_fingers.copy()
                self.latest_left = left_post
                self.latest_right = right_post
                self.latest_fps = fps
                self.frame_ready = True

    def _ui_update(self):
        """UI update loop - runs on main thread."""
        if not self.preview_running:
            return
        try:
            with self.lock:
                if self.frame_ready:
                    pil_img = self.latest_frame
                    notes = self.latest_notes
                    note_fingers = getattr(self, 'latest_note_fingers', {})
                    left = self.latest_left
                    right = self.latest_right
                    fps = self.latest_fps
                    self.frame_ready = False
                else:
                    pil_img = notes = left = right = None
                    note_fingers = {}
                    fps = 0

            if pil_img:
                photo = ImageTk.PhotoImage(pil_img)
                cx = self._canvas_width // 2
                cy = self._canvas_height // 2
                if self.canvas_item:
                    self.canvas.itemconfig(self.canvas_item, image=photo)
                    self.canvas.coords(self.canvas_item, cx, cy)
                else:
                    self.canvas_item = self.canvas.create_image(cx, cy, image=photo)
                self.photo = photo

                # Update notes display
                display_notes_left = []
                display_notes_right = []
                
                if notes:
                    for n in sorted(notes):
                        if n in note_fingers:
                            finger_label = note_fingers[n]
                            if finger_label.startswith("L-"):
                                display_notes_left.append(f"{n} ({finger_label[2:]})")
                            elif finger_label.startswith("R-"):
                                display_notes_right.append(f"{n} ({finger_label[2:]})")
                            else:
                                if n < 60: display_notes_left.append(str(n))
                                else: display_notes_right.append(str(n))
                        else:
                            if n < 60: display_notes_left.append(str(n))
                            else: display_notes_right.append(str(n))
                
                if display_notes_left:
                    self.left_notes_lbl.configure(
                        text=", ".join(display_notes_left),
                        text_color=self.colors["success"]
                    )
                else:
                    self.left_notes_lbl.configure(
                        text="—",
                        text_color=self.colors["text_muted"]
                    )

                if display_notes_right:
                    self.right_notes_lbl.configure(
                        text=", ".join(display_notes_right),
                        text_color=self.colors["success"]
                    )
                else:
                    self.right_notes_lbl.configure(
                        text="—",
                        text_color=self.colors["text_muted"]
                    )

                # Update posture labels
                for post, lbl_attr in [(left, "left"), (right, "right")]:
                    lbl = getattr(self, f"posture_{lbl_attr}_lbl")
                    if post:
                        lbl.configure(
                            text=post.message,
                            text_color=self._posture_color(post.status)
                        )
                    else:
                        lbl.configure(
                            text="—",
                            text_color=self.colors["text_muted"]
                        )

                # Update FPS
                self.fps_lbl.configure(text=f"FPS: {int(fps)}")

                # Update hand detection indicator
                hand_count = (1 if left else 0) + (1 if right else 0)
                if hand_count > 0:
                    self.detection_lbl.configure(
                        text=f"• Hands: {hand_count}",
                        text_color=self.colors["success"]
                    )
                else:
                    self.detection_lbl.configure(
                        text="• Hands: --",
                        text_color=self.colors["text_muted"]
                    )

        except Exception:
            pass

        self.preview_id = self.canvas.after(33, self._ui_update)

    def _posture_color(self, status: str) -> str:
        """Get color for posture status."""
        color_map = {
            "good": self.colors["success"],
            "stiff": self.colors["error"],
            "bent": self.colors["warning"],
            "octave_ok": self.colors["info"],
        }
        return color_map.get(status, self.colors["text_secondary"])

    def _stop(self):
        """Stop practice session."""
        self.running = False
        self.preview_running = False
        self.start_btn.configure(
            text="▶ Mulai Latihan",
            fg_color=self.colors["success"],
            hover_color=adjust_color(self.colors["success"], -15),
        )
        self.app.song_player.stop()
        self.mode_lbl.configure(
            text="FREE PLAY",
            text_color=self.colors["accent"]
        )
        self.mode_badge.configure(fg_color=self.colors["accent_light"])
        self._update_status()
        
        # Redraw placeholder
        self.canvas.delete("all")
        self.canvas_item = None  # Penting: reset agar tidak reference stale item
        w = max(320, self._canvas_width)
        h = max(240, self._canvas_height)
        cx, cy = w // 2, h // 2
        box_w, box_h = 340, 160
        x1, y1 = cx - box_w//2, cy - box_h//2
        x2, y2 = cx + box_w//2, cy + box_h//2
        
        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            outline=self.colors["border"],
            width=2,
            dash=(6, 4),
            fill=self.colors["bg_secondary"],
            tags="placeholder"
        )
        self.canvas.create_text(
            cx, cy - 15,
            text="🎹",
            fill=self.colors["text_muted"],
            font=("TkDefaultFont", 32),
            justify="center",
            tags="placeholder"
        )
        self.canvas.create_text(
            cx, cy + 25,
            text="Latihan Dihentikan",
            fill=self.colors["text_primary"],
            font=("TkDefaultFont", 16, "bold"),
            justify="center",
            tags="placeholder"
        )
        self.canvas.create_text(
            cx, cy + 50,
            text="Tekan [Mulai Latihan] untuk memulai\ndengan live camera preview",
            fill=self.colors["text_secondary"],
            font=("TkDefaultFont", 13),
            justify="center",
            tags="placeholder"
        )

    def _reset_calib(self):
        """Reset calibration."""
        from tkinter import messagebox
        if messagebox.askyesno("Reset", "Reset kalibrasi?"):
            self.app.config.calibration.points = []
            self.app.config.calibration.tuts_rects = {}
            self.app.config.save()
            self.app.keyboard_mapper.clear_calibration()
            self.app.show_page("calibration")

    def on_appear(self):
        """On page appear."""
        self._auto_connect_midi()
        self._update_status()
        self.preview_running = True
        self._ui_update()

    def on_disappear(self):
        """On page disappear."""
        self.running = False
        self.preview_running = False
        if self.preview_id:
            self.canvas.after_cancel(self.preview_id)

    def _auto_connect_midi(self):
        """Auto-connect MIDI if not connected."""
        if self.app.midi_manager.is_connected:
            return
        name = self.app.config.config.midi_input_name
        if name and self.app.midi_manager.connect(name):
            return
        ports = self.app.midi_manager.detect_inputs()
        if ports:
            for p in ports:
                if 'Roland' in p or 'E-X' in p:
                    self.app.midi_manager.connect(p)
                    self.app.config.config.midi_input_name = p
                    break
            else:
                self.app.midi_manager.connect(ports[0])
                self.app.config.config.midi_input_name = ports[0]

    def _update_status(self):
        """Update status labels."""
        cam = self.app.camera_manager
        midi = self.app.midi_manager
        calib = self.app.keyboard_mapper

        def update_item(name, text, color, status="idle"):
            if name in self.status_items:
                lbl, dot = self.status_items[name]
                lbl.configure(text=text, text_color=color)
                dot.configure(fg_color=status_map.get(status, self.colors["text_muted"]))

        status_map = {
            "success": self.colors["success"],
            "warning": self.colors["warning"],
            "error": self.colors["error"],
            "idle": self.colors["text_muted"],
        }

        if cam.is_opened:
            update_item("Kamera", f"Camera {cam.camera_index}", self.colors["success"], "success")
        else:
            update_item("Kamera", "Belum Terbuka", self.colors["error"], "error")

        if midi.is_connected:
            name = midi.port_name or "Terhubung"
            short_name = name[:18] + "..." if len(name) > 18 else name
            update_item("MIDI", short_name, self.colors["success"], "success")
        else:
            update_item("MIDI", "Belum Tersambung", self.colors["error"], "error")

        if calib and calib.is_calibrated():
            update_item("Kalibrasi", "Selesai", self.colors["success"], "success")
        else:
            update_item("Kalibrasi", "Belum", self.colors["warning"], "warning")