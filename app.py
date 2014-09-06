from socket import gethostname
import os
from jinja2 import Environment, FileSystemLoader
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.routing import Rule, Map
from werkzeug.wrappers import Request, Response
from werkzeug.wsgi import SharedDataMiddleware

import mimetypes
# workaround to serve svg with correct mimetype

mimetypes.add_type("image/svg+xml", ".svg", True)
mimetypes.add_type("image/svg+xml", ".svgz", True)


class ImpressJS(object):
	def __init__(self, config):
		template_path = os.path.join(os.path.dirname(__file__), 'templates')
		self.jinja_env = Environment(loader=FileSystemLoader(template_path),
		                             autoescape=True)
		self.url_map = Map([
			Rule('/', endpoint='main'),
		])

	def wsgi_app(self, environ, start_response):
		request = Request(environ)
		response = self.dispatch_request(request)
		return response(environ, start_response)

	def dispatch_request(self, request):
		adapter = self.url_map.bind_to_environ(request.environ)
		try:
			endpoint, values = adapter.match()
			return getattr(self, "on_%s" % endpoint)(request, **values)
		except NotFound, e:
			return self.not_found(request)
		except HTTPException as e:
			return e

	def __call__(self, environ, start_response):
		return self.wsgi_app(environ, start_response)

	def render_template(self, template_name, **context):
		template = self.jinja_env.get_template(template_name)
		return Response(template.render(context), mimetype='text/html')

	def on_main(self, request):
		return self.render_template('cv.html', debug=DEBUG)

	def not_found(self, request):
		print "404"
		return self.render_template('404.html', debug=DEBUG)


def create_app(with_static=True):
	app = ImpressJS(config={})
	if with_static:
		# wrap the wsgi_app with a middleware handling static exports
		app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
		'/static': os.path.join(os.path.dirname(__file__), 'static')
		})
	return app


hostname = gethostname()
DEBUG = "webfaction" not in hostname

cvapp = create_app()
cvapp.wsgi_app = ProxyFix(cvapp.wsgi_app)

if __name__ == '__main__':
	from werkzeug.serving import run_simple

	port = 5000 if DEBUG else 31045
	run_simple('0.0.0.0' if DEBUG else '127.0.0.1', port, cvapp, use_debugger=DEBUG, use_reloader=DEBUG)
