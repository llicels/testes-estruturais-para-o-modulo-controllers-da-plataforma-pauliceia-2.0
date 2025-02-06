# 2 tests failing
# funcao testada:
# def write_error(self, status_code, **kwargs):
#         """Override to implement custom error pages.

#         ``write_error`` may call `write`, `render`, `set_header`, etc
#         to produce output as usual.

#         If this error was caused by an uncaught exception (including
#         HTTPError), an ``exc_info`` triple will be available as
#         ``kwargs["exc_info"]``.  Note that this exception may not be
#         the "current" exception for purposes of methods like
#         ``sys.exc_info()`` or ``traceback.format_exc``.
#         """

#         if self.settings.get("serve_traceback") and "exc_info" in kwargs:
#             # in debug mode, try to send a traceback
#             self.set_header("Content-Type", "text/plain")

#             if len(kwargs["exc_info"]) >= 2:
#                 http_error = kwargs["exc_info"][1]

#                 track_message = ''.join(format_exception(*kwargs["exc_info"]))
#                 # error_message = format_exception(*kwargs["exc_info"])[-1]

#                 # the track message just will be logged then a 50X error occurs
#                 if status_code >= 500:
#                     logging.error(track_message)

#                 self.write(http_error.log_message)
#                 self.finish()
#             else:
#                 # original behavior
#                 for line in format_exception(*kwargs["exc_info"]):
#                     self.write(line)
#                 self.finish()

#         else:
#             self.finish(
#                 "<html><title>%(code)d: %(message)s</title>"
#                 "<body>%(code)d: %(message)s</body></html>"
#                 % {"code": status_code, "message": self._reason}
#             )

import unittest
from unittest.mock import MagicMock, patch
import logging
from tornado.web import HTTPError

from vgiws.controllers.base import BaseHandler

class TestWriteError(unittest.TestCase):
    def setUp(self):
        # Configuração inicial para os testes
        self.mock_application = MagicMock()
        self.handler = BaseHandler(self.mock_application, MagicMock())
        #self.handler.settings = {}
        self.handler._reason = "Test Reason"
        self.handler.set_header = MagicMock()
        self.handler.write = MagicMock()
        self.handler.finish = MagicMock()

    def test_write_error_with_exc_info_and_serve_traceback(self):
        # testa o caso em que há exc_info e serve_traceback está ativado
        self.handler.settings["serve_traceback"] = True
        exc_info = (HTTPError, HTTPError(500, log_message="Test Exception"), None)
        kwargs = {"exc_info": exc_info}

        with patch("logging.error") as mock_logging_error:
            self.handler.write_error(500, **kwargs)

            # verifica se a header foi definida corretamente
            self.handler.set_header.assert_called_once_with("Content-Type", "text/plain")

            # verifica se a mensagem de erro foi escrita
            self.handler.write.assert_called_once_with("Test Exception")

            # verifica se o método finish foi chamado
            self.handler.finish.assert_called_once()

            # verifica se a mensagem de erro foi logada
            mock_logging_error.assert_called_once()

    def test_write_error_with_exc_info_and_no_serve_traceback(self):
        # testa o caso em que há exc_info, mas serve_traceback está desativado
        self.handler.settings["serve_traceback"] = False
        exc_info = (HTTPError, HTTPError(500, log_message="Test Exception"), None)  # Use HTTPError
        kwargs = {"exc_info": exc_info}

        self.handler.write_error(500, **kwargs)

        # verifica se o método finish foi chamado com a mensagem de erro HTML
        self.handler.finish.assert_called_once_with(
            "<html><title>500: Test Reason</title>"
            "<body>500: Test Reason</body></html>"
        )

    def test_write_error_without_exc_info(self):
        # testa o caso em que não há exc_info
        kwargs = {}

        self.handler.write_error(404, **kwargs)

        # verifica se o método finish foi chamado com a mensagem de erro HTML
        self.handler.finish.assert_called_once_with(
            "<html><title>404: Test Reason</title>"
            "<body>404: Test Reason</body></html>"
        )

    def test_write_error_with_exc_info_and_status_below_500(self):
        # Testa o caso em que há exc_info, mas o código de status é menor que 500
        self.handler.settings["serve_traceback"] = True
        exc_info = (HTTPError, HTTPError(500, log_message="Test Exception"), None)
        kwargs = {"exc_info": exc_info}

        with patch("logging.error") as mock_logging_error:
            self.handler.write_error(400, **kwargs)

            # verifica se a header foi definida corretamente
            self.handler.set_header.assert_called_once_with("Content-Type", "text/plain")

            # verifica se a mensagem de erro foi escrita
            self.handler.write.assert_called_once_with("Test Exception")

            # verifica se o método finish foi chamado
            self.handler.finish.assert_called_once()

            # verifica se a mensagem de erro NÃO foi logada (status < 500)
            mock_logging_error.assert_not_called()

    def test_write_error_with_exc_info_and_invalid_exc_info_length(self):
        # testa o caso em que exc_info tem um comprimento inválido
        self.handler.settings["serve_traceback"] = True
        exc_info = (HTTPError, HTTPError(500, log_message="Test Exception"), None)
        kwargs = {"exc_info": exc_info}

        with patch("traceback.format_exception", return_value=["Traceback line 1\n", "Traceback line 2\n"]):
            self.handler.write_error(500, **kwargs)

            # verifica se a header foi definida corretamente
            self.handler.set_header.assert_called_once_with("Content-Type", "text/plain")

            # verifica se as linhas do traceback foram escritas
            self.handler.write.assert_any_call("Traceback line 1\n")
            self.handler.write.assert_any_call("Traceback line 2\n")

            # verifica se o método finish foi chamado
            self.handler.finish.assert_called_once()

if __name__ == "__main__":
    unittest.main()