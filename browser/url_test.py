from browser.url import URL


def test_host():
    url = URL("http://example.com/")
    assert url.host == "example.com"


def test_host_no_slash():
    url = URL("http://example.com")
    assert url.host == "example.com"


def test_scheme():
    url = URL("http://example.com")
    assert url.scheme == "http"
    url = URL("https://example.com")
    assert url.scheme == "https"
    url = URL("file:///Users/jgb/Learn/recurse.com/browser.engineering/dummy.txt")
    assert url.scheme == "file"


def test_port():
    url = URL("http://example.com")
    assert url.port == 80
    url = URL("https://example.com")
    assert url.port == 443


def test_custom_port():
    url = URL("http://example.com:8080")
    print(url.host)
    assert url.host == "example.com"
    assert url.port == 8080
