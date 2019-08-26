from dateutil import parser
import logging


async def save_import_in_db(conn, import_data, import_id):
    for i in import_data["citizens"]:
        await conn.execute("INSERT INTO imports_data (import_id, citizen_id, town, street, building, apartment, "
                           "citizen_name, birth_date, gender, relatives) VALUES "
                           "($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)",
                           import_id, i["citizen_id"], i["town"], i["street"],
                           i["building"], i["apartment"], i["name"], parser.parse(i["birth_date"]),
                           i["gender"], i["relatives"])


async def user_by_id_and_citizen_id_exist_in_db(conn, import_id, citizen_id):
    import_data = await conn.fetchrow(
        "SELECT * FROM imports_data WHERE import_id = $1 and citizen_id=$2", import_id, int(citizen_id))

    logging.info("result from db [search user]: " + str(import_data))

    return import_data


async def patch_in_db(conn, patch_data, import_id, citizen_id):
    s = "UPDATE imports_data SET "

    # todo: без цикла?
    # https://magicstack.github.io/asyncpg/current/api/index.html
    for i in patch_data:
        key = i
        if i == "name":
            key = "citizen_name"

        s += key + "=$3 "
        s += " WHERE import_id=$1 and citizen_id=$2"

        await conn.execute(s, import_id, int(citizen_id), patch_data[i])

        s = "UPDATE imports_data SET "


async def get_all_citizens_by_import_id(conn, import_id):
    all_citizens = await conn.fetch(
        "SELECT * FROM imports_data WHERE import_id = $1", import_id)

    return all_citizens
