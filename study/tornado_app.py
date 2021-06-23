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


def make_app():
	"""
	curl 127.0.0.1:8888
	curl 127.0.0.1:8888/sub
	curl 127.0.0.1:8888 -d message=1111
	"""

	return tornado.web.Application([
					(r"/", MainHandler),
					(r"/sub", SubHandler),
					])


if __name__ == "__main__":
	app = make_app()
	app.listen(8888)
	tornado.ioloop.IOLoop.current().start()
