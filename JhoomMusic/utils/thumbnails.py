import os
import aiohttp
import aiofiles
from PIL import Image, ImageDraw, ImageFont
from typing import Optional

class ThumbnailGenerator:
    def __init__(self):
        self.cache_dir = "cache/thumbnails"
        os.makedirs(self.cache_dir, exist_ok=True)
    
    async def download_image(self, url: str, filename: str) -> Optional[str]:
        """Download image from URL"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        file_path = os.path.join(self.cache_dir, filename)
                        async with aiofiles.open(file_path, 'wb') as f:
                            await f.write(await response.read())
                        return file_path
            return None
        except Exception as e:
            print(f"Error downloading image: {e}")
            return None
    
    def create_thumbnail(
        self, 
        title: str, 
        duration: str = "Unknown", 
        requester: str = "Unknown",
        background_path: Optional[str] = None
    ) -> str:
        """Create custom thumbnail"""
        try:
            # Create image
            width, height = 1280, 720
            img = Image.new('RGB', (width, height), color='#1a1a1a')
            draw = ImageDraw.Draw(img)
            
            # Load background if provided
            if background_path and os.path.exists(background_path):
                try:
                    bg = Image.open(background_path)
                    bg = bg.resize((width, height))
                    img.paste(bg, (0, 0))
                    
                    # Add overlay
                    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 128))
                    img = Image.alpha_composite(img.convert('RGBA'), overlay)
                    img = img.convert('RGB')
                except:
                    pass
            
            # Try to load fonts
            try:
                title_font = ImageFont.truetype("arial.ttf", 60)
                info_font = ImageFont.truetype("arial.ttf", 40)
            except:
                try:
                    title_font = ImageFont.load_default()
                    info_font = ImageFont.load_default()
                except:
                    title_font = None
                    info_font = None
            
            # Draw title
            if title_font:
                # Wrap title text
                max_width = width - 100
                words = title.split()
                lines = []
                current_line = []
                
                for word in words:
                    test_line = ' '.join(current_line + [word])
                    bbox = draw.textbbox((0, 0), test_line, font=title_font)
                    if bbox[2] - bbox[0] <= max_width:
                        current_line.append(word)
                    else:
                        if current_line:
                            lines.append(' '.join(current_line))
                            current_line = [word]
                        else:
                            lines.append(word)
                
                if current_line:
                    lines.append(' '.join(current_line))
                
                # Draw title lines
                y_offset = height // 2 - (len(lines) * 70) // 2
                for line in lines[:3]:  # Max 3 lines
                    bbox = draw.textbbox((0, 0), line, font=title_font)
                    text_width = bbox[2] - bbox[0]
                    x = (width - text_width) // 2
                    draw.text((x, y_offset), line, fill='white', font=title_font)
                    y_offset += 70
                
                # Draw info
                info_text = f"Duration: {duration} | Requested by: {requester}"
                bbox = draw.textbbox((0, 0), info_text, font=info_font)
                text_width = bbox[2] - bbox[0]
                x = (width - text_width) // 2
                y = height - 100
                draw.text((x, y), info_text, fill='#cccccc', font=info_font)
            
            # Save thumbnail
            filename = f"thumb_{hash(title)}.jpg"
            file_path = os.path.join(self.cache_dir, filename)
            img.save(file_path, "JPEG", quality=85)
            
            return file_path
            
        except Exception as e:
            print(f"Error creating thumbnail: {e}")
            return None
    
    def cleanup_thumbnails(self):
        """Clean up old thumbnails"""
        try:
            for filename in os.listdir(self.cache_dir):
                file_path = os.path.join(self.cache_dir, filename)
                if os.path.isfile(file_path):
                    # Remove files older than 1 hour
                    if time.time() - os.path.getctime(file_path) > 3600:
                        os.remove(file_path)
        except Exception as e:
            print(f"Error cleaning thumbnails: {e}")

# Global instance
thumb_gen = ThumbnailGenerator()