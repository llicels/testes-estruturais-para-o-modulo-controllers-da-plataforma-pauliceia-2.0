# funcao testada:
# def send_validation_email_to(self, to_email_address, user_id):
#         if self.DEBUG_MODE:
#             url_to_validate_email = __VALIDATE_EMAIL_DEBUG__
#         else:
#             url_to_validate_email = __VALIDATE_EMAIL__

#         email_token = generate_encoded_jwt_token({"user_id": user_id})

#         url_to_validate_email += "/" + email_token   # convert bytes to str

#         subject = "Email Validation - Not reply"
#         body = """
# Hello,

# Please, not reply this message.

# Please, click on under URL to validate your email:
# {0}

# {1}
#         """.format(url_to_validate_email, __EMAIL_SIGNATURE__)

#         send_email(to_email_address, subject=subject, body=body)

import unittest
from unittest.mock import MagicMock, patch

from vgiws.controllers.base import BaseHandler
import vgiws.settings.settings
import vgiws.settings.accounts

# Sequência 1: Inicio – Verifica modo debug – Define URL de validação debug – Gera token de validação de email – Elabora o corpo do email – Envia email via SMTP
# Sequência 2: Inicio – Verifica modo debug – Define URL de validação de produção – Gera token de validação de email – Elabora o corpo do email – Envia email via SMTP



class TestSendValidationEmail(unittest.TestCase):
    
    @patch("vgiws.controllers.base.send_email")  # primeiro patch -> ultimo argumento
    @patch("vgiws.controllers.base.generate_encoded_jwt_token", return_value="mock_token")
    @patch.object(vgiws.settings.settings, "__VALIDATE_EMAIL_DEBUG__", "http://localhost:8081/portal/valid/email")
    @patch.object(vgiws.settings.accounts, "__EMAIL_SIGNATURE__", """--

Best regards

Team""")
    
    # sequencia 1 - modo debug
    def test_validation_debug(self, mock_generate_token, mock_send_email):
        
        self.mock_application = MagicMock()
        self.mock_application.DEBUG_MODE = True
        self.handler = BaseHandler(self.mock_application, MagicMock())
        
        self.handler.send_validation_email_to("email@test.com", 1)
        
        expected_url = "http://localhost:8081/portal/valid/email/mock_token"
        expected_signature = """--

Best regards

Team"""
        expected_subject = "Email Validation - Not reply"
        expected_body = """
Hello,

Please, not reply this message.

Please, click on under URL to validate your email:
{0}

{1}

        """.format(expected_url, expected_signature)
             
        mock_send_email.assert_called_once_with(
            "email@test.com",
            subject=expected_subject,
            body=expected_body
        )
    
    @patch("vgiws.controllers.base.send_email")  # primeiro patch -> ultimo argumento
    @patch("vgiws.controllers.base.generate_encoded_jwt_token", return_value="mock_token")
    @patch.object(vgiws.settings.settings, "__VALIDATE_EMAIL__", "https://pauliceia.unifesp.br/portal/valid/email")
    @patch.object(vgiws.settings.accounts, "__EMAIL_SIGNATURE__", """--

Best regards

Team""")
    # sequencia 2 - modo producao
    def test_validation_prod(self, mock_generate_token, mock_send_email):
        
        self.mock_application = MagicMock()
        self.mock_application.DEBUG_MODE = False
        self.handler = BaseHandler(self.mock_application, MagicMock())
        
        self.handler.send_validation_email_to("email@test.com", 1)
        
        expected_url = "https://pauliceia.unifesp.br/portal/valid/email/mock_token"
        
        expected_signature = """--

Best regards

Team"""
        expected_subject = "Email Validation - Not reply"
        expected_body = """
Hello,

Please, not reply this message.

Please, click on under URL to validate your email:
{0}

{1}

        """.format(expected_url, expected_signature)
        
        mock_send_email.assert_called_once_with(
            "email@test.com",
            subject=expected_subject,
            body=expected_body
        )
        
if __name__ == '__main__':
    unittest.main()

