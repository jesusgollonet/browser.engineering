class URL:
    def __init__(self, url):
        self.scheme, url = url.split("://", 1)
        print(self.scheme, url)
        if "/" not in url:
            url += "/"
        self.host, url = url.split("/", 1)
        self.path = "/" + url
        print(self.host, url)
        assert self.scheme == "http"


URL("http://www.google.com")
URL("http://www.google.com/index.html")
