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
```

2. Launch your game on the phone (e.g., *PUBG Mobile*, *Homescapes*, or *Genshin Impact*).

3. Run the analyzer with the target package name:
```bash
python fps_analyzer.py --package com.playrix.homescapes --target-fps 60
```

4. Play for 60 seconds. The script will output an instant terminal report:
```text
============================================================
              GAMEPLAY BENCHMARK REPORT
============================================================
Package:           com.playrix.homescapes
Target Refresh:    60 FPS (16.67ms budget)
Total Frames:      3,580
------------------------------------------------------------
Average FPS:       59.2 FPS
1% Low FPS:        51.4 FPS
0.1% Low FPS:      42.1 FPS
Jank Ratio:        1.42% (51 janky frames)
Frame Time (p95):  16.82 ms
Frame Time (p99):  19.45 ms
============================================================
Verdict: PASS - Smooth gameplay with minimal micro-stutters.
```

---

## 📖 Methodology & Testing Guidelines

For our complete 4-step hardware benchmarking methodology across Snapdragon and Dimensity chips, visit our editorial review guidelines at:
👉 **[ModHello Editorial Review Standards](https://modhello.com/author/marcus-vance-sterling/)**

---

## 📄 License
MIT License. Maintained by **Marcus Vance Sterling** ([@marcusvancesterling](https://github.com/marcusvancesterling)).
