import unittest
from unittest.mock import MagicMock, patch
import unittest.mock
from tornado.web import RequestHandler


from vgiws.controllers.base import BaseHandler

# Sequência 1: Inicio – Define HTTP status 204  -  Termina solicitação

class TestOptions(unittest.TestCase):
    def test_options(self):
        
        # configura imitacoes
        self.mock_application = MagicMock()
        self.mock_request = MagicMock()
        
        self.handler = BaseHandler(self.mock_application, self.mock_request)
        
        # imita set_status e finish
        self.handler.set_status = MagicMock()
        self.handler.finish = MagicMock()
        
        self.handler.options()
        
        # verifica que a funcao define o status 204
        self.handler.set_status.assert_called_once_with(204)
        self.handler.finish.assert_called_once()
        
if __name__ == "__main__":
    unittest.main()
    