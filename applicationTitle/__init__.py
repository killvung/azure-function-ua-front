import logging
import azure.functions as func
import os
import requests


def main(req: func.HttpRequest) -> func.HttpResponse:
    url = 'https://oauth2-api.mapmyapi.com/v7.1/oauth2/access_token/'

    CLIENT_KEY = os.environ.get('CLIENT_KEY')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

    headers = {'Api-Key': CLIENT_KEY,
               'Content-Type': 'application/x-www-form-urlencoded'}

    data = {'grant_type': 'client_credentials',
            'client_id': CLIENT_KEY, 'client_secret': CLIENT_SECRET}

    try:
        response = requests.post(url, data=data, headers=headers)
        access_token = response.json()['access_token']
        headers = {'Authorization': 'Bearer ' +
                   access_token, 'Api-Key': CLIENT_KEY}
        url = 'https://api.ua.com/v7.2/api_client/' + CLIENT_KEY
        func.HttpResponse(f"Hello World")
        key_data = requests.get(url, headers=headers).json()
        logging.info(key_data['application_title'])
        return func.HttpResponse(
            key_data['application_title'],
            status_code=200
        )
    except Exception:
        return func.HttpResponse(
            "Unable to retrieve API information",
            status_code=400
        )
