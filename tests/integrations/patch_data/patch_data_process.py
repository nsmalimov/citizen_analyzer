from tests.integrations.patch_data.data_generator import gen_test_path_data_request_data
from tests.client import Client


def do_patch_data(client, import_id, method_type):
    request_data = gen_test_path_data_request_data(import_id)

    results = []

    for index, request in enumerate(request_data):
        res = client.do_request(request["url"], request["request"], method_type)

        results.append(res)

    return results


if __name__ == "__main__":
    client = Client()

    # import_id = str(uuid.uuid4())

    import_id = "2f66b20a-91fb-4e9a-94b4-214e5a5557ce"

    results = do_patch_data(client, import_id, "patch")

    for i in results:
        print(i)
