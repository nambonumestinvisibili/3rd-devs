import requests

article_url = "https://c3ntrala.ag3nts.org/dane/arxiv-draft.html"
try:
    response = requests.get(article_url)
    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
    html_content = response.text
    print("HTML content downloaded successfully!")

    with open("1-article.html", "w", encoding="utf-8") as file:
        file.write(html_content)
    # You would then save this to a file or pass it to a parser
except requests.exceptions.RequestException as e:
    print(f"Error downloading HTML: {e}")
    html_content = None