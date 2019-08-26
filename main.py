import json
import logging
import uuid
import asyncio
from aiohttp import web

from db.connector import connect_to_db
from workers.db_workers.worker import save_import_in_db, user_by_id_and_citizen_id_exist_in_db, path_in_db
from workers.processing.import_data import validate_request_import, validate_request_patch


class Handler:
    db = None

    def __init__(self):
        pass

    # todo: выдавать причину ошибки

    async def handle(self, request):
        logging.info("handle")

        text = "ping"
        return web.Response(text=text)

    async def post_imports_handler(self, request):
        logging.info("post_imports_handler")

        import_id = str(uuid.uuid4())

        res = {
            "data": {
                "import_id": import_id
            }
        }

        try:
            request_data = await request.json()
        except Exception as e:
            logging.error(e)
            return web.Response(status=400)

        is_valid, cause = validate_request_import(request_data)
        if is_valid:
            logging.info("valid")

            try:
                await save_import_in_db(self.db, request_data, import_id)
            except Exception as e:
                logging.error(e)
                return web.Response(status=500)
        else:
            logging.info("not valid")

            error_res = cause

            return web.Response(text=cause, status=400, content_type="application/json")

        return web.Response(text=json.dumps(res), status=201, content_type="application/json")

    async def patch_imports_handler(self, request):
        import_id = request.match_info.get('import_id', None)
        citizen_id = request.match_info.get('citizen_id', None)

        logging.info("patch_imports_handler, import_id: ", import_id, ", citizen_id: ", citizen_id)

        try:
            request_data = await request.json()
        except Exception as e:
            logging.error(e)
            return web.Response(status=400)

        if await user_by_id_and_citizen_id_exist_in_db(self.db, import_id, citizen_id):
            logging.info("user not exist in db")
            return web.Response(status=400)
        else:
            if validate_request_patch(request_data):
                logging.info("not valid")
                return web.Response(status=400)

        try:
            res = await path_in_db(self.db, request_data, import_id)

            return web.Response(text=json.dumps(res), status=201, content_type="application/json")
        except Exception as e:
            return web.Response(status=500)

    async def get_all_citizens_handler(self, request):
        import_id = request.match_info.get('import_id', None)

        text = "ok"
        return web.Response(text=text)

    async def get_citizens_by_gifts_handler(self, request):
        import_id = request.match_info.get('import_id', None)

        text = "ok"
        return web.Response(text=text)

    async def get_stats_handler(self, request):
        import_id = request.match_info.get('import_id', None)

        text = "ok"
        return web.Response(text=text)


def init_app(log_level, conn):
    app = web.Application()

    hanlder = Handler()
    hanlder.db = conn

    logging.basicConfig(level=log_level)

    app.add_routes([web.get('/', hanlder.handle),

                    web.post('/imports', hanlder.post_imports_handler),

                    web.patch('/imports/{import_id}/citizens/{citizen_id}', hanlder.patch_imports_handler),

                    web.get('/imports/{import_id}/citizens', hanlder.get_all_citizens_handler),

                    web.get('/imports/{import_id}/citizens/birthdays', hanlder.get_citizens_by_gifts_handler),

                    web.get('/imports/{import_id}/towns/stat/percentile/age', hanlder.get_stats_handler)])

    return app, conn


def main():
    conn = None

    db_host = "84.201.129.208"
    log_level = logging.INFO

    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(connect_to_db(db_host))

    try:
        app, conn = init_app(log_level, res)
        web.run_app(app)
    finally:
        if conn:
            conn.close()
            logging.info("conn.close")


if __name__ == "__main__":
    main()
