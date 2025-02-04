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
                
        self.handler.request.headers = {"Content-Type": "application/json"}
        self.handler.request.body = dumps({"key": "value"}).encode("utf-8")
        
        result = self.handler.get_the_json_validated()
        
        self.assertEqual(result, {"key": "value"})
    
    # testa a funcao com um json invalido e levanta o erro
    def test_get_the_json_validated_missing(self):
        self.mock_application = MagicMock()
        self.handler = BaseHandler(self.mock_application, MagicMock())
        
        self.handler.request.headers = {"Content-Type": "not json"}
        self.handler.request.body = dumps({"key": "value"}).encode("utf-8")
        
        with self.assertRaises(HTTPError) as context:
            self.handler.get_the_json_validated()
            
        self.assertEqual(context.exception.status_code, 400)
    
    # testa a funcao com um json vazio
    def test_get_the_json_empty(self):
        self.mock_application = MagicMock()
        self.handler = BaseHandler(self.mock_application, MagicMock())
        
        self.handler.request.headers = {"Content-Type": "application/json"}
        self.handler.request.body = dumps({}).encode("utf-8")
        
        with self.assertRaises(HTTPError) as context:
            self.handler.get_the_json_validated()
            
        self.assertEqual(context.exception.status_code, 400)
    
    # testa a funcao com um json NONE
    def test_get_the_json_none(self):
        self.mock_application = MagicMock()
        self.handler = BaseHandler(self.mock_application, MagicMock())
        
        self.handler.request.headers = {"Content-Type": "application/json"}
        self.handler.request.body = b""
        
        with self.assertRaises(HTTPError) as context:
            self.handler.get_the_json_validated()
            
        self.assertEqual(context.exception.status_code, 400)
    
    # erro levantado aqui!

if __name__ == "__main__":
    unittest.main()