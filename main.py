from dotenv import load_dotenv
from integration.notion import NotionIntegration
from integration.user_search import UserSearch

# TODO: Read from notion, create UserSearch objects


def gather_user_searches():
  ni = NotionIntegration()
  user_searches = ni.process_hub_page_entries()
  return user_searches

def main():
  load_dotenv()

  user_searches: list[UserSearch]  = gather_user_searches()
  print(f"User searches {user_searches}")
  for user_search in user_searches:
    result = user_search.scrape_urls()
    print(f'{user_search.search_name} result is {result}')

main()
# TODO: Threading for different user searches
