# funcao testada:
# def get_current_user_(self):
#         token = self.request.headers["Authorization"]
#         user = get_decoded_jwt_token(token)
#         return user

import unittest
from unittest.mock import MagicMock, patch
from tornado.web import HTTPError

from vgiws.controllers.base import BaseHandler

# Sequência 1: Inicio – Lê token de autorização – Decodifica token – Retorna dados do usuário
# Sequência 2: Inicio – Lê token de autorização – Decodifica token – Token Inválido – Erro 400

class TestGetCurrentUser(unittest.TestCase):
    # sequencia 1 - token valido
    def test_get_current_user_valid(self):
        
        self.mock_application = MagicMock()
        
        self.handler = BaseHandler(self.mock_application, MagicMock())
        
        # simula usuario
        mock_user_data = {"properties": {"user_id": "123", "email": "user@test.com"}}
        
        # simula autorizacao
        self.handler.request = MagicMock()
        self.handler.request.headers = {"Authorization": "mock_token"}
        
        with patch("vgiws.controllers.base.get_decoded_jwt_token", return_value=mock_user_data):
            user = self.handler.get_current_user_()
        
        # verifica que o usuario obtido e o simulado
        self.assertEqual(user, mock_user_data)
    
    # sequencia 2 - token invalido
    def test_get_current_user_invalid(self):
        
        self.mock_application = MagicMock()
        
        self.handler = BaseHandler(self.mock_application, MagicMock())
        
        # autorizacao invalida
        self.handler.request = MagicMock()
        self.handler.request.headers = {"Authorization": "invalid_token"}
        
        with patch("vgiws.controllers.base.get_decoded_jwt_token", side_effects=HTTPError(400, "Invalid Token")):
            with self.assertRaises(HTTPError) as context:
                self.handler.get_current_user_()
        
        # erro deve ser alertado
        self.assertEqual(context.exception.status_code, 400)
    
    # se o token e invalido o codigo nao alerta erro!

if __name__ == '__main__':
    unittest.main()
    
        
        

