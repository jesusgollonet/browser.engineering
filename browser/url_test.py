from browser.url import URL, URL_new


def test_host_slash_removal():
    url = URL("http://example.com/")
    assert url.host == "example.com"


# from Writing Knownledge-Building Tests in Python (Python Testing with Pytest)
def test_http_url():
    url = URL("http://example.com")
    assert url.scheme == "http"
    assert url.host == "example.com"
    assert url.port == 80
    assert url.path == "/"


def test_https_url():
    url = URL("https://example.com")
    assert url.scheme == "https"
    assert url.host == "example.com"
    assert url.port == 443
    assert url.path == "/"


def test_custom_port_url():
    url = URL("http://example.com:8080")
    assert url.scheme == "http"
    assert url.host == "example.com"
    assert url.port == 8080
    assert url.path == "/"


def test_file_url():
    url = URL("file:///Users/jgb/Learn/recurse.com/browser.engineering/dummy.txt")
    assert url.scheme == "file"
    assert url.host == ""
    assert url.path == "/Users/jgb/Learn/recurse.com/browser.engineering/dummy.txt"


def test_new_http_url():
    url = URL_new.parse("http://example.com")
    assert url.scheme == "http"
    assert url.host == "example.com"
    assert url.port == 80


def test_new_https_url():
    url = URL_new.parse("https://example.com")
    assert url.scheme == "https"
    assert url.host == "example.com"
    assert url.port == 443


def test_new_custom_port_url():
    url = URL_new.parse("http://example.com:8080")
    assert url.scheme == "http"
    assert url.host == "example.com"
    assert url.port == 8080
    assert url.path == "/"


def test_new_file_url():
    url = URL_new.parse(
        "file:///Users/jgb/Learn/recurse.com/browser.engineering/dummy.txt"
    )
    assert url.scheme == "file"
    assert url.host == ""
    assert url.path == "/Users/jgb/Learn/recurse.com/browser.engineering/dummy.txt"


def test_new_data_url():
    url = URL_new.parse("data:text/plain,hello%2C%20world")
    assert url.scheme == "data"
    assert url.host is None
    assert url.port is None
    assert url.path == "text/plain,hello%2C%20world"
