"""
AI Piano Coach - Guide / Panduan Page
Premium step-by-step usage guide with polished layout.
"""
import customtkinter as ctk
from app.ui.base_page import BasePage
from app.design_system import (
    get_light_colors,
    RADIUS_LG, RADIUS_FULL, RADIUS_XS,
    SECTION_GAP, CARD_GAP, CARD_PADDING,
)


class GuidePage(BasePage):
    """Panduan penggunaan aplikasi dengan layout premium."""

    def __init__(self, parent, app_controller):
        self.colors = get_light_colors()
        super().__init__(
            parent, app_controller,
            "Panduan",
            "Langkah-langkah penggunaan AI Piano Coach"
        )
        self._create_content()

    def _create_content(self):
        """Create guide content with step cards."""
        scroll = self.scrollable_frame(self.content_frame)
        scroll.pack(fill="both", expand=True)

        # Introduction card
        self._intro_card(scroll)

        # 7 step cards
        self._step_card(scroll, "1", "Hubungkan Keyboard MIDI", [
            "Sambungkan keyboard MIDI ke laptop via USB",
            "Pastikan keyboard dalam keadaan menyala",
            "Tunggu driver terinstall otomatis oleh sistem",
            "Verifikasi device muncul di halaman Setup",
        ])

        self._step_card(scroll, "2", "Pilih Kamera yang Tepat", [
            "Buka halaman Setup di sidebar",
            "Pilih kamera yang mengarah ke keyboard piano",
            "Tekan tombol [Test Camera] untuk memastikan berfungsi",
            "Pastikan seluruh keyboard terlihat jelas di preview",
            "Kamera yang terlalu jauh dapat mengurangi akurasi tracking",
        ])

        self._step_card(scroll, "3", "Pilih MIDI Input", [
            "Pilih nama keyboard Anda dari dropdown",
            "Jika tidak muncul, tekan tombol [Refresh MIDI Devices]",
            "Status hijau menandakan berhasil terhubung",
            "Pastikan kabel USB keyboard terhubung dengan benar",
        ])

        self._step_card(scroll, "4", "Pilih Ukuran Keyboard", [
            "61 Keys: Cocok untuk Roland E-X10 atau keyboard portable",
            "88 Keys: Untuk piano full-size atau grand digital",
            "Pilih sesuai dengan keyboard fisik yang Anda gunakan",
        ])

        self._step_card(scroll, "5", "Pilih File MIDI Guide (Opsional)", [
            "Klik [Pilih File MIDI] untuk memilih file .mid/.midi",
            "File guide digunakan untuk latihan terpandu (guided mode)",
            "Kosongkan jika hanya ingin mode Free Play tanpa guide",
            "Guided mode akan menampilkan target nada yang harus ditekan",
        ])

        self._step_card(scroll, "6", "Kalibrasi Keyboard", [
            "Buka halaman Kalibrasi dari sidebar",
            "Klik [Mulai Preview] untuk melihat feed kamera",
            "Klik 4 sudut keyboard secara berurutan:",
            "   - Kiri-atas (sudut kiri atas keyboard)",
            "   - Kanan-atas (sudut kanan atas keyboard)",
            "   - Kanan-bawah (sudut kanan bawah keyboard)",
            "   - Kiri-bawah (sudut kiri bawah keyboard)",
            "Tekan [Simpan Kalibrasi] jika sudah lengkap",
            "Kalibrasi ulang jika posisi kamera berubah",
        ])

        self._step_card(scroll, "7", "Mulai Latihan Piano", [
            "Buka halaman Latihan dari sidebar",
            "Tekan tombol hijau [▶ Mulai Latihan]",
            "Tekan tuts sesuai penunjukan visual di layar",
            "Mode Free Play: tekan tuts apa saja secara bebas",
            "Mode Guided: tunggu target nada muncul, lalu tekan",
            "Tekan tombol [■ Hentikan Latihan] untuk berhenti",
        ])

        # Color guide card
        self._color_guide(scroll)

        # Tips card
        self._tips_card(scroll)

        # Troubleshooting
        self._troubleshooting(scroll)

        # Footer
        footer = ctk.CTkLabel(
            scroll,
            text="ℹ Cek halaman Diagnostik untuk informasi debug dan troubleshooting lanjut.",
            font=ctk.CTkFont(size=13),
            text_color=self.colors["text_secondary"],
            wraplength=600,
        )
        footer.pack(pady=24)

    def _intro_card(self, parent):
        """Create introduction card."""
        card = self.card_with_header(
            parent,
            "Selamat Datang di Panduan AI Piano Coach",
            icon="?",
            pady=CARD_GAP
        )

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=CARD_PADDING, pady=(8, 16))

        intro = ctk.CTkLabel(
            content,
            text="Ikuti 7 langkah di bawah ini untuk memulai sesi latihan piano.\n"
                 "Panduan ini akan membantu Anda configure hardware dan memahami\n"
                 "fitur-fitur yang tersedia di aplikasi.",
            font=ctk.CTkFont(size=14),
            text_color=self.colors["text_secondary"],
            justify="left",
            wraplength=700,
        )
        intro.pack(anchor="w")

    def _step_card(self, parent, num: str, title: str, items: list):
        """Create a premium step card."""
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
        hdr.pack(fill="x", padx=CARD_PADDING, pady=(18, 10))

        # Step badge
        badge = ctk.CTkFrame(
            hdr,
            fg_color=self.colors["accent"],
            corner_radius=RADIUS_FULL,
            width=36,
            height=36,
        )
        badge.pack(side="left", padx=(0, 14))
        badge.pack_propagate(False)

        badge_lbl = ctk.CTkLabel(
            badge,
            text=num,
            text_color=self.colors["text_on_accent"],
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        badge_lbl.pack(expand=True)

        # Title
        title_lbl = ctk.CTkLabel(
            hdr,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors["text_primary"],
            anchor="w",
        )
        title_lbl.pack(side="left")

        # Items - with wraplength
        for item in items:
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=CARD_PADDING, pady=2)

            # Bullet
            bullet = ctk.CTkLabel(
                row,
                text="▸",
                font=ctk.CTkFont(size=12),
                text_color=self.colors["accent"],
                width=16,
            )
            bullet.pack(side="left")

            # Text with wraplength
            txt = ctk.CTkLabel(
                row,
                text=item,
                font=ctk.CTkFont(size=13),
                text_color=self.colors["text_secondary"],
                anchor="w",
                wraplength=650,
            )
            txt.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(card, text="").pack(pady=6)

        # Hover effect for premium feel
        def on_enter(e, c=card, b=badge):
            c.configure(border_color=self.colors["border_hover"])
            b.configure(fg_color=self.colors["accent_hover"])
        def on_leave(e, c=card, b=badge):
            c.configure(border_color=self.colors["border"])
            b.configure(fg_color=self.colors["accent"])
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

    def _color_guide(self, parent):
        """Color legend card with swatches."""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors["bg_secondary"],
            border_color=self.colors["border"],
            border_width=1,
            corner_radius=RADIUS_LG,
        )
        card.pack(fill="x", pady=(0, CARD_GAP))

        hdr = ctk.CTkLabel(
            card,
            text="Arti Warna Overlay Kamera",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=self.colors["text_primary"],
            anchor="w",
        )
        hdr.pack(anchor="w", padx=CARD_PADDING, pady=(16, 10))

        colors_data = [
            ("#059669", "Hijau", "Tuts sedang ditekan (pressed key)"),
            ("#059669", "Hijau", "Benar - note sesuai target (guided mode)"),
            ("#DC2626", "Merah", "Salah - note tidak sesuai (guided mode)"),
            ("#2563EB", "Biru", "Target nada untuk tangan kiri"),
            ("#D97706", "Kuning/Orange", "Target nada untuk tangan kanan"),
        ]

        for color, name, desc in colors_data:
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=CARD_PADDING, pady=4)

            # Color swatch
            swatch = ctk.CTkFrame(
                row,
                fg_color=color,
                corner_radius=RADIUS_XS,
                width=24,
                height=24,
            )
            swatch.pack(side="left", padx=(0, 14))
            swatch.pack_propagate(False)

            # Label
            lbl = ctk.CTkLabel(
                row,
                text=name,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=color,
                width=90,
                anchor="w",
            )
            lbl.pack(side="left")

            # Description with wraplength
            desc_lbl = ctk.CTkLabel(
                row,
                text=desc,
                font=ctk.CTkFont(size=13),
                text_color=self.colors["text_secondary"],
                anchor="w",
                wraplength=500,
            )
            desc_lbl.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(card, text="").pack(pady=10)

    def _tips_card(self, parent):
        """Tips card with light accent styling."""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors["info_light"],
            border_color=self.colors["info_border"],
            border_width=1,
            corner_radius=RADIUS_LG,
        )
        card.pack(fill="x", pady=(0, CARD_GAP))

        hdr = ctk.CTkLabel(
            card,
            text="Tips untuk Hasil Terbaik",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=self.colors["info_text"],
            anchor="w",
        )
        hdr.pack(anchor="w", padx=CARD_PADDING, pady=(14, 8))

        tips = [
            "Pencahayaan terang dan merata - hindari bayangan",
            "Posisi kamera tegak lurus di atas keyboard",
            "Pastikan seluruh keyboard terlihat di frame kamera",
            "Jaga tangan tetap rileks untuk tracking optimal",
            "Lakukan kalibrasi ulang jika posisi kamera berubah",
            "Hindari latar belakang yang terlalu ramai",
        ]

        for tip in tips:
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=CARD_PADDING, pady=3)

            dot = ctk.CTkLabel(
                row,
                text="→",
                font=ctk.CTkFont(size=12),
                text_color=self.colors["info"],
            )
            dot.pack(side="left")

            lbl = ctk.CTkLabel(
                row,
                text=tip,
                font=ctk.CTkFont(size=13),
                text_color=self.colors["info_text"],
                anchor="w",
                wraplength=600,
            )
            lbl.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(card, text="").pack(pady=10)

    def _troubleshooting_card(self, parent, problem: str, solutions: list):
        """Single troubleshooting item."""
        card = ctk.CTkFrame(parent, fg_color="transparent")
        card.pack(fill="x", pady=8)

        lbl = ctk.CTkLabel(
            card,
            text=f"⚠ {problem}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["warning_text"],
            anchor="w",
        )
        lbl.pack(anchor="w")

        for sol in solutions:
            row = ctk.CTkLabel(
                card,
                text=f"   • {sol}",
                font=ctk.CTkFont(size=12),
                text_color=self.colors["text_secondary"],
                anchor="w",
                wraplength=600,
            )
            row.pack(anchor="w")

    def _troubleshooting(self, parent):
        """Troubleshooting section."""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors["bg_secondary"],
            border_color=self.colors["border"],
            border_width=1,
            corner_radius=RADIUS_LG,
        )
        card.pack(fill="x", pady=(0, 12))

        hdr = ctk.CTkLabel(
            card,
            text="Troubleshooting Umum",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=self.colors["text_primary"],
            anchor="w",
        )
        hdr.pack(anchor="w", padx=CARD_PADDING, pady=(16, 8))

        issues = [
            ("Kamera tidak terdeteksi", [
                "Pastikan webcam tidak dipakai aplikasi lain (Zoom, browser)",
                "Cabut dan colok kembali kabel USB kamera",
                "Klik [Refresh] di halaman Setup",
            ]),
            ("MIDI keyboard tidak muncul", [
                "Pastikan keyboard MIDI menyala",
                "Coba port USB yang berbeda di laptop",
                "Restart aplikasi AI Piano Coach",
            ]),
            ("Overlay piano tidak cocok dengan keyboard", [
                "Lakukan kalibrasi ulang dengan teliti",
                "Pastikan 4 titik marking sesuai sudut keyboard",
                "Jangan ubah posisi kamera setelah kalibrasi",
            ]),
            ("Tracking tangan lambat atau tidak akurat", [
                "Tutup aplikasi berat lainnya",
                "Pastikan pencahayaan cukup terang",
                "Pastikan hanya 2 tangan yang terlihat di kamera",
            ]),
        ]

        for problem, solutions in issues:
            self._troubleshooting_card(card, problem, solutions)

        ctk.CTkLabel(card, text="").pack(pady=10)