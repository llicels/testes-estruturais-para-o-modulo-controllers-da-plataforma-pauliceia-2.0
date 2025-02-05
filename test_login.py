# funcao testada:
# @catch_generic_exception
#     def login(self, user_json, verified_social_login_email=False):
#         # looking for a user in db, if not exist user, so create a new one
#         user_in_db = self.PGSQLConn.get_users(email=user_json["properties"]["email"])

#         if not user_in_db["features"]:  # if the list is empty
#             # ... because I expected a 404 to create a new user
#             id_in_json = self.PGSQLConn.create_user(user_json, verified_social_login_email=verified_social_login_email)
#             user_in_db = self.PGSQLConn.get_users(user_id=str(id_in_json["user_id"]))

#         encoded_jwt_token = generate_encoded_jwt_token(user_in_db["features"][0])

#         return encoded_jwt_token

import unittest
from unittest.mock import MagicMock, patch

from vgiws.controllers.base import BaseHandler

# Sequência 1: Início – Verifica se o usuário existe – Usuário existe – Retorna token
# Sequência 2: Início – Verifica se o usuário existe – Usuário não encontrado – Adiciona usuário ao BD – Retorna token

class TestLogin(unittest.TestCase):
    # sequencia 1 - usuario existe
    def test_login_exists(self):
        self.mock_application = MagicMock()
        self.mock_application.PGSQLConn = MagicMock()
        
        self.handler = BaseHandler(self.mock_application, MagicMock())
        
        # simula json do usuario
        mock_user_json = {"properties": {"email": "email@test.com"}}
        
        # simula retorno de valores de uma conexao com  o banco
        self.mock_application.PGSQLConn.get_users.return_value = {
            "features":[
                {"properties": {"email": "email@test.com"}}
            ]
        }
        
        # codifica o token e o retorna
        with patch("vgiws.controllers.base.generate_encoded_jwt_token", return_value="mock_token"):
            token = self.handler.login(mock_user_json)
          
        # verifica que o token foi retornado      
        self.assertEqual(token, "mock_token")
    
    # sequencia 2 - usuario nao existe
    def test_login_not_exists(self):
        self.mock_application = MagicMock()
        self.mock_application.PGSQLConn = MagicMock()
        
        self.handler = BaseHandler(self.mock_application, MagicMock())
        
        mock_user_json = {"properties": {"email": "newuser@test.com"}}
        
        # simula que usuario nao existe
        self.mock_application.PGSQLConn.get_users.return_value = {
            "features":[]
        }
        
        # simula criacao de usuario
        self.mock_application.PGSQLConn.create_user.return_value = {"user_id": "123"}
        
        # na primeira vez o usuario nao existe, mas depois foi criado
        self.mock_application.PGSQLConn.get_users.side_effect = [
            {"features": []},
            {"features": [{"properties": {"email": "newuser@test.com"}}]}
        ]
        
        with patch("vgiws.controllers.base.generate_encoded_jwt_token",return_value="mock_token"):
            token = self.handler.login(mock_user_json)
        
        # verifica que o token e retornado
        self.assertEqual(token, "mock_token")
        self.mock_application.PGSQLConn.create_user.assert_called_once_with(mock_user_json, verified_social_login_email=False)


if __name__ == '__main__':
    unittest.main()