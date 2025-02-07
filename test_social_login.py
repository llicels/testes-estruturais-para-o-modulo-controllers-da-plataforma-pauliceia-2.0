# funcao testada:
# def social_login(self, user, social_account):
#         # print("\nuser: ", user, "\n")
#         # for key in user:
#         #     print(key, ": ", user[key])

#         if isinstance(user["picture"], str):  # google photo
#             picture = user["picture"]
#         elif isinstance(user["picture"], dict):  # facebook photo
#             # picture = user["picture"]["data"]["url"]  # this image is 50x50
#             picture = "https://graph.facebook.com/{0}/picture?type=large&height=500".format(user['id'])
#         else:
#             picture = ''

#         user_json = {
#             'type': 'User',
#             'properties': {'user_id': -1, 'email': user["email"], 'password': '', 'username': user["email"],
#                            'name': user['name'], 'terms_agreed': True, 'receive_notification_by_email': False,
#                            'picture': picture, 'social_id': user['id'], 'social_account': social_account}
#         }

#         if "verified_email" not in user:  # login with facebook doesn't have "verified_email", but google has, so put it
#             user["verified_email"] = True

#         encoded_jwt_token = self.login(user_json, verified_social_login_email=user["verified_email"])

#         #self.write(json_encode({"token": encoded_jwt_token}))
#         URL_TO_REDIRECT = self.__AFTER_LOGIN_REDIRECT_TO__ + "/" + encoded_jwt_token
#         super(BaseHandler, self).redirect(URL_TO_REDIRECT)

import unittest
from unittest.mock import MagicMock, patch
from tornado.web import HTTPError

from vgiws.controllers.base import BaseHandlerSocialLogin

# Sequência 1: Inicio – Extrai dados da conta – Verifica verificação do email – Email verificado – Login ou cria novo usuário – Gera token JWT – Redireciona usuário com token
# Sequência 2: Inicio – Extrai dados da conta – Verifica verificação do email – Email não verificado – Levanta erro


class TestSocialLogin(unittest.TestCase):
    # sequencia 1 - email verificado
    
    @patch("tornado.web.RequestHandler.redirect")
    @patch.object(BaseHandlerSocialLogin, "login")
    def test_verified_email(self, mock_login, mock_redirect):
        self.mock_application = MagicMock()
        self.mock_request = MagicMock()
        self.handler = BaseHandlerSocialLogin(self.mock_application, self.mock_request)
        self.handler.__AFTER_LOGIN_REDIRECT_TO__ = "http://redirect.com"
        
        user = {
            "picture": "http://example.com/photo.jpg", 
            "email": "test@example.com",
            "name": "Test User",
            "id": "12345",
            "verified_email": True  
        }
        social_account = "google"

        mock_login.return_value = "dummy_jwt"

        self.handler.social_login(user, social_account)

        expected_user_json = {
            'type': 'User',
            'properties': {
                'user_id': -1,
                'email': "test@example.com",
                'password': '',
                'username': "test@example.com",
                'name': "Test User",
                'terms_agreed': True,
                'receive_notification_by_email': False,
                'picture': "http://example.com/photo.jpg",
                'social_id': "12345",
                'social_account': social_account
            }
        }
        mock_login.assert_called_once_with(expected_user_json, verified_social_login_email=True)

        expected_url = self.handler.__AFTER_LOGIN_REDIRECT_TO__ + "/dummy_jwt"
        mock_redirect.assert_called_once_with(expected_url)


    
    # sequencia 2 - email nao verificado
    
    @patch.object(BaseHandlerSocialLogin, "login")
    def test_unverified_email(self, mock_login):
        self.mock_application = MagicMock()
        self.mock_request = MagicMock()
        self.handler = BaseHandlerSocialLogin(self.mock_application, self.mock_request)
        self.handler.__AFTER_LOGIN_REDIRECT_TO__ = "http://redirect.com"
        
        user = {
            "picture": {"data": {"url": "http://example.com/photo_small.jpg"}},
            "email": "test2@example.com",
            "name": "Test User2",
            "id": "67890",
            "verified_email": False
        }
        social_account = "facebook"

        expected_picture = "https://graph.facebook.com/67890/picture?type=large&height=500"
        
        mock_login.side_effect = ValueError("Email not verified")

        with self.assertRaises(ValueError) as context:
            self.handler.social_login(user, social_account)
        
        self.assertEqual(str(context.exception), "Email not verified")
        
        expected_user_json = {
            'type': 'User',
            'properties': {
                'user_id': -1,
                'email': "test2@example.com",
                'password': '',
                'username': "test2@example.com",
                'name': "Test User2",
                'terms_agreed': True,
                'receive_notification_by_email': False,
                'picture': expected_picture,
                'social_id': "67890",
                'social_account': social_account
            }
        }
        mock_login.assert_called_once_with(expected_user_json, verified_social_login_email=False)
        


if __name__ == '__main__':
    unittest.main()