"""
AI Piano Coach - Practice Engine Module
Mengkoordinasikan semua komponen untuk mode latihan.
"""
import threading
from typing import Set, Optional, Dict, List, Callable
import time

from app.core.camera_manager import CameraManager
from app.core.midi_input import MidiInputManager
from app.core.keyboard_mapper import KeyboardMapper
from app.core.hand_tracker import HandTracker, FingerTip, PostureResult
from app.core.midi_song import MidiSongPlayer
from app.core.overlay_renderer import OverlayRenderer
from app.state import PracticeState, HandTrackingState


class PracticeEngine:
    """
    Engine utama untuk practice mode.
    Mengkoordinasikan camera, MIDI, hand tracking, dan rendering.
    """

    def __init__(
        self,
        camera_manager: CameraManager,
        midi_manager: MidiInputManager,
        keyboard_mapper: KeyboardMapper,
    ):
        self.camera = camera_manager
        self.midi = midi_manager
        self.keyboard_mapper = keyboard_mapper

        # Hand tracking
        self.hand_tracker = HandTracker()

        # MIDI song player
        self.song_player = MidiSongPlayer()

        # Overlay renderer
        self.overlay_renderer = OverlayRenderer(keyboard_mapper)

        # State
        self.practice_state = PracticeState()
        self.hand_state = HandTrackingState()

        # Running state
        self.is_running = False
        self._running = False
        self._loop_thread: Optional[threading.Thread] = None
        self._update_callback: Optional[Callable] = None

        # Callbacks untuk song player
        self.song_player.on_target_note_on = self._on_target_note_on
        self.song_player.on_target_note_off = self._on_target_note_off
        self.song_player.on_playback_start = self._on_playback_start
        self.song_player.on_playback_end = self._on_playback_end

    def set_update_callback(self, callback: Callable):
        """Set callback yang dipanggil setiap frame di-update."""
        self._update_callback = callback

    def load_midi_file(self, file_path: str) -> bool:
        """Load file MIDI untuk guided mode."""
        keyboard_config = self._get_keyboard_config()
        success = self.song_player.load_file(
            file_path,
            base_midi=keyboard_config["base_midi"],
            total_keys=keyboard_config["total_keys"],
        )

        if success:
            self.practice_state.midi_file_loaded = True
            self.practice_state.midi_file_path = file_path

        return success

    def unload_midi_file(self):
        """Unload file MIDI."""
        self.song_player.unload()
        self.practice_state.midi_file_loaded = False
        self.practice_state.midi_file_path = None

    def _get_keyboard_config(self) -> Dict:
        """Dapatkan konfigurasi keyboard."""
        return {
            "base_midi": self.keyboard_mapper.base_midi,
            "total_keys": self.keyboard_mapper.total_keys,
        }

    def start(self, mode: str = "free_play"):
        """
        Mulai practice mode.
        Args:
            mode: "free_play" atau "guided"
        """
        if self.is_running:
            print("[PracticeEngine] Already running")
            return

        if not self.camera.is_opened:
            print("[PracticeEngine] Camera not opened")
            return

        if mode == "guided" and not self.song_player.is_loaded:
            print("[PracticeEngine] No MIDI file loaded for guided mode")
            return

        self._running = True
        self.is_running = True
        self.practice_state.is_running = True
        self.practice_state.mode = mode

        # Start camera loop
        self._loop_thread = threading.Thread(target=self._main_loop, daemon=True)
        self._loop_thread.start()

        # Start MIDI song if guided mode
        if mode == "guided":
            keyboard_config = self._get_keyboard_config()
            self.song_player.start_playback(
                base_midi=keyboard_config["base_midi"],
                total_keys=keyboard_config["total_keys"],
                active_notes_getter=self.midi.get_active_notes,
            )

        print(f"[PracticeEngine] Started in {mode} mode")

    def stop(self):
        """Stop practice mode."""
        self._running = False
        self.is_running = False
        self.practice_state.is_running = False

        # Stop MIDI song
        self.song_player.stop()

        # Wait for thread
        if self._loop_thread and self._loop_thread.is_alive():
            self._loop_thread.join(timeout=1.0)

        print("[PracticeEngine] Stopped")

    def get_current_frame(self):
        """Dapatkan frame terakhir dengan overlay."""
        return self._current_frame

    def _main_loop(self):
        """Main loop yang berjalan di background thread."""
        print("[PracticeEngine] Main loop started")

        while self._running:
            try:
                # 1. Read camera frame
                frame = self.camera.read_frame()
                if frame is None:
                    time.sleep(0.01)
                    continue

                # 2. Poll MIDI
                self.midi.poll_messages()
                active_notes = self.midi.get_active_notes()

                # 3. Process hand tracking
                hands_data = self.hand_tracker.process_frame(frame, mirror=False)

                # Extract finger tips
                all_finger_tips: List[FingerTip] = []
                posture_left: Optional[PostureResult] = None
                posture_right: Optional[PostureResult] = None

                for hand_data in hands_data:
                    all_finger_tips.extend(hand_data["finger_tips"])

                    posture = hand_data["posture"]
                    if posture.hand == "L":
                        posture_left = posture
                    else:
                        posture_right = posture

                # Update hand state
                self.hand_state.is_detecting = len(hands_data) > 0
                self.hand_state.hands_detected = len(hands_data)
                self.hand_state.landmarks = all_finger_tips
                self.hand_state.postures = [p for p in [posture_left, posture_right] if p]

                # 4. Update overlay renderer
                is_guided = self.practice_state.mode == "guided" and self.song_player.is_playing

                self.overlay_renderer.update_state(
                    active_notes=active_notes,
                    target_notes=self.song_player.active_target_notes,
                    waiting_notes=self.song_player.waiting_notes,
                    is_guided=is_guided,
                )

                self.overlay_renderer.update_hands(
                    finger_tips=all_finger_tips,
                    posture_left=posture_left,
                    posture_right=posture_right,
                )

                # 5. Render overlay
                output_frame = self.overlay_renderer.render(frame)
                output_frame = self.overlay_renderer.render_info_panel(output_frame)

                # Store current frame
                self._current_frame = output_frame

                # 6. Call update callback
                if self._update_callback:
                    try:
                        self._update_callback(output_frame)
                    except Exception as e:
                        print(f"[PracticeEngine] Callback error: {e}")

                time.sleep(0.033)  # ~30 FPS

            except Exception as e:
                print(f"[PracticeEngine] Loop error: {e}")
                import traceback
                traceback.print_exc()

        print("[PracticeEngine] Main loop ended")

    # Song player callbacks
    def _on_target_note_on(self, note: int):
        """Dipanggil saat target note muncul."""
        pass

    def _on_target_note_off(self, note: int):
        """Dipanggil saat target note selesai."""
        pass

    def _on_playback_start(self):
        """Dipanggil saat playback dimulai."""
        self.practice_state.mode = "guided"
        print("[PracticeEngine] Playback started")

    def _on_playback_end(self):
        """Dipanggil saat playback selesai."""
        self.practice_state.mode = "free_play"
        print("[PracticeEngine] Playback ended")

    def get_status(self) -> Dict:
        """Dapatkan status engine."""
        return {
            "is_running": self.is_running,
            "mode": self.practice_state.mode,
            "hands_detected": self.hand_state.hands_detected,
            "active_notes": sorted(list(self.midi.get_active_notes())),
            "target_notes": sorted(list(self.song_player.active_target_notes)),
            "song_playing": self.song_player.is_playing,
            "song_loaded": self.song_player.is_loaded,
        }

    def close(self):
        """Tutup semua resources."""
        self.stop()
        self.hand_tracker.close()
        self.song_player.unload()