"""
AI Piano Coach - Design System Module
Premium modern light theme with professional styling.
Clean, fresh, and polished visual design.
"""
import math

# =============================================================================
# PREMIUM LIGHT THEME COLOR PALETTE
# =============================================================================

# --- Backgrounds ---
BG_PRIMARY = "#F7FAFF"        # Main page background - very light cool blue
BG_SECONDARY = "#FFFFFF"       # Card/surface background - pure white
BG_TERTIARY = "#EEF5FF"        # Elevated/section background - soft panel blue
BG_HOVER = "#E2EAF8"           # Hover state background
BG_ACTIVE = "#D6E0F4"          # Active/pressed state
BG_SIDEBAR = "#FFFFFF"         # Sidebar background - white
BG_CARDS = "#FFFFFF"           # Explicit card background

# --- Accent Colors ---
ACCENT_PRIMARY = "#4A5CF5"     # Premium confident indigo
ACCENT_SECONDARY = "#06B6D4"   # Vibrant cyan - secondary
ACCENT_LIGHT = "#EEF2FF"       # Very light indigo tint
ACCENT_HOVER = "#3730A3"       # Darker indigo for hover
ACCENT_SUBTLE = "#A5B4FC"      # Subtle accent for icons

# --- Text Colors ---
TEXT_PRIMARY = "#0F172A"       # Very dark slate - primary text
TEXT_SECONDARY = "#475569"     # Medium slate - secondary text
TEXT_MUTED = "#94A3B8"         # Light slate - tertiary/hint text
TEXT_ON_ACCENT = "#FFFFFF"     # Text on accent color
TEXT_DISABLED = "#CBD5E1"      # Disabled state

# --- Status Colors ---
SUCCESS = "#10B981"            # Emerald green - success
SUCCESS_LIGHT = "#D1FAE5"      # Light green background
SUCCESS_TEXT = "#065F46"       # Dark green text
SUCCESS_BORDER = "#A7F3D0"     # Green border

WARNING = "#F59E0B"           # Amber/orange - warning
WARNING_LIGHT = "#FEF3C7"      # Light amber background
WARNING_TEXT = "#92400E"       # Dark amber text
WARNING_BORDER = "#FDE68A"     # Amber border

ERROR = "#EF4444"             # Red - error
ERROR_LIGHT = "#FEE2E2"       # Light red background
ERROR_TEXT = "#991B1B"        # Dark red text
ERROR_BORDER = "#FECACA"      # Red border

INFO = "#4A5CF5"              # Indigo - info
INFO_LIGHT = "#E0E7FF"        # Light indigo background
INFO_TEXT = "#3730A3"         # Dark indigo text
INFO_BORDER = "#C7D2FE"       # Indigo border

# --- Border & Surface ---
BORDER = "#E2E8F0"            # Default border color
BORDER_HOVER = "#CBD5E1"      # Hover border
BORDER_ACTIVE = "#94A3B8"      # Active border
BORDER_FOCUS = "#4A5CF5"      # Focus ring

# --- Shadows & Depth ---
SHADOW_LIGHT = "#F1F5F9"      # Subtle shadow
SHADOW_MEDIUM = "#E2E8F0"     # Medium shadow
SHADOW_HEAVY = "#CBD5E1"      # Strong shadow

# --- Sidebar ---
SIDEBAR_BG = "#FFFFFF"
SIDEBAR_TEXT = "#64748B"
SIDEBAR_TEXT_ACTIVE = "#FFFFFF"
SIDEBAR_HOVER = "#F1F5F9"
SIDEBAR_ACTIVE_BG = "#4F46E5"

# --- Navigation ---
NAV_ITEM_HOVER = "#F1F5F9"
NAV_ITEM_ACTIVE_BG = "#EEF2FF"
NAV_ITEM_ACTIVE_TEXT = "#4F46E5"

# --- Piano Overlay (on camera) ---
KEY_WHITE = "#F8FAFC"
KEY_BLACK = "#334155"
KEY_PRESSED = "#059669"
KEY_TARGET = "#2563EB"
KEY_TARGET_RIGHT = "#D97706"
KEY_WRONG = "#DC2626"
KEY_PRESSED_OPACITY = 0.9

# --- Canvas ---
CANVAS_BG = "#F8FAFC"

# =============================================================================
# TYPOGRAPHY SYSTEM
# =============================================================================

FONT_FAMILY = "Segoe UI"
FONT_MONO = "Consolas"

