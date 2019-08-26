import asyncio
import json

import aiohttp


class Client():
    url = "http://localhost:8080"

    async def parse_result(self, response):
        if response.status == 400:
            return {
                "cause": await response.text(),
                "status": response.status,
                "result": {
                    "data": None
                }
            }
        else:
            return {
                "cause": None,
                "status": response.status,
                "result": json.loads(await response.text()),
            }

    def do_request(self, url, data, method_type):
        loop = asyncio.get_event_loop()
        res = loop.run_until_complete(self.do_single(url, data, method_type))
        return res

    async def fetch(self, session, url_path, data, method_type):
        data = json.dumps(data)

        if method_type == "post":
            async with session.post(self.url + url_path, data=data) as response:
                return await self.parse_result(response)
        elif method_type == "patch":
            async with session.patch(self.url + url_path, data=data) as response:
                return await self.parse_result(response)
        elif method_type == "get":
            async with session.get(self.url + url_path) as response:
                return await self.parse_result(response)
        else:
            return "unknown method type"

    async def do_single(self, url_path, data, method_type):
        async with aiohttp.ClientSession() as session:
            return await self.fetch(session, url_path, data, method_type)
