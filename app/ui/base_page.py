"""
AI Piano Coach - Base Page
Premium modern light theme base class with polished reusable components.
"""
import customtkinter as ctk
from app.design_system import (
    get_light_colors, get_premium_colors, adjust_color, adjust_brightness,
    RADIUS_XS, RADIUS_SM, RADIUS_MD, RADIUS_LG, RADIUS_XL, RADIUS_2XL, RADIUS_FULL,
    SPACING_SM, SPACING_MD, SPACING_LG, SPACING_XL, SPACING_2XL,
    HEADER_HEIGHT, SECTION_GAP, CARD_GAP, CARD_PADDING,
)


class BasePage(ctk.CTkFrame):
    """Base class for all pages with premium light theme styling."""

    def __init__(self, parent, app_controller, title: str = "Page", subtitle: str = None):
        self.app = app_controller
        self.colors = get_light_colors()
        self.page_title = title
        self.page_subtitle = subtitle

        super().__init__(
            parent,
            fg_color=self.colors["bg_primary"],
        )

        self._create_header()
        self._create_content_area()

    def _create_header(self):
        """Create polished page header with bottom border."""
        header = ctk.CTkFrame(
            self,
            fg_color=self.colors["bg_secondary"],
            height=HEADER_HEIGHT,
        )
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)

        # Title area
        title_area = ctk.CTkFrame(header, fg_color="transparent")
        title_area.pack(side="left", fill="y", padx=28)

        # Page icon/indicator
        icon_frame = ctk.CTkFrame(
            title_area,
            fg_color=self.colors["accent_light"],
            corner_radius=RADIUS_SM,
            width=32,
            height=32,
        )
        icon_frame.pack(side="left", pady=0, padx=(0, 12))
        icon_frame.pack_propagate(False)

        # Title
        title = ctk.CTkLabel(
            title_area,
            text=self.page_title,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors["text_primary"],
        )
        title.pack(side="left")

        if self.page_subtitle:
            # Separator dot
            sep = ctk.CTkLabel(
                title_area,
                text="•",
                font=ctk.CTkFont(size=14),
                text_color=self.colors["text_muted"],
            )
            sep.pack(side="left", padx=(10, 10))

            subtitle = ctk.CTkLabel(
                title_area,
                text=self.page_subtitle,
                font=ctk.CTkFont(size=13),
                text_color=self.colors["text_secondary"],
            )
            subtitle.pack(side="left")

        # Bottom border line only (removed floating accent dot)
        border_line = ctk.CTkFrame(header, fg_color=self.colors["border"], height=1)
        border_line.pack(side="bottom", fill="x")

    def _create_content_area(self):
        """Create content area with proper padding."""
        self.content_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        self.content_frame.pack(fill="both", expand=True, padx=28, pady=SECTION_GAP)

    def on_appear(self):
        """Called when page is shown."""
        pass

    def on_disappear(self):
        """Called when page is hidden."""
        pass

    # ========================================================================
    # PREMIUM CARD COMPONENTS
    # ========================================================================

    def card(self, parent=None, title: str = None, pady: int = CARD_GAP, padx: int = 0, elevation: str = "light") -> ctk.CTkFrame:
        """Create a premium card/panel with optional title."""
        container = parent or self.content_frame
        card = ctk.CTkFrame(
            container,
            fg_color=self.colors["bg_secondary"],
            border_color=self.colors["border"],
            border_width=1,
            corner_radius=RADIUS_LG,
        )
        card.pack(fill="x", pady=(0, pady), padx=padx)
        return card

    def section_card(self, parent, title: str = None, subtitle: str = None, icon: str = None) -> ctk.CTkFrame:
        """Create a section card with header, used in Setup and other pages."""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors["bg_secondary"],
            border_color=self.colors["border"],
            border_width=1,
            corner_radius=RADIUS_LG,
        )
        card.pack(fill="x", pady=(0, CARD_GAP))

        if title:
            header = ctk.CTkFrame(card, fg_color="transparent")
            header.pack(fill="x", padx=CARD_PADDING, pady=(18, 10))

            # Optional icon
            if icon:
                icon_frame = ctk.CTkFrame(
                    header,
                    fg_color=self.colors["accent_light"],
                    corner_radius=RADIUS_SM,
                    width=28,
                    height=28,
                )
                icon_frame.pack(side="left", padx=(0, 10), pady=0)
                icon_frame.pack_propagate(False)

                icon_lbl = ctk.CTkLabel(
                    icon_frame,
                    text=icon,
                    font=ctk.CTkFont(size=14),
                    text_color=self.colors["accent"],
                )
                icon_lbl.pack(expand=True)

            # Title
            title_lbl = ctk.CTkLabel(
                header,
                text=title,
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color=self.colors["text_primary"],
                anchor="w",
            )
            title_lbl.pack(side="left")

            # Subtitle
            if subtitle:
                sub_lbl = ctk.CTkLabel(
                    header,
                    text=subtitle,
                    font=ctk.CTkFont(size=12),
                    text_color=self.colors["text_secondary"],
                    anchor="w",
                    wraplength=500,
                )
                sub_lbl.pack(side="left", padx=(8, 0))

        return card

    def card_with_header(self, parent, title: str, subtitle: str = None, icon: str = None, pady: int = CARD_GAP):
        """Create a card with a styled header section."""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors["bg_secondary"],
            border_color=self.colors["border"],
            border_width=1,
            corner_radius=RADIUS_LG,
        )
        card.pack(fill="x", pady=(0, pady))

        # Header
        hdr = ctk.CTkFrame(card, fg_color=self.colors["bg_tertiary"], corner_radius=0)
        hdr.pack(fill="x")
        hdr.configure(height=42)
        hdr.pack_propagate(False)

        hdr_inner = ctk.CTkFrame(hdr, fg_color="transparent")
        hdr_inner.pack(fill="x", padx=16, pady=8)

        # Icon if provided
        if icon:
            icon_lbl = ctk.CTkLabel(
                hdr_inner,
                text=icon,
                font=ctk.CTkFont(size=14),
                text_color=self.colors["accent"],
            )
            icon_lbl.pack(side="left", padx=(0, 8))

        title_lbl = ctk.CTkLabel(
            hdr_inner,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["text_primary"],
        )
        title_lbl.pack(side="left")

        if subtitle:
            sep = ctk.CTkLabel(
                hdr_inner,
                text="•",
                font=ctk.CTkFont(size=12),
                text_color=self.colors["text_muted"],
            )
            sep.pack(side="left", padx=(8, 8))
            sub_lbl = ctk.CTkLabel(
                hdr_inner,
                text=subtitle,
                font=ctk.CTkFont(size=12),
                text_color=self.colors["text_secondary"],
                wraplength=400,
            )
            sub_lbl.pack(side="left")

        return card

    # ========================================================================
    # STATUS COMPONENTS
    # ========================================================================

    def status_badge(self, parent, text: str, status: str = "info") -> ctk.CTkFrame:
        """Create a premium status badge/chip."""
        colors_map = {
            "success": (self.colors["success"], self.colors["success_light"], self.colors["success_text"]),
            "warning": (self.colors["warning"], self.colors["warning_light"], self.colors["warning_text"]),
            "error": (self.colors["error"], self.colors["error_light"], self.colors["error_text"]),
            "info": (self.colors["info"], self.colors["info_light"], self.colors["info_text"]),
        }
        fg, light, text_color = colors_map.get(status, colors_map["info"])

        badge = ctk.CTkFrame(parent, fg_color=light, corner_radius=RADIUS_SM)
        label = ctk.CTkLabel(
            badge,
            text=text,
            text_color=text_color,
            font=ctk.CTkFont(size=11, weight="bold"),
        )
        label.pack(padx=10, pady=5)
        return badge

    def status_indicator(self, parent, status: str = "idle") -> ctk.CTkFrame:
        """Create a small status dot indicator."""
        status_colors = {
            "success": self.colors["success"],
            "warning": self.colors["warning"],
            "error": self.colors["error"],
            "info": self.colors["info"],
            "idle": self.colors["text_muted"],
        }
        color = status_colors.get(status, self.colors["text_muted"])

        dot = ctk.CTkFrame(
            parent,
            fg_color=color,
            corner_radius=10,
            width=10,
            height=10,
        )
        dot.pack_propagate(False)
        return dot

    def metric_card(self, parent, title: str, value: str, status: str = "info",
                    subtitle: str = None, icon: str = None) -> ctk.CTkFrame:
        """Create a premium metric/status card with optional icon."""
        colors_map = {
            "success": (self.colors["success"], self.colors["success_light"]),
            "warning": (self.colors["warning"], self.colors["warning_light"]),
            "error": (self.colors["error"], self.colors["error_light"]),
            "info": (self.colors["info"], self.colors["info_light"]),
            "neutral": (self.colors["text_secondary"], self.colors["bg_tertiary"]),
        }
        color, bg = colors_map.get(status, colors_map["info"])

        card = ctk.CTkFrame(
            parent,
            fg_color=bg,
            corner_radius=RADIUS_MD,
        )

        # Header with icon
        if icon or subtitle:
            hdr = ctk.CTkFrame(card, fg_color="transparent")
            hdr.pack(fill="x", padx=14, pady=(12, 0))

            if icon:
                icon_lbl = ctk.CTkLabel(
                    hdr,
                    text=icon,
                    font=ctk.CTkFont(size=16),
                    text_color=color,
                )
                icon_lbl.pack(side="left", padx=(0, 8))

            if subtitle:
                sub_lbl = ctk.CTkLabel(
                    hdr,
                    text=subtitle,
                    font=ctk.CTkFont(size=11),
                    text_color=self.colors["text_secondary"],
                    wraplength=180,
                )
                sub_lbl.pack(side="left")

        # Title
        title_lbl = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.colors["text_secondary"],
            anchor="w",
            wraplength=180,
        )
        title_lbl.pack(fill="x", padx=14, pady=(8 if icon or subtitle else 12, 0))

        # Value
        value_lbl = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=color,
            anchor="w",
            wraplength=180,
        )
        value_lbl.pack(fill="x", padx=14, pady=(2, 12))

        return card

    def device_status_card(self, parent, title: str, value: str, status: str,
                           hint: str = None) -> ctk.CTkFrame:
        """Create a device status card with dot, value, and status."""
        colors_map = {
            "success": (self.colors["success"], self.colors["success_light"], self.colors["success_text"]),
            "warning": (self.colors["warning"], self.colors["warning_light"], self.colors["warning_text"]),
            "error": (self.colors["error"], self.colors["error_light"], self.colors["error_text"]),
            "info": (self.colors["info"], self.colors["info_light"], self.colors["info_text"]),
        }
        color, bg, text_color = colors_map.get(status, colors_map["info"])

        card = ctk.CTkFrame(
            parent,
            fg_color=bg,
            corner_radius=RADIUS_MD,
        )
        # Let card size naturally, but set min height
        card.configure(height=100)

        # Inner content with proper padding - no place()
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=16, pady=14)

        # Top row: status dot + title
        top_row = ctk.CTkFrame(content, fg_color="transparent")
        top_row.pack(fill="x")

        dot_frame = ctk.CTkFrame(top_row, fg_color=color, corner_radius=5, width=8, height=8)
        dot_frame.pack(side="left", padx=(0, 8))
        dot_frame.pack_propagate(False)

        title_lbl = ctk.CTkLabel(
            top_row,
            text=title,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=text_color,
            anchor="w",
        )
        title_lbl.pack(side="left")

        # Value
        value_lbl = ctk.CTkLabel(
            content,
            text=value,
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=text_color,
            anchor="w",
            wraplength=200,
        )
        value_lbl.pack(fill="x", pady=(4, 0))

        # Hint
        if hint:
            hint_lbl = ctk.CTkLabel(
                content,
                text=hint,
                font=ctk.CTkFont(size=10),
                text_color=self.colors["text_secondary"],
                anchor="w",
                wraplength=200,
            )
            hint_lbl.pack(fill="x", pady=(2, 0))

        return card

    # ========================================================================
    # STEP COMPONENTS
    # ========================================================================

    def step_card(self, parent, num: str, title: str, items: list, status: str = "pending") -> ctk.CTkFrame:
        """Create a numbered step card with items list."""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors["bg_secondary"],
            border_color=self.colors["border"] if status != "active" else self.colors["accent"],
            border_width=1,
            corner_radius=RADIUS_LG,
        )
        card.pack(fill="x", pady=(0, 12))

        # Header row
        hdr = ctk.CTkFrame(card, fg_color="transparent")
        hdr.pack(fill="x", padx=CARD_PADDING, pady=(16, 10))

        # Step number badge
        badge_bg = self.colors["accent"] if status == "active" else self.colors["bg_tertiary"]
        badge_text = self.colors["text_on_accent"] if status == "active" else self.colors["text_secondary"]

        badge = ctk.CTkFrame(
            hdr,
            fg_color=badge_bg,
            corner_radius=RADIUS_FULL,
            width=32,
            height=32,
        )
        badge.pack(side="left", padx=(0, 12))
        badge.pack_propagate(False)

        badge_lbl = ctk.CTkLabel(
            badge,
            text=num,
            text_color=badge_text,
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        badge_lbl.pack(expand=True)

        # Step title
        title_lbl = ctk.CTkLabel(
            hdr,
            text=title,
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=self.colors["text_primary"],
            anchor="w",
        )
        title_lbl.pack(side="left")

        # Items
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

            # Text - with wraplength
            txt = ctk.CTkLabel(
                row,
                text=item,
                font=ctk.CTkFont(size=13),
                text_color=self.colors["text_secondary"],
                anchor="w",
                wraplength=600,
            )
            txt.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(card, text="").pack(pady=6)
        return card

    def step_indicator(self, parent, steps: list, current_step: int = 0) -> ctk.CTkFrame:
        """Create a horizontal step progress indicator."""
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack()

        for i, step in enumerate(steps):
            # Step
            step_frame = ctk.CTkFrame(container, fg_color="transparent")
            step_frame.pack(side="left")

            # Circle
            if i < current_step:
                circle_color = self.colors["success"]
                text_color = self.colors["text_on_accent"]
            elif i == current_step:
                circle_color = self.colors["accent"]
                text_color = self.colors["text_on_accent"]
            else:
                circle_color = self.colors["bg_tertiary"]
                text_color = self.colors["text_muted"]

            circle = ctk.CTkFrame(
                step_frame,
                fg_color=circle_color,
                corner_radius=14,
                width=28,
                height=28,
            )
            circle.pack()
            circle.pack_propagate(False)

            circle_lbl = ctk.CTkLabel(
                circle,
                text=str(i + 1),
                text_color=text_color,
                font=ctk.CTkFont(size=12, weight="bold"),
            )
            circle_lbl.pack(expand=True)

            # Label
            lbl = ctk.CTkLabel(
                step_frame,
                text=step,
                font=ctk.CTkFont(size=11),
                text_color=self.colors["text_secondary"] if i != current_step else self.colors["text_primary"],
            )
            lbl.pack(pady=(4, 0))

            # Connector
            if i < len(steps) - 1:
                connector = ctk.CTkFrame(
                    step_frame,
                    fg_color=self.colors["border"] if i < current_step else self.colors["bg_tertiary"],
                    height=2,
                    width=40,
                )
                connector.pack(side="left", padx=(8, 8), pady=(13, 0))
                connector.pack_propagate(False)

        return container

    # ========================================================================
    # INFO & ALERT COMPONENTS
    # ========================================================================

    def info_banner(self, parent, text: str, status: str = "info") -> ctk.CTkFrame:
        """Create an informational banner/card."""
        colors_map = {
            "success": (self.colors["success_light"], self.colors["success"], self.colors["success_text"]),
            "warning": (self.colors["warning_light"], self.colors["warning"], self.colors["warning_text"]),
            "error": (self.colors["error_light"], self.colors["error"], self.colors["error_text"]),
            "info": (self.colors["info_light"], self.colors["info"], self.colors["info_text"]),
        }
        bg, border, text_color = colors_map.get(status, colors_map["info"])

        banner = ctk.CTkFrame(
            parent,
            fg_color=bg,
            border_color=border,
            border_width=1,
            corner_radius=RADIUS_MD,
        )

        lbl = ctk.CTkLabel(
            banner,
            text=text,
            font=ctk.CTkFont(size=13),
            text_color=text_color,
            wraplength=700,
        )
        lbl.pack(padx=16, pady=12)

        return banner

    def color_legend_item(self, parent, color_hex: str, label: str, description: str) -> ctk.CTkFrame:
        """Create a single color legend row."""
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=CARD_PADDING, pady=4)

        # Color swatch
        swatch = ctk.CTkFrame(
            row,
            fg_color=color_hex,
            corner_radius=RADIUS_XS,
            width=20,
            height=20,
        )
        swatch.pack(side="left", padx=(0, 12))
        swatch.pack_propagate(False)

        # Label
        lbl = ctk.CTkLabel(
            row,
            text=label,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=color_hex,
            width=80,
            anchor="w",
        )
        lbl.pack(side="left")

        # Description
        desc = ctk.CTkLabel(
            row,
            text=description,
            font=ctk.CTkFont(size=13),
            text_color=self.colors["text_secondary"],
            anchor="w",
            wraplength=500,
        )
        desc.pack(side="left", fill="x", expand=True)

        return row

    def tip_card(self, parent, title: str, items: list) -> ctk.CTkFrame:
        """Create a tips card with light accent styling."""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors["info_light"],
            border_color=self.colors["info_border"],
            border_width=1,
            corner_radius=RADIUS_LG,
        )
        card.pack(fill="x", pady=(0, 12))

        hdr = ctk.CTkLabel(
            card,
            text=f"💡 {title}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["info_text"],
            anchor="w",
        )
        hdr.pack(anchor="w", padx=16, pady=(14, 8))

        for tip in items:
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=16, pady=2)

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

        ctk.CTkLabel(card, text="").pack(pady=8)
        return card

    def troubleshooting_card(self, parent, problem: str, solutions: list) -> ctk.CTkFrame:
        """Create a troubleshooting card."""
        card = ctk.CTkFrame(parent, fg_color="transparent")
        card.pack(fill="x", pady=6)

        lbl = ctk.CTkLabel(
            card,
            text=f"⚠ {problem}",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.colors["warning_text"],
            anchor="w",
        )
        lbl.pack(anchor="w")

        for sol in solutions:
            row = ctk.CTkLabel(
                card,
                text=f"  • {sol}",
                font=ctk.CTkFont(size=12),
                text_color=self.colors["text_secondary"],
                anchor="w",
                wraplength=600,
            )
            row.pack(anchor="w")

    def empty_state_panel(self, parent, icon: str, title: str, description: str,
                          button_text: str = None, button_command = None) -> ctk.CTkFrame:
        """Create a beautiful empty state panel (e.g. for no camera, no midi)."""
        panel = ctk.CTkFrame(
            parent,
            fg_color=self.colors["bg_tertiary"],
            corner_radius=RADIUS_LG,
        )
        # We don't pack it here, let caller do it so they can expand it
        
        inner = ctk.CTkFrame(panel, fg_color="transparent")
        inner.pack(expand=True, pady=40, padx=20)
        
        # Icon circle
        icon_bg = ctk.CTkFrame(
            inner,
            fg_color=self.colors["bg_secondary"],
            corner_radius=RADIUS_FULL,
            width=64,
            height=64,
        )
        icon_bg.pack(pady=(0, 16))
        icon_bg.pack_propagate(False)
        
        lbl_icon = ctk.CTkLabel(
            icon_bg,
            text=icon,
            font=ctk.CTkFont(size=28),
            text_color=self.colors["text_muted"],
        )
        lbl_icon.pack(expand=True)
        
        lbl_title = ctk.CTkLabel(
            inner,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors["text_primary"],
        )
        lbl_title.pack(pady=(0, 8))
        
        lbl_desc = ctk.CTkLabel(
            inner,
            text=description,
            font=ctk.CTkFont(size=13),
            text_color=self.colors["text_secondary"],
            wraplength=400,
            justify="center",
        )
        lbl_desc.pack(pady=(0, 16))
        
        if button_text and button_command:
            self.btn_secondary(inner, text=button_text, command=button_command).pack()
            
        return panel

    # ========================================================================
    # BUTTON COMPONENTS
    # ========================================================================

    def btn_primary(self, parent, text: str, command, width: int = 160,
                    icon: str = None) -> ctk.CTkButton:
        """Create a primary button with accent color."""
        display_text = f"{icon} {text}" if icon else text
        return ctk.CTkButton(
            parent,
            text=display_text,
            command=command,
            width=width,
            height=42,
            corner_radius=RADIUS_MD,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            text_color=self.colors["text_on_accent"],
            font=ctk.CTkFont(size=14, weight="bold"),
            border_width=0,
        )

    def btn_cta(self, parent, text: str, command, width: int = 200,
                icon: str = None) -> ctk.CTkButton:
        """Create a large, prominent Call To Action button."""
        display_text = f"{icon} {text}" if icon else text
        return ctk.CTkButton(
            parent,
            text=display_text,
            command=command,
            width=width,
            height=54,
            corner_radius=RADIUS_LG,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            text_color=self.colors["text_on_accent"],
            font=ctk.CTkFont(size=16, weight="bold"),
            border_width=0,
        )

    def btn_secondary(self, parent, text: str, command, width: int = 140,
                      icon: str = None) -> ctk.CTkButton:
        """Create a secondary button with subtle styling."""
        display_text = f"{icon} {text}" if icon else text
        return ctk.CTkButton(
            parent,
            text=display_text,
            command=command,
            width=width,
            height=42,
            corner_radius=RADIUS_MD,
            fg_color=self.colors["bg_tertiary"],
            hover_color=self.colors["bg_hover"],
            text_color=self.colors["text_primary"],
            font=ctk.CTkFont(size=14),
            border_width=0,
        )

    def btn_success(self, parent, text: str, command, width: int = 160,
                    icon: str = None) -> ctk.CTkButton:
        """Create a success button (green)."""
        display_text = f"{icon} {text}" if icon else text
        return ctk.CTkButton(
            parent,
            text=display_text,
            command=command,
            width=width,
            height=42,
            corner_radius=RADIUS_MD,
            fg_color=self.colors["success"],
            hover_color=adjust_color(self.colors["success"], -15),
            text_color=self.colors["text_on_accent"],
            font=ctk.CTkFont(size=14, weight="bold"),
            border_width=0,
        )

    def btn_warning(self, parent, text: str, command, width: int = 160,
                     icon: str = None) -> ctk.CTkButton:
        """Create a warning button (amber)."""
        display_text = f"{icon} {text}" if icon else text
        return ctk.CTkButton(
            parent,
            text=display_text,
            command=command,
            width=width,
            height=42,
            corner_radius=RADIUS_MD,
            fg_color=self.colors["warning"],
            hover_color=adjust_color(self.colors["warning"], -15),
            text_color=self.colors["text_on_accent"],
            font=ctk.CTkFont(size=14, weight="bold"),
            border_width=0,
        )

    def btn_danger(self, parent, text: str, command, width: int = 140,
                    icon: str = None) -> ctk.CTkButton:
        """Create a danger/warning button (red)."""
        display_text = f"{icon} {text}" if icon else text
        return ctk.CTkButton(
            parent,
            text=display_text,
            command=command,
            width=width,
            height=42,
            corner_radius=RADIUS_MD,
            fg_color=self.colors["error"],
            hover_color=adjust_color(self.colors["error"], -15),
            text_color=self.colors["text_on_accent"],
            font=ctk.CTkFont(size=14, weight="bold"),
            border_width=0,
        )

    def btn_outline(self, parent, text: str, command, width: int = 140,
                    color: str = None) -> ctk.CTkButton:
        """Create an outline button."""
        border_color = color or self.colors["accent"]
        display_text = text
        return ctk.CTkButton(
            parent,
            text=display_text,
            command=command,
            width=width,
            height=42,
            corner_radius=RADIUS_MD,
            fg_color="transparent",
            hover_color=adjust_brightness(border_color, 240),
            text_color=border_color,
            font=ctk.CTkFont(size=14),
            border_width=2,
            border_color=border_color,
        )

    # ========================================================================
    # FORM COMPONENTS
    # ========================================================================

    def section_title(self, parent, text: str) -> ctk.CTkLabel:
        """Create a section title label."""
        return ctk.CTkLabel(
            parent,
            text=text,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["text_primary"],
            anchor="w",
        )

    def label(self, parent, text: str, size: int = 13, color: str = None,
              weight: str = "normal") -> ctk.CTkLabel:
        """Create a generic label."""
        text_color = color or self.colors["text_primary"]
        return ctk.CTkLabel(
            parent,
            text=text,
            font=ctk.CTkFont(size=size, weight=weight),
            text_color=text_color,
        )

    def form_row(self, parent) -> ctk.CTkFrame:
        """Create a horizontal form row."""
        row = ctk.CTkFrame(parent, fg_color="transparent")
        return row

    def info_row(self, parent, label_text: str, value: str, value_color: str = None) -> ctk.CTkFrame:
        """Create an info row with label and value."""
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="x", pady=4)

        lbl = ctk.CTkLabel(
            container,
            text=f"{label_text}:",
            font=ctk.CTkFont(size=13),
            text_color=self.colors["text_secondary"],
            anchor="w",
        )
        lbl.pack(side="left")

        val_color = value_color or self.colors["text_primary"]
        val = ctk.CTkLabel(
            container,
            text=value,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=val_color,
            anchor="w",
            wraplength=400,
        )
        val.pack(side="left", padx=(6, 0))
        return container

    def dropdown(self, parent, values: list, command=None, width: int = 200):
        """Create a styled dropdown/optionmenu."""
        var = ctk.StringVar(value=values[0] if values else "Pilih...")
        dropdown = ctk.CTkOptionMenu(
            parent,
            variable=var,
            values=values,
            command=command,
            width=width,
            height=38,
            corner_radius=RADIUS_MD,
            fg_color=self.colors["bg_tertiary"],
            button_color=self.colors["accent"],
            button_hover_color=self.colors["accent_hover"],
            dropdown_fg_color=self.colors["bg_secondary"],
            dropdown_hover_color=self.colors["bg_hover"],
            text_color=self.colors["text_primary"],
        )
        return dropdown, var

    def switch(self, parent, text: str, variable, command=None) -> ctk.CTkSwitch:
        """Create a styled toggle switch."""
        sw = ctk.CTkSwitch(
            parent,
            text=text,
            variable=variable,
            command=command,
            font=ctk.CTkFont(size=13),
            progress_color=self.colors["accent"],
        )
        return sw

    def slider(self, parent, variable, from_: float, to: float,
               command=None, width: int = 250) -> ctk.CTkSlider:
        """Create a styled slider."""
        slider = ctk.CTkSlider(
            parent,
            variable=variable,
            from_=from_,
            to=to,
            width=width,
            button_color=self.colors["accent"],
            button_hover_color=self.colors["accent_hover"],
            progress_color=self.colors["accent"],
        )
        if command:
            slider.configure(command=command)
        return slider

    def radio(self, parent, text: str, variable, value, command=None) -> ctk.CTkRadioButton:
        """Create a styled radio button."""
        return ctk.CTkRadioButton(
            parent,
            text=text,
            variable=variable,
            value=value,
            command=command,
            border_color=self.colors["accent"],
            fg_color=self.colors["accent"],
            hover_color=adjust_color(self.colors["accent"], -20),
        )

    def radio_card(self, parent, text: str, description: str, variable, value,
                   command=None) -> ctk.CTkFrame:
        """Create a card-style radio button option."""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors["bg_tertiary"],
            border_color=self.colors["border"],
            border_width=1,
            corner_radius=RADIUS_MD,
            cursor="hand2",
            height=52,
        )
        card.pack_propagate(False)

        radio = ctk.CTkRadioButton(
            card,
            text="",
            variable=variable,
            value=value,
            command=command,
            border_color=self.colors["accent"],
            fg_color=self.colors["accent"],
        )
        radio.pack(side="left", padx=14, pady=0)

        txt = ctk.CTkFrame(card, fg_color="transparent")
        txt.pack(side="left", fill="both", pady=8)

        title_lbl = ctk.CTkLabel(
            txt,
            text=text,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["text_primary"],
            anchor="w",
        )
        title_lbl.pack()

        desc_lbl = ctk.CTkLabel(
            txt,
            text=description,
            font=ctk.CTkFont(size=11),
            text_color=self.colors["text_secondary"],
            anchor="w",
            wraplength=250,
        )
        desc_lbl.pack()

        # Hover effects
        def on_enter(e, c=card):
            c.configure(border_color=self.colors["accent"])
        def on_leave(e, c=card):
            c.configure(border_color=self.colors["border"])
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

        return card

    # ========================================================================
    # LAYOUT COMPONENTS
    # ========================================================================

    def divider(self, parent, color: str = None) -> ctk.CTkFrame:
        """Create a horizontal divider."""
        div_color = color or self.colors["border"]
        div = ctk.CTkFrame(parent, fg_color=div_color, height=1)
        return div

    def spacer(self, parent, height: int = 12) -> ctk.CTkFrame:
        """Create a vertical spacer."""
        sp = ctk.CTkFrame(parent, fg_color="transparent", height=height)
        return sp

    def row(self, parent) -> ctk.CTkFrame:
        """Create a horizontal row container."""
        return ctk.CTkFrame(parent, fg_color="transparent")

    def scrollable_frame(self, parent) -> ctk.CTkScrollableFrame:
        """Create a styled scrollable frame."""
        return ctk.CTkScrollableFrame(
            parent,
            fg_color="transparent",
            scrollbar_fg_color=self.colors["bg_tertiary"],
            scrollbar_button_color=self.colors["accent"],
            scrollbar_button_hover_color=self.colors["accent_hover"],
        )

    def canvas(self, parent, width: int = 640, height: int = 480,
               bg: str = None) -> ctk.CTkCanvas:
        """Create a canvas for camera preview."""
        bg_color = bg or self.colors["canvas_bg"]
        return ctk.CTkCanvas(
            parent,
            width=width,
            height=height,
            bg=bg_color,
            highlightthickness=0,
        )

    # ========================================================================
    # MESSAGE BOX HELPERS
    # ========================================================================

    def show_error(self, message: str):
        """Show error message."""
        from tkinter import messagebox
        messagebox.showerror("Error", message)

    def show_info(self, message: str):
        """Show info message."""
        from tkinter import messagebox
        messagebox.showinfo("Info", message)

    def show_warning(self, message: str):
        """Show warning message."""
        from tkinter import messagebox
        messagebox.showwarning("Warning", message)

    def ask_yesno(self, title: str, message: str) -> bool:
        """Ask yes/no question."""
        from tkinter import messagebox
        return messagebox.askyesno(title, message)

    # ========================================================================
    # ANIMATION HELPERS
    # ========================================================================

    def fade_in_widget(self, widget, duration: int = 250):
        """Simple fade-in animation for a widget."""
        alpha = 0.0
        step = 1.0 / (duration / 16)  # ~60fps

        def animate():
            nonlocal alpha
            alpha += step
            if alpha >= 1.0:
                return
            widget.after(16, animate)

        animate()