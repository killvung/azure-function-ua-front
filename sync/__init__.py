import logging
import azure.functions as func
import os
import requests


class OAuthClient:
    def __init__(self, client_key, client_secret):
        self.client_key = client_key
        self.client_secret = client_secret
        self.base_url = 'https://oauth2-api.mapmyapi.com/v7.1/oauth2/'

    def get_access_token(self, code):
        try:
            headers = {'Api-Key':  self.client_key,
                       'Content-Type': 'application/x-www-form-urlencoded'}
            data = {'grant_type': 'authorization_code',
                    'client_id': self.client_key, 'client_secret':  self.client_secret,
                    'code': code}
            response = requests.post(
                self.base_url + 'access_token', data=data, headers=headers)
            return response.json()['access_token']
        except Exception:
            return func.HttpResponse(
                "Unable to retrieve access token",
                status_code=400
            )


class UAClient:
    """
    class to abstract Under Armour developer API request logic
    """

    def __init__(self, access_token=None):
        self.baseurl = "https://api.ua.com/v7.1/"

    def self(self, access_token):
        headers = {'Authorization': 'Bearer ' + access_token}
        response = requests.get(
            self.baseurl + 'user/self', headers=headers).json()
        return response

    def routes(self, access_token):
        """
        TODO: Implement instance method for retrieving routes data
        """
        pass


CLIENT_KEY = os.environ.get('CLIENT_KEY')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
oauth_client = OAuthClient(CLIENT_KEY, CLIENT_SECRET)
ua_client = UAClient()


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure functions for syncing walks and runs to database
    It first request access token through oauth 2, then 
    call UA API for stuff
    """
    logging.info('Python HTTP trigger function processed a request.')
    if req.params.get('code') == None:
        return func.HttpResponse(
            "code param is not provided",
            status_code=400
        )

    code = req.params.get('code')
    access_token = oauth_client.get_access_token(code)
    self_response = ua_client.self(access_token)
    return func.HttpResponse(
        self_response['display_name'],
        status_code=200
    )
