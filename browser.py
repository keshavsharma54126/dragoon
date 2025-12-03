import socket
import sys
import ssl
import os
from typing import Optional


class URL:
    def __init__(self, url: Optional[str]):
        if url and url.startswith("file://"):
            self.scheme, self.path = url.split("://", 1)

        elif url is None:
            self.scheme = "file"
            self.path = "/home/keshav/dragoon/temp.txt"

        else:
            self.scheme, url = url.split("://", 1)
            assert self.scheme in ["http", "https"]
            if self.scheme == "http":
                self.port = 80
            if self.scheme == "https":
                self.port = 443
            if "/" not in url:
                url += "/"
            self.host, url = url.split("/", 1)
            if ":" in self.host:
                self.host, port = self.host.split(":", 1)
                self.port = int(port)
            self.path = "/"+url

    def add_header(self, request, headers: dict[str, str]):
        for key in headers:
            header_key = key
            header_value = headers.get(key, "")
            request += f"{key}: {header_value}\r\n"

        request += "\r\n"
        return request

    def request(self):
        if self.scheme == "file":
            self.show()
            return
        if self.scheme in ["http", "https"]:
            ctx = ssl.create_default_context()

            s = socket.socket(
                family=socket.AF_INET,
                type=socket.SOCK_STREAM,
                proto=socket.IPPROTO_TCP
            )

            if self.scheme == "https":
                s = ctx.wrap_socket(s, server_hostname=self.host)

            s.connect((self.host, self.port))

            request = "GET {} HTTP/1.1\r\n".format(self.path)

            headers = {
                "Host": self.host,
                "Connection": "close"
            }
            request = self.add_header(request=request, headers=headers)

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

            self.content = response.read()
            s.close()
            self.show()
            return
        else:
            return

    def show(self):
        if self.scheme == "file" and self.path:
            filepath = os.path.abspath(self.path)
            with open(file=filepath) as f:
                data = f.read()
            print(data)

        else:
            in_tag = False
            for char in body:
                if char == "<":
                    in_tag = True
                elif char == ">":
                    in_tag = False
                elif not in_tag:
                    print(char, end="")


def load(url):
    url.request()


if __name__ == "__main__":
    import sys
    url = None
    if len(sys.argv) > 1:
        url = sys.argv[1]

    load(URL(url=url))
