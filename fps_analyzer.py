
---

### 2.2. File `fps_analyzer.py`

```python
#!/usr/bin/env python3
"""
Android FPS & Frame Pacing Analyzer
Author: Marcus Vance Sterling (Lead Reviewer @ ModHello)
GitHub: https://github.com/marcusvancesterling
"""

import argparse
import subprocess
import time
import sys

def parse_gfxinfo(package_name):
    try:
        output = subprocess.check_output(
            ["adb", "shell", "dumpsys", "gfxinfo", package_name, "framestats"],
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running ADB command: {e.output}")
        return []

    lines = output.splitlines()
    frame_times_ms = []

    in_framestats = False
    for line in lines:
        line = line.strip()
        if "Flags,IntendedVsync" in line:
            in_framestats = True
            continue
        if in_framestats:
            if not line or "---PROFILEDATA---" in line:
                break
            parts = line.split(",")
            if len(parts) >= 14:
                try:
                    intended_vsync = int(parts[1])
                    frame_completed = int(parts[13])
                    duration_ns = frame_completed - intended_vsync
                    duration_ms = duration_ns / 1_000_000.0
                    if 0.5 < duration_ms < 500:  # Ignore idle/sleep frames
                        frame_times_ms.append(duration_ms)
                except ValueError:
                    continue

    return frame_times_ms

def compute_metrics(frame_times, target_fps=60):
    if not frame_times:
        return None

    frame_times_sorted = sorted(frame_times)
    total_frames = len(frame_times)
    total_time_s = sum(frame_times) / 1000.0
    avg_fps = total_frames / total_time_s if total_time_s > 0 else 0

    target_budget_ms = 1000.0 / target_fps
    janky_frames = sum(1 for t in frame_times if t > (target_budget_ms * 1.15))
    jank_ratio = (janky_frames / total_frames) * 100.0

    # Percentiles
    idx_p95 = int(total_frames * 0.95)
    idx_p99 = int(total_frames * 0.99)
    p95_ms = frame_times_sorted[idx_p95] if idx_p95 < total_frames else frame_times_sorted[-1]
    p99_ms = frame_times_sorted[idx_p99] if idx_p99 < total_frames else frame_times_sorted[-1]

    # 1% Low and 0.1% Low
    one_percent_count = max(1, int(total_frames * 0.01))
    point_one_percent_count = max(1, int(total_frames * 0.001))
    
    worst_1_percent = frame_times_sorted[-one_percent_count:]
    worst_0_1_percent = frame_times_sorted[-point_one_percent_count:]

    avg_1_percent_ms = sum(worst_1_percent) / len(worst_1_percent)
    avg_0_1_percent_ms = sum(worst_0_1_percent) / len(worst_0_1_percent)

    fps_1_low = 1000.0 / avg_1_percent_ms if avg_1_percent_ms > 0 else 0
    fps_0_1_low = 1000.0 / avg_0_1_percent_ms if avg_0_1_percent_ms > 0 else 0

    return {
        "total_frames": total_frames,
        "avg_fps": round(avg_fps, 1),
        "fps_1_low": round(fps_1_low, 1),
        "fps_0_1_low": round(fps_0_1_low, 1),
        "jank_ratio": round(jank_ratio, 2),
        "janky_frames": janky_frames,
        "p95_ms": round(p95_ms, 2),
        "p99_ms": round(p99_ms, 2),
        "target_budget_ms": round(target_budget_ms, 2),
    }

def main():
    parser = argparse.ArgumentParser(description="Android Frame Pacing & FPS Profiler")
    parser.add_argument("--package", required=True, help="Android package name (e.g. com.dts.freefireth)")
    parser.add_argument("--target-fps", type=int, default=60, help="Target screen refresh rate (60, 90, 120)")
    parser.add_argument("--duration", type=int, default=15, help="Sampling duration in seconds")
    args = parser.parse_args()

    print(f"🚀 Profiling {args.package} for {args.duration} seconds...")
    print("Resetting gfxinfo buffer...")
    subprocess.run(["adb", "shell", "dumpsys", "gfxinfo", args.package, "reset"], stdout=subprocess.DEVNULL)

    time.sleep(args.duration)

    frame_times = parse_gfxinfo(args.package)
    metrics = compute_metrics(frame_times, args.target_fps)

    if not metrics:
        print("⚠️ No frame data collected. Ensure the game is running actively in the foreground.")
        sys.exit(1)

    print("\n" + "=" * 56)
    print("             GAMEPLAY BENCHMARK REPORT")
    print("=" * 56)
    print(f"Package:           {args.package}")
    print(f"Target Refresh:    {args.target_fps} FPS ({metrics['target_budget_ms']}ms budget)")
    print(f"Total Frames:      {metrics['total_frames']}")
    print("-" * 56)
    print(f"Average FPS:       {metrics['avg_fps']} FPS")
    print(f"1% Low FPS:        {metrics['fps_1_low']} FPS")
    print(f"0.1% Low FPS:      {metrics['fps_0_1_low']} FPS")
    print(f"Jank Ratio:        {metrics['jank_ratio']}% ({metrics['janky_frames']} janky frames)")
    print(f"Frame Time (p95):  {metrics['p95_ms']} ms")
    print(f"Frame Time (p99):  {metrics['p99_ms']} ms")
    print("=" * 56)

if __name__ == "__main__":
    main()
