from tests.send_import.send_import_process import do_send_import
from tests.patch_data.patch_data_process import do_patch_data
from tests.client import Client

# todo: проверь, что там больше 256 может приехать (вдруг default = 255)

# 10 секунд на запрос при 10000 в базе
# не более 1000 родственных связей (2000 связанных жителей)

def start():
    client = Client()

    # change url if need

    import_id = do_send_import(client, "post")

    print ("import_id: ", import_id)

    # todo: check in db

    do_patch_data(client, import_id, "patch")

    # todo: check in db

    # ...

# todo: more cases

if __name__ == "__main__":
    start()