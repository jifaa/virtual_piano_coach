"""
AI Piano Coach - Configuration Module
Berisi konfigurasi yang persistens antara sesi aplikasi.
"""
import json
import os
from dataclasses import dataclass, asdict
from typing import Optional, List
from app.constants import KEYBOARD_61, KEYBOARD_88, DEFAULT_CONFIG_FILE, CALIBRATION_FILE


@dataclass
class KeyboardConfig:
    """Konfigurasi keyboard (61 atau 88 keys)."""
    size: str = "61"  # "61" atau "88"
    base_midi: int = 36
    total_keys: int = 61
    white_keys: int = 36

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


@dataclass
class CalibrationData:
    """Data kalibrasi keyboard."""
    points: List[List[float]] = None  # 4 points [(x,y), ...]
    keyboard_size: str = "61"
    camera_index: int = 0
    tuts_rects: dict = None  # Pre-computed key rectangles

    def __post_init__(self):
        if self.points is None:
            self.points = []
        if self.tuts_rects is None:
            self.tuts_rects = {}

    def to_dict(self):
        return {
            "points": self.points,
            "keyboard_size": self.keyboard_size,
            "camera_index": self.camera_index,
            "tuts_rects": self.tuts_rects,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            points=data.get("points", []),
            keyboard_size=data.get("keyboard_size", "61"),
            camera_index=data.get("camera_index", 0),
            tuts_rects=data.get("tuts_rects", {}),
        )

    def is_complete(self) -> bool:
        return len(self.points) == 4 and len(self.tuts_rects) > 0


@dataclass
class AppConfig:
    """Konfigurasi utama aplikasi."""
    # Hardware selection
    camera_index: int = 0
    midi_input_name: Optional[str] = None
    midi_file_path: Optional[str] = None

    # Keyboard config
    keyboard_size: str = "61"  # "61" atau "88"

    # UI Settings
    appearance_mode: str = "dark"  # "dark", "light", "system"
    color_theme: str = "blue"  # "blue", "green"

    # Overlay settings
    overlay_opacity: float = 0.8
    show_finger_labels: bool = True
    show_posture_feedback: bool = True
    show_note_numbers: bool = False
    wrong_note_feedback: bool = True
    camera_mirror: bool = False

    # Hand split point (MIDI note for middle C)
    hand_split_note: int = 60  # C4

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        # Filter out unknown fields
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered_data)

    def get_keyboard_config(self) -> KeyboardConfig:
        """Get keyboard configuration based on size."""
        if self.keyboard_size == "88":
            return KeyboardConfig(
                size="88",
                base_midi=KEYBOARD_88["base_midi"],
                total_keys=KEYBOARD_88["total_keys"],
                white_keys=KEYBOARD_88["white_keys"],
            )
        else:
            return KeyboardConfig(
                size="61",
                base_midi=KEYBOARD_61["base_midi"],
                total_keys=KEYBOARD_61["total_keys"],
                white_keys=KEYBOARD_61["white_keys"],
            )


class ConfigManager:
    """Manager untuk menyimpan dan memuat konfigurasi aplikasi."""

    def __init__(self, config_file: str = DEFAULT_CONFIG_FILE):
        self.config_file = config_file
        self.config = AppConfig()
        self.calibration = CalibrationData()

    def load(self):
        """Muat konfigurasi dari file."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.config = AppConfig.from_dict(data.get("app", {}))
                    self.calibration = CalibrationData.from_dict(data.get("calibration", {}))
                print(f"[Config] Loaded from {self.config_file}")
        except Exception as e:
            print(f"[Config] Error loading config: {e}")

    def save(self):
        """Simpan konfigurasi ke file."""
        try:
            data = {
                "app": self.config.to_dict(),
                "calibration": self.calibration.to_dict(),
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"[Config] Saved to {self.config_file}")
        except Exception as e:
            print(f"[Config] Error saving config: {e}")

    def save_calibration(self, calibration: CalibrationData):
        """Simpan data kalibrasi."""
        self.calibration = calibration
        self.save()

    def is_setup_complete(self) -> bool:
        """Cek apakah setup sudah lengkap."""
        return (
            self.config.camera_index >= 0 and
            self.config.midi_input_name is not None
        )

    def is_calibration_complete(self) -> bool:
        """Cek apakah kalibrasi sudah lengkap."""
        return self.calibration.is_complete()