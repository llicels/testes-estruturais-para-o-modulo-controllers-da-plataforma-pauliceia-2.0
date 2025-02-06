# o nome da funcao em base.py deveria ser arguments

# funcao testada:
# def get_aguments(self):
#         """
#         Create the 'arguments' dictionary.
#         :return: the 'arguments' dictionary contained the arguments and parameters of URL,
#                 in a easier way to work with them.
#         """
#         arguments = {k: self.get_argument(k) for k in self.request.arguments}

#         for key in arguments:
#             argument = arguments[key].lower()

#             # transform in boolean the string received
#             if argument == 'true':
#                 arguments[key] = True
#             if argument == 'false':
#                 arguments[key] = False

#         # "q" is the query argument, that have the fields of query
#         # if "q" in arguments:
#         #     arguments["q"] = self.get_q_param_as_dict_from_str(arguments["q"])
#         # else:
#         #     # if "q" is not in arguments, so put None value
#         #     arguments["q"] = None

#         # if key "format" not in arguments, put a default value, the "geojson"
#         # if "format" not in arguments:
#         #     arguments["format"] = "geojson"

#         return arguments

import unittest
from unittest.mock import MagicMock

from vgiws.controllers.base import BaseHandler

class TestGetAguments(unittest.TestCase):
    def test_get_arguments_with_boolean(self):
        self.mock_application = MagicMock()
        self.handler = BaseHandler(self.mock_application, MagicMock())
        self.handler.request = MagicMock()
        
        self.handler.request.arguments = {'param1': [b'true'], 'param2': [b'false']}
        expected_result = {'param1': True, 'param2': False}
        
        result = self.handler.get_aguments()
        self.assertEqual(result, expected_result)
    
    def test_get_arguments_no_boolean(self):
        self.mock_application = MagicMock()
        self.handler = BaseHandler(self.mock_application, MagicMock())
        self.handler.request = MagicMock()
        
        self.handler.request.arguments = {'param1': [b'value1'], 'param2': [b'value2']}
        
        expected_result = {'param1': 'value1', 'param2': 'value2'}
        
        result = self.handler.get_aguments()
        
        self.assertEqual(result, expected_result)
        
    def test_get_arguments_with_mixed_values(self):
        self.mock_application = MagicMock()
        self.handler = BaseHandler(self.mock_application, MagicMock())
        self.handler.request = MagicMock()
        
        self.handler.request.arguments = {'param1': [b'true'], 'param2': [b'value2'], 'param3': [b'false']}
        
        expected_result = {'param1': True, 'param2': 'value2', 'param3': False}
        
        result = self.handler.get_aguments()
        
        self.assertEqual(result, expected_result)
    
    def test_get_arguments_empty(self):
        self.mock_application = MagicMock()
        self.handler = BaseHandler(self.mock_application, MagicMock())
        self.handler.request = MagicMock()
        
        self.handler.request.arguments = {}
        expected_result = {}
        
        result = self.handler.get_aguments()
        
        self.assertEqual(result, expected_result)
    


if __name__ == "__main__":
    unittest.main()