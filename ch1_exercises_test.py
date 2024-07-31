from browser.url import URL, RequestHeaders, Request, Net

"""
1-1 HTTP/1.1. Along with Host, send the Connection header in the request
function with the value close. Your browser can now declare that it is using
HTTP/1.1.  Also add a User-Agent header. Its value can be whatever you want—it
identifies your browser to the host. Make it easy to add further headers in the
future.
"""


def test_ch1_ex11_http11():
    url = URL.parse("http://example.com")
    headers = RequestHeaders(
        headers={
            "Host": url.host,
            "Connection": "close",
            "User-Agent": "browser-engineering",
        }
    )
    request = Request(method="GET", uri=url, version="HTTP/1.1", headers=headers)
    request_str = request.to_string()
    assert "Connection: close" in request_str
    assert "User-Agent: browser-engineering" in request_str
    assert "HTTP/1.1" in request_str

    # test that the headers can be easily added
    headers.add("Accept", "text/html")
    request_str = request.to_string()
    assert "Accept: text/html" in request_str


""" 
1-2 File URLs. Add support for the file scheme, which allows the browser to
open local files. For example, file:///path/goes/here should refer to the file
on your computer at location /path/goes/here. Also make it so that, if your
browser is started without a URL being given, some specific file on your
computer is opened. You can use that file for quick testing 
"""


def test_ch1_ex12_file_urls():
    url = URL.parse("file:///path/goes/here")
    # url parsing
    assert url.scheme == "file"
    assert url.path == "/path/goes/here"
    # file request
    url = URL.parse(
        "file:///Users/jgb/Learn/recurse.com/browser.engineering/mock/dummy.txt"
    )
    net = Net(url)
    response = net.request(None)

    assert "Raw content" in response


""" 
1-3 data. Yet another scheme is data, which allows inlining HTML content
into the URL itself. Try navigating to data:text/html,Hello world! in a real
browser to see what happens. Add support for this scheme to your browser. The
data scheme is especially convenient for making tests without having to put
them in separate files.  
"""


def test_ch1_ex13_data_urls():
    url = URL.parse("data:text/html,Hello world!")
    net = Net(url)
    response = net.request(None)
    assert "Hello world!" in response
