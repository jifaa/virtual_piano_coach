"""
AI Piano Coach - MIDI Song Module
Mengelola loading dan parsing file MIDI untuk guided practice mode.
"""
try:
    import mido
    _mido_available = True
except ImportError:
    _mido_available = False
    mido = None
from typing import List, Set, Optional, Callable, Tuple
import threading
import time
from dataclasses import dataclass


@dataclass
class MidiNote:
    """Representasi satu note dalam file MIDI."""
    note: int  # MIDI note number
    velocity: int
    time: float  # Waktu dalam detik dari note sebelumnya
    is_note_on: bool


class MidiSongPlayer:
    """
    Player untuk file MIDI dengan fitur pause-until-correct.
    Cocok untuk mode latihan Synthesia-style.
    """

    def __init__(self):
        self.midi_file: Optional[mido.MidiFile] = None
        self.file_path: Optional[str] = None
        self.is_loaded: bool = False
        self.error_message: Optional[str] = None

        # Playback state
        self.is_playing: bool = False
        self.is_paused: bool = False
        self.stop_requested: bool = False

        # Notes
        self.active_target_notes: Set[int] = set()
        self.waiting_notes: Set[int] = set()

        # Callbacks
        self.on_target_note_on: Optional[Callable[[int], None]] = None
        self.on_target_note_off: Optional[Callable[[int], None]] = None
        self.on_playback_start: Optional[Callable[[], None]] = None
        self.on_playback_end: Optional[Callable[[], None]] = None
        self.on_waiting_for_notes: Optional[Callable[[Set[int]], None]] = None

        # Thread
        self._playback_thread: Optional[threading.Thread] = None

    def load_file(self, file_path: str, base_midi: int = 36, total_keys: int = 61) -> bool:
        """
        Load file MIDI.
        Args:
            file_path: Path ke file .mid atau .midi
            base_midi: MIDI note terendah untuk keyboard
            total_keys: Jumlah total keys
        Returns: True jika berhasil
        """
        if not _mido_available:
            self.error_message = "Module mido belum terinstall. Jalankan: pip install mido"
            print(f"[MidiSong] {self.error_message}")
            return False

        try:
            self.midi_file = mido.MidiFile(file_path)
            self.file_path = file_path
            self.is_loaded = True
            self.error_message = None
            print(f"[MidiSong] Loaded: {file_path}")
            return True

        except FileNotFoundError:
            self.error_message = f"File tidak ditemukan: {file_path}"
            print(f"[MidiSong] {self.error_message}")
            return False

        except Exception as e:
            self.error_message = f"Error loading MIDI: {e}"
            print(f"[MidiSong] {self.error_message}")
            return False

    def unload(self):
        """Unload file MIDI."""
        self.stop()
        self.midi_file = None
        self.file_path = None
        self.is_loaded = False
        self.active_target_notes.clear()
        self.waiting_notes.clear()

    def start_playback(
        self,
        base_midi: int = 36,
        total_keys: int = 61,
        active_notes_getter: Optional[Callable[[], Set[int]]] = None,
    ):
        """
        Mulai playback MIDI di background thread.
        Args:
            base_midi: MIDI note terendah
            total_keys: Jumlah keys
            active_notes_getter: Function untuk dapetin active notes dari MIDI input
        """
        if not self.is_loaded:
            print("[MidiSong] No MIDI file loaded")
            return

        if self.is_playing:
            print("[MidiSong] Already playing")
            return

        self.stop_requested = False
        self.is_playing = True

        self._playback_thread = threading.Thread(
            target=self._playback_loop,
            args=(base_midi, total_keys, active_notes_getter),
            daemon=True,
        )
        self._playback_thread.start()

        if self.on_playback_start:
            self.on_playback_start()

    def stop(self):
        """Stop playback."""
        self.stop_requested = True
        self.is_playing = False
        self.is_paused = False

        if self._playback_thread and self._playback_thread.is_alive():
            self._playback_thread.join(timeout=1.0)

        self.active_target_notes.clear()
        self.waiting_notes.clear()

    def pause(self):
        """Pause playback."""
        self.is_paused = True

    def resume(self):
        """Resume playback."""
        self.is_paused = False

    def _playback_loop(
        self,
        base_midi: int,
        total_keys: int,
        active_notes_getter: Optional[Callable[[], Set[int]]],
    ):
        """
        Main playback loop.
        Berjalan di background thread.
        """
        print("[MidiSong] Playback started")

        try:
            for msg in self.midi_file:
                if self.stop_requested:
                    break

                # Wait if paused
                while self.is_paused and not self.stop_requested:
                    time.sleep(0.01)

                # ==========================================
                # CORE SYNTHESIA LOGIC: Pause until correct notes
                # ==========================================
                if msg.time > 0.05 and len(self.waiting_notes) > 0:
                    # MODE PAUSE: Tunggu sampai semua target note ditekan
                    if active_notes_getter:
                        while not self.waiting_notes.issubset(active_notes_getter()):
                            if self.stop_requested:
                                break
                            time.sleep(0.01)
                    else:
                        # Fallback: check internal state
                        while not self.waiting_notes.issubset(self.active_target_notes):
                            if self.stop_requested:
                                break
                            time.sleep(0.01)

                    # Clear waiting notes after all pressed
                    for note in list(self.waiting_notes):
                        if self.on_target_note_off:
                            self.on_target_note_off(note)
                    self.waiting_notes.clear()

                # Natural delay between notes
                if msg.time > 0:
                    time.sleep(msg.time)

                # Process MIDI message
                if getattr(msg, 'channel', 0) != 9:  # Skip drum channel (9)
                    self._process_message(msg, base_midi, total_keys)

        except Exception as e:
            print(f"[MidiSong] Playback error: {e}")
            self.error_message = str(e)

        finally:
            self.is_playing = False
            self.active_target_notes.clear()
            self.waiting_notes.clear()

            if self.on_playback_end:
                self.on_playback_end()

            print("[MidiSong] Playback ended")

    def _process_message(
        self, msg, base_midi: int, total_keys: int
    ):
        """Proses satu MIDI message."""
        max_note = base_midi + total_keys

        if msg.type == 'note_on' and msg.velocity > 0:
            note = msg.note
            if base_midi <= note < max_note:
                self.active_target_notes.add(note)
                self.waiting_notes.add(note)

                if self.on_target_note_on:
                    self.on_target_note_on(note)

        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            note = msg.note
            if base_midi <= note < max_note:
                self.active_target_notes.discard(note)
                self.waiting_notes.discard(note)

                if self.on_target_note_off:
                    self.on_target_note_off(note)

    def get_info(self) -> dict:
        """Dapatkan informasi tentang file MIDI."""
        return {
            "is_loaded": self.is_loaded,
            "file_path": self.file_path,
            "is_playing": self.is_playing,
            "is_paused": self.is_paused,
            "active_target_notes": sorted(list(self.active_target_notes)),
            "waiting_notes": sorted(list(self.waiting_notes)),
            "error": self.error_message,
        }


def parse_midi_notes(file_path: str, base_midi: int = 36, total_keys: int = 61) -> List[MidiNote]:
    """
    Parse file MIDI dan return list semua notes.
    Tidak untuk playback, hanya untuk analisis.
    """
    notes = []

    try:
        mid = mido.MidiFile(file_path)
        time_accumulated = 0.0

        for msg in mid:
            time_accumulated += msg.time

            if getattr(msg, 'channel', 0) != 9:  # Skip drums
                if msg.type == 'note_on' and msg.velocity > 0:
                    note = msg.note
                    if base_midi <= note < (base_midi + total_keys):
                        notes.append(MidiNote(
                            note=note,
                            velocity=msg.velocity,
                            time=time_accumulated,
                            is_note_on=True,
                        ))

    except Exception as e:
        print(f"[MidiSong] Error parsing MIDI: {e}")

    return notes