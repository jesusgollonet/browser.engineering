import socket


s = socket.create_connection(("browser.engineering", 80))

request = (
    "GET /http.html HTTP/1.1\r\n"
    "User-Agent: browser-engineering\r\n"
    "Host: browser.engineering\r\n"
    "Connection: keep-alive\r\n"
    "\r\n"
)

s.send(request.encode("utf-8"))

response = s.makefile("rb", newline="\r\n")

status_line = response.readline().decode("utf-8")
print(status_line)

version, status, explanation = tuple(
    map(lambda s: s.strip(), status_line.split(" ", 2))
)
print(version, status, explanation, len(explanation))
assert version == "HTTP/1.1"


line = response.readline().decode("utf-8")
headers = {}
while line != "\r\n":
    line = response.readline().decode("utf-8")
    if line == "\r\n":
        print("end of headers!")
        break
    h, v = line.strip().split(":", 1)
    headers.update({h.lower(): v.strip()})

print(int(headers.get("content-length", 0)))
body = response.read(int(headers.get("content-length", 0))).decode("utf-8")
print(body)
response.close()
