import requests
import json
from requests.exceptions import RequestException


def fetch_data(url):
    """
    Fetches and returns json data 
    :param url: 
    :return Result object with data and boolean status: 
    """
    result = Result(status=False, data=None)

    try:
        response = requests.get(url)
        data = json.loads(response.text)
        result.data = data
        result.status = True
    except RequestException:
        pass

    return result


class Result:
    def __init__(self, data, status):
        self.data = data
        self.status = status
