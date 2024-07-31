from browser.url import URL, Net, RequestHeaders


def load(url_str):
    view_source = False
    if url_str.startswith("view-source:"):
        url_str = url_str.split(":", 1)[1]
        view_source = True

    url = URL.parse(url_str)
    headers = RequestHeaders(headers={})
    headers.add("User-Agent", "browser-engineering")

    net = Net(url)
    body = net.request(headers=headers)
    show(body, view_source)


def show(body, view_source=False):
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
    print(output)
