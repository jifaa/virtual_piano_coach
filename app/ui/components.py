"""
AI Piano Coach - Premium UI Components
Reusable animated UI components with modern styling.
"""
import customtkinter as ctk
import math
from app.design_system import (
    get_premium_colors,
    adjust_color,
    adjust_brightness,
    ANIMATION_FAST,
    ANIMATION_NORMAL,
    RADIUS_SM,
    RADIUS_MD,
    RADIUS_LG,
)


class PremiumButton(ctk.CTkButton):
    """
    Premium button with hover glow animation and modern styling.
    """

    def __init__(
        self,
        parent,
        text: str = "",
        command=None,
        width: int = 200,
        height: int = 44,
        corner_radius: int = RADIUS_MD,
        font_size: int = 14,
        font_weight: str = "bold",
        fg_color: str = None,
        hover_color: str = None,
        text_color: str = None,
        icon: str = None,
        is_primary: bool = True,
        **kwargs
    ):
        colors = get_premium_colors()

        # Set colors based on primary/secondary style
        if is_primary:
            self.base_fg = fg_color or colors["accent"]
            self.base_hover = hover_color or adjust_brightness(self.base_fg, -20)
            self.base_text = text_color or "white"
        else:
            self.base_fg = fg_color or colors["bg_tertiary"]
            self.base_hover = hover_color or adjust_brightness(self.base_fg, 15)
            self.base_text = text_color or colors["text_primary"]

        # Add icon to text if provided
        if icon:
            text = f"{icon}  {text}"

        super().__init__(
            parent,
            text=text,
            command=command,
            width=width,
            height=height,
            corner_radius=corner_radius,
            fg_color=self.base_fg,
            hover_color=self.base_hover,
            text_color=self.base_text,
            font=ctk.CTkFont(size=font_size, weight=font_weight),
            border_width=0,
            **kwargs
        )

        # Animation state
        self._glow_id = None
        self._hover_animation_running = False

    def bind_hover_animations(self):
        """Bind hover enter/leave events for glow animation."""
        self.bind("<Enter>", self._on_hover_enter)
        self.bind("<Leave>", self._on_hover_leave)

    def _on_hover_enter(self, event=None):
        """Handle mouse enter - start glow animation."""
        if self._glow_id:
            self.after_cancel(self._glow_id)
        self._animate_glow(0, 1)  # Fade in glow

    def _on_hover_leave(self, event=None):
        """Handle mouse leave - stop glow animation."""
        self._hover_animation_running = False
        self.configure(border_width=0)

    def _animate_glow(self, current: float, direction: int):
        """Animate the glow effect."""
        if not self._hover_animation_running:
            return

        new_value = current + (0.05 * direction)
        new_value = max(0, min(1, new_value))

        # Apply subtle border glow
        if new_value > 0.3:
            glow_color = adjust_brightness(self.base_fg, int(new_value * 30))
            self.configure(
                border_color=glow_color,
                border_width=1 if new_value > 0.5 else 0
            )

        if direction == 1 and new_value < 1:
            self._glow_id = self.after(20, lambda: self._animate_glow(new_value, direction))
        elif direction == -1 and new_value > 0:
            self._glow_id = self.after(15, lambda: self._animate_glow(new_value, direction))
        else:
            self._glow_id = None

    def set_primary_style(self):
        """Set this button as primary (accent color)."""
        colors = get_premium_colors()
        self.configure(
            fg_color=colors["accent"],
            hover_color=adjust_brightness(colors["accent"], -20),
            text_color="white"
        )

    def set_success_style(self):
        """Set this button as success (green)."""
        colors = get_premium_colors()
        self.configure(
            fg_color=colors["success"],
            hover_color=adjust_brightness(colors["success"], -20),
            text_color="white"
        )

    def set_warning_style(self):
        """Set this button as warning (orange)."""
        colors = get_premium_colors()
        self.configure(
            fg_color=colors["warning"],
            hover_color=adjust_brightness(colors["warning"], -20),
            text_color="white"
        )

    def set_error_style(self):
        """Set this button as error (red)."""
        colors = get_premium_colors()
        self.configure(
            fg_color=colors["error"],
            hover_color=adjust_brightness(colors["error"], -20),
            text_color="white"
        )

    def set_secondary_style(self):
        """Set this button as secondary (muted)."""
        colors = get_premium_colors()
        self.configure(
            fg_color=colors["bg_tertiary"],
            hover_color=adjust_brightness(colors["bg_tertiary"], 15),
            text_color=colors["text_primary"]
        )


