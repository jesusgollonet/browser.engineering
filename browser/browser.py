def load(url):
    body = url.request()
    show(body)


def show(body):
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
