def gen_test_import_send_request_data():
    d = [{
        "request": {
            "citizens": [
                {
                    "citizen_id": 1,
                    "town": "Москва",
                    "street": "Льва Толстого",
                    "building": "16к7стр5",
                    "apartment": 7,
                    "name": "Иванов Иван Иванович",
                    "birth_date": "26.12.1986",
                    "gender": "male",
                    "relatives": [2]
                },
                {
                    "citizen_id": 2,
                    "town": "Москва",
                    "street": "Льва Толстого",
                    "building": "16к7стр5",
                    "apartment": 7,
                    "name": "Иванов Сергей Иванович",
                    "birth_date": "01.04.1997",
                    "gender": "male",
                    "relatives": [1]
                },
                {
                    "citizen_id": 3,
                    "town": "Керчь",
                    "street": "Иосифа Бродского",
                    "building": "2",
                    "apartment": 11,
                    "name": "Романова Мария Леонидовна",
                    "birth_date": "23.11.1986",
                    "gender": "female",
                    "relatives": []
                }
            ]
        }
    }]

    return d
