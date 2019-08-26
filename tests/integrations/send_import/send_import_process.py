from tests.integrations.send_import.data_generator import gen_test_import_send_request_data
from tests.client import Client


def do_send_import(client, method_type):
    request_data = gen_test_import_send_request_data()

    request_data = request_data[0]

    res = client.do_request(request_data["url"], request_data["request"], method_type)

    if res["status"] == 201:
        res = res["result"]
        return res["data"]["import_id"]


if __name__ == "__main__":
    client = Client()

    res = do_send_import(client, "post")

    print(res)
