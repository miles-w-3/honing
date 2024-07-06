class Scrape:
  base_url = ''


class Listing():
  def __init__(self, address, price, url, title, description='', details=''):
    self.address: str = address
    self.price: str = price
    self.details: str = details
    self.description: str = description
    self.url: str = url
    self.title: str = title

  def __repr__(self) -> str:
    return f"A: {self.address} | T: {self.title}"


