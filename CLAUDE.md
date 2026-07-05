# CLAUDE.md — AI Piano Coach App

## Project Goal
Build a professional desktop application from the existing `pianonew.py` prototype.

The app is an **AI Piano Coach** that combines:
- webcam-based hand/finger tracking,
- MIDI keyboard input,
- optional MIDI-file guided practice,
- keyboard calibration,
- real-time visual piano overlay,
- posture/fingering feedback,
- a clean multi-page UI using **CustomTkinter**.

The app must feel like a real product, not a one-file experiment.

---

## Original Prototype Summary
The current prototype already does these things:
- Opens a webcam using OpenCV.
- Connects to a MIDI input device using `mido` and `python-rtmidi`.
- Tracks hands and finger landmarks using MediaPipe Hands.
- Lets the user click 4 points to calibrate the keyboard area.
- Draws piano-key rectangles over the camera feed.
- Detects pressed MIDI notes.
- Reads a `.mid` file and uses its notes as visual targets.
- Pauses guided playback until the user presses all required target notes.
- Colors correct notes green and wrong notes red during guided mode.
- Shows target notes for left/right hand based on MIDI note range.
- Labels which finger appears to press a key.
- Gives simple posture feedback based on finger angle and thumb-to-pinky distance.

Preserve these core behaviors, but refactor them into maintainable modules with a professional UI.

---

## Non-Negotiable Requirements
1. Use **Python**.
2. Use **CustomTkinter** for the main UI.
3. Do not keep the whole app in one giant script.
4. The UI must have multiple pages.
5. The user must configure the app before starting practice:
   - choose camera device,
   - choose MIDI input device,
   - choose optional MIDI guide file,
   - choose keyboard size: **61 keys** or **88 keys**.
6. MIDI guide file is optional:
   - If selected, enable guided song/practice mode.
   - If not selected, enable free-play/coaching mode only.
7. Add a dedicated **How To Use / Panduan** page with step-by-step instructions.
8. The camera feed and MIDI polling must not freeze the UI.
9. Do not call Tkinter/CustomTkinter widget updates directly from background threads.
10. Use queues, app state objects, or `.after()` callbacks to sync background work to UI.
11. Keep the UI wording professional but still easy for Indonesian users to understand.
12. Add clear error messages for camera, MIDI, missing MIDI file, and calibration problems.

---

## Recommended App Name
Use this name unless the user asks otherwise:

**AI Piano Coach**

Optional subtitle:

**Computer Vision + MIDI Practice Assistant**

---

## Target User Flow

### 1. Launch App
Show a clean welcome/dashboard page.

User sees:
- app title,
- short explanation,
- quick status cards for Camera, MIDI, Keyboard Size, and MIDI Guide File,
- button: `Mulai Setup`,
- button: `Free Play Cepat` only if a valid saved setup exists.

### 2. Setup Page
Before entering practice, user must configure:

#### Camera Selection
- Show available camera indices, for example:
  - `Camera 0`
  - `Camera 1`
  - `Camera 2`
- Provide a `Test Camera` button.
- Show a small camera preview or a success/fail status.

Implementation notes:
- Probe camera indices from 0 to 5 by default.
- A camera is valid if `cv2.VideoCapture(index).read()` succeeds.
- Store selected camera index in app config.

#### MIDI Input Selection
- Show detected MIDI input devices using `mido.get_input_names()`.
- Provide a `Refresh MIDI Devices` button.
- Show warning if no MIDI device is detected.
- Do not crash if MIDI is missing.

#### MIDI Guide File Selection Optional
- Provide button: `Pilih File MIDI`.
- Accept `.mid` and `.midi` files.
- Provide button: `Hapus File MIDI`.
- If no MIDI file is selected, app still works in free-play mode.

#### Keyboard Size Selection
User must choose:
- `61 Keys`
- `88 Keys`

Default can be `61 Keys` because the original prototype targeted a 61-key Roland E-X10 style setup.

