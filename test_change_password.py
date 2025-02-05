# funcao sendo testada:
# @catch_generic_exception
#     def change_password(self, email, current_password, new_password):
#         # try to login with the email and password, it doesn't raise an exception, so it is OK
#         try:
#             self.auth_login(email, current_password)
#         except HTTPError as error:
#             if error.status_code == 404:
#                 raise HTTPError(409, "Current password is invalid.")

#         # try to update the user's password by id
#         current_user_id = self.get_current_user_id()
#         self.PGSQLConn.update_user_password(current_user_id, new_password)

import unittest
from unittest.mock import MagicMock, patch
from tornado.web import HTTPError

from vgiws.controllers.base import BaseHandler

# Sequência 1: Inicio – Valida senha atual – Atualiza nova senha no BD – Sucesso
# Sequência 2: Inicio – Valida senha atual – Senha invalida – Erro 409


class TestChangePassword(unittest.TestCase):
    # sequencia 1 - sucesso
    def test_change_password_successful(self):
        self.mock_application = MagicMock()
        self.mock_application.PGSQLConn = MagicMock()
        
        self.handler = BaseHandler(self.mock_application, MagicMock())
        
        # simula um chamado da funcao auth_login
        with patch.object(self.handler, "auth_login", return_value=None):
            # simula um chamado da funcao que obtem o id do usuario
            with patch.object(self.handler, "get_current_user_id", return_value=1):
                # simula conexao com o banco e muda a senha
                with patch.object(self.handler.PGSQLConn, "update_user_password") as mock_update:
                    self.handler.change_password("test@example.com", "password123", "newpassword")
        
        # verifica que o chamado foi correto
        mock_update.assert_called_once_with(1, "newpassword")
    
    #sequencia 2 - erro 409
    def test_change_password_unvalid(self):
        self.mock_application = MagicMock()
        self.mock_application.PGSQLConn = MagicMock()
        
        self.handler = BaseHandler(self.mock_application, MagicMock())
        
        # simula um chamado da funcao auth_login porem retorna erro
        with patch.object(self.handler, "auth_login", side_effect=HTTPError(404)):
            with self.assertRaises(HTTPError) as context:
                self.handler.change_password("test@example.com", "wrongpassword", "newpassword123")
          
        # verifica que o erro foi levantado e corretamente "transformado"  
        self.assertEqual(context.exception.status_code, 409)

if __name__ == '__main__':
    unittest.main()
    