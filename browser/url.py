import socket
import ssl

# a URL takes a string and returns something that can be used to make a request
# the request method is not defined here, but in the URL class
# the URL class is responsible for making the request
# the URL class is responsible for handling the response


class URL:
    def __init__(self, url):
        self.s = None
        self.pre_scheme = None
        self.port = None

        if url.startswith("data:"):
            self.pre_scheme = "data"
            self.path = url.split(":", 1)[1]
            return
        elif url.startswith("view-source:"):
            self.pre_scheme = "view-source"
            url = url.split(":", 1)[1]

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

    def request(self):
        if self.pre_scheme == "view-source":
            return self.__http_request()
        elif self.pre_scheme == "data":
            return self.__data_request()
        else:
            if self.scheme == "file":
                return self.__file_request()
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
        if not self.s:
            self.s = socket.socket(
                family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP
            )
        self.s.connect((self.host, self.port))
        if self.scheme == "https":
            ctx = ssl.create_default_context()
            self.s = ctx.wrap_socket(self.s, server_hostname=self.host)

        headers = {
            "Host": self.host,
            # "Connection": "close",
            "User-Agent": "jgb",
        }

        request = f"GET {self.path} HTTP/1.1\r\n"

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
        print(response_headers["content-length"])
        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers
        body = response.read(int(response_headers["content-length"]))
        # s.close()
        # TODO this is icky. we should probably extract parts of http_request into a separate function and treat teh body outside
        if self.pre_scheme == "view-source":
            return body.replace("<", "&lt;").replace(">", "&gt;")
        return body
