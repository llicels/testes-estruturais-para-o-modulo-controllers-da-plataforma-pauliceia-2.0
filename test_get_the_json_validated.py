# funcao testada:
#     def get_the_json_validated(self):
#         """
#             Responsible method to validate the JSON received in the POST method.

#             Args:
#                 Nothing until the moment.

#             Returns:
#                 The JSON validated.

#             Raises:
#                 - HTTPError (400 - Bad request): if don't receive a JSON.
#                 - HTTPError (400 - Bad request): if the JSON received is empty or is None.
#         """

#         # Check if the type of the content is JSON
#         if self.request.headers["Content-Type"].startswith("application/json"):
#             # Convert string to unicode in Python 2 or convert bytes to string in Python 3
#             # How string in Python 3 is unicode, so independent of version, both are converted in unicode
#             foo = self.request.body.decode("utf-8")

#             # Transform the string/unicode received to JSON (dictionary in Python)
#             search = loads(foo)
#         else:
#             raise HTTPError(400, "It is not a JSON...")  # 400 - Bad request

#         if search == {} or search is None:
#             raise HTTPError(400, "The search given is empty...")  # 400 - Bad request

#         return search

import unittest
from unittest.mock import MagicMock, patch
import unittest.mock
from tornado.web import RequestHandler, HTTPError
from json import dumps


from vgiws.controllers.base import BaseHandler

# Sequência 1: Inicio – Verifica que conteúdo é JSON – Conteúdo inválido – Erro 400
# Sequência 2: Inicio - Verifica que conteúdo é JSON - Analisa solicitação para o JSON – JSON vazio – Erro 400
# Sequência 3: Inicio – Verifica que conteúdo é JSON – Analisa solicitação para o JSON – JSON válido – Retorna JSON válido


class TestJsonValidation(unittest.TestCase):
    
    # testa a funcao com um json valido
    def test_get_the_json_validated_valid(self):
        
        self.mock_application = MagicMock()
        
        self.handler = BaseHandler(self.mock_application, MagicMock())
        
        # simula headers validas
        self.handler.request.headers = {"Content-Type": "application/json"}
        # codifica
        self.handler.request.body = dumps({"key": "value"}).encode("utf-8")
        
        result = self.handler.get_the_json_validated()
        
        # verifica corretude
        self.assertEqual(result, {"key": "value"})
    
    # testa a funcao com um json invalido e levanta o erro
    def test_get_the_json_validated_missing(self):
        self.mock_application = MagicMock()
        self.handler = BaseHandler(self.mock_application, MagicMock())
        
        # simula json invalido
        self.handler.request.headers = {"Content-Type": "not json"}
        self.handler.request.body = dumps({"key": "value"}).encode("utf-8")
        
        with self.assertRaises(HTTPError) as context:
            self.handler.get_the_json_validated()
        
        # verifica que resultou no erro esperado  
        self.assertEqual(context.exception.status_code, 400)
    
    # testa a funcao com um json vazio
    def test_get_the_json_empty(self):
        self.mock_application = MagicMock()
        self.handler = BaseHandler(self.mock_application, MagicMock())
        
        # simula um json vazio
        self.handler.request.headers = {"Content-Type": "application/json"}
        self.handler.request.body = dumps({}).encode("utf-8")
        
        with self.assertRaises(HTTPError) as context:
            self.handler.get_the_json_validated()
        
        # verifica que o erro esperado foi levantado 
        self.assertEqual(context.exception.status_code, 400)
    
    # testa a funcao com um json NONE
    def test_get_the_json_none(self):
        self.mock_application = MagicMock()
        self.handler = BaseHandler(self.mock_application, MagicMock())
        
        # simula um json com formato None
        self.handler.request.headers = {"Content-Type": "application/json"}
        self.handler.request.body = b""
        
        with self.assertRaises(HTTPError) as context:
            self.handler.get_the_json_validated()
        
        # verifica se o erro foi levantando
        self.assertEqual(context.exception.status_code, 400)
    
    # erro aqui, o codigo nao alerta para erro quando o json é None

if __name__ == "__main__":
    unittest.main()