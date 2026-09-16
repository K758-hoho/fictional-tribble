from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import requests
import sys

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36"
}

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
response = requests.get(base_url, headers=headers)
if response.status_code == 200:

    # Get the content of the news
    html = response.content
    detik = BeautifulSoup(html, "lxml")

    # Extract the article links
    articles = detik.select("a.media__link")

    # Add every new RSS feed entry
    for a in articles:
        article_link = a["href"]
        article_title = a.get_text(strip=True)
        if not article_title:
            continue
        img = a.find_parent().select_one(".media__image")

        fe = fg.add_entry()
        fe.id(article_link)
        fe.title(article_title)
        fe.description(article_title)
        fe.link(href=article_link)

        if img:
            fe.content(f'<p>{article_title}</p><img src="{img["src"]}"/>', type="CDATA")

    # Generate the RSS Feed
    fg.rss_file("rss/detik.xml", pretty=True)

else:
    print(f"Sorry, can't connect to {base_url}")
    sys.exit(1)
