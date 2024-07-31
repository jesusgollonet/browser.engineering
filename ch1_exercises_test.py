"""
1-1 HTTP/1.1. Along with Host, send the Connection header in the request function 
with the value close. Your browser can now declare that it is using HTTP/1.1. 
Also add a User-Agent header. Its value can be whatever you want—it identifies 
your browser to the host. Make it easy to add further headers in the future.
"""

from browser.url import URL, Net, RequestHeaders


def test_ch1_ex11_():
    url = URL.parse("http://example.com")
    # net = Net(url)
    # headers = RequestHeaders(headers={})
    # headers.add("User-Agent", "browser-engineering")
    # body = net.request(headers=headers)
    # test that the request function sends the Connection header
    # test that http 1.1 is set
    # test that the Connection header is set to close
    # test that the User-Agent header is set
    # test that the headers can be easily added
    return None
