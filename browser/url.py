import socket
import ssl
from dataclasses import dataclass


@dataclass
class URL:
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
            return URL(scheme, host, port, path)

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

        return URL(scheme, host, port, path)


@dataclass
class RequestHeaders:
    headers: dict[str, str]

    def add(self, header: str, value: str):
        self.headers[header] = value

    def remove(self, header: str):
        del self.headers[header]

    def get(self, header: str):
        return self.headers[header]

    def __iter__(self):
        return iter(self.headers)

    def __len__(self):
        return len(self.headers)

    def __getitem__(self, header: str):
        return self.headers[header]

    def __setitem__(self, header: str, value: str):
        self.headers[header] = value

    def __delitem__(self, header: str):
        del self.headers[header]

    def __contains__(self, header: str):
        return header in self.headers

    def items(self):
        return self.headers.items()

    def __repr__(self):
        return f"RequestHeaders({self.headers})"


@dataclass
class Request:
    method: str
    uri: str
    version: str
    headers: RequestHeaders

    def to_string(self):
        request_str = f"{self.method} {self.uri.path} { self.version }\r\n"

        for header, value in self.headers.items():
            request_str += f"{header}: {value}\r\n"

        request_str += "\r\n"
        return request_str


class Net:
    def __init__(self, url):
        self.url = url
        self.s = None

    def request(self, headers: RequestHeaders | None):
        if self.url.scheme == "data":
            return self.__data_request()
        elif self.url.scheme == "file":
            return self.__file_request()
        else:
            return self.__http_request(headers)

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

    def __http_request(self, headers):
        if not self.s:
            self.s = socket.socket(
                family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP
            )
        self.s.connect((self.url.host, self.url.port))
        if self.url.scheme == "https":
            ctx = ssl.create_default_context()
            self.s = ctx.wrap_socket(self.s, server_hostname=self.url.host)

        headers.add("Host", self.url.host)
        request = Request("GET", self.url, "HTTP/1.1", headers)

        self.s.send(request.to_string().encode("utf8"))
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
