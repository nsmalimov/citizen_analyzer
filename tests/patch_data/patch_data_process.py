from tests.patch_data.data_generator import gen_test_path_data_request_data
import uuid

def do_patch_data(client, import_id=None):
    if import_id is None:
        import_id = str(uuid.uuid4())

    request_data = gen_test_path_data_request_data(import_id)

    for index, request in enumerate(request_data):
        res = client.do_request(request["url"], request["request"])

        print(index, res['status'], res['cause'])
