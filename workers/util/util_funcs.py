from datetime import date

def prepare_user_data_to_response_from_db(user_info):
    user_info = dict(user_info)

    formatted_date = user_info["birth_date"]
    formatted_date = str(formatted_date).replace("-", ".")
    formatted_date_splitted = formatted_date.split(".")
    user_info["birth_date"] = formatted_date_splitted[2] + "." + formatted_date_splitted[1] + "." + \
                              formatted_date_splitted[0]

    user_info["name"] = user_info["citizen_name"]
    del user_info["citizen_name"]

    return user_info

def calc_age_by_birth_date(birth_date):
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    return age
