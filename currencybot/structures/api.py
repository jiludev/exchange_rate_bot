
import asyncio 

import aiohttp

host = 'https://api.frankfurter.app/'


async def get_currencies_data(query: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(host + query) as response:
            data = await response.json(encoding='utf-8')
            return data
            
            
            
            
