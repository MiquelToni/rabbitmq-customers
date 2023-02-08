import requests
from ..IDataResolver import IDataResolver

payload = {}
headers = {
    'Cookie': 'CTK=1gop1tahtjv67800; __cf_bm=XKFTWrrtRadJeVM0gy72e3HzaRjrDiWheChkki2XyqM-1675878116-0-AV0Kyb8bz6kknsTQblZLY6srlRqBKtXWARXxTKYm5voljCE9MrSqIkHMnhFNmCrh6j3ZqV1Lx6NwaEM19kh8XJc=; _cfuvid=jhpbFYQgO3mCRUuWYAb6GEiRM.lETQbzni88tmAN_Z0-1675878116363-0-604800000; INDEED_CSRF_TOKEN=Bi9NvV0YTRb7qg1do7iIiEQIXbX53v6S; JSESSIONID=EA3772246A24C7BF26C8B719B52E417F; LV="LA=1675878115:CV=1675878115:TS=1675878115"; RQ="q=rabbitmq&l=&ts=1675878115941"; UD="LA=1675878115:CV=1675878115:TS=1675878115:SG=c46400ab8866458aefc218bf1718d6ab"; ctkgen=1; indeed_rcc=""; jaSerpCount=1'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)


class DataResolver(IDataResolver):
    def get_data_html(self, q: str, offset: int) -> str:
        url = f"https://es.indeed.com/jobs?q={q}&start={str(offset)}"
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 200:
          return response.text
        else:
           return ""
