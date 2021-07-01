import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world\n")

    def post(self):
        self.set_header("Content-Type", "text/plain")
        self.write("You wrote " + self.get_body_argument("message"))


class SubHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, Sub request\n")


class StoryHandler(tornado.web.RequestHandler):
    def initialize(self, story, author):
        self.story = story
        self.author = author

    def get(self, story_id):
        self.write("this is story {} {} by {}".format(story_id, self.story, self.author))


class BookHandler(tornado.web.RequestHandler):
    def initialize(self, books):
        self.books = books
        # print('books:{} type {}'.format(books, type(books)))

    def get(self, book_id):
        id = int(book_id)
        if id > len(self.books) - 1:
            return self.write("max index is {}".format(len(self.books) - 1))

        # print('book_id:{} is {}'.format(id, self.books[id]))
        self.write("this is book {}, write by {}".format(self.books[id]['name'], self.books[id]['author']))


def make_app():
    """
	curl 127.0.0.1:8888
	curl 127.0.0.1:8888/sub
	curl 127.0.0.1:8888 -d message=1111
	curl 127.0.0.1:8888/story/12
	"""

    books = [
        {
            'name': "活着",
            'author': "余华"
        },
        {
            'name': "第七天",
            'author': "余华"
        },
        {
            'name': "许三观卖血记",
            'author': "余华"
        },
        {
            'name': "在微风细雨中呐喊",
            'author': "余华"
        },
        {
            'name': "兄弟",
            'author': "余华"
        }
    ]
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/sub", SubHandler),
        (r"/story/([0-9]+)", StoryHandler, {'story': '农夫和蛇', 'author': '柳宗元'}),
        (r'/book/([0-9]+)', BookHandler, dict(books=books))  # url的第三个字典类型参数会在调用的时候传给initialize
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
