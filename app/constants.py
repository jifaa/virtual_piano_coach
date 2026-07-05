"""
AI Piano Coach - Constants Module
Berisi konstanta-konstanta yang digunakan di seluruh aplikasi.
"""
from dataclasses import dataclass

# ==========================================
# KONFIGURASI MIDI KEYBOARD
# ==========================================

# 61-Key Mode (Roland E-X10 style)
KEYBOARD_61 = {
    "name": "61 Keys",
    "total_keys": 61,
    "base_midi": 36,  # C2
    "lowest_note": "C2",
    "white_keys": 36,
}

# 88-Key Mode (Full piano)
KEYBOARD_88 = {
    "name": "88 Keys",
    "total_keys": 88,
    "base_midi": 21,  # A0
    "lowest_note": "A0",
    "white_keys": 52,
}

# Black key detection using MIDI pitch class
BLACK_PITCH_CLASSES = {1, 3, 6, 8, 10}

MEDIAPIPE_CONFIG = {
    "model_complexity": 1,
    "min_detection_confidence": 0.5,
    "min_tracking_confidence": 0.5,
    "max_num_hands": 2,
}


FINGER_NAMES = {
    4: "Jp",   # Jempol / Thumb
    8: "Tl",   # Telunjuk / Index
    12: "Tg",  # Tengah / Middle
    16: "Mn",  # Manis / Ring
    20: "Kl",  # Kelingking / Pinky
}

# Left hand fingers
LEFT_HAND_FINGERS = {4, 8, 12, 16, 20}
# Right hand fingers
RIGHT_HAND_FINGERS = {4, 8, 12, 16, 20}

POSTURE_THRESHOLDS = {
    "stiff_angle": 172,      # Finger too straight (warning)
    "bent_angle": 90,        # Finger too bent (warning)
    "octave_span": 0.16,     # Thumb to pinky distance for octave reach
}


UI_COLORS = {
    "dark": {
        "bg_primary": "#1a1a1a",
        "bg_secondary": "#2d2d2d",
        "bg_tertiary": "#3d3d3d",
        "text_primary": "#ffffff",
        "text_secondary": "#a0a0a0",
        "accent": "#3B82F6",
        "success": "#22c55e",
        "warning": "#f59e0b",
        "error": "#ef4444",
        "border": "#404040",
    },
    "light": {
        "bg_primary": "#f5f5f5",
        "bg_secondary": "#ffffff",
        "bg_tertiary": "#e5e5e5",
        "text_primary": "#1a1a1a",
        "text_secondary": "#666666",
        "accent": "#3B82F6",
        "success": "#22c55e",
        "warning": "#f59e0b",
        "error": "#ef4444",
        "border": "#d4d4d4",
    }
}

# Window dimensions
WINDOW_MIN_WIDTH = 1200
WINDOW_MIN_HEIGHT = 700
WINDOW_DEFAULT_WIDTH = 1400
WINDOW_DEFAULT_HEIGHT = 820
SIDEBAR_WIDTH = 260

# ==========================================
# FILE PATHS
# ==========================================

DEFAULT_CONFIG_FILE = "config.json"
CALIBRATION_FILE = "calibration.json"

# ==========================================
# CAMERA SETTINGS
# ==========================================

CAMERA_MAX_INDEX = 5
CAMERA_DEFAULT_INDEX = 0

# ==========================================
# NOTE COLORS (BGR format for OpenCV)
# ==========================================

NOTE_COLORS = {
    "idle_white": (255, 0, 0),        # Blue outline for white keys
    "idle_black": (100, 100, 100),     # Gray for black keys
    "pressed": (0, 255, 0),            # Green when pressed
    "correct": (0, 255, 0),            # Green for correct note
    "wrong": (0, 0, 255),              # Red for wrong note
    "target_left": (255, 255, 0),      # Cyan/Yellow for left hand target
    "target_right": (0, 255, 255),     # Yellow for right hand target
    "calibration_point": (0, 255, 255),# Yellow for calibration points
}

# Middle C = MIDI note 60
MIDDLE_C = 60
