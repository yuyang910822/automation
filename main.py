import datetime
import time
import requests


begin = int(time.mktime(datetime.date.today().timetuple())*1000)
end = begin + (86400000-60000)
url = "http://10.3.7.244:8023/rpm-server/picking/page"

jsons = {
  "status": "500",
  "lastFinishTime": [
    1654012800000,
    1654099140000
  ],
  "lastFinishTimeBegin": 1654012800000,
  "lastFinishTimeEnd": 1654099140000,
  "pageNumber": 1,
  "pageSize": 200
}
headers = {
  'Content-Type': 'application/json',
  'token': 'eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTQzNDQ1MDEsImp0aSI6IkZHOHk0U3p5SkhOYmlGS1JYMVVkTmciLCJpYXQiOjE2MTQzMjY1MDEsInVzZXIiOiJ7XCJpZFwiOjIwNTEsXCJ1c2VyTmFtZVwiOlwiamRfYWRtaW5cIixcInJlYWxOYW1lXCI6XCJqZF9hZG1pblwiLFwiaXNJbml0UGFzc3dvcmRcIjowLFwiZGV2aWNlVHlwZVwiOjEsXCJ0eXBlXCI6NSxcImN1c3RvbWVySWRcIjo3MSxcImN1c3RvbWVyTmFtZVwiOlwi5Lqs5LicXCIsXCJwYXJlbnRJZFwiOjF9In0.uChQ5RelmK0fBl7WAlsIwY5jlRJJb-C3QBsPT1qSa2w',
  'deviceType': '1',
  'userId': '2051'
}

jsons['lastFinishTime'][0] = begin
jsons['lastFinishTime'][1] = end
jsons['lastFinishTimeBegin'] = begin
jsons['lastFinishTimeEnd'] = end

response = requests.request("POST", url, headers=headers, json=jsons)
print(response.json()['result']['totalCount'])
