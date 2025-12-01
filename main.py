import socket
import sys


class URL:
    def __init__(self, url):
        self.scheme, url = url.split("://", 1)
        print(self.scheme)
        print(url)
        assert self.scheme == "http"
        if "/" not in url:
            url += "/"
        self.host, url = url.split("/", 1)
        self.path = "/"+url
        print(self.host)
        print(self.path)

    def request(self):
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP
        )

        s.connect((self.host, 80))

        request = "GET {} HTTP/1.0\r\n".format(self.path)
        request += "Host: {}\r\n".format(self.host)
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

        content = response.read()
        s.close()
        return content

    def show(self, body):
        in_tag = False
        for char in body:
            if char == "<":
                in_tag = True
            elif char == ">":
                in_tag = False
            elif not in_tag:
                print(char, end="")


if __name__ == "__main__":
    url = URL(url="http://example.org")
    content = url.request()
    url.show(content)
