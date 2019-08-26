from tests.client import Client


def do_birthday_presents(client, import_id, method_type):
    url = "/imports/" + import_id + "/citizens/birthdays"

    res = client.do_request(url, None, method_type)

    if res["status"] != 200:
        print(res)

    return res["result"]["data"]


if __name__ == "__main__":
    client = Client()

    # import_id = str(uuid.uuid4())

    import_id = "6b5ff45c-04fb-405f-b560-7d71f24f8611"

    res = do_birthday_presents(client, import_id, "get")

    if res is None:
        exit()

    for i in res:
        print(i, res[i])
