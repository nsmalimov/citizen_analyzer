from dateutil import parser

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
        'SELECT * FROM imports_data WHERE import_id = $1 and citizen_id=$2', import_id, citizen_id)

    return import_data !=None

async def path_in_db(conn, patch_data, import_id):
    res = None

    return res