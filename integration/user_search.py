from urllib.parse import urlparse
from bs4 import BeautifulSoup
from models.domu import DomuScrape
from models import Scrape
from integration.notion import NotionIntegration
from playwright.sync_api import sync_playwright

def generate_scrape_identifier():
  acc = dict()
  # TODO: base url-parsed key to associated class type. keeps single source of truth

# to avoid circular import
def create_user_search(database_id: str, search_name: str, search_urls: list[str]):
  return UserSearch(database_id, search_urls, search_name)


class UserSearch():

  enabled_scrapes: list[Scrape] = [DomuScrape]
  user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62'

  def __init__(self, target_page_id, search_urls, search_name):
    self.target_page_id: str = target_page_id
    self.search_urls: list[str] = search_urls
    self.search_name: str = search_name

    self.listings = []

  # Accumulate urls into a list of listings
  def scrape_urls(self):
    all_listings = []
    with sync_playwright() as p:
      browser = p.chromium.launch(headless=True)
      context = browser.new_context(user_agent=self.user_agent)
      page = context.new_page()

      for search_url in self.search_urls:
        # TODO: Abstract
        domu_base_parse = urlparse(DomuScrape.base_url)
        search_parse = urlparse(search_url)

        if not (domu_base_parse.netloc == search_parse.netloc):
          continue

        page.goto(search_url)
        content = page.content()
        soup = BeautifulSoup(content, "html.parser")
        scrape = DomuScrape(soup)
        # TODO: Make sure that there aren't duplicates between URLS/"searches"
        all_listings.extend(scrape.parse_listings())

      browser.close()
    self.listings.extend(all_listings)

  # TODO: This model does not make sense. I want the notion stuff abstracted, and this doesn't cut it because non-notion method is expecting to take it in
  def update_results(self, notion_integration: 'NotionIntegration'):
    dest_db_id = notion_integration.get_listings_db_id(self.target_page_id)
    if dest_db_id == '':
      print(f'Failed to update listings for search {self.search_name}: target sub page does not have listings DB')
      return
    print(f"ddid is {dest_db_id}")

    notion_integration.post_listings(dest_db_id, self.listings)




# gather all the items in each search run here