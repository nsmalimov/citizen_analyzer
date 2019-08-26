from tests.integrations.send_import.send_import_process import do_send_import
from tests.integrations.patch_data.patch_data_process import do_patch_data
from tests.client import Client
from tests.integrations.all_citizens.get_all_citizens import do_get_all_citizens


# todo: проверь, что там больше 256 может приехать (вдруг default = 255)

# 10 секунд на запрос при 10000 в базе
# не более 1000 родственных связей (2000 связанных жителей)

def start():
    client = Client()

    # change url if need

    import_id = do_send_import(client, "post")

    print("import_id: ", import_id)

    # todo: check in db

    print()

    user_after_patched = do_patch_data(client, import_id, "patch")

    print("user_after_patched")

    for i in user_after_patched:
        print(i)

    # todo: check in db

    print()

    all_citizens = do_get_all_citizens(client, import_id, "get")

    print("all_citizens")

    for i in all_citizens:
        print(i)


# todo: more cases

if __name__ == "__main__":
    start()
