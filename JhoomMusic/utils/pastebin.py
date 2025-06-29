import aiohttp
import asyncio
from typing import Optional

class PasteBin:
    def __init__(self):
        self.base_url = "https://nekobin.com"
    
    async def paste(self, content: str, title: str = "JhoomMusic Log") -> Optional[str]:
        """Upload content to pastebin"""
        try:
            data = {
                "title": title,
                "content": content
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/documents", 
                    json=data
                ) as response:
                    if response.status == 201:
                        result = await response.json()
                        return f"{self.base_url}/{result['result']['key']}"
                    return None
        except Exception as e:
            print(f"Error uploading to pastebin: {e}")
            return None

# Global instance
paste = PasteBin()