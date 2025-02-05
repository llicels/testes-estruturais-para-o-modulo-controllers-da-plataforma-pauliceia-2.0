# funcao sendo testada:
#     def auth_login(self, email, password):
#         user_in_db = self.PGSQLConn.get_users(email=email, password=password)

#         if not user_in_db["features"]:  # if the list is empty
#             raise HTTPError(404, "Not found any user.")

#         if not user_in_db["features"][0]["properties"]["is_email_valid"]:
#             raise HTTPError(409, "The email has not been validated.")

#         encoded_jwt_token = generate_encoded_jwt_token(user_in_db["features"][0])

#         return encoded_jwt_token

import unittest
from unittest.mock import patch, MagicMock
from tornado.web import RequestHandler, HTTPError

from vgiws.controllers.base import BaseHandler

# Sequência 1: Inicio – Verifica usuário no BD – Usuário não encontrado – Erro 404
# Sequência 2: Inicio – Verifica usuário no BD – Email inválido – Erro 409
# Sequência 3: Inicio – Verifica usuário no BD – Token gerado – Retorna token


class TestAuthLogin(unittest.TestCase):
    # sequencia 3 - sucesso
    def test_auth_login_successful(self):
        self.mock_application = MagicMock()
        self.mock_application.PGSQLConn = MagicMock()
        
        # simula usuario com email valido
        self.mock_application.PGSQLConn.get_users.return_value = {
            "features":[
                {"properties": {"is_email_valid": True}}
            ]
        }
        
        self.handler = BaseHandler(self.mock_application, MagicMock())
        
        # simula codificacao de um token
        with patch("vgiws.controllers.base.generate_encoded_jwt_token", return_value="mock_token"):
            token = self.handler.auth_login("test@example.com", "password123")
        
        # verifica que o token foi retornado
        self.assertEqual(token, "mock_token")
    
    # sequencia 1 - erro 404
    def test_auth_login_user_not_found(self):
        self.mock_application = MagicMock()
        self.mock_application.PGSQLConn = MagicMock()
        
        # simula um usuario nao existente
        self.mock_application.PGSQLConn.get_users.return_value = {"features":[]}
        
        self.handler = BaseHandler(self.mock_application, MagicMock())
        
        # chama a funcao esperando o erro
        with self.assertRaises(HTTPError) as context:
            self.handler.auth_login("test@example.com", "password123")
        
        # verifica que o erro correto foi chamado
        self.assertEqual(context.exception.status_code, 404)
     
    # sequencia 2 - erro 409   
    def test_auth_login_user_not_validated(self):
        self.mock_application = MagicMock()
        self.mock_application.PGSQL = MagicMock()
        
        # simula usuario com email invalido
        self.mock_application.PGSQLConn.get_users.return_value = {
            "features":[
                {"properties": {"is_email_valid": False}}
            ]
        }
        
        self.handler = BaseHandler(self.mock_application, MagicMock())
        
        # chama funcao esperando erro
        with self.assertRaises(HTTPError) as context:
            self.handler.auth_login("test@example.com", "password123")
        
        # verifica que o erro correto foi chamado
        self.assertEqual(context.exception.status_code, 409)

if __name__ == '__main__':
    unittest.main()