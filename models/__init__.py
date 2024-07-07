class Scrape:
  base_url = ''


class Listing():
  def __init__(self, address, price, url, title, details=''):
    self.address: str = address
    self.price: str = price
    self.details: str = details
    self.url: str = url
    self.title: str = title

  def __repr__(self) -> str:
    return f"A: {self.address} | T: {self.title}"


  def notion_model(self, parent_id):
    return {
      "parent": { "database_id": parent_id },
      "properties": {
        "Address": {
          "title": [
            {
              "text": {
                "content": self.address
              }
            }
          ]
        },
        "Price": {
          "rich_text": [
            {
              "text": {
                "content": self.price
              }
            },
          ]
        },
        "URL": {
          "rich_text": [
            {
              "text": {
                "content": self.url
              }
            },
          ]
        },
        "Description": {
          "rich_text": [
            {
              "text": {
                "content": self.title
              }
            },
          ]
        },
      }
    }

