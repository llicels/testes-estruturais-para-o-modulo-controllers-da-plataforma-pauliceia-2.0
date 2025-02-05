# funcao testada:
#     def set_default_headers(self):
#         # self.set_header('Content-Type', 'application/json; charset="utf-8"')
#         self.set_header('Content-Type', 'application/json')

#         # how solve the CORS problem: https://stackoverflow.com/questions/32500073/request-header-field-access-control-allow-headers-is-not-allowed-by-itself-in-pr
#         self.set_header("Access-Control-Allow-Origin", "*")
#         self.set_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Authorization")
#         self.set_header('Access-Control-Allow-Methods', ' POST, GET, PUT, DELETE, OPTIONS')
#         self.set_header('Access-Control-Expose-Headers', 'Authorization')
#         self.set_header("Access-Control-Allow-Credentials", "true")

import unittest
from unittest.mock import MagicMock, patch
import unittest.mock
from tornado.web import RequestHandler


from vgiws.controllers.base import BaseHandler

# Sequência: Inicio – Define tipo de conteúdo para JSON – 
# Define Headers CORS – Expõe header de autorização – 
# Permite credenciais

class TestDefaultHeader(unittest.TestCase):
    def test_set_default_headers(self):
        
        self.mock_application = MagicMock()
        
        self.handler = BaseHandler(self.mock_application, MagicMock())
        
        self.handler.set_header = MagicMock()
        
        self.handler.set_default_headers()
        
        # simula headers
        expected_calls = [
            unittest.mock.call('Content-Type', 'application/json'),
            unittest.mock.call("Access-Control-Allow-Origin", '*'),
            unittest.mock.call("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Authorization"),
            unittest.mock.call('Access-Control-Allow-Methods', ' POST, GET, PUT, DELETE, OPTIONS'),
            unittest.mock.call('Access-Control-Expose-Headers', 'Authorization'),
            unittest.mock.call("Access-Control-Allow-Credentials", "true")
        ]
        
        # verifica que as headers desejadas foram chamadas
        self.handler.set_header.assert_has_calls(expected_calls, any_order=False)

if __name__ == '__main__':
    unittest.main()
        
# para testar: python -m unittest -v vgiws.controllers.test_set_default_headers