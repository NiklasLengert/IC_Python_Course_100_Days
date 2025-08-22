# from bs4 import BeautifulSoup
# from pathlib import Path
# import lxml

# directory = Path(__file__).parent

# with open(directory / "website.html") as file:
#     contents = file.read()

# soup = BeautifulSoup(contents, "html.parser")
# print(soup.title)
# print(soup.title.name)
# print(soup.title.string)

# print(soup.prettify())
# all_anchor_tags = soup.find_all(name="a")

# for tag in all_anchor_tags:
#     print(tag.getText())
#     print(tag.get("href"))

# heading = soup.find(name="h1", id="name")
# print(heading.getText())

# section = soup.find(name="h3", class_="heading")
# print(section.getText())

# company_url = soup.select_one(selector="p a")
# print(company_url.get("href"))

from bs4 import BeautifulSoup
import requests

response = requests.get("https://ycombinator.com")
yc_web_page = response.text

soup = BeautifulSoup(yc_web_page, "html.parser")
article_tag = soup.find(name="a", class_="storylink")
print(article_tag.getText())

article_link = article_tag.get("href")
print(article_link)

article_upvote = soup.find(name="span", class_="score")
print(article_upvote.getText())

articles = soup.find_all(name="a", class_="storylink")
article_texts = []
article_links = []
for article in articles:
    article_texts.append(article.getText())
    article_links.append(article.get("href"))

article_upvotes = [int(score.getText().split()[0]) for score in soup.find_all(name="span", class_="score")]
