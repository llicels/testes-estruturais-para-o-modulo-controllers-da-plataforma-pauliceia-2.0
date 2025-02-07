# funcao testada:
# def send_email_to_selected_users(self, users_to_send_email, current_user_id, resource_json):
#         user_that_is_sending_email = self.PGSQLConn.get_users(user_id=current_user_id)["features"][0]

#         subject = "Notification - Not reply"
#         body = """
# Hello,

# Please, not reply this message.

# {0} has sent a new notification:

# "{1}"

# Enter on the Pauliceia platform to visualize or reply this notification.

# {2}
#         """.format(user_that_is_sending_email["properties"]["name"],
#                    resource_json["properties"]["description"],
#                    __EMAIL_SIGNATURE__)

#         for user in users_to_send_email["features"]:
#             if user["properties"]["receive_notification_by_email"] and user["properties"]["is_email_valid"]:
#                 send_email(user["properties"]["email"], subject=subject, body=body)

import unittest
from unittest.mock import MagicMock, patch

from vgiws.controllers.base import BaseHandler
import vgiws.settings.accounts

# Sequência 1: Inicio – Recupera informações do usuário atual – Elabora o corpo do email – Itera pelos usuários selecionados – Verifica validez do email – Envia email – Itera pelos usuários selecionados
# Sequência 2: Inicio – Recupera informações do usuário atual – Elabora o corpo do email – Itera pelos usuários selecionados – Todos os emails enviados
# Sequência 3: Inicio – Recupera informações do usuário atual – Elabora o corpo do email – Itera pelos usuários selecionados – Checa validez do email – Pula usuário (Email inválido) – Itera pelos usuários selecionados

class TestEmailSelectedUser(unittest.TestCase):
    @patch.object(vgiws.settings.accounts, "__EMAIL_SIGNATURE__", """--

Best regards

Team""")
    @patch("vgiws.controllers.base.send_email")
    def test_email_users(self, mock_send_email):
        self.mock_application = MagicMock()
        self.mock_application.PGSQLConn = MagicMock()
        
        self.handler = BaseHandler(self.mock_application, MagicMock())
        
        mock_user_sending_email = {"properties": {"name": "Jane", "user_id": 1}}
        self.mock_application.PGSQLConn.get_users.return_value = {"features": [mock_user_sending_email]}
        
        mock_resource_json = {"properties": {"description": "Mock-description"}}
        
        mock_users_to_send_email = {
            "features": [
                # email valido e com notificacoes ativadas
                {"properties": {"email": "user1@example.com", "receive_notification_by_email": True, "is_email_valid": True}},
                # email com notificacoes desativadas
                {"properties": {"email": "user2@example.com", "receive_notification_by_email": False, "is_email_valid": True}},
                # email invalido
                {"properties": {"email": "user3@example.com", "receive_notification_by_email": True, "is_email_valid": False}},
            ]
        }
        
        expected_subject = "Notification - Not reply"
        
        expected_signature = """--

Best regards

Team"""
        
        expected_body = """
Hello,

Please, not reply this message.

{0} has sent a new notification:

"{1}"

Enter on the Pauliceia platform to visualize or reply this notification.

{2}

        """.format(mock_user_sending_email["properties"]["name"],
                   mock_resource_json["properties"]["description"],
                   expected_signature)
        
        self.handler.send_email_to_selected_users(mock_users_to_send_email, 1, mock_resource_json)
        
        mock_send_email.assert_called_once_with(
            "user1@example.com",
            subject=expected_subject,
            body=expected_body
        )

if __name__ == '__main__':
    unittest.main()
        