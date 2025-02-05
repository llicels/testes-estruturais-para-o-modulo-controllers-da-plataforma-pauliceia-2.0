# funcao testada:
# def is_current_user_an_administrator(self):
#         """
#         Check if the current user is an administrator
#         :return: True or False
#         """

#         current_user = self.get_current_user_()

#         return current_user["properties"]["is_the_admin"]

import unittest
from unittest.mock import MagicMock, patch

from vgiws.controllers.base import BaseHandler

# Sequência 1: Inicio – Obtém usuário atual – Verifica se admin – Usuário admin – Retorna true
# Sequência 2: Inicio – Obtém usuário atual – Verifica se admin – Usuário não é admin – Retorna false


class TestIsCurrentUserAdmin(unittest.TestCase):
    
    # sequencia 1 - usuario admin
    def test_current_user_admin(self):
        
        # configuracoes basicas
        self.mock_application = MagicMock()
        self.handler = BaseHandler(self.mock_application, MagicMock())
        
        # usuario simulado
        mock_user_data = {"properties": {"is_the_admin": True}}
        
        # simula que a funcao get user devolve os dados do usuario simulado
        with patch.object(self.handler, "get_current_user_", return_value=mock_user_data):
            # chama a funcao testada
            current_user = self.handler.is_current_user_an_administrator()
        
        # verifica que o usuario e admin
        self.assertTrue(current_user)
    
    # sequencia 2 - usuario nao e admin
    def test_current_user_not_admin(self):
        # configuracoes basicas
        self.mock_application = MagicMock()
        self.handler = BaseHandler(self.mock_application, MagicMock())
        
        # usuario simulado
        mock_user_data = {"properties": {"is_the_admin": False}}
        
        # simula que a funcao get user devolve os dados do usuario simulado
        with patch.object(self.handler, "get_current_user_", return_value=mock_user_data):
            # chama a funcao testada
            current_user = self.handler.is_current_user_an_administrator()
        
        # verifica que o usuario nao e admin
        self.assertFalse(current_user)

if __name__ == '__main__':
    unittest.main()