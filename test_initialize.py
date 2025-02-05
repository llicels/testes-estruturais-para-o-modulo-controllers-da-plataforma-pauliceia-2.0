# funcao testada:
#     def initialize(self):
#         # get the database instance
#         self.PGSQLConn = self.application.PGSQLConn

#         # get the mode of system (debug or not)
#         self.DEBUG_MODE = self.application.DEBUG_MODE

#         if self.DEBUG_MODE:
#             self.__REDIRECT_URI_GOOGLE__ = __REDIRECT_URI_GOOGLE_DEBUG__
#             self.__REDIRECT_URI_FACEBOOK__ = __REDIRECT_URI_FACEBOOK_DEBUG__
#             self.__AFTER_LOGIN_REDIRECT_TO__ = __AFTER_LOGIN_REDIRECT_TO_DEBUG__
#         else:
#             self.__REDIRECT_URI_GOOGLE__ = __REDIRECT_URI_GOOGLE__
#             self.__REDIRECT_URI_FACEBOOK__ = __REDIRECT_URI_FACEBOOK__
#             self.__AFTER_LOGIN_REDIRECT_TO__ = __AFTER_LOGIN_REDIRECT_TO__

import unittest
from unittest.mock import patch, MagicMock
from requests.exceptions import HTTPError
from tornado.web import RequestHandler

from vgiws.controllers.base import BaseHandler

# Sequência 1: Inicio – Recupera conexão com o BD – Verifica modo debug – Define configuração de debug
# Sequência 2: Inicio – Recupera conexão com o BD – Verifica o modo debug – Define configurações de produção

class TestInitialize(unittest.TestCase):
    def setUp(self):
        self.mock_application = MagicMock()
        self.mock_application.PGSQLConn = MagicMock() # imita uma conexao com o DB
        self.mock_application.DEBUG_MODE = True
        
        self.handler = BaseHandler(self.mock_application, MagicMock()) #chama a funcao testada (argumentos imitados)
        self.handler.initialize()
        
        BaseHandler.urls = []
    
    # testa que a url é inicialmente vazia
    def test_urls_initially_empty(self):
        self.assertEqual(BaseHandler.urls, [])
        
    # adiciona as urls dinamicamente
    def test_add_urls(self):
        BaseHandler.urls.append("/test-url")
        self.assertIn("/test-url", BaseHandler.urls)
        
    # checa conexao BD
    def test_missing_database_connection(self):
       self.mock_application.PGSQLConn = None  # conexao vazia com o banco
       self.handler.initialize() 

       # tenta acessar um metodo nao existente para estimular o erro
       with self.assertRaises(AttributeError):
           _ = self.handler.PGSQLConn.some_method  
        
    # testa modo debug / direcionamento das URIs corretas
    def test_debug_mode_redirects(self):
        with patch("vgiws.controllers.base.__REDIRECT_URI_GOOGLE_DEBUG__", "debug_google"),  \
             patch("vgiws.controllers.base.__REDIRECT_URI_FACEBOOK_DEBUG__", "debug_facebook"), \
             patch("vgiws.controllers.base.__AFTER_LOGIN_REDIRECT_TO_DEBUG__", "debug_redirect"):
           self.handler.initialize()
           self.assertEqual(self.handler.__REDIRECT_URI_GOOGLE__, "debug_google")
           self.assertEqual(self.handler.__REDIRECT_URI_FACEBOOK__, "debug_facebook")
           self.assertEqual(self.handler.__AFTER_LOGIN_REDIRECT_TO__, "debug_redirect")
    
    # test modo producao / direcionamento das URIs corretas
    def test_production_mode_redirects(self):
        self.mock_application.DEBUG_MODE = False
        with patch("vgiws.controllers.base.__REDIRECT_URI_GOOGLE__", "prod_google"), \
             patch("vgiws.controllers.base.__REDIRECT_URI_FACEBOOK__", "prod_facebook"), \
             patch("vgiws.controllers.base.__AFTER_LOGIN_REDIRECT_TO__", "prod_redirect"):
            self.handler.initialize()
            self.assertEqual(self.handler.__REDIRECT_URI_GOOGLE__, "prod_google")
            self.assertEqual(self.handler.__REDIRECT_URI_FACEBOOK__, "prod_facebook")
            self.assertEqual(self.handler.__AFTER_LOGIN_REDIRECT_TO__, "prod_redirect")
    
   


if __name__ == "__main__":
    unittest.main()