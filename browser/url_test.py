from browser.url import URL


def test_host_slash_removal():
    url = URL.parse("http://example.com/")
    assert url.host == "example.com"


# from Writing Knownledge-Building Tests in Python (Python Testing with Pytest)


def test_http_url():
    url = URL.parse("http://example.com")
    assert url.scheme == "http"
    assert url.host == "example.com"
    assert url.port == 80


def test_https_url():
    url = URL.parse("https://example.com")
    assert url.scheme == "https"
    assert url.host == "example.com"
    assert url.port == 443


def test_custom_port_url():
    url = URL.parse("http://example.com:8080")
    assert url.scheme == "http"
    assert url.host == "example.com"
    assert url.port == 8080
    assert url.path == "/"


def test_file_url():
    url = URL.parse("file:///Users/jgb/Learn/recurse.com/browser.engineering/dummy.txt")
    assert url.scheme == "file"
    assert url.host == ""
    assert url.path == "/Users/jgb/Learn/recurse.com/browser.engineering/dummy.txt"


def test_data_url():
    url = URL.parse("data:text/plain,hello%2C%20world")
    assert url.scheme == "data"
    assert url.host is None
    assert url.port is None
    assert url.path == "text/plain,hello%2C%20world"
