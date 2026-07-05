"""
AI Piano Coach - Main Entry Point
Start the AI Piano Coach application.
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk


def main():
    """Main entry point for AI Piano Coach."""
    print("=" * 50)
    print("AI Piano Coach - Starting...")
    print("=" * 50)

    try:
        # Import app
        from app.app import AIPianoCoachApp

        # Create and run app
        app = AIPianoCoachApp()
        app.mainloop()

    except ImportError as e:
        print(f"\n[ERROR] Import Error: {e}")
        print("\nPastikan semua dependencies sudah terinstall:")
        print("  pip install customtkinter opencv-python numpy mido python-rtmidi mediapipe Pillow")
        sys.exit(1)

    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    finally:
        print("\nAI Piano Coach closed. Goodbye!")


if __name__ == "__main__":
    main()