import socket


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
        s.send(request.encode("utf8"))
        response = s.makefile("r", encoding="utf8", newline="\r\n")


if __name__ == "__main__":
    url = URL(url="http://example.org")
    url.request()
