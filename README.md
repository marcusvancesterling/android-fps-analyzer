# Android FPS & Frame Pacing Analyzer 🚀

A lightweight, automated Python profiling utility designed for mobile game testers, reviewers, and performance engineers. It leverages Android Debug Bridge (`adb`) and `dumpsys gfxinfo` to capture raw render time histograms, calculating true frame pacing, Jank percentages, and 1% low FPS.

Developed as part of the editorial benchmark protocol at **[ModHello](https://modhello.com/author/marcus-vance-sterling/)**.

---

## 📊 Key Features

- **Real-time Frame Time Extraction:** Captures IntendedVsync, Vsync, and GPU Completion timestamps directly from SurfaceFlinger.
- **1% Low & 0.1% Low Metrics:** Identifies severe micro-stutters that average FPS counters often hide.
- **Jank Detection:** Flags any frame that exceeds the target refresh rate interval (e.g. > 16.6ms for 60Hz, > 8.3ms for 120Hz).
- **Zero Overhead:** Operates via ADB shell over USB or Wi-Fi with zero on-device performance penalty.

---

## ⚙️ Requirements

1. **Python 3.8+**
2. **Android Debug Bridge (ADB)** installed and added to your system `PATH`.
3. An Android smartphone with **USB Debugging** enabled.

---

## 🚀 Quick Start

1. Connect your Android device via USB and verify ADB connection:
```bash
adb devices
