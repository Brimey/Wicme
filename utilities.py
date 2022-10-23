import json
import requests
import os
from dotenv import load_dotenv


def get_response(url):
    return requests.get(url)


def grab_data(server_response):
    """
    :param server_response: Response object returned from the GET request.
    :return: Returns a string containing dictionaries of the data.
    """
    data, start, end = server_response.text, server_response.text.index(
        '[{\\"donation_id'), server_response.text.index('\\"identity\\":[]')
    return data[start + 1:end - 2].replace('\\', '').replace("'", '"')


def retrieve_keys(env_var):
    load_dotenv()
    return os.getenv(env_var)


def transform_data(raw_json):
    """
    :param raw_json: A string containing dictionaries of the donations.
    :return: A dictionary from the raw string full of dictionaries retrieved from the grab_data function.
    """
    return json.loads('{"data":[' + grab_data(raw_json) + ']}')
