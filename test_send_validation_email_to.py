#erro
import unittest
from unittest.mock import MagicMock, patch

from vgiws.controllers.base import BaseHandler


class TestSendValidationEmail(unittest.TestCase):
    def normalize_text(self, text):
        """Remove espaços extras e normaliza quebras de linha para evitar erros de comparação"""
        return "\n".join(line.strip() for line in text.strip().splitlines())

    # Sequência 1 - Modo debug
    @patch("vgiws.settings.settings.__EMAIL_SIGNATURE__", "Equipe Pauliceia")
    @patch("vgiws.settings.settings.__VALIDATE_EMAIL_DEBUG__", "http://debug-url.com")
    @patch("vgiws.controllers.base.send_email")
    @patch("vgiws.controllers.base.generate_encoded_jwt_token", return_value="mock_token")
    def test_notification_debug(self, mock_generate_token, mock_send_email):
        self.mock_application = MagicMock()
        self.handler = BaseHandler(self.mock_application, MagicMock())

        # Simula o modo debug
        self.handler.DEBUG_MODE = True
        self.handler.send_validation_email_to("test@exemplo.com", "123")

        # Verifica se a URL debug foi usada
        expected_url = "http://debug-url.com/mock_token"
        expected_body = f"""
            Hello,

            Please, not reply this message.

            Please, click on under URL to validate your email:
            {expected_url}

            Equipe Pauliceia
        """

        # Normaliza as strings antes de comparar
        expected_body = self.normalize_text(expected_body)
        actual_body = self.normalize_text(mock_send_email.call_args[0][2])

        self.assertEqual(actual_body, expected_body)
        mock_send_email.assert_called_once_with(
            "test@exemplo.com", subject="Email Validation - Not reply", body=mock_send_email.call_args[0][2]
        )

    # Sequência 2 - Modo produção
    @patch("vgiws.settings.settings.__EMAIL_SIGNATURE__", "Equipe Pauliceia")
    @patch("vgiws.settings.settings.__VALIDATE_EMAIL__", "http://prod-url.com")
    @patch("vgiws.controllers.base.send_email")
    @patch("vgiws.controllers.base.generate_encoded_jwt_token", return_value="mock_token")
    def test_notification_prod(self, mock_generate_token, mock_send_email):
        self.mock_application = MagicMock()
        self.handler = BaseHandler(self.mock_application, MagicMock())

        # Simula o modo produção
        self.handler.DEBUG_MODE = False
        self.handler.send_validation_email_to("test@exemplo.com", "123")

        # Verifica se a URL de produção foi usada
        expected_url = "http://prod-url.com/mock_token"
        expected_body = f"""
            Hello,

            Please, not reply this message.

            Please, click on under URL to validate your email:
            {expected_url}

            Equipe Pauliceia
        """

        # Normaliza as strings antes de comparar
        expected_body = self.normalize_text(expected_body)
        actual_body = self.normalize_text(mock_send_email.call_args[0][2])

        self.assertEqual(actual_body, expected_body)
        mock_send_email.assert_called_once_with(
            "test@exemplo.com", subject="Email Validation - Not reply", body=mock_send_email.call_args[0][2]
        )


if __name__ == '__main__':
    unittest.main()