Keyboard mapping rules:

| Keyboard Size | Total Keys | Lowest MIDI Note | Lowest Note | White Keys |
|---|---:|---:|---|---:|
| 61 | 61 | 36 | C2 | 36 |
| 88 | 88 | 21 | A0 | 52 |

Important:
- Do not assume `i % 12` for black keys when supporting 88 keys.
- Use actual MIDI note number modulo 12.
- Black-key MIDI pitch classes are `{1, 3, 6, 8, 10}` for C#, D#, F#, G#, A#.

### 3. Calibration Page
After setup, user calibrates the keyboard.

Required behavior:
- Show live camera feed.
- Ask the user to click 4 keyboard corners.
- Recommended order:
  1. top-left,
  2. top-right,
  3. bottom-right,
  4. bottom-left.
- Show visual markers for clicked points.
- Add buttons:
  - `Reset Titik`,
  - `Simpan Kalibrasi`,
  - `Lewati jika sudah ada kalibrasi tersimpan`.

Professional improvement:
- Prefer perspective transform or a mapping system that handles angled camera views better than a simple bounding box.
- If perspective transform is too complex for the first pass, keep a clean abstraction so it can be upgraded later.

Calibration data should be saved per camera + keyboard size.

### 4. Practice Page
This is the main coaching screen.

It should contain:
- large camera preview with piano overlay,
- current mode label:
  - `Free Play`
  - `Guided Song Practice`,
- Start/Stop buttons,
- Reset Calibration button,
- MIDI status indicator,
- camera FPS indicator if easy,
- currently pressed notes,
- target notes if guide mode is active,
- left/right hand posture status,
- fingering labels if detected.

Guided mode behavior:
- If MIDI guide file is selected, parse the song notes.
- Show target notes on the piano overlay.
- Pause progress until required notes are pressed.
- Correct pressed target = green.
- Wrong pressed note = red.
- Target note not pressed yet = guide color.

Free-play behavior:
- No MIDI target notes.
- Pressed keys are highlighted.
- Continue showing hand/finger/posture feedback.

### 5. How To Use / Panduan Page
Add a dedicated page named one of:
- `Panduan`
- `Cara Pakai`
- `How To Use`

Content must be written inside the app UI, not only in README.

Suggested page content:

1. **Hubungkan Keyboard MIDI**
   - Sambungkan keyboard ke laptop/PC via USB.
   - Pastikan driver keyboard terbaca oleh sistem.

2. **Pilih Kamera**
   - Buka halaman Setup.
   - Pilih kamera yang mengarah ke keyboard.
   - Gunakan tombol Test Camera.

3. **Pilih MIDI Input**
   - Pilih nama keyboard dari daftar MIDI.
   - Jika tidak muncul, tekan Refresh MIDI Devices.
   - Jika masih tidak muncul, cek kabel/driver.

4. **Pilih Ukuran Keyboard**
   - Pilih 61 keys untuk keyboard seperti Roland E-X10.
   - Pilih 88 keys untuk piano full-size.

5. **Pilih File MIDI Opsional**
   - Pilih file `.mid` atau `.midi` jika ingin latihan lagu.
   - Kosongkan jika hanya ingin Free Play.

6. **Kalibrasi Keyboard**
   - Klik 4 sudut area keyboard di layar kamera.
   - Pastikan kamera stabil dan keyboard terlihat penuh.
   - Simpan kalibrasi.

7. **Mulai Latihan**
   - Masuk ke Practice.
   - Tekan Start.
   - Tekan tuts sesuai target jika guided mode aktif.

8. **Arti Warna**
   - Hijau: benar / sedang ditekan.
   - Merah: salah saat guided mode.
   - Kuning/Biru muda: target nada yang harus ditekan.

9. **Tips Kamera**
   - Pakai pencahayaan terang.
   - Jangan terlalu banyak bayangan.
   - Usahakan tangan dan seluruh keyboard terlihat.

