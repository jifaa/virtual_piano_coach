"""
AI Piano Coach - Overlay Renderer Module
Menyediakan fungsi untuk menggambar overlay piano, note targets, dan UI di frame kamera.
"""
import cv2
import numpy as np
from typing import Dict, List, Set, Tuple, Optional
from app.constants import NOTE_COLORS, FINGER_NAMES
from app.core.keyboard_mapper import KeyboardMapper
from app.core.hand_tracker import FingerTip, PostureResult


class OverlayRenderer:
    """
    Renderer untuk menggambar overlay piano dan UI di frame kamera.
    """

    def __init__(self, keyboard_mapper: Optional[KeyboardMapper] = None):
        self.keyboard_mapper = keyboard_mapper
        self.frame_width = 640
        self.frame_height = 480

        # State
        self.active_notes: Set[int] = set()
        self.target_notes: Set[int] = set()
        self.waiting_notes: Set[int] = set()
        self.is_guided_mode: bool = False

        # Posture
        self.posture_left: Optional[PostureResult] = None
        self.posture_right: Optional[PostureResult] = None

        # Finger tips
        self.finger_tips: List[FingerTip] = []

        # UI Settings
        self.show_finger_labels: bool = True
        self.show_posture: bool = True
        self.show_note_numbers: bool = False
        self.show_target_labels: bool = True

        # Middle C for hand split
        self.hand_split_note: int = 60

    def set_keyboard_mapper(self, mapper: KeyboardMapper):
        """Set keyboard mapper."""
        self.keyboard_mapper = mapper

    def update_state(
        self,
        active_notes: Set[int],
        target_notes: Set[int] = None,
        waiting_notes: Set[int] = None,
        is_guided: bool = False,
    ):
        """Update state untuk rendering."""
        self.active_notes = active_notes
        if target_notes is not None:
            self.target_notes = target_notes
        if waiting_notes is not None:
            self.waiting_notes = waiting_notes
        self.is_guided_mode = is_guided

    def update_hands(
        self,
        finger_tips: List[FingerTip],
        posture_left: Optional[PostureResult] = None,
        posture_right: Optional[PostureResult] = None,
    ):
        """Update data tangan untuk rendering."""
        self.finger_tips = finger_tips
        self.posture_left = posture_left
        self.posture_right = posture_right

    def render(self, frame: np.ndarray) -> np.ndarray:
        """
        Render semua overlay ke frame.
        Returns: Frame dengan overlay.
        """
        if frame is None:
            return frame

        # Overlay features dikendalikan oleh settings (show_finger_labels, show_target_labels, dll)

        self.frame_height, self.frame_width = frame.shape[:2]
        output = frame.copy()

        if self.keyboard_mapper and self.keyboard_mapper.is_calibrated():
            output = self._render_piano_overlay(output)

        return output

    def _render_piano_overlay(self, frame: np.ndarray) -> np.ndarray:
        """Render overlay piano di frame."""
        if not self.keyboard_mapper:
            return frame

        self.current_note_fingers = {}

        # Render tuts satu per satu
        for midi_note, rect_data in self.keyboard_mapper.get_all_key_rects().items():
            pts_list, is_black = rect_data
            pts_array = np.array([pts_list], dtype=np.int32)
            
            # Cari bounding box untuk menempatkan teks (finger label, note number)
            x_min = min(p[0] for p in pts_list)
            y_min = min(p[1] for p in pts_list)
            x_max = max(p[0] for p in pts_list)
            y_max = max(p[1] for p in pts_list)

            is_pressed = midi_note in self.active_notes
            is_target = midi_note in self.target_notes

            # Tentukan warna
            color = None
            text = ""

            if is_pressed:
                if self.is_guided_mode:
                    # Guided mode: hijau jika target, merah jika salah
                    color = NOTE_COLORS["correct"] if is_target else NOTE_COLORS["wrong"]
                else:
                    # Free play: hijau saja
                    color = NOTE_COLORS["pressed"]
            elif is_target:
                # Target note yang belum ditekan
                if midi_note < self.hand_split_note:
                    color = NOTE_COLORS["target_left"]
                    if self.show_target_labels:
                        text = "L"
                else:
                    color = NOTE_COLORS["target_right"]
                    if self.show_target_labels:
                        text = "R"

            # Gambar polygon
            if color:
                if is_black:
                    cv2.fillPoly(frame, pts_array, color)
                    cv2.polylines(frame, pts_array, True, (0,0,0), 2)
                else:
                    cv2.fillPoly(frame, pts_array, color)
                    cv2.polylines(frame, pts_array, True, (0,0,0), 1)

                # Gambar finger label jika ditekan
                if is_pressed:
                    finger_label = self._find_finger_label(pts_array[0])
                    if finger_label:
                        self.current_note_fingers[midi_note] = finger_label
                        if self.show_finger_labels:
                            cv2.putText(
                                frame,
                                finger_label,
                                (x_min + 2, y_min - 5),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.4,
                                (255, 255, 255),
                                1,
                                cv2.LINE_AA,
                            )
            else:
                # Tuts idle
                if is_black:
                    cv2.polylines(frame, pts_array, True, NOTE_COLORS["idle_black"], 2)
                else:
                    cv2.polylines(frame, pts_array, True, NOTE_COLORS["idle_white"], 1)

            # Tampilkan note number jika diaktifkan
            if self.show_note_numbers:
                pos_y = y_max - 10 if not is_black else y_max - 5
                text_color = (255, 255, 255)
                cv2.putText(
                    frame,
                    str(midi_note),
                    (x_min + 2, pos_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.3,
                    text_color,
                    1,
                    cv2.LINE_AA,
                )

        return frame

    def _find_finger_label(self, pts_array: np.ndarray) -> Optional[str]:
        """Cari finger label untuk tuts yang ditekan menggunakan polygon test dan distance."""
        candidates = []

        for tip in self.finger_tips:
            # Gunakan pointPolygonTest dengan measureDist=True
            dist = cv2.pointPolygonTest(pts_array, (float(tip.x), float(tip.y)), True)
            
            # Toleransi -20 pixel (karena ujung jari / tracking bisa sedikit meleset keluar dari polygon tuts tipis)
            if dist >= -20.0:
                candidates.append((dist, tip.y, f"{tip.hand}-{tip.finger}"))

        if candidates:
            # Pilih yang paling tengah/dalam (dist paling besar)
            return max(candidates, key=lambda c: c[0])[2]

        return None

    def render_calibration_markers(self, frame: np.ndarray, points: List[Tuple[int, int]]) -> np.ndarray:
        """Render marker titik kalibrasi."""
        for i, (x, y) in enumerate(points):
            # Gambar circle
            cv2.circle(frame, (x, y), 10, NOTE_COLORS["calibration_point"], -1)
            # Gambar nomor
            cv2.putText(
                frame,
                str(i + 1),
                (x - 5, y + 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 0),
                2,
                cv2.LINE_AA,
            )

        return frame

    def render_info_panel(self, frame: np.ndarray) -> np.ndarray:
        """Render panel info di bagian atas/bawah frame: postur tangan, note aktif."""
        if frame is None:
            return frame

        h, w = frame.shape[:2]

        if self.show_posture:
            # Render posture info at top-right corner
            y_offset = 20
            if self.posture_left:
                text = f"Kiri: {self.posture_left.message}"
                color = self.posture_left.color
                cv2.putText(frame, text, (w - 300, y_offset),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)
                y_offset += 22
            if self.posture_right:
                text = f"Kanan: {self.posture_right.message}"
                color = self.posture_right.color
                cv2.putText(frame, text, (w - 300, y_offset),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)

        # Show active notes count at bottom-left
        if self.active_notes:
            notes_text = f"Notes: {len(self.active_notes)} aktif"
            cv2.putText(frame, notes_text, (10, h - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1, cv2.LINE_AA)

        return frame

    def render_calibration_prompt(self, frame: np.ndarray, current_points: int) -> np.ndarray:
        """Render prompt untuk kalibrasi."""
        h, w = frame.shape[:2]

        text = f"Klik 4 sudut keyboard! (Skrg: {current_points}/4)"
        cv2.putText(
            frame,
            text,
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2,
            cv2.LINE_AA,
        )

        # Instructions
        instructions = [
            "1. Klik sudut kiri atas keyboard",
            "2. Klik sudut kanan atas keyboard",
            "3. Klik sudut kanan bawah keyboard",
            "4. Klik sudut kiri bawah keyboard",
        ]

        for i, instr in enumerate(instructions):
            y = 80 + i * 25
            color = (0, 255, 0) if i < current_points else (150, 150, 150)
            cv2.putText(
                frame,
                instr,
                (20, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                1,
            )

        return frame