# funcao testada:
# def send_notification_by_email(self, resource_json, current_user_id):
#         try:
#             users_to_send_email = self.get_users_to_send_email(resource_json)
#         except HTTPError as error:
#             # if not found users, send to 0 users the notifications
#             if error.status_code == 404:
#                 users_to_send_email = {"features": []}
#             else:
#                 raise error

#         self.send_email_to_selected_users(users_to_send_email, current_user_id, resource_json)

import unittest
from unittest.mock import MagicMock, patch
from tornado.web import HTTPError

from vgiws.controllers.base import BaseHandler

# Sequência 1: Inicio – Obtém usuários para notificar – Notifica usuários selecionados
# Sequência 2: Inicio – Obtém usuários para notificar – Exceções de erro


class TestSendNotification(unittest.TestCase):
    # sequencia 1 - válida
    def test_email_notification(self):
        self.mock_application = MagicMock()
        self.handler = BaseHandler(self.mock_application, MagicMock())
        
        mock_resource_json = {"properties": {"description": "Mock-description"}}
        
        mock_users = {
            "features": [
                {"properties": {"user_id": 1}},
                {"properties": {"user_id": 2}}
            ]
        }
        
        with patch.object(self.handler, "get_users_to_send_email", return_value=mock_users) as mock_get_users:
            with patch.object(self.handler, "send_email_to_selected_users") as mock_send_email:
                self.handler.send_notification_by_email(mock_resource_json, 1)
                mock_get_users.assert_called_once_with(mock_resource_json)
                mock_send_email.assert_called_once_with(mock_users, 1, mock_resource_json)
        
    
    # sequencia 2 - erro
    def test_email_notification_error(self):
        self.mock_application = MagicMock()
        self.handler = BaseHandler(self.mock_application, MagicMock())
        
        mock_resource_json = {"properties": {"description": "Mock-description"}}
        
        with patch.object(self.handler, "get_users_to_send_email", side_effect=HTTPError(404)) as mock_get_users:
            with patch.object(self.handler, "send_email_to_selected_users") as mock_send_email:
                self.handler.send_notification_by_email(mock_resource_json, 1)
                mock_send_email.assert_called_once_with({"features": []}, 1, mock_resource_json)
        

if __name__ == '__main__':
    unittest.main()
    
        