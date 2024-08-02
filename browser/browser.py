from browser.url import URL, Net, RequestHeaders


def load(url_str):
    url_str, view_source = strip_view_source(url_str)

    url = URL.parse(url_str)
    headers = RequestHeaders(headers={})
    headers.add("User-Agent", "browser-engineering")

    net = Net(url)
    response = net.request(headers=headers)
    body = parse(response.body, view_source)
    print(body, response.headers)


def strip_view_source(url_str):
    if url_str.startswith("view-source:"):
        return url_str.split(":", 1)[1], True
    return url_str, False


def parse(body, view_source=False):
    if view_source:
        body = body.replace("<", "&lt;").replace(">", "&gt;")
    in_tag = False
    output = ""
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            output += c

    output = output.replace("&lt;", "<").replace("&gt;", ">")
    return output
