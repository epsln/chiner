import json
import unittest

from src.chiner.database import DatabaseFormatter

class TestDatabaseFormatter(unittest.TestCase):
    def test_init(self):
        test_scheme = {"test": {"field1": 1, "field2": 2}} 
        db = DatabaseFormatter(test_scheme)

    def test_init_fail(self):
        scheme = "notadict"
        with self.assertRaises(ValueError):
            db = DatabaseFormatter(scheme)

    def test_from_file(self):
        scheme = {"test": {"field1": 1, "field2": 2}}
        with open("/tmp/chiner_test/test_scheme.json") as fi:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def test_get_field_sql_insert_table(self):
        test_scheme = {"test": {"field1": 1, "field2": 2}} 
        db_formatter = DatabaseFormatter(test_scheme)
        expected_res = "( field1 int, field2 int)"
        res = db_formatter._get_field_sql_insert_table(test_scheme)
        self.assertTrue(expected_res == res)
        
        test_scheme = {"test": {"field1": 3.1415, "field2": "text"}} 
        expected_res = "( field1 real, field2 text)"
        res = db_formatter._get_field_sql_insert_table(test_scheme)
        self.assertTrue(expected_res == res)

    def get_insert_value(self):
        test_scheme = {"test": {"field1": 1, "field2": 2}} 
        db_formatter = DatabaseFormatter(test_scheme)
        expected_res = "INSERT INTO test VALUES (1, 2)"
        res = db_formatter.get_insert_value(test_scheme)

        self.assertTrue(expected_res == res)

        test_input = {"test": {"field1": "test", "field2": 2}} 
        res = db_formatter._get_field_sql_insert_table(test_scheme)

        with self.assertRaise(ValueError):
            db_formatter.get_insert_value(test_input)

    def test_validate_input(self):
        test_scheme = {"test": {"field1": 1, "field2": 2}} 
        db_formatter = DatabaseFormatter(test_scheme)
        test_input = {"field1": 1, "field2": 2}
        self.assertTrue(db_formatter.validate_input(test_input))

        test_input = {"field1": "text", "field2": 2}
        self.assertFalse(db_formatter.validate_input(test_input))

        test_input = {"notfield1": 1 , "field2": 2}
        self.assertFalse(db_formatter.validate_input(test_input))
