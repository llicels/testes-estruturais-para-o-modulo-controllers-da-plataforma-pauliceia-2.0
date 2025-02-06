# funcao testada:
# def get_q_param_as_dict_from_str(self, str_query):
#         str_query = str_query.strip()

#         # normal case: I have a query
#         prequery = str_query.replace(r"[", "").replace(r"]", "").split(",")

#         # with each part of the string, create a dictionary
#         query = {}
#         for condiction in prequery:
#             parts = condiction.split("=")
#             query[parts[0]] = parts[1]

#         return query

import unittest
from unittest.mock import MagicMock

from vgiws.controllers.base import BaseHandler

class TestParam(unittest.TestCase):
    def test_param(self):
        self.mock_application = MagicMock()
        self.handler = BaseHandler(self.mock_application, MagicMock())
        
        str_query = "[field1=value1,field2=value2,field3=value3]"
        
        # espera que a str seja devidamente separada
        expected_result = {
            "field1": "value1",
            "field2": "value2",
            "field3": "value3"
        }
        
        result = self.handler.get_q_param_as_dict_from_str(str_query)
        
        # verifica que a separacao foi correta
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()