Use `CTkScrollableFrame` for this page so the guide can scroll neatly.

### 6. Settings Page
Add settings for:
- appearance mode: System / Light / Dark,
- color theme: Blue / Dark Blue / Green,
- default camera,
- default MIDI input,
- default keyboard size,
- save/load/reset calibration,
- advanced MIDI base note if needed.

### 7. Diagnostics Page Optional But Recommended
Show debug info:
- detected camera list,
- detected MIDI inputs,
- active MIDI notes,
- selected MIDI file,
- selected keyboard config,
- MediaPipe detection status,
- calibration status.

This page helps troubleshoot user hardware problems.

---

## Recommended UI Layout
Use a sidebar navigation layout.

Suggested pages:
- Dashboard
- Setup
- Calibration
- Practice
- Panduan
- Settings
- Diagnostics

Desktop window:
- Minimum size: `1100x700`
- Default size: `1280x780`
- Sidebar width: around `220`
- Main content fills remaining space.

Use CustomTkinter widgets such as:
- `CTkFrame`
- `CTkButton`
- `CTkLabel`
- `CTkOptionMenu`
- `CTkComboBox`
- `CTkRadioButton`
- `CTkSegmentedButton`
- `CTkScrollableFrame`
- `CTkTabview` if tabs are cleaner for Setup or Diagnostics.

Visual style:
- Modern dark mode by default.
- Rounded cards.
- Clear spacing.
- Status badges for hardware readiness.
- Avoid cluttering the Practice page with too much text.

---

## Recommended Project Structure
Create this structure:

```text
ai-piano-coach/
├── CLAUDE.md
├── README.md
├── requirements.txt
├── main.py
├── app/
│   ├── __init__.py
│   ├── app.py
│   ├── config.py
│   ├── constants.py
│   ├── state.py
│   ├── assets/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── camera_manager.py
│   │   ├── hand_tracker.py
│   │   ├── keyboard_mapper.py
│   │   ├── midi_input.py
│   │   ├── midi_song.py
│   │   ├── practice_engine.py
│   │   ├── posture_analyzer.py
│   │   └── overlay_renderer.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── base_page.py
│   │   ├── dashboard_page.py
│   │   ├── setup_page.py
│   │   ├── calibration_page.py
│   │   ├── practice_page.py
│   │   ├── guide_page.py
│   │   ├── settings_page.py
│   │   ├── diagnostics_page.py
│   │   └── widgets.py
│   └── utils/
│       ├── __init__.py
│       ├── file_dialogs.py
│       ├── image_utils.py
│       └── logging_utils.py
└── tests/
    ├── test_keyboard_mapper.py
    ├── test_midi_song.py
    └── test_practice_engine.py
```

---

## Module Responsibilities

### `main.py`
Entry point only.

Responsibilities:
- import app,
- start CustomTkinter main loop,
- no heavy logic.

### `app/app.py`
Main application class.

Responsibilities:
- create root window,
- configure theme,
- create sidebar,
- manage page switching,
- hold shared `AppState`,
- load/save config.

### `app/config.py`
Persistent configuration.

Use JSON config stored in a user-friendly local path, for example:
- project-local `config.json` during development,
- later upgrade to app data directory.

Config should store:
- selected camera index,
- selected MIDI input name,
- selected MIDI file path or `None`,
- keyboard size,
- base MIDI note,
- calibration points,
- appearance/theme.

### `app/state.py`
Runtime state dataclasses.

Suggested dataclasses:
- `KeyboardConfig`
- `AppConfig`
- `CalibrationState`
- `PracticeState`
- `MidiState`
- `CameraState`

### `core/camera_manager.py`
Responsibilities:
- list available cameras,
- open selected camera,
- read frames,
- release camera safely,
- avoid UI freeze.

### `core/midi_input.py`
Responsibilities:
- list MIDI inputs,
- connect selected MIDI input,
- poll pending messages,
- expose `active_notes` as a set,
- handle disconnects safely.

