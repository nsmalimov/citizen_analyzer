import re
from dateutil import parser
from datetime import datetime, timedelta
import logging


def check_str_req(str_to_check):
    if not (isinstance(str_to_check, str)):
        return False, "not str"

    if len(str_to_check) > 256 or len(str_to_check) == 0:
        return False, "no in [1, 256]"

    if re.search('[a-zA-Zа-яА-Я]', str_to_check) is None and (re.search('[0-9]', str_to_check) is None):
        return False, "no one digit or a-zA-Z"

    return True, ""


def check_int_req(int_to_check):
    if not (isinstance(int_to_check, int)):
        return False, "not int"
    else:
        if int_to_check < 0:
            return False, "< 0"

    return True, ""


# todo: что если их несколько в 1 (set?)
def validate_relations(relations_dict):
    all_relation_ids = []

    is_valid = True

    for citizen_id_orig in relations_dict:
        for citizen_id_another in relations_dict[citizen_id_orig]:
            if is_valid and not (citizen_id_orig in relations_dict[citizen_id_another]):
                is_valid = False

            all_relation_ids.append(citizen_id_another)

    return is_valid, len(set(all_relation_ids))

def validate_request_patch(request_data):
    return True

# todo: выдавать причину ошибки
def validate_request_import(request_data):
    if not "citizens" in request_data:
        return False, "not citizens key"

    correct_fields = ["citizen_id", "town", "street", "building", "apartment", "birth_date", "name", "birth_day",
                      "gender", "relatives"]

    relations_dict = {}

    citizen_id = None

    for citizen in request_data["citizens"]:
        if "citizen_id" in citizen:
            citizen_id = citizen["citizen_id"]

            res, cause = check_int_req(citizen_id)
            if not (res):
                return False, "citizen_id " + cause + ", citizen data: " + citizen

            relations_dict[citizen_id] = None
        else:
            return False, "no citizen_id key, citizen data: " + citizen

        for key in citizen:
            if not (key in correct_fields):
                return False, "unknown key, citizen_id: " + str(citizen_id)

        if "town" in citizen:
            town = citizen["town"]

            res, cause = check_str_req(town)
            if not (res):
                return False, "town " + cause + ", citizen_id: " + str(citizen_id)

        else:
            return False, "no town key, citizen_id: " + str(citizen_id)

        if "street" in citizen:
            street = citizen["street"]

            res, cause = check_str_req(street)
            if not (res):
                return False, "street " + cause + ", citizen_id: " + str(citizen_id)
        else:
            return False, "no street key, citizen_id: " + str(citizen_id)

        if "building" in citizen:
            building = citizen["building"]

            res, cause = check_str_req(building)
            if not (res):
                return False, "building " + cause + ", citizen_id: " + str(citizen_id)
        else:
            return False, "no building key, citizen_id: " + str(citizen_id)

        if "apartment" in citizen:
            apartment = citizen["apartment"]

            res, cause = check_int_req(apartment)
            if not (res):
                return False, "apartment " + cause + ", citizen_id: " + str(citizen_id)
        else:
            return False, "no apartment key, citizen_id: " + str(citizen_id)

        if "name" in citizen:
            name = citizen["name"]

            if not (isinstance(name, str)) or len(name) == 0 or len(name) > 256:
                return False, "name not str or not in [1,256], citizen_id: " + str(citizen_id)
        else:
            return False, "no name key, citizen_id: " + str(citizen_id)

        if "birth_date" in citizen:
            birth_date = citizen["birth_date"]

            try:
                dt = parser.parse(birth_date)

                # todo: если родился сегодня, то валидно?
                dt_now = datetime.today() - timedelta(days=1)

                if dt >= dt_now:
                    return False, "birth_date >= then now date, citizen_id: " + str(citizen_id)
            except Exception as e:
                return False, "birth_date not valid DD.MM.YYYY, error: " + str(e) +\
                       ", citizen_id: " + str(citizen_id)
        else:
            return False, "no town key, citizen_id: " + str(citizen_id)

        if "gender" in citizen:
            gender = citizen["gender"]

            if not (gender in ["male", "female"]):
                return False, "gender not in [male, female], citizen_id: " + str(citizen_id)
        else:
            return False, "no gender key, citizen_id: " + str(citizen_id)

        if "relatives" in citizen:
            relatives = citizen["relatives"]

            for i in relatives:
                if not (isinstance(i, int)):
                    return False, "relatives not int, citizen_id: " + str(citizen_id)

            relations_dict[citizen_id] = relatives
        else:
            return False, "no relatives key, citizen_id: " + str(citizen_id)

    is_relations_valid, count_relations = validate_relations(relations_dict)

    if not(is_relations_valid):
        return False, "relations data is not valid,"+ ", citizen_id: " + str(citizen_id)

    logging.info("count_relations: " + str(count_relations))

    return True, ""
