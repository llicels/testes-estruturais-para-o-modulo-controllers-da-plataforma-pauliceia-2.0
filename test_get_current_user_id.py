# funcao testada:
# def get_current_user_id(self):
#         try:
#             current_user = self.get_current_user_()
#             return current_user["properties"]["user_id"]
#         except KeyError:
#             return None

import unittest
from unittest.mock import MagicMock, patch
from tornado.web import RequestHandler

from vgiws.controllers.base import BaseHandler

# Sequência 1: Inicio – Lê usuário – Extrai ID – Retorna ID do usuário
# Sequência 2: Inicio – Lê usuário – Chave faltando – Retorna vazio


class TestGetCurrentUser(unittest.TestCase):
    # sequencia 1 - retorna ID
    def test_get_current_user_id_valid(self):
        
        self.mock_application = MagicMock()
        
        self.handler = BaseHandler(self.mock_application, MagicMock())
        
        # simula o usuario
        mock_user_data = {"properties": {"user_id": "123"}}
        
        with patch.object(self.handler, "get_current_user_", return_value=mock_user_data):
            user_id = self.handler.get_current_user_id()
        
        # verifica que a id retornada e a do usuario simulado
        self.assertEqual(user_id, "123")
    
    # sequencia 2 - retorna vazio
    def test_get_current_user_id_invalid(self):
        
        self.mock_application = MagicMock()
        
        self.handler = BaseHandler(self.mock_application, MagicMock())
        
        # usuario nao existe
        mock_user_data = {"properties": {}}
        
        with patch.object(self.handler, "get_current_user_", return_value=mock_user_data):
            user_id = self.handler.get_current_user_id()
        
        # retorna vazio
        self.assertIsNone(user_id)

if __name__ == '__main__':
    unittest.main()
    
        
        

