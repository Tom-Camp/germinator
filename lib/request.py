import requests


class Requester:

    def __init__(self, url: str):
        self.base_url = url
        self.headers: dict = {"Content-Type": "application/json"}
        self.kwargs: dict = {}
        self.url: str = ""

    def headers(self, headers: dict):
        self.headers.update(headers)

    def post(self, path: str, data: dict) -> dict | None:
        self.url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        self.kwargs = {"headers": self.headers, "json": data}
        return self.__make_request("POST")

    def get(self, path: str) -> dict | None:
        self.url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        self.kwargs = {"headers": self.headers}
        return self.__make_request()

    def __make_request(self, method: str = "GET"):
        try:
            response = requests.request(method, self.url, **self.kwargs)
            try:
                result = response.json()
            except ValueError:
                result = response.text

            return {
                "status": response.status_code,
                "data": result
            }
        except OSError as os_error:
            return {
                'status': 500,
                'error': 'Network error',
                'detail': str(os_error),
                'type': 'OSError'
            }
        except ValueError as value_error:
            return {
                'status': 400,
                'error': 'Invalid request',
                'detail': str(value_error),
                'type': 'ValueError'
            }
        except BaseException as error:
            return {
                'status': 500,
                'error': 'Unknown error',
                'detail': str(error),
                'type': type(error).__name__
            }
        finally:
            if "response" in locals():
                response.close()
