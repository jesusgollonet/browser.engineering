from browser.browser import load

if __name__ == "__main__":
    import sys

    url = sys.argv[1] if len(sys.argv) > 1 else None
    if url:
        load(url)
    else:
        print("Usage: python main.py <url>")