### `core/midi_song.py`
Responsibilities:
- load `.mid` / `.midi`,
- extract playable note events,
- ignore drum channel 9/10,
- provide target notes over time,
- support pause-until-correct practice.

### `core/keyboard_mapper.py`
Responsibilities:
- generate key rectangles for 61 or 88 keys,
- map MIDI note to screen rectangle,
- distinguish black and white keys,
- support calibration points,
- prepare for perspective transform.

Critical rule:
- Detect black keys using `midi_note % 12 in {1, 3, 6, 8, 10}`.
- Do not rely on keyboard index modulo 12.

### `core/hand_tracker.py`
Responsibilities:
- wrap MediaPipe Hands,
- return hand landmarks,
- return fingertip screen positions,
- normalize handedness labels.

### `core/posture_analyzer.py`
Responsibilities:
- calculate finger angle,
- calculate thumb-to-pinky span,
- return posture label and severity.

Keep thresholds configurable:
- stiff angle threshold,
- bent angle threshold,
- octave span threshold.

### `core/practice_engine.py`
Responsibilities:
- combine MIDI input + MIDI song target state,
- determine correct/wrong notes,
- decide when guided song can advance,
- expose render state to UI.

### `core/overlay_renderer.py`
Responsibilities:
- draw keyboard overlay,
- draw target notes,
- draw pressed notes,
- draw finger labels,
- draw calibration markers.

Keep OpenCV drawing logic here, not inside UI page classes.

---

## Threading and Realtime Rules
CustomTkinter runs on the Tkinter main thread. Do not block it.

Recommended approach:
- UI main thread owns all widgets.
- Camera frame capture can run in a background loop or scheduled `.after()` loop.
- MIDI polling can run in a background loop or scheduled `.after()` loop.
- Guided MIDI playback can run in a background thread.
- Use thread-safe queues or shared state protected by locks.
- Only update widgets from the main thread using `.after()`.

Avoid:
- long `while` loops inside UI callbacks,
- `time.sleep()` in UI callbacks,
- direct CTk widget updates inside worker threads,
- multiple unmanaged camera/MIDI handles.

---

## Keyboard Mapping Details

### 61-Key Mode
- total keys: 61
- base MIDI: 36
- lowest note: C2
- highest MIDI: 96
- white keys: 36

### 88-Key Mode
- total keys: 88
- base MIDI: 21
- lowest note: A0
- highest MIDI: 108
- white keys: 52

### Black Key Detection
Use:

```python
BLACK_PITCH_CLASSES = {1, 3, 6, 8, 10}
is_black = midi_note % 12 in BLACK_PITCH_CLASSES
```

### White Key Counting
For a selected keyboard range:
- Iterate MIDI notes from `base_midi` to `base_midi + total_keys - 1`.
- Count only non-black notes to determine white-key index.
- Use total white keys to calculate white key width.

This is required so both 61 and 88 key layouts align correctly.

---

## MIDI Guided Practice Behavior
The guided practice mode must support the old prototype behavior but in cleaner architecture.

Rules:
1. Load MIDI file only if selected.
2. Ignore drum channel.
3. Convert MIDI note events into target notes.
4. When target notes are active, wait until all required notes are pressed.
5. Allow chords.
6. Clear target notes when note-off happens.
7. Show error if MIDI file cannot be parsed.
8. Allow Stop/Restart.
9. Do not freeze the camera feed while waiting for notes.

Important:
- The original prototype used `while not waiting_notes.issubset(active_notes)`. That behavior is correct conceptually, but should be implemented without freezing UI.

---

## Professional Error Handling
Show clean UI messages for:
- no camera detected,
- selected camera cannot open,
- no MIDI input detected,
- MIDI input disconnected,
- MIDI file missing,
- invalid MIDI file,
- calibration incomplete,
- MediaPipe fails to detect hands,
- camera frame read failed.

