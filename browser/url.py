import socket
import ssl
from dataclasses import dataclass


@dataclass
class URL_new:
    scheme: str
    host: str | None
    port: int | None
    path: str

    @staticmethod
    def parse(url_str):
        # special case for data
        if url_str.startswith("data:"):
            scheme = "data"
            path = url_str.split(":", 1)[1]
            host = None
            port = None
            return URL_new(scheme, host, port, path)

        scheme, rest = url_str.split("://", 1)

        if "/" not in rest:
            rest += "/"

        print(rest)
        host, rest = rest.split("/", 1)
        if ":" in host:
            host, port = host.split(":", 1)
            port = int(port)
        elif scheme == "https":
            port = 443
        else:
            port = 80

        path = "/" + rest

        return URL_new(scheme, host, port, path)


class URL:
    def __init__(self, url):
        self.s = None
        self.port = None

        if url.startswith("data:"):
            self.scheme = "data"
            self.path = url.split(":", 1)[1]
            return

        self.scheme, url = url.split("://", 1)

        if "/" not in url:
            url += "/"

        self.host, url = url.split("/", 1)
        if ":" in self.host:
            self.host, port = self.host.split(":", 1)
            self.port = int(port)

        self.path = "/" + url

        assert self.scheme in ["http", "https", "file"]
        if not self.port:
            if self.scheme == "https":
                self.port = 443
            else:
                self.port = 80


class Net:
    def __init__(self, url):
        self.url = url
        self.s = None

    def request(self):
        if self.url.scheme == "data":
            return self.__data_request()
        elif self.url.scheme == "file":
            return self.__file_request()
        else:
            return self.__http_request()

    def __data_request(self):
        path_parts = self.url.path.split(";", -1)
        body = path_parts[-1]
        # TODO handle media type
        if len(path_parts) > 1:
            media_type = path_parts[:-1]

        return body

    def __file_request(self):
        with open(self.url.path, encoding="utf-8") as f:
            read_data = f.read()
        return read_data

    def __http_request(self):
        if not self.s:
            self.s = socket.socket(
                family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP
            )
        self.s.connect((self.url.host, self.url.port))
        if self.url.scheme == "https":
            ctx = ssl.create_default_context()
            self.s = ctx.wrap_socket(self.s, server_hostname=self.url.host)

        headers = {
            "Host": self.url.host,
            # "Connection": "close",
            "User-Agent": "jgb",
        }

        request = f"GET {self.url.path} HTTP/1.1\r\n"

        for header, value in headers.items():
            request += f"{header}: {value}\r\n"

        request += "\r\n"
        self.s.send(request.encode("utf8"))
        response = self.s.makefile("r", encoding="utf8", newline="\r\n")
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
        body = response.read(int(response_headers["content-length"]))
        # s.close()
        # TODO this is icky. we should probably extract parts of http_request into a separate function and treat the body outside
        return body
