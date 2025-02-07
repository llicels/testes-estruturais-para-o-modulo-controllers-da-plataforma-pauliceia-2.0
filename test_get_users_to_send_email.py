# funcao testada:
# def get_users_to_send_email(self, resource_json):
#         users = {"features": []}

#         # (1) general notification, everybody receives a notification by email
#         if resource_json["properties"]["layer_id"] is None and resource_json["properties"]["keyword_id"] is None \
#                 and resource_json["properties"]["notification_id_parent"] is None:
#             users = self.PGSQLConn.get_users()

#         # (2) notification by layer
#         elif resource_json["properties"]["layer_id"] is not None:
#             # (2.1) everybody who is collaborator of the layer, will receive a not. by email

#             # get all the collaborators of the layer
#             # users_layer = self.PGSQLConn.get_user_layers(layer_id=resource_json["properties"]["layer_id"])
#             #
#             # # get the user information of the collaborators
#             # for user_layer in users_layer["features"]:
#             #     user = self.PGSQLConn.get_users(user_id=user_layer["properties"]["user_id"])["features"][0]
#             #     users["features"].append(user)

#             # (2.1) everybody who follows the layer, will receive a notification by email

#             users_follow_layer = self.PGSQLConn.get_layer_follower(layer_id=resource_json["properties"]["layer_id"])

#             # get the user information of the collaborators
#             for user_follow_layer in users_follow_layer["features"]:
#                 user = self.PGSQLConn.get_users(user_id=user_follow_layer["properties"]["user_id"])["features"][0]
#                 users["features"].append(user)

#         # TODO: (3) notification by keyword: everybody who follows the keyword, will receive a notification by email
#         # elif resource_json["properties"]["keyword_id"] is not None:
#         #     pass

#         return users

import unittest
from unittest.mock import MagicMock, patch

from vgiws.controllers.base import BaseHandler

# Sequência 1: Inicio – Determina tipo de notificação – Notificação geral – Busca todos os usuários
# Sequência 2: Inicio – Determina tipo de notificação – Notificação por camada – Busca seguidores da camada


class TestGetUsersSendEmail(unittest.TestCase):
    # sequencia 1 - notificacao geral
    def test_notify_all(self):
        self.mock_application = MagicMock()
        self.mock_application.PGSQLConn = MagicMock()
        
        self.handler = BaseHandler(self.mock_application, MagicMock())
        
        mock_resource_json = {"properties": 
            {"layer_id": None, 
             "keyword_id": None, 
             "notification_id_parent": None}}
        
        mock_users = {
            "features": [
                {"properties": {"user_id": 1}},
                {"properties": {"user_id": 2}}
            ]
        }
        
        self.mock_application.PGSQLConn.get_users.return_value = mock_users
        
        result = self.handler.get_users_to_send_email(mock_resource_json)
        
        self.mock_application.PGSQLConn.get_users.assert_called_once()
        
        self.assertEqual(result, mock_users)
    
    # sequencia 2 - notificacao selecionada
    # teste falhando!
    def test_notify_selected(self):
        self.mock_application = MagicMock()
        self.mock_application.PGSQLConn = MagicMock()
        
        self.handler = BaseHandler(self.mock_application, MagicMock())
        
        mock_resource_json = {"properties": 
            {"layer_id": 1, 
             "keyword_id": None, 
             "notification_id_parent": None}}
        
        mock_users = {
            "features": [
                {"properties": {"user_id": 1, "user_follow_layer": True}},
                {"properties": {"user_id": 2, "user_follow_layer": False}}
            ]
        }
        
        self.mock_application.PGSQLConn.get_layer_follower.return_value = mock_users
        
        def get_users_side_effect(*args, **kwargs):
            if 'user_id' in kwargs:
                uid = kwargs['user_id']
                
                if uid == 1:
                    return {"features": [{"properties": {"user_id": 1, "user_follow_layer": True}}]}
                
                else:
                    return {"features": [{"properties": {"user_id": uid, "user_follow_layer": False}}]}
                
            return {"features": []}
        
        self.mock_application.PGSQLConn.get_users.side_effect = get_users_side_effect
        
        result = self.handler.get_users_to_send_email(mock_resource_json)
        
        self.mock_application.PGSQLConn.get_layer_follower.assert_called_once_with(layer_id=1)
        
        self.assertEqual(self.mock_application.PGSQLConn.get_users.call_count, 2)
        
        expected_result = [{"properties": {"user_id": 1, "user_follow_layer": True}}]
        
        self.assertEqual(result["features"], expected_result)

if __name__ == '__main__':
    unittest.main()
        
        