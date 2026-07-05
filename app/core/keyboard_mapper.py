"""
AI Piano Coach - Keyboard Mapper Module
Menghasilkan rectangle tuts piano dan mapping MIDI note ke koordinat layar.
"""
import numpy as np
from typing import Dict, Tuple, List, Optional
from app.constants import BLACK_PITCH_CLASSES


class KeyboardMapper:
    """
    Mapper untuk keyboard piano virtual.
    Mendukung keyboard 61 keys dan 88 keys dengan base MIDI yang berbeda.
    """

    def __init__(
        self,
        total_keys: int = 61,
        base_midi: int = 36,
    ):
        self.total_keys = total_keys
        self.base_midi = base_midi
        self.last_midi = base_midi + total_keys - 1

        # Calibration points (4 corners)
        self.calibration_points: List[Tuple[int, int]] = []
        self.calibration_complete: bool = False

        # Computed key rectangles: midi_note -> (x1, y1, x2, y2, is_black)
        self.key_rects: Dict[int, Tuple[int, int, int, int, bool]] = {}

    def set_calibration_points(self, points: List[Tuple[int, int]]):
        """
        Set 4 titik kalibrasi untuk mapping keyboard ke layar.
        Points harus berurutan: top-left, top-right, bottom-right, bottom-left.
        """
        if len(points) != 4:
            raise ValueError("Harus ada tepat 4 titik kalibrasi")

        self.calibration_points = points
        self._compute_key_rects()
        self.calibration_complete = True

    def clear_calibration(self):
        """Hapus kalibrasi."""
        self.calibration_points = []
        self.key_rects = {}
        self.calibration_complete = False

    def _compute_key_rects(self):
        """
        Hitung rectangle (polygon) untuk semua tuts piano berdasarkan titik kalibrasi.
        Menggunakan perspective transform untuk akurasi tinggi pada perspektif kamera.
        """
        import cv2
        pts = np.array(self.calibration_points, dtype=np.float32)

        # Urutin titik (top-left, top-right, bottom-right, bottom-left)
        rect = self._order_points(pts)
        (tl, tr, br, bl) = rect

        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))

        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]
        ], dtype=np.float32)

        # Transform matrix FROM perfect TO original camera
        M = cv2.getPerspectiveTransform(dst, rect)

        # Hitung jumlah white keys
        white_key_count = self._count_white_keys()
        if white_key_count == 0:
            white_key_count = 36  # Default fallback

        lebar_satu_putih = maxWidth / white_key_count

        # Generate polygons untuk setiap key
        self.key_rects = {}
        white_index = 0

        for i in range(self.total_keys):
            midi_note = self.base_midi + i

            # Gunakan MIDI note modulo 12 untuk deteksi black key
            pitch_class = midi_note % 12
            is_black = pitch_class in BLACK_PITCH_CLASSES

            if is_black:
                # Black key: posisi di tengah antara white key
                center_x = white_index * lebar_satu_putih
                lebar_hitam = lebar_satu_putih * 0.65

                px1 = center_x - (lebar_hitam / 2)
                px2 = center_x + (lebar_hitam / 2)
                py1 = 0
                py2 = maxHeight * 0.65  # Black keys lebih pendek

                perfect_pts = np.array([
                    [[px1, py1]],
                    [[px2, py1]],
                    [[px2, py2]],
                    [[px1, py2]]
                ], dtype=np.float32)

            else:
                # White key
                px1 = white_index * lebar_satu_putih
                px2 = (white_index + 1) * lebar_satu_putih
                py1 = 0
                py2 = maxHeight

                perfect_pts = np.array([
                    [[px1, py1]],
                    [[px2, py1]],
                    [[px2, py2]],
                    [[px1, py2]]
                ], dtype=np.float32)

                white_index += 1

            # Transform back to camera coordinates
            cam_pts = cv2.perspectiveTransform(perfect_pts, M)
            cam_pts = cam_pts.reshape(4, 2).astype(np.int32)

            # Store as list of tuples for JSON serialization
            poly_list = [(int(p[0]), int(p[1])) for p in cam_pts]
            self.key_rects[midi_note] = (poly_list, is_black)

        print(f"[KeyboardMapper] Generated {len(self.key_rects)} key polygons")

    def _order_points(self, pts: np.ndarray) -> np.ndarray:
        """
        Urutkan 4 titik menjadi: top-left, top-right, bottom-right, bottom-left.
        """
        rect = np.zeros((4, 2), dtype=np.float32)

        # Sum untuk top-left (terkecil) dan bottom-right (terbesar)
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]  # top-left
        rect[2] = pts[np.argmax(s)]  # bottom-right

        # Difference untuk top-right dan bottom-left
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]  # top-right
        rect[3] = pts[np.argmax(diff)]  # bottom-left

        return rect

    def _count_white_keys(self) -> int:
        """Hitung jumlah white keys dalam range keyboard."""
        count = 0
        for i in range(self.total_keys):
            midi_note = self.base_midi + i
            pitch_class = midi_note % 12
            if pitch_class not in BLACK_PITCH_CLASSES:
                count += 1
        return count

    def get_key_rect(self, midi_note: int) -> Optional[Tuple[int, int, int, int, bool]]:
        """Dapatkan rectangle untuk MIDI note tertentu."""
        return self.key_rects.get(midi_note)

    def get_all_key_rects(self) -> Dict[int, Tuple[int, int, int, int, bool]]:
        """Dapatkan semua key rectangles."""
        return self.key_rects

    def get_white_key_width(self) -> float:
        """Dapatkan lebar satu white key rata-rata dalam piksel (estimasi)."""
        if not self.calibration_complete or len(self.calibration_points) != 4:
            return 0.0

        pts = np.array(self.calibration_points, dtype=np.float32)
        rect = self._order_points(pts)
        
        tl, tr, br, bl = rect
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(widthA, widthB)

        white_count = self._count_white_keys()
        return maxWidth / white_count if white_count > 0 else 0.0

    def is_calibrated(self) -> bool:
        """Cek apakah kalibrasi sudah selesai."""
        return self.calibration_complete and len(self.key_rects) > 0

    def get_keyboard_range(self) -> Tuple[int, int]:
        """Dapatkan range MIDI note untuk keyboard ini."""
        return (self.base_midi, self.last_midi)

    def midi_note_to_key_name(self, midi_note: int) -> str:
        """Konversi MIDI note ke nama not (misalnya 'C4', 'D#5')."""
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        octave = (midi_note // 12) - 1
        note_name = note_names[midi_note % 12]
        return f"{note_name}{octave}"

    def get_config(self) -> dict:
        """Dapatkan konfigurasi keyboard mapper."""
        return {
            "total_keys": self.total_keys,
            "base_midi": self.base_midi,
            "last_midi": self.last_midi,
            "is_calibrated": self.is_calibrated(),
            "key_count": len(self.key_rects),
        }