import requests
import json
import uuid
from pathlib import Path

class _screenshotapi():
    url = "https://screenshotapi.net/api/v1/screenshot"

    def __init__(self,apiToken,ca=None,requestTimeout=30):
        self.apiToken = apiToken
        self.requestTimeout = requestTimeout
        if ca:
            self.ca = Path(ca)
        else:
            self.ca = None

    def takeScreenshot(self,targetURL):
        try:
            url = "{0}?url={1}&token={2}".format(self.url,targetURL,self.apiToken)
            if self.ca:
                response = requests.get(url, verify=self.ca, timeout=self.requestTimeout)
            else:
                response = requests.get(url, timeout=self.requestTimeout)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            return 0, "Connection Timeout"

        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return None

    def downloadScreenshot(self,url):
        try:
            if self.ca:
                response = requests.get(url, verify=self.ca, timeout=self.requestTimeout, stream=True)
            else:
                response = requests.get(url, timeout=self.requestTimeout, stream=True)
            if response.status_code == 200:
                filename = "{0}{1}".format(str(uuid.uuid4()),".png")
                with open(Path("plugins/screenshotapi/screenshots/{0}".format(filename)),'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                return filename
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            pass
        return None
