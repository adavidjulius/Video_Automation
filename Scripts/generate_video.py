import os
import sys
import random
import textwrap
import numpy as np
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont

class FreeVideoGenerator:
    def __init__(self):
        self.width, self.height = 1080, 1920   # Vertical (Reels/Shorts)
        self.fps = 24
        self.duration_per_scene = 5            # seconds

    def get_topic(self):
        """Get topic from command line or use default"""
        if len(sys.argv) > 1:
            return sys.argv[1]
        return "Tech Facts"

    def generate_script_parts(self, topic):
        """Generate script lines without any API"""
        templates = [
            f"Did you know about {topic}?",
            f"Here's a crazy fact: {topic} is everywhere!",
            f"3 reasons why {topic} matters:",
            f"Number one: It's changing the world.",
            f"Number two: You use it every day.",
            f"Number three: The future belongs to {topic}.",
            f"Subscribe for more {topic} content!"
        ]
        # Shuffle and pick first 5 to keep video short
        random.shuffle(templates)
        return templates[:5]

    def create_gradient_background(self, index):
        """Create a gradient image using numpy"""
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        # Random color offsets based on index
        r_offset = (index * 50) % 256
        g_offset = (index * 80) % 256
        b_offset = (index * 110) % 256

        for y in range(self.height):
            # Smooth gradient
            r = int(100 + 155 * (y / self.height) + r_offset) % 256
            g = int(50 + 205 * (y / self.height) + g_offset) % 256
            b = int(150 + 105 * (y / self.height) + b_offset) % 256
            frame[y, :, :] = [r, g, b]

        img_path = f"bg_{index}.png"
        Image.fromarray(frame).save(img_path)
        return img_path

    def create_text_image(self, text, index):
        """Create text overlay with outline"""
        img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Use default font (scaled up)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
        except:
            font = ImageFont.load_default()

        # Wrap text
        wrapper = textwrap.TextWrapper(width=15)
        lines = wrapper.wrap(text=text)

        y_start = self.height // 3
        line_height = 100

        for i, line in enumerate(lines):
            # Get text size
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (self.width - text_width) // 2
            y = y_start + i * line_height

            # Draw outline (black)
            for dx in (-4, 0, 4):
                for dy in (-4, 0, 4):
                    if dx != 0 or dy != 0:
                        draw.text((x+dx, y+dy), line, font=font, fill='black')

            # Draw main text (white)
            draw.text((x, y), line, font=font, fill='white')

        text_path = f"text_{index}.png"
        img.save(text_path)
        return text_path

    def create_video(self):
        topic = self.get_topic()
        print(f"🎬 Generating video about: {topic}")

        script_parts = self.generate_script_parts(topic)
        clips = []

        for i, text in enumerate(script_parts):
            print(f"  Scene {i+1}: {text[:40]}...")

            # Create background and text images
            bg_path = self.create_gradient_background(i)
            text_path = self.create_text_image(text, i)

            # Create clips
            bg_clip = ImageClip(bg_path, duration=self.duration_per_scene)
            text_clip = ImageClip(text_path, duration=self.duration_per_scene, transparent=True)

            # Composite
            scene = CompositeVideoClip([bg_clip, text_clip])

            # Add a simple zoom effect
            scene = scene.resize(lambda t: 1 + 0.02 * t)  # slow zoom in
            clips.append(scene)

        # Concatenate all scenes
        final_video = concatenate_videoclips(clips, method="compose")

        # Generate a simple synthetic audio (beep per scene)
        audio_clips = []
        for _ in script_parts:
            tone = AudioClip(lambda t: 0.1 * np.sin(440 * 2 * np.pi * t),
                             duration=self.duration_per_scene, fps=44100)
            audio_clips.append(tone)
        final_audio = concatenate_audioclips(audio_clips)
        final_video = final_video.set_audio(final_audio)

        # Output filename
        safe_topic = topic.replace(' ', '_').replace('/', '_')
        output_path = f"{safe_topic}.mp4"
        final_video.write_videofile(output_path, fps=self.fps, codec='libx264', audio_codec='aac')

        # Cleanup temporary images
        for i in range(len(script_parts)):
            for f in [f"bg_{i}.png", f"text_{i}.png"]:
                if os.path.exists(f):
                    os.remove(f)

        print(f"✅ Video saved: {output_path}")
        return output_path

if __name__ == "__main__":
    generator = FreeVideoGenerator()
    generator.create_video()