Use status labels/cards instead of only printing to terminal.

Still log technical details to terminal or log file.

---

## Dependencies
Suggested `requirements.txt`:

```text
customtkinter
opencv-python
numpy
mido
python-rtmidi
mediapipe
Pillow
```

Optional later:

```text
pytest
pyinstaller
```

---

## Code Style Rules
- Write clean, readable Python.
- Prefer classes for app pages and core services.
- Keep UI and core logic separated.
- Use type hints where helpful.
- Use dataclasses for state/config models.
- Keep functions small and named clearly.
- Avoid global mutable state from the prototype.
- Replace slang/debug messages from the prototype with professional UI messages.
- Indonesian UI labels are allowed and preferred.
- Internal code comments may be Indonesian or English, but keep them useful.

---

## Migration Plan For Claude Code
When implementing, follow this order:

### Phase 1 — Project Skeleton
- Create folder structure.
- Add `main.py`.
- Add CustomTkinter app shell with sidebar navigation.
- Add placeholder pages.
- Add config dataclasses.

### Phase 2 — Setup Page
- Implement camera detection.
- Implement MIDI input detection.
- Implement MIDI file picker.
- Implement keyboard size selector.
- Save selected setup to config.

### Phase 3 — Camera Preview
- Implement camera manager.
- Show live camera preview inside CustomTkinter.
- Convert OpenCV frame to RGB/PIL/CTkImage safely.
- Make sure UI does not freeze.

### Phase 4 — Calibration
- Implement 4-point click calibration.
- Draw clicked points.
- Generate keyboard mapping for 61/88 keys.
- Save calibration.

### Phase 5 — MIDI Input
- Connect selected MIDI input.
- Read active notes.
- Show active notes on UI.
- Highlight pressed keys in overlay.

### Phase 6 — Hand Tracking
- Wrap MediaPipe logic.
- Detect fingertips.
- Draw hand landmarks or simplified finger markers.
- Match fingertips to key rectangles.

### Phase 7 — Practice Engine
- Add free-play mode.
- Add guided MIDI song mode.
- Implement correct/wrong note feedback.
- Implement pause-until-target-pressed logic.

### Phase 8 — Panduan Page
- Add full step-by-step guide using `CTkScrollableFrame`.
- Include troubleshooting tips.

### Phase 9 — Polish
- Add Settings.
- Add Diagnostics.
- Add reset buttons.
- Improve visual style.
- Add README.
- Add basic tests.

---

## Acceptance Criteria
The app is acceptable when:

1. App opens with a professional CustomTkinter UI.
2. User can navigate between pages.
3. User can select camera.
4. User can select MIDI input.
5. User can optionally select MIDI file.
6. User can choose 61 or 88 keys.
7. User can calibrate keyboard using camera view.
8. User can enter Practice page.
9. Pressed MIDI notes appear visually.
10. Free-play mode works without MIDI file.
11. Guided mode works with MIDI file.
12. UI does not freeze during camera preview or guided practice.
13. Panduan page explains usage step by step.
14. Settings/config persist between app launches.
15. Code is split into modules and not a single messy file.

---

## First Prompt To Run In Claude Code
Use this as the first instruction after placing this file in the project root:

```text
Read CLAUDE.md carefully. Refactor the existing pianonew.py prototype into the proposed CustomTkinter multi-page application. Start with Phase 1 and Phase 2 only: create the project skeleton, main app window, sidebar navigation, placeholder pages, config dataclasses, Setup page with camera selection, MIDI input selection, optional MIDI file picker, and keyboard size selector for 61/88 keys. Do not implement camera tracking or practice engine yet. Keep the app runnable after this phase.
```

---

## Important Notes
- Keep every phase runnable.
- Do not rewrite everything at once if it risks breaking the app.
- Prefer small working increments.
- Preserve the original prototype as reference, but move its logic into modules gradually.
- The goal is a maintainable professional desktop app, not just a prettier script.
