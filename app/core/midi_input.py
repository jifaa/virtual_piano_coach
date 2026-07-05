"""
AI Piano Coach - MIDI Input Module
Mengelola koneksi dan pembacaan input dari MIDI keyboard.
"""
try:
    import mido
    _mido_available = True
except ImportError:
    _mido_available = False
    mido = None

from typing import List, Optional, Set, Callable
import threading
import time


class MidiInputManager:
    """
    Manager untuk mengelola input MIDI keyboard.
    Mendukung deteksi device, koneksi, dan pembacaan note events.
    """

    def __init__(self):
        self.port = None
        self.port_name: Optional[str] = None
        self.is_connected: bool = False
        self.active_notes: Set[int] = set()
        self.error_message: Optional[str] = None

        # Callback untuk note events
        self.on_note_on: Optional[Callable[[int], None]] = None
        self.on_note_off: Optional[Callable[[int], None]] = None

        # Lock untuk thread safety
        self._lock = threading.Lock()

    def detect_inputs(self) -> List[str]:
        """
        Deteksi semua MIDI input yang tersedia.
        Returns: List nama port MIDI.
        """
        if not _mido_available:
            self.error_message = "Module mido/rtmidi belum terinstall. Jalankan: pip install mido python-rtmidi"
            print(f"[MIDI] {self.error_message}")
            return []

        try:
            ports = mido.get_input_names()
            if ports:
                print(f"[MIDI] Found {len(ports)} input(s): {ports}")
            else:
                print("[MIDI] No MIDI input devices found. Pastikan keyboard sudah terhubung via USB dan driver terinstall.")
            return ports
        except ImportError as e:
            self.error_message = f"Module rtmidi belum terinstall. Jalankan: pip install python-rtmidi"
            print(f"[MIDI] {self.error_message}")
            return []
        except Exception as e:
            self.error_message = f"Error detecting MIDI inputs: {e}"
            print(f"[MIDI] {self.error_message}")
            return []

    def auto_select_device(self) -> Optional[str]:
        """
        Otomatis pilih device MIDI yang paling mungkin.
        Prioritas: Roland > E-X >其他的。
        Returns: Nama port yang dipilih atau None.
        """
        ports = self.detect_inputs()
        if not ports:
            return None

        # Cari Roland atau E-X
        for port in ports:
            if 'Roland' in port or 'E-X10' in port or 'E-X' in port:
                return port

        # Fallback ke port pertama
        return ports[0]

    def connect(self, port_name: str) -> bool:
        """
        Hubungkan ke MIDI input dengan nama tertentu.
        Returns: True jika berhasil.
        """
        if not _mido_available:
            self.error_message = "MIDI backend tidak tersedia"
            return False

        self.disconnect()

        try:
            self.port = mido.open_input(port_name)
            self.port_name = port_name
            self.is_connected = True
            self.error_message = None
            print(f"[MIDI] Connected to {port_name}")
            return True

        except Exception as e:
            self.error_message = f"Error connecting to {port_name}: {e}"
            print(f"[MIDI] {self.error_message}")
            self.port_name = None
            self.is_connected = False
            return False

    def disconnect(self):
        """Putuskan koneksi MIDI."""
        with self._lock:
            if self.port is not None:
                try:
                    self.port.close()
                    print(f"[MIDI] Disconnected from {self.port_name}")
                except Exception as e:
                    print(f"[MIDI] Error disconnecting: {e}")
                finally:
                    self.port = None
                    self.port_name = None
                    self.is_connected = False
                    self.active_notes.clear()

    def poll_messages(self):
        """
        Baca semua pending MIDI messages.
        Harus dipanggil secara berkala (misalnya di loop utama atau thread).
        """
        if self.port is None or not self.is_connected:
            return

        try:
            for msg in self.port.iter_pending():
                self._process_message(msg)
        except Exception as e:
            self.error_message = f"Error polling MIDI: {e}"
            print(f"[MIDI] {self.error_message}")

    def _process_message(self, msg):
        """Proses satu MIDI message."""
        if msg.type == 'note_on' and msg.velocity > 0:
            with self._lock:
                self.active_notes.add(msg.note)

            if self.on_note_on:
                try:
                    self.on_note_on(msg.note)
                except Exception as e:
                    print(f"[MIDI] Error in on_note_on callback: {e}")

        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            with self._lock:
                self.active_notes.discard(msg.note)

            if self.on_note_off:
                try:
                    self.on_note_off(msg.note)
                except Exception as e:
                    print(f"[MIDI] Error in on_note_off callback: {e}")

    def get_active_notes(self) -> Set[int]:
        """Dapatkan semua note yang sedang aktif."""
        with self._lock:
            return set(self.active_notes)

    def is_note_pressed(self, note: int) -> bool:
        """Cek apakah note tertentu sedang aktif."""
        with self._lock:
            return note in self.active_notes

    def clear_notes(self):
        """Hapus semua active notes."""
        with self._lock:
            self.active_notes.clear()

    def get_info(self) -> dict:
        """Dapatkan informasi koneksi MIDI."""
        return {
            "port_name": self.port_name,
            "is_connected": self.is_connected,
            "active_notes": sorted(list(self.active_notes)),
            "error": self.error_message,
        }

    def __del__(self):
        """Cleanup saat object dihapus."""
        self.disconnect()