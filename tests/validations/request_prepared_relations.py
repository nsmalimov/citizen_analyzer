import unittest
from workers.processing.import_data import validate_relations


class TestValidators(unittest.TestCase):
    def test_validate_relations(self):
        test_cases = [
            {
                "dict_to_test": {
                    1: [2, 3, 4],
                    2: [1, 3, 7],
                    3: [1, 2],
                    4: [1],
                    5: [],
                    6: [],
                    7: [2]
                },
                "is_valid": True,
                "count_relations": 5,
            },
            {
                "dict_to_test": {
                    1: [],
                    2: [7],
                    3: [5],
                    4: [],
                    5: [3],
                    6: [],
                    7: [2]
                },
                "is_valid": True,
                "count_relations": 4,
            },
            {
                "dict_to_test": {
                    1: [2, 3, 4],
                    2: [1, 3, 7],
                    3: [1, 2],
                    4: [1],
                    5: [7],
                    6: [],
                    7: [2]
                },
                "is_valid": False,
                "count_relations": 5,
            }
        ]

        for test_case in test_cases:
            is_valid, count_relations = validate_relations(test_case["dict_to_test"])
            self.assertEqual(is_valid, test_case["is_valid"], test_case)
            self.assertEqual(count_relations, test_case["count_relations"], test_case)


if __name__ == '__main__':
    unittest.main()
