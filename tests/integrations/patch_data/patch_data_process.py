from tests.integrations.patch_data.data_generator import gen_test_path_data_request_data
from tests.client import Client
from tests.integrations.all_citizens.get_all_citizens_process import do_get_all_citizens


def do_patch_data(client, import_id, method_type):
    request_data = gen_test_path_data_request_data(import_id)

    results = []

    for index, request in enumerate(request_data):
        res = client.do_request(request["url"], request["request"], method_type)

        all_citizens = do_get_all_citizens(client, import_id, "get")

        for i in all_citizens:
           print (i)

        print()

        results.append(res)

        for index, elem in enumerate(results):
            print("result == correct_response: ", elem["result"] == results[index]["result"])

    return results


if __name__ == "__main__":
    client = Client()

    # import_id = str(uuid.uuid4())

    import_id = "6b5ff45c-04fb-405f-b560-7d71f24f8611"

    results = do_patch_data(client, import_id, "patch")

    for i in results:
        print(i)
