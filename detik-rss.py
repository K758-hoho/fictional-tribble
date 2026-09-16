from bs4 import BeautifulSoup
from feedgen import feed
from feedgen.feed import FeedGenerator
import requests
import sys

# Define URL
base_url = "https://news.detik.com/indeks"

# Setting up FeedGenerator
fg = FeedGenerator()
fg.title("Berita - DetikNews")
fg.id(base_url)
fg.link(href=base_url, rel="alternate")
fg.language("id")
fg.description("Berita hari ini di Indonesia dan Internasional")
fg.author({"name": "Detikcom", "email": "info@detik.com"})
fg.logo(
    "https://akcdn.detik.net.id/community/media/visual/2020/09/17/logo-detiknews.png"
)

# Run process if URL is reachable
response = requests.get(base_url)
if response.status_code == 200:

    # Get the content of the news
    html = response.content
    detik = BeautifulSoup(html, "lxml")

    # Extract the article links
    articles = detik.select("a.media__link")

    for a in articles:
        article_link = a["href"]
        article_title = a.get_text(strip=True)

        if not article_title:
            continue

        fe = fg.add_entry()
        fe.id(article_link)
        fe.title(article_title)
        fe.description(article_title)
        fe.link(href=article_link)

    # Generate the RSS Feed
    fg.rss_file("rss/detik.xml", pretty=True)

else:
    print(f"Sorry, can't connect to {base_url}")
    sys.exit(1)
