import socket
import sys
import ssl


class URL:
    def __init__(self, url):
        self.scheme, url = url.split("://", 1)
        print(self.scheme)
        print(url)
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
        print(self.host)
        print(self.path)

    def request(self):
        ctx = ssl.create_default_context()

        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP
        )

        if self.scheme == "https":
            s = ctx.wrap_socket(s, server_hostname=self.host)

        s.connect((self.host, self.port))

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


def load(url):
    body = url.request()
    url.show(body)


if __name__ == "__main__":
    import sys
    load(URL(sys.argv[1]))