FONT_SIZE_2XL = 28
FONT_SIZE_XL = 22
FONT_SIZE_LG = 18
FONT_SIZE_MD = 16
FONT_SIZE_BASE = 14
FONT_SIZE_SM = 13
FONT_SIZE_XS = 11

FONT_WEIGHT_BOLD = "bold"
FONT_WEIGHT_NORMAL = "normal"
FONT_WEIGHT_MEDIUM = "medium"

# =============================================================================
# SPACING SYSTEM
# =============================================================================

SPACING_XS = 4
SPACING_SM = 8
SPACING_MD = 12
SPACING_LG = 16
SPACING_XL = 20
SPACING_2XL = 24
SPACING_3XL = 32
SPACING_4XL = 40

# =============================================================================
# BORDER RADIUS
# =============================================================================

RADIUS_XS = 4
RADIUS_SM = 6
RADIUS_MD = 10
RADIUS_LG = 14
RADIUS_XL = 18
RADIUS_2XL = 24
RADIUS_FULL = 9999

# =============================================================================
# ANIMATION CONSTANTS
# =============================================================================

ANIMATION_FAST = 150
ANIMATION_NORMAL = 250
ANIMATION_SLOW = 400

# =============================================================================
# DESIGN TOKENS
# =============================================================================

SIDEBAR_WIDTH = 260
HEADER_HEIGHT = 72

WINDOW_MIN_WIDTH = 1200
WINDOW_MIN_HEIGHT = 700
WINDOW_DEFAULT_WIDTH = 1400
WINDOW_DEFAULT_HEIGHT = 820

# Layout tokens
STATUS_CARD_MIN_HEIGHT = 100
ACTION_CARD_MIN_WIDTH = 180
CONTENT_MAX_WIDTH = 1200
SECTION_GAP = 20
CARD_GAP = 16
CARD_PADDING = 20

# =============================================================================
# PREMIUM COLOR GETTERS
# =============================================================================

def get_light_colors():
    """Returns the complete light theme color palette as a dictionary."""
    return {
        # Backgrounds
        "bg_primary": BG_PRIMARY,
        "bg_secondary": BG_SECONDARY,
        "bg_tertiary": BG_TERTIARY,
        "bg_hover": BG_HOVER,
        "bg_active": BG_ACTIVE,
        "bg_sidebar": BG_SIDEBAR,
        "bg_cards": BG_CARDS,

        # Accents
        "accent": ACCENT_PRIMARY,
        "accent_secondary": ACCENT_SECONDARY,
        "accent_light": ACCENT_LIGHT,
        "accent_hover": ACCENT_HOVER,
        "accent_subtle": ACCENT_SUBTLE,

        # Text
        "text_primary": TEXT_PRIMARY,
        "text_secondary": TEXT_SECONDARY,
        "text_muted": TEXT_MUTED,
        "text_on_accent": TEXT_ON_ACCENT,
        "text_disabled": TEXT_DISABLED,

        # Success
        "success": SUCCESS,
        "success_light": SUCCESS_LIGHT,
        "success_text": SUCCESS_TEXT,
        "success_border": SUCCESS_BORDER,

        # Warning
        "warning": WARNING,
        "warning_light": WARNING_LIGHT,
        "warning_text": WARNING_TEXT,
        "warning_border": WARNING_BORDER,

        # Error
        "error": ERROR,
        "error_light": ERROR_LIGHT,
        "error_text": ERROR_TEXT,
        "error_border": ERROR_BORDER,

        # Info
        "info": INFO,
        "info_light": INFO_LIGHT,
        "info_text": INFO_TEXT,
        "info_border": INFO_BORDER,

        # Borders
        "border": BORDER,
        "border_hover": BORDER_HOVER,
        "border_active": BORDER_ACTIVE,
        "border_focus": BORDER_FOCUS,

        # Shadows
        "shadow_light": SHADOW_LIGHT,
        "shadow_medium": SHADOW_MEDIUM,
        "shadow_heavy": SHADOW_HEAVY,

        # Sidebar
        "sidebar_bg": SIDEBAR_BG,
        "sidebar_text": SIDEBAR_TEXT,
        "sidebar_text_active": SIDEBAR_TEXT_ACTIVE,
        "sidebar_hover": SIDEBAR_HOVER,
        "sidebar_active_bg": SIDEBAR_ACTIVE_BG,

        # Nav
        "nav_hover": NAV_ITEM_HOVER,
        "nav_active_bg": NAV_ITEM_ACTIVE_BG,
        "nav_active_text": NAV_ITEM_ACTIVE_TEXT,

        # Piano keys
        "key_white": KEY_WHITE,
        "key_black": KEY_BLACK,
        "key_pressed": KEY_PRESSED,
        "key_target": KEY_TARGET,
        "key_target_right": KEY_TARGET_RIGHT,
        "key_wrong": KEY_WRONG,

        # Canvas
        "canvas_bg": CANVAS_BG,
    }

