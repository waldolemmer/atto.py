import AttoNode
import httpx
import asyncio
from typing import AsyncIterator

async def _stream_lines(url):
    async with httpx.AsyncClient() as client:
        async with client.stream("GET", url) as response:
            async for line in response.aiter_lines():
                print(f"Got line: {line}")

asyncio.run(stream_lines("http://example.com/stream"))

class Stream:
    def __init__(self, type_, stream):
        self.type_ = type_
        self.stream_path = stream
    
    def newer(self):
        return AttoNode._get_as_dict(self.stream_path)


