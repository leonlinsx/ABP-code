# https://topherpedersen.blog/2019/10/12/my-job-application-to-plaid-inc/
# script to submit job app via Plaid API
# https://plaid.com/job/?id=999aae38-1405-4ed7-805f-440181e7ac62
# https://plaid.com/job/?id=a2ab74d3-0cf1-4c7c-8506-d6c7582d8061

import requests
import json

url = "https://contact.plaid.com/jobs"

data = {
  "name": "Leon Lin",
  "email": "leon.lin.sx+pm@gmail.com",
  "resume": "https://docs.google.com/document/d/1kHiBgAr5vvt9NGN8Mel7neTvFx1lmh16rqwuDxyBVbE/edit?usp=sharing",
  "phone": "434-466-6773",
  "job_id": "999aae38-1405-4ed7-805f-440181e7ac62",
  "github": "github.com/leonlinsx/ABP-code",
  "twitter": "@leonlinsx",
  "website": "https://avoidboringpeople.substack.com/",
  "location": "NYC",
  "favorite_candy": "all of them",
  "superpower": "looking up old notes on sending json requests. on a more serious note, here: https://www.leonlinsx.com/about-me/"
}

data = json.dumps(data)

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

http_post_request = requests.post(url=url, data=data, headers=headers)

server_response = http_post_request.text

print(server_response)