from tests.client import Client


def do_get_all_citizens(client, import_id, method_type):
    url = "/imports/" + import_id + "/citizens"

    res = client.do_request(url, None, method_type)

    return res["result"]["data"]


if __name__ == "__main__":
    client = Client()

    # import_id = str(uuid.uuid4())

    import_id = "2f66b20a-91fb-4e9a-94b4-214e5a5557ce"

    res = do_get_all_citizens(client, import_id, "get")

    for i in res:
        print(i)
