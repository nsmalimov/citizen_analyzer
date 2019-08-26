import aiohttp
import asyncio
import json


class Client():
    url = "http://localhost:8080"

    def do_request(self, url, data, method_type):
        loop = asyncio.get_event_loop()
        res = loop.run_until_complete(self.do_single(url, data))
        return res

    async def fetch(self, session, url_path, data):
        data = json.dumps(data)

        async with session.post(self.url + url_path, data=data) as response:
            if response.status == 400:
                return {
                    "cause": await response.text(),
                    "status": response.status
                }
            else:
                return {
                    "cause": None,
                    "status": response.status,
                    "result": await response.text(),
                }

    async def do_single(self, url_path, data):
        async with aiohttp.ClientSession() as session:
            return await self.fetch(session, url_path, data)
