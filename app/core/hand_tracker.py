"""
AI Piano Coach - Hand Tracker Module
Wrapping untuk MediaPipe Hands tracking.
"""
import cv2
import mediapipe as mp
import numpy as np
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
import math
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from app.constants import FINGER_NAMES, POSTURE_THRESHOLDS, MEDIAPIPE_CONFIG


@dataclass
class FingerTip:
    """Data ujung jari."""
    x: int
    y: int
    hand: str  # "L" atau "R"
    finger: str  # "Jp", "Tl", "Tg", "Mn", "Kl"


@dataclass
class PostureResult:
    """Hasil analisis postur tangan."""
    hand: str  # "L" atau "R"
    status: str  # "good", "stiff", "bent", "octave_ok"
    message: str
    color: Tuple[int, int, int]  # BGR color


class HandTracker:
    """
    Wrapper untuk MediaPipe Hands.
    Mendeteksi tangan, landmark jari, dan analisis postur.
    Using MediaPipe Tasks Python API (v0.10+)
    """

    def __init__(self):
        # Initialize MediaPipe Tasks HandLandmarker
        base_options = python.BaseOptions(
            model_asset_path='mediapipe/tasks/models/hand_landmarker.task'
        )
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=MEDIAPIPE_CONFIG["max_num_hands"],
            min_hand_detection_confidence=MEDIAPIPE_CONFIG["min_detection_confidence"],
            min_hand_presence_confidence=MEDIAPIPE_CONFIG["min_tracking_confidence"],
            min_tracking_confidence=MEDIAPIPE_CONFIG["min_tracking_confidence"],
        )
        self.detector = vision.HandLandmarker.create_from_options(options)

        # Drawing specs (using new API's DrawingSpec)
        from mediapipe.tasks.python.vision import drawing_utils as mp_drawing
        self.drawing_spec = mp_drawing.DrawingSpec(
            color=(0, 255, 0), thickness=2, circle_radius=2
        )
        self.connection_drawing_spec = mp_drawing.DrawingSpec(
            color=(255, 255, 255), thickness=1
        )

    def process_frame(self, frame: np.ndarray, mirror: bool = False) -> List[Dict]:
        """
        Proses satu frame untuk deteksi tangan.
        Args:
            frame: Frame gambar dalam format BGR
            mirror: Apakah perlu mirror frame
        Returns:
            List of hand data dictionaries
        """
        if frame is None:
            return []

        # Convert BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Mirror if needed
        if mirror:
            rgb_frame = cv2.flip(rgb_frame, 1)

        # Create MediaPipe Image
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        # Detect hands (VIDEO mode requires timestamp in ms)
        import time
        timestamp_ms = int(time.monotonic() * 1000)
        results = self.detector.detect_for_video(mp_image, timestamp_ms)

        hands_data = []

        if results.hand_landmarks and results.handedness:
            for idx, (hand_landmarks, handedness) in enumerate(zip(
                results.hand_landmarks, results.handedness
            )):
                # handedness is a list of Classifications
                hand_label = (
                    "L" if handedness[0].category_name == "Left"
                    else "R"
                )

                # Extract finger tips
                h, w = frame.shape[:2]
                finger_tips = self._extract_finger_tips(hand_landmarks, hand_label, w, h)

                # Analyze posture
                posture = self._analyze_posture(hand_landmarks, hand_label)

                hands_data.append({
                    "hand": hand_label,
                    "landmarks": hand_landmarks,
                    "finger_tips": finger_tips,
                    "posture": posture,
                })

        return hands_data

    def _extract_finger_tips(
        self, hand_landmarks, hand_label: str, frame_width: int, frame_height: int
    ) -> List[FingerTip]:
        """Ekstrak posisi ujung semua jari."""
        finger_tips = []

        for tip_id, finger_name in FINGER_NAMES.items():
            lm = hand_landmarks[tip_id]  # New API: direct index access
            finger_tips.append(FingerTip(
                x=int(lm.x * frame_width),  # Normalized to actual frame width
                y=int(lm.y * frame_height), # Normalized to actual frame height
                hand=hand_label,
                finger=finger_name,
            ))

        return finger_tips

    def _analyze_posture(
        self, hand_landmarks, hand_label: str
    ) -> PostureResult:
        """Analisis postur tangan berdasarkan sudut jari."""
        # Landmark indices for MediaPipe hand model:
        # 0: WRIST, 1: THUMB_CMC, 2: THUMB_MCP, 3: THUMB_IP, 4: THUMB_TIP
        # 5: INDEX_FINGER_MCP, 6: INDEX_FINGER_PIP, 7: INDEX_FINGER_DIP, 8: INDEX_FINGER_TIP
        # 9: MIDDLE_FINGER_MCP, 10: MIDDLE_FINGER_PIP, 11: MIDDLE_FINGER_DIP, 12: MIDDLE_FINGER_TIP
        # 13: RING_FINGER_MCP, 14: RING_FINGER_PIP, 15: RING_FINGER_DIP, 16: RING_FINGER_TIP
        # 17: PINKY_MCP, 18: PINKY_PIP, 19: PINKY_DIP, 20: PINKY_TIP

        # Get relevant landmarks
        mcp = hand_landmarks[5]    # INDEX_FINGER_MCP
        pip = hand_landmarks[6]   # INDEX_FINGER_PIP
        tip = hand_landmarks[8]   # INDEX_FINGER_TIP
        thumb_tip = hand_landmarks[4]  # THUMB_TIP
        pinky_tip = hand_landmarks[20] # PINKY_TIP

        # Calculate finger angle
        angle = self._calculate_angle_3d(mcp, pip, tip)

        # Calculate thumb-pinky span
        span = self._calculate_distance(thumb_tip, pinky_tip)

        # Determine posture status
        thresholds = POSTURE_THRESHOLDS

        if span > thresholds["octave_span"]:
            status = "octave_ok"
            message = "Rentang Oktaf (Aman!)"
            color = (0, 255, 255)  # Yellow
        elif angle > thresholds["stiff_angle"]:
            status = "stiff"
            message = "Jari Kaku! Relakskan."
            color = (0, 0, 255)  # Red
        elif angle < thresholds["bent_angle"]:
            status = "bent"
            message = "Jari Tertekuk! Luruskan."
            color = (0, 165, 255)  # Orange
        else:
            status = "good"
            message = "Postur Bagus!"
            color = (0, 255, 0)  # Green

        return PostureResult(
            hand=hand_label,
            status=status,
            message=message,
            color=color,
        )

    def _calculate_angle_3d(self, p1, p2, p3) -> float:
        """Hitung sudut 3D antara 3 titik."""
        ax, ay, az = p1.x - p2.x, p1.y - p2.y, p1.z - p2.z
        bx, by, bz = p3.x - p2.x, p3.y - p2.y, p3.z - p2.z

        dot = ax * bx + ay * by + az * bz
        mag_a = math.sqrt(ax**2 + ay**2 + az**2)
        mag_b = math.sqrt(bx**2 + by**2 + bz**2)

        if mag_a * mag_b == 0:
            return 0

        cos_angle = dot / (mag_a * mag_b)
        cos_angle = max(min(cos_angle, 1.0), -1.0)
        return math.acos(cos_angle) * 180.0 / math.pi

    def _calculate_distance(self, p1, p2) -> float:
        """Hitung jarak 2D antara 2 titik landmark."""
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    def draw_landmarks(self, frame: np.ndarray, hand_landmarks) -> np.ndarray:
        """Gambar landmark tangan di frame."""
        # Use MediaPipe drawing utilities
        from mediapipe.tasks.python.vision import drawing_utils as mp_drawing

        mp_drawing.draw_landmarks(
            frame,
            hand_landmarks,
            vision.HandLandmarksConnections.HAND_CONNECTIONS,
            self.drawing_spec,
            self.connection_drawing_spec,
        )
        return frame

    def close(self):
        """Tutup MediaPipe Hands."""
        try:
            self.detector.close()
        except:
            pass