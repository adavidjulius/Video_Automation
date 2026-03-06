# generate_video.py - Runs entirely on GitHub's free runners
import os
import random
import textwrap
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

class FreeLocalVideoGenerator:
    def __init__(self):
        # All assets are created programmatically - NO DOWNLOADS NEEDED
        self.width, self.height = 1080, 1920  # Vertical video (TikTok/Reels format)
        self.fps = 30
        
    def generate_script(self, topic):
        """Generate script without any API - using templates"""
        templates = {
            "tech": [
                f"Did you know that {topic} is changing the game? ",
                f"Here's why {topic} matters in 2024. ",
                f"3 mind-blowing facts about {topic}. ",
                f"The truth about {topic} revealed. ",
                f"Subscribe for more {topic} content!"
            ],
            "motivation": [
                f"Stop scrolling and listen up! ",
                f"Here's your daily dose of motivation about {topic}. ",
                f"Remember why you started with {topic}. ",
                f"Success with {topic} starts now. ",
                f"Like and share to inspire others!"
            ],
            "random": [
                f"Random fact about {topic}: ",
                f"You won't believe this {topic} hack. ",
                f"The secret to mastering {topic}. ",
                f"Day 1 of learning {topic}. ",
                f"Follow for daily {topic} tips!"
            ]
        }
        
        # Pick random category or use tech as default
        category = random.choice(list(templates.keys()))
        script_parts = templates.get(category, templates["tech"])
        
        # Combine into full script
        full_script = " ".join(script_parts)
        return full_script, script_parts
    
    def create_background(self, scene_index, style="gradient"):
        """Create dynamic backgrounds using pure Python"""
        # Create solid color or gradient background
        if style == "gradient":
            # Create gradient
            array = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            for i in range(self.height):
                # Random color scheme based on scene index
                r = int(100 + 155 * (i / self.height) + scene_index * 50) % 255
                g = int(50 + 205 * (i / self.height) + scene_index * 30) % 255
                b = int(150 + 105 * (i / self.height) + scene_index * 70) % 255
                array[i, :, :] = [r, g, b]
            
            img = Image.fromarray(array)
        else:
            # Solid color with slight variation
            color = (
                random.randint(50, 200),
                random.randint(50, 200),
                random.randint(50, 200)
            )
            img = Image.new('RGB', (self.width, self.height), color)
            
            # Add some texture/noise
            pixels = img.load()
            for i in range(self.width):
                for j in range(self.height):
                    if random.random() > 0.95:  # 5% chance of noise
                        pixels[i, j] = tuple(min(255, c + 30) for c in pixels[i, j])
        
        # Save image
        img_path = f"bg_{scene_index}.png"
        img.save(img_path)
        return img_path
    
    def create_text_overlay(self, text, scene_index):
        """Create text overlay with effects"""
        # Create a transparent image for text
        img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Use default PIL font (no downloads needed)
        try:
            # Try to use a larger default font
            font = ImageFont.load_default()
            # Scale up by creating larger font
            font = ImageFont.load_default().font_variant(size=60)
        except:
            font = ImageFont.load_default()
        
        # Wrap text
        wrapper = textwrap.TextWrapper(width=20)
        lines = wrapper.wrap(text=text)
        
        # Calculate text position
        y_start = self.height // 3
        line_height = 70
        
        # Draw each line with outline effect
        for i, line in enumerate(lines):
            # Get text size (approximate)
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (self.width - text_width) // 2
            y = y_start + i * line_height
            
            # Draw outline (multiple passes)
            outline_range = 3
            for dx in [-outline_range, 0, outline_range]:
                for dy in [-outline_range, 0, outline_range]:
                    if dx != 0 or dy != 0:
                        draw.text((x + dx, y + dy), line, font=font, fill='black')
            
            # Draw main text
            draw.text((x, y), line, font=font, fill='white')
        
        # Save with transparency
        text_path = f"text_{scene_index}.png"
        img.save(text_path)
        return text_path
    
    def add_visual_effects(self, clip):
        """Add cool effects without external assets"""
        # Add some random effects
        effect = random.choice(['fade', 'slide', 'zoom', 'rotate'])
        
        if effect == 'fade':
            return clip.crossfadein(0.5)
        elif effect == 'zoom':
            return clip.resize(lambda t: 1 + 0.1 * t)
        else:
            return clip
    
    def create_video(self, topic, duration=15):
        """Main video creation function"""
        print(f"🎬 Creating video about: {topic}")
        
        # Generate script
        full_script, script_parts = self.generate_script(topic)
        
        # Create clips for each script part
        clips = []
        per_scene_duration = duration / len(script_parts)
        
        for i, text in enumerate(script_parts):
            print(f"  Scene {i+1}: {text[:50]}...")
            
            # Create background
            bg_path = self.create_background(i, random.choice(['gradient', 'solid']))
            
            # Create text overlay
            text_path = self.create_text_overlay(text, i)
            
            # Create video clip
            bg_clip = ImageClip(bg_path, duration=per_scene_duration)
            text_clip = ImageClip(text_path, duration=per_scene_duration, transparent=True)
            
            # Combine
            scene_clip = CompositeVideoClip([bg_clip, text_clip])
            
            # Add effects
            scene_clip = self.add_visual_effects(scene_clip)
            
            clips.append(scene_clip)
        
        # Add transitions between scenes
        final_clip = concatenate_videoclips(clips, method="compose")
        
        # Generate synthetic voiceover (beep tones as placeholders)
        print("🔊 Creating audio...")
        audio_clips = []
        for text in script_parts:
            # Create simple tone for each scene (just for rhythm)
            tone = AudioClip(lambda t: 0.1 * np.sin(440 * 2 * np.pi * t), 
                           duration=per_scene_duration, fps=44100)
            audio_clips.append(tone)
        
        final_audio = concatenate_audioclips(audio_clips)
        final_clip = final_clip.set_audio(final_audio)
        
        # Write final video
        output_path = f"output_{topic.replace(' ', '_')}.mp4"
        print(f"💾 Rendering video: {output_path}")
        final_clip.write_videofile(output_path, fps=self.fps, 
                                  codec='libx264', audio_codec='aac')
        
        # Cleanup temp files
        for i in range(len(script_parts)):
            try:
                os.remove(f"bg_{i}.png")
                os.remove(f"text_{i}.png")
            except:
                pass
        
        return output_path
        # Add these enhancements (still free!)
def add_background_music(self):
    """Generate synthetic music"""
    import numpy as np
    duration = 15
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Create simple melody
    frequencies = [440, 554, 659, 880]  # A, C#, E, A
    music = np.zeros_like(t)
    
    for i, freq in enumerate(frequencies):
        segment_start = i * len(t) // len(frequencies)
        segment_end = (i + 1) * len(t) // len(frequencies)
        music[segment_start:segment_end] = 0.1 * np.sin(2 * np.pi * freq * t[segment_start:segment_end])
    
    return AudioClip(lambda t: music[int(t * sample_rate) % len(music)], 
                    duration=duration, fps=sample_rate)

# Run it!
if __name__ == "__main__":
    import sys
    topic = sys.argv[1] if len(sys.argv) > 1 else "Python Programming"
    generator = FreeLocalVideoGenerator()
    video_path = generator.create_video(topic, duration=15)
    print(f"✅ Video created: {video_path}")
