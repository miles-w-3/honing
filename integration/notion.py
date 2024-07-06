import requests
import os
from integration.user_search import UserSearch


class NotionIntegration:

  def __init__(self):
    self.token = os.environ['NOTION_TOKEN']

    self.session = requests.Session()
    self.session.headers.update({
      "Authorization": "Bearer " + self.token,
      "Content-Type": "application/json",
      "Notion-Version": "2022-06-28",
    })

  def process_hub_page_entries(self):
    user_searches = []
    hub_page_entries = self._query_hub_page()
    for result in hub_page_entries:
      try:
        search_urls = self._grab_urls(result["properties"]["Searches"]["rich_text"])
        user_search = UserSearch(
          database_id=result['id'],
          search_name=result["properties"]["Name"]["title"][0]["plain_text"],
          search_urls=search_urls
        )
        print(f'User search is {user_search}')
        user_searches.append(user_search)
      except KeyError:
        continue
    return user_searches

  def _grab_urls(self, rich_text_list) -> list[str]:
    urls = []
    for rich_text_entry in rich_text_list:
      try:
        url = rich_text_entry["href"]
        if url:
          print(f'url is {url}')
          urls.append(url)
      except AttributeError:
        continue
    return urls

  def _query_hub_page(self):
    hub_page_id = self._get_hub_page_id()
    print(f'page id is {hub_page_id}')
    QUERY_PAYLOAD =  {
      "filter": {
        "property": "Name",
        "title": {
            "is_not_empty": True
        }
      }
    }
    result = self.session.post(f"https://api.notion.com/v1/databases/{hub_page_id}/query", json=QUERY_PAYLOAD)
    return result.json()["results"]

  def _get_hub_page_id(self) -> str:
    PAGE_SEARCH_PAYLOAD = {
    "query": "HomeSearch",
    "filter": {
        "value": "database",
        "property": "object"
    },
    "sort":{
      "direction":"ascending",
      "timestamp":"last_edited_time"
    }
  }
    response = self.session.post("https://api.notion.com/v1/search", json=PAGE_SEARCH_PAYLOAD)
    return response.json()['results'][0]['id']
