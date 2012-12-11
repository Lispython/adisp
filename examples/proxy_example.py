'''
A simple "proxy server" using [Tornado][1] web framework. Runs an asynchronous
HTTP server that queries requested URLs using asynchronous HTTP client. Adisp
makes it posible to process a response without defining an explicit callback
for it.

To use it run this file and point your browser at
http://localhost:8888/http://somehost.com/

[1]: http://www.tornadoweb.org/
'''
import tornado.httpserver
import tornado.httpclient
import tornado.web

from adisp import async, process

class Handler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @process
    def get(self, url):
        http = tornado.httpclient.AsyncHTTPClient()
        response = yield async(http.fetch, cbwrapper=self.async_callback)(url)
        if response.error:
            raise tornado.web.HTTPError(500, 'Ooops')
        self.write(response.body)
        self.finish()

application = tornado.web.Application([
    (r"/(.*)", Handler),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    print 'Listening on port 8888...'
    tornado.ioloop.IOLoop.instance().start()
