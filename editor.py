# editor.py

import os
import glob
import config  # ✅ Import once, use everywhere
from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip

def get_filename(path):
    return path.strip().split('/')[-1].split('\\')[-1]

def create_split_screen_videos():
    if not os.path.exists(config.EDITED_DIR):
        os.makedirs(config.EDITED_DIR, exist_ok=True)

    video_files = sorted(glob.glob(os.path.join(config.DOWNLOAD_DIR, "*.mp4")))
    print(f"[📄] Found {len(video_files)} videos to process")

    if len(video_files) < 2:
        print("[⚠️] Not enough videos to pair.")
        return []

    pairs = [(video_files[i], video_files[i+1]) for i in range(0, len(video_files) - 1, 2)]
    edited_paths = []

    for idx, (left_path, right_path) in enumerate(pairs):
        try:
            left_name = get_filename(left_path)
            right_name = get_filename(right_path)
            print(f"[🎬] Editing Pair {idx+1}: {left_name} → {right_name}")

            left_clip = VideoFileClip(left_path)
            right_clip = VideoFileClip(right_path)

            # Resize for vertical split-screen
            left_resized = left_clip.resize(height=config.VIDEO_HEIGHT).set_position(("left", "center"))
            right_resized = right_clip.resize(height=config.VIDEO_HEIGHT).set_position(("right", "center"))

            total_duration = left_clip.duration + right_clip.duration
            background = ColorClip(size=(config.VIDEO_WIDTH, config.VIDEO_HEIGHT), color=(0,0,0)).set_duration(total_duration)

            # Timing
            left_phase = left_resized.set_start(0)
            right_phase = right_resized.set_start(left_clip.duration)

            # Build visual clip
            final_clip = CompositeVideoClip([
                background,
                left_phase,
                right_phase
            ], size=(config.VIDEO_WIDTH, config.VIDEO_HEIGHT))

            # 🔊 AUDIO HANDLING – Use config.REMOVE_AUDIO dynamically
            if config.REMOVE_AUDIO:
                print(f"[🔇] Audio removed by user choice.")
                final_clip = final_clip.set_audio(None)
            else:
                try:
                    combined_audio = left_clip.audio.audio_fadeout(1).concatenate_audio(right_clip.audio.audio_fadein(1))
                    final_clip = final_clip.set_audio(combined_audio)
                    print(f"[🔊] Audio preserved and stitched.")
                except Exception as e:
                    print(f"[⚠️] Audio error (using silent): {e}")
                    final_clip = final_clip.set_audio(None)

            # Export
            output_path = os.path.join(config.EDITED_DIR, f"comparison_{idx+1}.mp4")
            final_clip.write_videofile(
                output_path,
                fps=30,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                threads=4,
                preset='fast'
            )

            edited_paths.append(output_path)
            print(f"[✅] Saved: {output_path}")

            # Close clips
            left_clip.close()
            right_clip.close()
            final_clip.close()

        except Exception as e:
            print(f"[❌] Failed to edit pair {idx+1}: {str(e)}")
            continue

    return edited_paths
