import json
import logging
import uuid
import asyncio
from aiohttp import web

from db.connector import connect_to_db
from workers.db_workers.worker import save_import_in_db, user_by_id_and_citizen_id_exist_in_db, patch_in_db, \
    get_all_citizens_by_import_id
from workers.processing.import_data import validate_request_import, validate_request_patch
from workers.util.util_funcs import prepare_user_data_to_response_from_db


class Handler:
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
                await save_import_in_db(request.app.db_connect, request_data, import_id)
            except Exception as e:
                logging.error(e)
                return web.Response(text=str(e), status=500)
        else:
            logging.info("not valid")

            return web.Response(text=cause, status=400)

        return web.Response(text=json.dumps(res), status=201, content_type="application/json")

    async def patch_imports_handler(self, request):
        import_id = request.match_info.get("import_id", None)
        citizen_id = request.match_info.get("citizen_id", None)

        logging.info("patch_imports_handler, import_id: " + import_id + ", citizen_id: " + str(citizen_id))

        try:
            request_data = await request.json()
        except Exception as e:
            logging.error(e)
            return web.Response(status=400)

        # присутствует ли user в базе
        if await user_by_id_and_citizen_id_exist_in_db(request.app.db_connect, import_id, citizen_id) is None:
            s = "import_id: " + import_id + ", citizen_id:" + citizen_id + " not exist in db"
            logging.info(s)
            return web.Response(text=s, status=400)
        else:
            is_valid, cause = validate_request_patch(request_data, citizen_id)

            if not (is_valid):
                logging.info("not valid")
                return web.Response(text=cause, status=400)
            else:
                try:
                    await patch_in_db(request.app.db_connect, request_data, import_id, citizen_id)

                    # todo: упростить (без запроса, обмен в дикте)
                    user_info = await user_by_id_and_citizen_id_exist_in_db(request.app.db_connect,
                                                                            import_id, citizen_id)

                    user_info = prepare_user_data_to_response_from_db(user_info)

                    res = {
                        "data": user_info
                    }

                    return web.Response(text=json.dumps(res), status=200, content_type="application/json")
                except Exception as e:
                    logging.error(e)
                    return web.Response(text=str(e), status=500)

    async def get_all_citizens_handler(self, request):
        import_id = request.match_info.get("import_id", None)

        logging.info("get_all_citizens_handler, import_id: " + import_id)

        try:
            all_citizens_data = await get_all_citizens_by_import_id(request.app.db_connect, import_id)
        except Exception as e:
            logging.error(e)
            return web.Response(text=str(e), status=500)

        for index, elem in enumerate(all_citizens_data):
            all_citizens_data[index] = prepare_user_data_to_response_from_db(all_citizens_data[index])

        res = {
            "data": all_citizens_data
        }

        print (res)

        return web.Response(text=json.dumps(res), status=200, content_type="application/json")

    # optional
    async def get_citizens_by_gifts_handler(self, request):
        import_id = request.match_info.get("import_id", None)

        text = "ok"
        return web.Response(text=text)

    # optional
    async def get_stats_handler(self, request):
        import_id = request.match_info.get("import_id", None)

        text = "ok"
        return web.Response(text=text)


def init_app(log_level, db_connect):
    app = web.Application()

    hanlder = Handler()
    hanlder.db = db_connect

    logging.basicConfig(level=log_level)

    app.add_routes([web.get("/", hanlder.handle),

                    web.post("/imports", hanlder.post_imports_handler),

                    web.patch("/imports/{import_id}/citizens/{citizen_id}", hanlder.patch_imports_handler),

                    web.get("/imports/{import_id}/citizens", hanlder.get_all_citizens_handler),

                    web.get("/imports/{import_id}/citizens/birthdays", hanlder.get_citizens_by_gifts_handler),

                    web.get("/imports/{import_id}/towns/stat/percentile/age", hanlder.get_stats_handler)])

    app.db_connect = hanlder.db

    return app


async def on_shutdown(app):
    logging.info("on_shutdown")
    await app.db_connect.close()


def main():
    db_host = "84.201.129.208"
    log_level = logging.INFO

    loop = asyncio.get_event_loop()
    db_connection = loop.run_until_complete(connect_to_db(db_host))

    app = init_app(log_level, db_connection)

    app.on_shutdown.append(on_shutdown)
    web.run_app(app)


if __name__ == "__main__":
    main()
