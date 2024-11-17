#pip install flask beautifulsoup4 requests
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    news = None
    if request.method == "POST":
        topic = request.form.get("topic")
        if topic:
            news = fetch_news(topic)
    return render_template("index.html", news=news)

def fetch_news(topic):
    """Fetches news headlines related to the topic using web scraping."""
    try:
        url = f"https://www.google.com/search?q={topic}+news&tbm=nws"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract news headlines and links
        articles = []
        for item in soup.select(".dbsr"):
            headline = item.select_one(".nDgy9d").text
            link = item.a["href"]
            articles.append({"headline": headline, "link": link})

        return articles if articles else [{"headline": "No news found", "link": "#"}]

    except Exception as e:
        return [{"headline": "Error fetching news", "link": "#"}]

if __name__ == "__main__":
    app.run(debug=True)
