"""
AI Piano Coach - Runtime State Module
Berisi state yang berubah selama aplikasi berjalan.
"""
from dataclasses import dataclass, field
from typing import Set, Optional, List, Tuple, Dict
import threading


@dataclass
class CameraState:
    """State kamera."""
    is_opened: bool = False
    current_frame: Optional[object] = None  # OpenCV frame
    fps: float = 0.0
    error_message: Optional[str] = None


@dataclass
class MidiState:
    """State MIDI input."""
    is_connected: bool = False
    port_name: Optional[str] = None
    active_notes: Set[int] = field(default_factory=set)  # Currently pressed notes
    error_message: Optional[str] = None


@dataclass
class HandLandmark:
    """Data landmark satu jari."""
    x: float
    y: float
    hand: str  # "L" atau "R"
    finger: str  # "Jp", "Tl", "Tg", "Mn", "Kl"


@dataclass
class PostureInfo:
    """Informasi postur tangan."""
    hand: str  # "L" atau "R"
    status: str  # "good", "stiff", "bent", "octave_ok"
    message: str
    angle: float
    span: float


@dataclass
class HandTrackingState:
    """State tracking tangan."""
    is_detecting: bool = False
    landmarks: List[HandLandmark] = field(default_factory=list)
    postures: List[PostureInfo] = field(default_factory=list)
    hands_detected: int = 0


@dataclass
class PracticeState:
    """State mode latihan."""
    is_running: bool = False
    mode: str = "free_play"  # "free_play" atau "guided"
    midi_file_loaded: bool = False
    midi_file_path: Optional[str] = None

    # Target notes untuk guided mode
    target_notes: Set[int] = field(default_factory=set)
    waiting_notes: Set[int] = field(default_factory=set)

    # Thread untuk playback
    playback_thread: Optional[threading.Thread] = None
    stop_playback: bool = False


@dataclass
class CalibrationState:
    """State kalibrasi."""
    is_calibrating: bool = False
    points: List[Tuple[int, int]] = field(default_factory=list)
    is_complete: bool = False
    tuts_rects: Dict[int, Tuple[int, int, int, int, bool]] = field(default_factory=dict)  # midi_note: (x1,y1,x2,y2,is_black)


@dataclass
class AppState:
    """State utama aplikasi."""
    camera: CameraState = field(default_factory=CameraState)
    midi: MidiState = field(default_factory=MidiState)
    hand_tracking: HandTrackingState = field(default_factory=HandTrackingState)
    practice: PracticeState = field(default_factory=PracticeState)
    calibration: CalibrationState = field(default_factory=CalibrationState)

    current_page: str = "dashboard"
    is_initialized: bool = False


# Default instance
HAND_TRACKING_STATE_DEFAULT = HandTrackingState()
app_state = AppState()