from tests.patch_data.data_generator import gen_test_path_data_request_data
import uuid
from tests.client import Client
import uuid


def do_patch_data(client, import_id, method_type):
    request_data = gen_test_path_data_request_data(import_id)

    for index, request in enumerate(request_data):
        res = client.do_request(request["url"], request["request"], method_type)

        print(index, res)


if __name__ == "__main__":
    client = Client()

    # import_id = str(uuid.uuid4())

    import_id = "2f66b20a-91fb-4e9a-94b4-214e5a5557ce"

    do_patch_data(client, import_id, "patch")
