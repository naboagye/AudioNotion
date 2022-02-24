import requests

page_id = "9f8b41acdfb34d31bb05000e8127a723"

url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100"

headers = {
  'Notion-Version': '2021-05-13',
  'Authorization': f'Bearer {token}'
}

response = requests.get(url, headers=headers)

for result in response.json()["results"]:
    if "paragraph" in result:
        for text in result["paragraph"]["text"]:
            print(text["plain_text"])
