from browser.url import URL, RequestHeaders, Request, Net, Response
from browser.browser import load, parse, strip_view_source


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
    response, _ = net.request(None)

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
    response, _ = net.request(None)
    assert "Hello world!" in response


""" 
1-4 Entities. Implement support for the less-than (&lt;) and greater-than
(&gt;) entities. These should be printed as < and >, respectively. For example,
if the HTML response was &lt;div&gt;, the show method of your browser should
print <div>. Entities allow web pages to include these special characters
without the browser interpreting them as tags.  
"""


def test_ch1_ex14_entities():
    raw_body = "&lt;div&gt;"
    body = parse(raw_body)
    assert "<div>" in body


"""
1-5 view-source. Add support for the view-source scheme; navigating to
view-source:http://example.org/ should show the HTML source instead of the
rendered page. Add support for this scheme. Your browser should print the
entire HTML file as if it was text. You’ll want to have also implemented
Exercise 1-4.1-5 view-source. Add support for the view-source scheme;
navigating to view-source:http://example.org/ should show the HTML source
instead of the rendered page. Add support for this scheme. Your browser should
print the entire HTML file as if it was text. You’ll want to have also
implemented Exercise 1-4.
"""


def test_ch1_ex15_view_source():
    # view-source should be ignored by the URL parser
    url = URL.parse("view-source:http://example.org")
    assert url.scheme == "http"
    assert url.host == "example.org"
    assert url.path == "/"

    # browser should print the entire HTML file as text
    parsed_body = parse(
        "<html><body><h1>Hello world!</h1></body></html>", view_source=True
    )
    assert "<html><body><h1>Hello world!</h1></body></html>" in parsed_body

    url_str, view_source = strip_view_source("view-source:http://example.org")
    assert url_str == "http://example.org"
    assert view_source

    url_str, view_source = strip_view_source("http://example.org")
    assert url_str == "http://example.org"
    assert view_source is False


""" 
1-6 Keep-alive. Implement Exercise 1-1; however, do not send the
Connection: close header. Instead, when reading the body from the socket, only
read as many bytes as given in the Content-Length header and don’t close the
socket afterward. Instead, save the socket, and if another request is made to
the same socket reuse the same socket instead of creating a new one. This will
speed up repeated requests to the same server, which is common.  
"""


def test_ch1_ex16_keep_alive():
    url = URL.parse("http://example.org")
    headers = RequestHeaders(
        headers={
            "Host": url.host,
            "User-Agent": "browser-engineering",
        }
    )
    request = Request(method="GET", uri=url, version="HTTP/1.1", headers=headers)
    request_str = request.to_string()
    assert "Connection: close" not in request_str
    response = Net(url).request(headers)
    assert "content-length" in response.headers
    # Convert the body to bytes if it's not already
    # Extract charset from content-type header, defaulting to utf-8
    content_type = response.headers.get("content-type")
    charset = "utf-8"  # default
    if "charset=" in content_type:
        charset = content_type.split("charset=")[-1].split(";")[0].strip()

    # Convert the body to bytes using the detected charset
    if isinstance(response.body, str):
        body = response.body.encode(charset)

    assert len(body) == int(response.headers["content-length"])


""" 1-7 Redirects. Error codes in the 300 range request a redirect. When your
browser encounters one, it should make a new request to the URL given in the
Location header. Sometimes the Location header is a full URL, but sometimes it
skips the host and scheme and just starts with a / (meaning the same host and
scheme as the original request). The new URL might itself be a redirect, so
make sure to handle that case. You don’t, however, want to get stuck in a
redirect loop, so make sure to limit how many redirects your browser can follow
in a row. You can test this with the URL http://browser.engineering/redirect,
which redirects back to this page, and its /redirect2 and /redirect3 cousins
which do more complicated redirect chains.
"""


def test_ex17_redirects():
    url = URL.parse("http://browser.engineering/http.html")
    net = Net(url)

    headers = RequestHeaders(headers={})
    headers.add("User-Agent", "browser-engineering")
    response = net.request(headers)

    print(response.status)
    assert response.status == "200"
    return None


""""
1-8 Caching. Typically, the same images, styles, and scripts are used on
multiple pages; downloading them repeatedly is a waste. It’s generally valid to
cache any HTTP response, as long as it was requested with GET and received a
200 response.Some other status codes like 301 and 404 can also be cached.
Implement a cache in your browser and test it by requesting the same file
multiple times. Servers control caches using the Cache-Control header. Add
support for this header, specifically for the no-store and max-age values. If
the Cache-Control header contains any value other than these two, it’s best not
to cache the response.
"""


def test_ex18_caching():
    return None


"""
1-9 Compression. Add support for HTTP compression, in which the browser informs
the server that compressed data is acceptable. Your browser must send the
Accept-Encoding header with the value gzip. If the server supports compression,
its response will have a Content-Encoding header with value gzip. The body is
then compressed. Add support for this case. To decompress the data, you can use
the decompress method in the gzip module. GZip data is not utf8-encoded, so
pass "rb" to makefile to work with raw bytes instead. Most web servers send
compressed data in a Transfer-Encoding called chunked. You’ll need to add
support for that, too.
"""


def test_ex19_compression():
    return None
