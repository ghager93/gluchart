import requests

import jwt

LINK_UP_VERSION = "4.7.0"
LINK_UP_PRODUCT = "llu.android"
LINK_UP_REGION = "AU"

LINK_UP_BASE_URL = "https://api.libreview.io/llu/"
LINK_UP_LOGIN_URL = LINK_UP_BASE_URL + "auth/login/"
LINK_UP_CONNECTIONS_URL = LINK_UP_BASE_URL + "connections"


def get_token(email, password):
    body = {
        "email": email,
        "password": password
    }
    headers = {
        "version": LINK_UP_VERSION,
        "product": LINK_UP_PRODUCT
    }
    response = requests.post(LINK_UP_LOGIN_URL, json=body, headers=headers)
    token = response.json()["data"]["authTicket"]["token"]
    expiry = response.json()["data"]["authTicket"]["expires"]
    _validate_token(token)
    return token, expiry


def get_patient_id(token):
    headers = {
        "version": LINK_UP_VERSION,
        "product": LINK_UP_PRODUCT,
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(LINK_UP_CONNECTIONS_URL, headers=headers)
    return response.json()["data"][0]["patientId"]


def get_device_info(token, patient_id):
    headers = {
        "version": LINK_UP_VERSION,
        "product": LINK_UP_PRODUCT,
        "Authorization": f"Bearer {token}"
    }
    url = f"{LINK_UP_CONNECTIONS_URL}/{patient_id}/graph"
    response = requests.get(url, headers=headers)
    sensor_start_epoch = response.json()["data"]["connection"]["sensor"]["a"]
    graph_data = [{
            "timestamp": datum["Timestamp"], 
            "value": datum["Value"]
        } for datum in response.json()["data"]["graphData"]
    ]
    return sensor_start_epoch, graph_data


def _validate_token(token):
    jwt.decode(token, options={"verify_signature": False})