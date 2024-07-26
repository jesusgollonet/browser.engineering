from browser.browser import load
from browser.url import URL

if __name__ == "__main__":
    import sys

    url = sys.argv[1] if len(sys.argv) > 1 else None
    if url:
        load(URL(url))
    else:
        print("Usage: python main.py <url>")
