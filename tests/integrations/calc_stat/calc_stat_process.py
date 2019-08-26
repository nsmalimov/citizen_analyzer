from tests.client import Client


def do_calc_stat(client, import_id, method_type):
    url = "/imports/" + import_id + "/towns/stat/percentile/age"

    res = client.do_request(url, None, method_type)

    return res["result"]["data"]


if __name__ == "__main__":
    client = Client()

    # import_id = str(uuid.uuid4())

    import_id = "4a545f62-b7a4-4782-bc92-9006e369038d"

    res = do_calc_stat(client, import_id, "get")

    for i in res:
        print(i)
