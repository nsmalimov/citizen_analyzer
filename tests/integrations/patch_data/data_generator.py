def gen_test_path_data_request_data(import_id):
    requests = \
        [
            {
                "request": {
                    "name": "Иванова Мария Леонидовна",
                    "town": "Москва",
                    "street": "Льва Толстого",
                    "building": "16к7стр5",
                    "apartment": 7,
                    "relatives": [1]
                },
                "url": "/imports/" + import_id + "/citizens/3",
                "result": {
                    "data": {
                        "citizen_id": 3,
                        "town": "Москва",
                        "street": "Льва Толстого",
                        "building": "16к7стр5",
                        "apartment": 7,
                        "name": "Иванова Мария Леонидовна",
                        "birth_date": "23.11.1986",
                        "gender": "female",
                        "relatives": [1]
                    }
                }
            },
            {
                "request": {
                    "relatives": []
                },
                "url": "/imports/" + import_id + "/citizens/3",
                "result": {
                    "data": {
                        "citizen_id": 3,
                        "town": "Москва",
                        "street": "Льва Толстого",
                        "building": "16к7стр5",
                        "apartment": 7,
                        "name": "Иванова Мария Леонидовна",
                        "birth_date": "23.11.1986",
                        "gender": "female",
                        "relatives": []
                    }
                }
            }
        ]

    return requests
