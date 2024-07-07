from dotenv import load_dotenv
from integration.notion import NotionIntegration
from integration.user_search import UserSearch

# TODO: Read from notion, create UserSearch objects



def gather_user_searches(ni: NotionIntegration):
  hub_page_entries = ni.query_db()
  user_searches = []
  for result in hub_page_entries:
    try:
      user_search = UserSearch(
        target_page_id=ni.get_listings_page_id(result),
        search_name=ni.get_search_name(result),
        search_urls=ni.get_search_urls(result)
      )
      print(f'User search is {user_search}')
      user_searches.append(user_search)
    except KeyError:
      continue
  return user_searches

def main():
  load_dotenv()

  ni = NotionIntegration()

  user_searches: list[UserSearch]  = gather_user_searches(ni)
  user_searches[0].update_results(ni)
  #ni.update_db_results(user_searches[0].search_name, user_searches[0].db_id, [])
  # print(f"User searches {user_searches}")
  for user_search in user_searches:
    user_search.scrape_urls()
    user_search.update_results(ni)


main()
# TODO: Threading for different user searches
