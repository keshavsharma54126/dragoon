from url import URL
import tkinter
WIDTH = 800
HEIGHT = 600
HSTEP, VSTEP = 13, 18


class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT
        )
        self.canvas.pack()

    def load(self, url):
        url.request()
        self.canvas.create_rectangle(10, 20, 400, 300)
        self.canvas.create_oval(100, 100, 150, 150)
        self.canvas.create_text(200, 150, text="Hi!")
        text = url.show()
        cursor_x, cursor_y = HSTEP, VSTEP
        for c in text:
            self.canvas.create_text(cursor_x, cursor_y, text=c)
            cursor_x += HSTEP


if __name__ == "__main__":
    import sys
    url = None
    if len(sys.argv) > 1:
        url = sys.argv[1]
    browser = Browser()
    browser.load(URL(url=url))
    tkinter.mainloop()