def get_premium_colors():
    """Alias for get_light_colors() - premium theme."""
    return get_light_colors()


def get_dark_colors():
    """Returns the dark theme color palette."""
    return {
        "bg_primary": "#0F172A",
        "bg_secondary": "#1E293B",
        "bg_tertiary": "#334155",
        "bg_hover": "#475569",
        "bg_active": "#64748B",
        "bg_sidebar": "#1E293B",
        "bg_cards": "#1E293B",
        "accent": "#6366F1",
        "accent_secondary": "#818CF8",
        "accent_light": "#312E81",
        "accent_hover": "#4F46E5",
        "accent_subtle": "#A5B4FC",
        "text_primary": "#F8FAFC",
        "text_secondary": "#CBD5E1",
        "text_muted": "#94A3B8",
        "text_on_accent": "#FFFFFF",
        "text_disabled": "#64748B",
        "success": "#10B981",
        "success_light": "#065F46",
        "success_text": "#34D399",
        "success_border": "#065F46",
        "warning": "#F59E0B",
        "warning_light": "#92400E",
        "warning_text": "#FBBF24",
        "warning_border": "#92400E",
        "error": "#EF4444",
        "error_light": "#991B1B",
        "error_text": "#F87171",
        "error_border": "#991B1B",
        "info": "#3B82F6",
        "info_light": "#1E40AF",
        "info_text": "#60A5FA",
        "info_border": "#1E40AF",
        "border": "#334155",
        "border_hover": "#475569",
        "border_active": "#64748B",
        "border_focus": "#6366F1",
        "shadow_light": "#1E293B",
        "shadow_medium": "#334155",
        "shadow_heavy": "#475569",
        "sidebar_bg": "#1E293B",
        "sidebar_text": "#94A3B8",
        "sidebar_text_active": "#FFFFFF",
        "sidebar_hover": "#334155",
        "sidebar_active_bg": "#6366F1",
        "nav_hover": "#334155",
        "nav_active_bg": "#312E81",
        "nav_active_text": "#818CF8",
        "key_white": "#E2E8F0",
        "key_black": "#1E293B",
        "key_pressed": "#10B981",
        "key_target": "#3B82F6",
        "key_target_right": "#F59E0B",
        "key_wrong": "#EF4444",
        "canvas_bg": "#0F172A",
    }

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def adjust_color(hex_color: str, amount: int) -> str:
    """Adjust hex color brightness by adding/subtracting from RGB channels."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        return hex_color
    try:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        r = max(0, min(255, r + amount))
        g = max(0, min(255, g + amount))
        b = max(0, min(255, b + amount))
        return f"#{r:02x}{g:02x}{b:02x}"
    except Exception:
        return hex_color


def adjust_brightness(hex_color: str, amount: int) -> str:
    """Alias for adjust_color - adjusts hex color brightness."""
    return adjust_color(hex_color, amount)


def interpolate_color(color1: str, color2: str, factor: float) -> str:
    """Interpolate between two hex colors. Factor 0 = color1, 1 = color2."""
    c1 = color1.lstrip('#')
    c2 = color2.lstrip('#')
    if len(c1) != 6 or len(c2) != 6:
        return color1
    try:
        r1, g1, b1 = int(c1[0:2], 16), int(c1[2:4], 16), int(c1[4:6], 16)
        r2, g2, b2 = int(c2[0:2], 16), int(c2[2:4], 16), int(c2[4:6], 16)
        r = int(r1 + (r2 - r1) * factor)
        g = int(g1 + (g2 - g1) * factor)
        b = int(b1 + (b2 - b1) * factor)
        return f"#{r:02x}{g:02x}{b:02x}"
    except Exception:
        return color1


def darken_color(hex_color: str, percent: float = 0.1) -> str:
    """Darken a hex color by a percentage."""
    return adjust_color(hex_color, int(-255 * percent))


def lighten_color(hex_color: str, percent: float = 0.1) -> str:
    """Lighten a hex color by a percentage."""
    return adjust_color(hex_color, int(255 * percent))


def hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        return (0, 0, 0)
    try:
        return (int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16))
    except Exception:
        return (0, 0, 0)


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB tuple to hex color."""
    return f"#{r:02x}{g:02x}{b:02x}"