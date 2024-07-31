"""
1-1 HTTP/1.1. Along with Host, send the Connection header in the request function 
with the value close. Your browser can now declare that it is using HTTP/1.1. 
Also add a User-Agent header. Its value can be whatever you want—it identifies 
your browser to the host. Make it easy to add further headers in the future.
"""

from browser.url import URL, RequestHeaders, Request


def test_ch1_ex11():
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
    return None
