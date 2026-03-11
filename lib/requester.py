import json
import requests
import secrets
import gc

gc.enable()

class Requester:

    def __init__(self):
        self.base_url = secrets.API_URL
        self.headers: dict = {
            "Content-Type": "application/json",
            "X-API-Key": secrets.API_KEY,
            "X-Device-Id": secrets.DEVICE_ID,
        }
        self.data: str | None = None

    def headers(self, headers: dict):
        self.headers.update(headers)

    def post(self, path: str, data: dict) -> dict | None:
        url = f"{self.base_url}/{path}"
        self.data = json.dumps(data)
        return self.__make_request(method="POST", url=url)

    def get(self, path: str) -> dict | None:
        url = f"{self.base_url}/{path}"
        return self.__make_request(url=url)

    def __make_request(self, url: str, method: str = "GET"):
        response = None
        try:
            response = requests.request(
                method, url,
                headers=self.headers,
                data=self.data,
                timeout=10,
            )
            return_value = {
                "status": response.status_code,
                "data": response.json(),
            }
        except ValueError as value_error:
            return_value = {
                "status": 400,
                "error": "Invalid request",
                "detail": str(value_error),
                "type": "ValueError"
            }
        except BaseException as error:
            return_value = {
                "status": 500,
                "error": "Unknown error",
                "detail": str(error),
                "type": type(error).__name__
            }
        finally:
            if response:
                response.close()
                gc.collect()
        return return_value
