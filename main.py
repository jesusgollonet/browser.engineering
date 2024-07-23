import socket
import ssl


class URL:
    def __init__(self, url):
        # Steps
        # detect pre scheme
        if url.startswith("data:"):
            self.scheme = "data"
            self.path = url.split(":", 1)[1]
            return

        self.scheme, url = url.split("://", 1)

        if "/" not in url:
            url += "/"

        self.host, url = url.split("/", 1)
        self.path = "/" + url

        assert self.scheme in ["http", "https", "file"]
        if self.scheme == "https":
            self.port = 443
        else:
            self.port = 80

    def request(self):
        if self.scheme == "file":
            return self.__file_request()
        elif self.scheme == "data":
            return self.__data_request()
        else:
            return self.__http_request()

    def __data_request(self):
        path_parts = self.path.split(";", -1)
        body = path_parts[-1]
        # TODO handle media type
        if len(path_parts) > 1:
            media_type = path_parts[:-1]

        return body

    def __file_request(self):
        with open(self.path, encoding="utf-8") as f:
            read_data = f.read()
        return read_data

    def __http_request(self):
        s = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP
        )
        s.connect((self.host, self.port))
        if self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)

        headers = {
            "Host": self.host,
            "Connection": "close",
            "User-Agent": "jgb",
        }

        request = f"GET {self.path} HTTP/1.1\r\n"

        for header, value in headers.items():
            request += f"{header}: {value}\r\n"

        request += "\r\n"
        s.send(request.encode("utf8"))
        response = s.makefile("r", encoding="utf8", newline="\r\n")
        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)
        response_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n":
                break
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()
        # we won't handle these
        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers
        body = response.read()
        s.close()
        return body


def load(url):
    body = url.request()
    show(body)


def show(body):
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            print(c, end="")


if __name__ == "__main__":
    import sys

    url = sys.argv[1] if len(sys.argv) > 1 else None
    if url:
        load(URL(url))
    else:
        print("Usage: python main.py <url>")
