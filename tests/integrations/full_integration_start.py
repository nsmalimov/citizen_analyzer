from tests.client import Client
from tests.integrations.all_citizens.get_all_citizens_process import do_get_all_citizens
from tests.integrations.calc_stat.calc_stat_process import do_calc_stat
from tests.integrations.patch_data.patch_data_process import do_patch_data
from tests.integrations.send_import.send_import_process import do_send_import
from tests.integrations.birthdays_gifts.birthdays_gifts import do_birthday_presents

# todo: проверь, что там больше 256 может приехать (вдруг default = 255)

# 10 секунд на запрос при 10000 в базе
# не более 1000 родственных связей (2000 связанных жителей)

def start():
    client = Client()

    # client.url = "http://84.201.129.208:8080"

    # change url if need

    import_id = do_send_import(client, "post")

    print("import_id: ", import_id)

    # todo: check in db

    print()

    print("all_citizens")

    all_citizens = do_get_all_citizens(client, import_id, "get")

    for i in all_citizens:
        print(i)

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

    print()

    print("presents")

    presents = do_birthday_presents(client, import_id, "get")

    for i in presents:
        print(i, presents[i])

    print()

    print("stats")

    stats = do_calc_stat(client, import_id, "get")

    for i in stats:
        print(i)


# todo: more cases

if __name__ == "__main__":
    start()