class PremiumCard(ctk.CTkFrame):
    """
    Premium card with subtle border and hover animation.
    """

    def __init__(
        self,
        parent,
        title: str = None,
        subtitle: str = None,
        corner_radius: int = RADIUS_LG,
        padding: int = 20,
        is_focusable: bool = False,
        **kwargs
    ):
        colors = get_premium_colors()

        super().__init__(
            parent,
            fg_color=colors["bg_secondary"],
            border_color=colors["border"],
            border_width=1,
            corner_radius=corner_radius,
            **kwargs
        )

        self.colors = colors
        self.padding = padding
        self.is_focusable = is_focusable

        # Store for animation
        self._hover_animation_id = None

        if title or subtitle:
            self._create_header(title, subtitle)

        if is_focusable:
            self.bind("<Enter>", self._on_hover_enter)
            self.bind("<Leave>", self._on_hover_leave)

    def _create_header(self, title: str, subtitle: str):
        """Create card header with title and optional subtitle."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=self.padding, pady=(self.padding, 8))

        if title:
            self.title_label = ctk.CTkLabel(
                header_frame,
                text=title,
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=self.colors["text_primary"],
                anchor="w",
            )
            self.title_label.pack(anchor="w")

        if subtitle:
            self.subtitle_label = ctk.CTkLabel(
                header_frame,
                text=subtitle,
                font=ctk.CTkFont(size=12),
                text_color=self.colors["text_secondary"],
                anchor="w",
            )
            self.subtitle_label.pack(anchor="w", pady=(2, 0) if title else (0, 0))

    def _on_hover_enter(self, event=None):
        """Handle hover enter."""
        self._animate_border(0, 1)

    def _on_hover_leave(self, event=None):
        """Handle hover leave."""
        self._animate_border(1, -1)

    def _animate_border(self, current: float, direction: int):
        """Animate border color on hover."""
        new_value = current + (0.1 * direction)
        new_value = max(0, min(1, new_value))

        # Interpolate border color
        if new_value > 0.5:
            border_color = adjust_brightness(self.colors["border"], int(new_value * 30))
        else:
            border_color = self.colors["border"]

        self.configure(border_color=border_color)

        if direction == 1 and new_value < 1:
            self._hover_animation_id = self.after(30, lambda: self._animate_border(new_value, direction))
        elif direction == -1 and new_value > 0:
            self._hover_animation_id = self.after(20, lambda: self._animate_border(new_value, direction))
        else:
            self._hover_animation_id = None

    def add_content(self, content_frame):
        """Add a content frame to the card."""
        content_frame.pack(fill="both", expand=True, padx=self.padding, pady=(0, self.padding))


class StatusBadge(ctk.CTkFrame):
    """
    Status badge with animated pulse effect.
    """

    def __init__(
        self,
        parent,
        text: str = "",
        status: str = "info",  # "success", "warning", "error", "info"
        show_icon: bool = True,
        animated: bool = True,
        **kwargs
    ):
        colors = get_premium_colors()

        status_colors = {
            "success": (colors["success"], colors["success_glow"]),
            "warning": (colors["warning"], colors["warning_glow"]),
            "error": (colors["error"], colors["error_glow"]),
            "info": (colors["accent"], colors["accent_glow"]),
        }

        self.status_color, self.glow_color = status_colors.get(status, status_colors["info"])

        # Icon mapping (text-based, no emoji)
        icons = {
            "success": "OK",
            "warning": "!",
            "error": "X",
            "info": "i",
        }
        icon = icons.get(status, "i") if show_icon else ""
        display_text = f"{icon}  {text}" if icon else text

        glow_bg = self.glow_color

        super().__init__(
            parent,
            fg_color=glow_bg,
            corner_radius=RADIUS_SM,
            **kwargs
        )

        self.label = ctk.CTkLabel(
            self,
            text=display_text,
            text_color=self.status_color,
            font=ctk.CTkFont(size=11, weight="bold"),
        )
        self.label.pack(padx=10, pady=4)

        # Start pulse animation if animated
        if animated:
            self._start_pulse()

    def _start_pulse(self):
        """Start subtle pulse animation."""
        self._pulse_phase = 0

        def animate():
            self._pulse_phase = (self._pulse_phase + 0.05) % (2 * math.pi)
            # Very subtle opacity change
            alpha = int(abs(math.sin(self._pulse_phase)) * 30)
            bg = adjust_brightness(self.glow_color, -200) if alpha < 15 else self.glow_color
            self.configure(fg_color=bg)
            self.after(100, animate)

        animate()

    def set_status(self, status: str, text: str = None):
        """Update the status and optionally the text."""
        colors = get_premium_colors()

        status_colors = {
            "success": (colors["success"], colors["success_glow"]),
            "warning": (colors["warning"], colors["warning_glow"]),
            "error": (colors["error"], colors["error_glow"]),
            "info": (colors["accent"], colors["accent_glow"]),
        }

        self.status_color, self.glow_color = status_colors.get(status, status_colors["info"])
        self.label.configure(text_color=self.status_color)
        self.configure(fg_color=self.glow_color)


class ProgressIndicator(ctk.CTkFrame):
    """
    Multi-step progress indicator with animated current step.
    """

    def __init__(
        self,
        parent,
        steps: list,
        current_step: int = 0,
        **kwargs
    ):
        colors = get_premium_colors()

        super().__init__(
            parent,
            fg_color="transparent",
            **kwargs
        )

        self.colors = colors
        self.steps = steps
        self.current_step = current_step
        self.step_widgets = []

        self._create_steps()

    def _create_steps(self):
        """Create step indicators."""
        for i, step in enumerate(self.steps):
            # Step container
            step_frame = ctk.CTkFrame(self, fg_color="transparent")
            step_frame.pack(side="left")

            # Step circle
            circle_size = 32
            circle = ctk.CTkFrame(
                step_frame,
                width=circle_size,
                height=circle_size,
                corner_radius=circle_size // 2,
                fg_color=self._get_step_color(i),
            )
            circle.pack()
            circle.pack_propagate(False)

            # Step number
            step_label = ctk.CTkLabel(
                circle,
                text=str(i + 1),
                text_color="white",
                font=ctk.CTkFont(size=12, weight="bold"),
            )
            step_label.pack(expand=True)

            # Step label
            label = ctk.CTkLabel(
                step_frame,
                text=step,
                text_color=self.colors["text_secondary"] if i != self.current_step else self.colors["text_primary"],
                font=ctk.CTkFont(size=10),
            )
            label.pack(pady=(4, 0))

            self.step_widgets.append((circle, label))

            # Connector line (except for last step)
            if i < len(self.steps) - 1:
                connector = ctk.CTkFrame(
                    step_frame,
                    height=2,
                    width=40,
                    fg_color=self.colors["border"] if i < self.current_step else self.colors["bg_tertiary"],
                )
                connector.pack(side="left", padx=(8, 8), pady=(15, 0))

        # Animate current step
        self._animate_current_step()

    def _get_step_color(self, index: int) -> str:
        """Get color for step based on state."""
        if index < self.current_step:
            return self.colors["success"]
        elif index == self.current_step:
            return self.colors["accent"]
        else:
            return self.colors["bg_tertiary"]

    def _animate_current_step(self):
        """Animate the current step indicator."""
        if self.step_widgets and self.current_step < len(self.step_widgets):
            circle, _ = self.step_widgets[self.current_step]
            # Subtle scale animation would go here in a more advanced implementation

    def set_step(self, step: int):
        """Set the current step."""
        self.current_step = step
        for i, (circle, label) in enumerate(self.step_widgets):
            circle.configure(fg_color=self._get_step_color(i))
            label.configure(
                text_color=self.colors["text_secondary"] if i != step else self.colors["text_primary"]
            )
        self._animate_current_step()


class AnimatedSection(ctk.CTkFrame):
    """
    Section container with fade-in animation.
    """

    def __init__(
        self,
        parent,
        title: str = None,
        icon: str = None,
        corner_radius: int = RADIUS_LG,
        **kwargs
    ):
        colors = get_premium_colors()

        super().__init__(
            parent,
            fg_color=colors["bg_secondary"],
            border_color=colors["border"],
            border_width=1,
            corner_radius=corner_radius,
            **kwargs
        )

        self.colors = colors

        # Animation state
        self._animation_progress = 0
        self._animation_running = False

        if title:
            self._create_header(title, icon)

    def _create_header(self, title: str, icon: str = None):
        """Create section header."""
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(18, 10))

        if icon:
            icon_label = ctk.CTkLabel(
                header,
                text=icon,
                text_color=self.colors["accent"],
                font=ctk.CTkFont(size=16),
            )
            icon_label.pack(side="left", padx=(0, 10))

        title_label = ctk.CTkLabel(
            header,
            text=title,
            text_color=self.colors["text_primary"],
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w",
        )
        title_label.pack(side="left")

    def fade_in(self, duration: int = ANIMATION_NORMAL):
        """Start fade-in animation."""
        self._animation_running = True
        self._fade_animation(0, duration)

    def _fade_animation(self, current: int, duration: int):
        """Run fade animation."""
        if not self._animation_running or current >= duration:
            self._animation_running = False
            return

        # Alpha could be managed via opacity in a more advanced implementation
        self._animation_progress = current / duration

        # Schedule next frame
        frame_time = 16  # ~60 FPS
        self.after(frame_time, lambda: self._fade_animation(current + frame_time, duration))


class InfoPanel(ctk.CTkFrame):
    """
    Terminal-style info panel for diagnostics page.
    """

    def __init__(
        self,
        parent,
        title: str = None,
        monospace: bool = True,
        **kwargs
    ):
        colors = get_premium_colors()

        super().__init__(
            parent,
            fg_color="#1E293B",  # Dark slate for contrast even in light theme
            border_color=colors["border"],
            border_width=1,
            corner_radius=RADIUS_MD,
            **kwargs
        )

        self.colors = colors

        if title:
            title_frame = ctk.CTkFrame(self, fg_color=colors["bg_tertiary"])
            title_frame.pack(fill="x")
            title_frame.configure(height=32)

            title_label = ctk.CTkLabel(
                title_frame,
                text=title,
                text_color=colors["text_secondary"],
                font=ctk.CTkFont(size=11, weight="bold"),
                anchor="w",
            )
            title_label.pack(side="left", padx=12, pady=6)

        # Content area
        self.content_label = ctk.CTkLabel(
            self,
            text="",
            text_color=colors["text_primary"],
            font=ctk.CTkFont(size=12, family="Consolas" if monospace else "Inter"),
            justify="left",
            anchor="nw",
        )
        self.content_label.pack(fill="both", expand=True, padx=15, pady=12)

    def set_content(self, text: str):
        """Set the panel content."""
        self.content_label.configure(text=text)

    def update_line(self, key: str, value: str):
        """Update or append a line to the content."""
        current = self.content_label.cget("text")
        lines = current.split("\n") if current else []

        # Try to update existing key
        updated = False
        for i, line in enumerate(lines):
            if line.startswith(f"{key}:") or line.startswith(f"{key} "):
                lines[i] = f"{key}: {value}"
                updated = True
                break

        if not updated:
            lines.append(f"{key}: {value}")

        self.content_label.configure(text="\n".join(lines))


class MetricCard(ctk.CTkFrame):
    """
    Metric display card with icon and animated value.
    """

    def __init__(
        self,
        parent,
        title: str,
        value: str,
        icon: str = None,
        status: str = "info",
        **kwargs
    ):
        colors = get_premium_colors()

        super().__init__(
            parent,
            fg_color=colors["bg_secondary"],
            border_color=colors["border"],
            border_width=1,
            corner_radius=RADIUS_LG,
            **kwargs
        )

        self.colors = colors

        status_colors = {
            "success": colors["success"],
            "warning": colors["warning"],
            "error": colors["error"],
            "info": colors["accent"],
        }

        self.status_color = status_colors.get(status, colors["accent"])

        # Icon and title row
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=18, pady=(16, 6))

        if icon:
            icon_label = ctk.CTkLabel(
                header,
                text=icon,
                text_color=self.status_color,
                font=ctk.CTkFont(size=20),
            )
            icon_label.pack(side="left", padx=(0, 10))

        title_label = ctk.CTkLabel(
            header,
            text=title,
            text_color=colors["text_secondary"],
            font=ctk.CTkFont(size=11, weight="bold"),
            anchor="w",
        )
        title_label.pack(side="left")

        # Value
        self.value_label = ctk.CTkLabel(
            self,
            text=value,
            text_color=self.status_color,
            font=ctk.CTkFont(size=22, weight="bold"),
            anchor="w",
        )
        self.value_label.pack(fill="x", padx=18, pady=(0, 14))

    def update_value(self, value: str, status: str = None):
        """Update the displayed value and optionally the status color."""
        self.value_label.configure(text=value)

        if status:
            colors = get_premium_colors()
            status_colors = {
                "success": colors["success"],
                "warning": colors["warning"],
                "error": colors["error"],
                "info": colors["accent"],
            }
            self.status_color = status_colors.get(status, colors["accent"])
            self.value_label.configure(text_color=self.status_color)


def create_premium_scrollable_frame(parent, **kwargs):
    """Create a premium styled scrollable frame."""
    colors = get_premium_colors()

    scrollable = ctk.CTkScrollableFrame(
        parent,
        fg_color="transparent",
        scrollbar_fg_color=colors["bg_tertiary"],
        scrollbar_button_color=colors["accent"],
        scrollbar_button_hover_color=adjust_brightness(colors["accent"], -20),
        **kwargs
    )

    return scrollable


def create_premium_dropdown(parent, values: list, command=None, width: int = 200, **kwargs):
    """Create a premium styled dropdown."""
    colors = get_premium_colors()

    dropdown = ctk.CTkOptionMenu(
        parent,
        values=values,
        command=command,
        width=width,
        height=36,
        corner_radius=RADIUS_MD,
        fg_color=colors["bg_tertiary"],
        button_color=colors["accent"],
        button_hover_color=adjust_brightness(colors["accent"], -20),
        dropdown_fg_color=colors["bg_secondary"],
        dropdown_hover_color=colors["bg_hover"],
        dropdown_text_color=colors["text_primary"],
        text_color=colors["text_primary"],
        **kwargs
    )

    return dropdown