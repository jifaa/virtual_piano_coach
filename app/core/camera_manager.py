"""
AI Piano Coach - Camera Manager Module
Mengelola kamera webcam termasuk deteksi dan pembacaan frame.
"""
import cv2
import numpy as np
from typing import List, Optional, Tuple
import threading
import time
from app.constants import CAMERA_MAX_INDEX, CAMERA_DEFAULT_INDEX


class CameraManager:
    """
    Manager untuk mengelola kamera webcam.
    Mendukung deteksi kamera, preview, dan pembacaan frame.
    """

    def __init__(self):
        self.cap: Optional[cv2.VideoCapture] = None
        self.camera_index: int = CAMERA_DEFAULT_INDEX
        self.is_opened: bool = False
        self.current_frame: Optional[np.ndarray] = None
        self.fps: float = 0.0
        self.error_message: Optional[str] = None
        self._lock = threading.Lock()

        # Frame reading state
        self._reading: bool = False
        self._read_thread: Optional[threading.Thread] = None

    def detect_cameras(self, max_index: int = CAMERA_MAX_INDEX) -> List[Tuple[int, str]]:
        """
        Deteksi kamera yang tersedia.
        Returns: List of (index, description) tuples.
        """
        available_cameras = []

        for i in range(max_index + 1):
            try:
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    ret, frame = cap.read()
                    cap.release()
                    if ret:
                        h, w = frame.shape[:2] if frame is not None else (0, 0)
                        available_cameras.append((i, f"Camera {i} ({w}x{h})"))
                    else:
                        available_cameras.append((i, f"Camera {i}"))
                else:
                    cap.release()
            except Exception as e:
                print(f"[Camera] Error detecting camera {i}: {e}")
                continue

        return available_cameras

    def open(self, camera_index: int = CAMERA_DEFAULT_INDEX) -> bool:
        """
        Buka kamera dengan index tertentu.
        Returns: True jika berhasil.
        """
        self.close()

        try:
            self.camera_index = camera_index
            self.cap = cv2.VideoCapture(camera_index)

            # Set camera properties for better performance
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)

            if self.cap.isOpened():
                # Test read
                ret, frame = self.cap.read()
                if ret:
                    self.is_opened = True
                    self.error_message = None
                    print(f"[Camera] Opened camera {camera_index}")
                    return True
                else:
                    self.error_message = f"Cannot read from camera {camera_index}"
                    print(f"[Camera] {self.error_message}")
            else:
                self.error_message = f"Cannot open camera {camera_index}"
                print(f"[Camera] {self.error_message}")

            self.cap.release()
            self.cap = None
            return False

        except Exception as e:
            self.error_message = f"Error opening camera: {e}"
            print(f"[Camera] {self.error_message}")
            return False

    def close(self):
        """Tutup kamera dengan aman."""
        with self._lock:
            if self.cap is not None:
                try:
                    self.cap.release()
                    print("[Camera] Closed camera")
                except Exception as e:
                    print(f"[Camera] Error closing camera: {e}")
                finally:
                    self.cap = None
                    self.is_opened = False
                    self.current_frame = None

    def read_frame(self) -> Optional[np.ndarray]:
        """
        Baca satu frame dari kamera.
        Returns: Frame dalam format BGR (OpenCV format) atau None jika gagal.
        """
        if self.cap is None or not self.cap.isOpened():
            return None

        try:
            ret, frame = self.cap.read()
            if ret:
                return frame
            else:
                self.error_message = "Failed to read frame"
                return None
        except Exception as e:
            self.error_message = f"Error reading frame: {e}"
            return None

    def get_frame_with_fps(self) -> Tuple[Optional[np.ndarray], float]:
        """
        Baca frame dan hitung FPS.
        Returns: (frame, fps)
        """
        start_time = time.time()
        frame = self.read_frame()
        end_time = time.time()

        if frame is not None:
            self.fps = 1.0 / (end_time - start_time + 0.001)  # Avoid division by zero

        return frame, self.fps

    def is_working(self) -> bool:
        """Cek apakah kamera sedang berjalan dengan baik."""
        if self.cap is None:
            return False

        try:
            ret, frame = self.cap.read()
            return ret and frame is not None
        except:
            return False

    def get_info(self) -> dict:
        """Dapatkan informasi kamera."""
        return {
            "index": self.camera_index,
            "is_opened": self.is_opened,
            "fps": self.fps,
            "error": self.error_message,
        }

    def __del__(self):
        """Cleanup saat object dihapus."""
        self.close()