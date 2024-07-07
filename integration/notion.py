import requests
import os
import time
from models import Listing

# goal is to abstract away notion schema/api semantics
class NotionIntegration:

  def __init__(self):
    self.token = os.environ['NOTION_TOKEN']

    self.session = requests.Session()
    self.session.headers.update({
      "Authorization": "Bearer " + self.token,
      "Content-Type": "application/json",
      "Notion-Version": "2022-06-28",
    })

  def get_search_name(self, search_request_details) -> str:
    return search_request_details["properties"]["Name"]["title"][0]["plain_text"]

  def get_listings_page_id(self, search_request_details) -> str:
    return search_request_details['id']

  def get_search_urls(self, search_request_details) -> list[str]:
    urls = []
    rich_text_list = search_request_details["properties"]["Searches"]["rich_text"]
    for rich_text_entry in rich_text_list:
      try:
        url = rich_text_entry["href"]
        if url:
          print(f'url is {url}')
          urls.append(url)
      except AttributeError:
        continue
    return urls

  def query_db(self, db_id=None):
    if not db_id:
      db_id = self._get_hub_page_id()
    print(f'page id is {db_id}')
    QUERY_PAYLOAD =  {
      "filter": {
        "property": "Name",
        "title": {
            "is_not_empty": True
        }
      }
    }
    result = self.session.post(f"https://api.notion.com/v1/databases/{db_id}/query", json=QUERY_PAYLOAD)
    print(f'got db {result.json()["results"]}')
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

  def get_listings_db_id(self, target_db_id):
    result = self.session.get(f'https://api.notion.com/v1/blocks/{target_db_id}/children').json()

    dest_db_id = ''
    try:
      # find first match
      for result in result["results"]:
        if result["type"] == "child_database" and result["child_database"]["title"] == "Listings":
          dest_db_id = result["id"]
    except KeyError:
      return dest_db_id
    return dest_db_id

  # TODO: Return a list of all the addresses present in the target DB already
  def get_current_target_addresses(self, target_db_id):
    self.query_db(target_db_id)

  def post_listings(self, target_db_id: str, listings: Listing):
    # sleep to avoid rate limit
    for listing in listings:
      print(f"Creating listing {listing}")
      res = self.session.post("https://api.notion.com/v1/pages", json=listing.notion_model(target_db_id))
      print(f"listing creation code {res.status_code}: {res.text}")
      if res.status_code == 400:
        print("Backing off failed upload")
        return
      time.sleep(1)
