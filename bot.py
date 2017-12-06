# -*- coding: utf-8 -*-
import os
import message

from slackclient import SlackClient

authed_teams = {}


class Bot(object):
    def __init__(self):
        super(Bot, self).__init__()
        self.name = "adservicesbot"
        self.emoji = ":robot_face:"
        # When we instantiate a new bot object, we can access the app
        # credentials we set earlier in our local development environment.
        self.oauth = {"client_id": os.environ.get("CLIENT_ID"),
                      "client_secret": os.environ.get("CLIENT_SECRET"),
                      # Scopes provide and limit permissions to what our app
                      # can access. It's important to use the most restricted
                      # scope that your app will need.
                      "scope": "bot chat:write:bot"}
        self.verification = os.environ.get("VERIFICATION_TOKEN")

        self.client = SlackClient("")
        self.messages = {}

    def auth(self, code):
        auth_response = self.client.api_call(
                                "oauth.access",
                                client_id=self.oauth["client_id"],
                                client_secret=self.oauth["client_secret"],
                                code=code
                                )
        team_id = auth_response["team_id"]
        authed_teams[team_id] = {"bot_token":
                                 auth_response["bot"]["bot_access_token"]}
        self.client = SlackClient(authed_teams[team_id]["bot_token"])


    def send_reply(self, event, team_id, user_id):
        print(event['event']['channel'])
        post_message = self.client.api_call("chat.postMessage",
                                            channel=event['event']['channel'],
                                            text='Echo!',
                                            )
        print(post_message)


