import asyncio
import json
import logging
import uuid

import numpy as np
from aiohttp import web

from db.connector import connect_to_db
from workers.db_workers.worker import save_import_in_db, get_user_data_by_id_and_citizen_id, patch_in_db, \
    get_all_citizens_by_import_id, update_relations_data_in_db
from workers.processing.import_data import validate_request_import, validate_request_patch
from workers.util.util_funcs import prepare_user_data_to_response_from_db, calc_age_by_birth_date


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

        user_from_db = await get_user_data_by_id_and_citizen_id(request.app.db_connect, import_id, citizen_id)
        # присутствует ли user в базе
        if user_from_db is None:
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
                    user_info = await get_user_data_by_id_and_citizen_id(request.app.db_connect,
                                                                         import_id, citizen_id)

                    if "relatives" in request_data:
                        await update_relations_data_in_db(request.app.db_connect, import_id,
                                                          user_from_db["relatives"], request_data["relatives"],
                                                          citizen_id)

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

        return web.Response(text=json.dumps(res), status=200, content_type="application/json")

    # optional
    async def get_citizens_by_gifts_handler(self, request):
        import_id = request.match_info.get("import_id", None)

        logging.info("get_citizens_by_gifts_handler, import_id: " + import_id)

        try:
            all_citizens_data = await get_all_citizens_by_import_id(request.app.db_connect, import_id)
        except Exception as e:
            logging.error(e)
            return web.Response(text=str(e), status=500)

        if all_citizens_data == []:
            return web.Response(text="no import_id in db", status=400)

        citizens_birth_month_dict = {}

        for i in all_citizens_data:
            citizens_birth_month_dict[i["citizen_id"]] = i["birth_date"].month

        months_dict = {}

        for i in range(12):
            months_dict[str(i + 1)] = []

        for i in all_citizens_data:
            citizen_data = dict(i)
            for relate in citizen_data["relatives"]:
                month_num = str(citizens_birth_month_dict[relate])

                not_added = True

                for index, j in enumerate(months_dict[month_num]):
                    if j["citizen_id"] == citizen_data["citizen_id"]:
                        months_dict[month_num][index]["presents"] += 1
                        not_added = False

                if not_added:
                    months_dict[month_num].append({
                        "citizen_id": citizen_data["citizen_id"],
                        "presents": 1
                    })

        res = {
            "data": months_dict
        }

        return web.Response(text=json.dumps(res), status=200, content_type="application/json")

    # optional
    async def get_stats_handler(self, request):
        import_id = request.match_info.get("import_id", None)

        logging.info("get_stats_handler, import_id: " + import_id)

        try:
            all_citizens_data = await get_all_citizens_by_import_id(request.app.db_connect, import_id)
        except Exception as e:
            logging.error(e)
            return web.Response(text=str(e), status=500)

        if all_citizens_data == []:
            return web.Response(text="no import_id in db", status=400)

        by_town_dict = {}
        for index, elem in enumerate(all_citizens_data):
            elem_updated = dict(elem)
            town = elem_updated["town"]

            age = calc_age_by_birth_date(elem_updated["birth_date"])

            if town in by_town_dict:

                by_town_dict[town].append(age)
            else:
                by_town_dict[town] = [age]

        res = {
            "data": []
        }

        for town in by_town_dict:
            res["data"].append({
                "town": town,
                "p50": ("%.2f" % np.percentile(by_town_dict[town], 50)),
                "p75": ("%.2f" % np.percentile(by_town_dict[town], 75)),
                "p90": ("%.2f" % np.percentile(by_town_dict[town], 90)),
            })

        return web.Response(text=json.dumps(res), status=200, content_type="application/json")


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
