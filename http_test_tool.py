#!/usr/bin/env python

import web, httplib, os, urlparse

class Home(object):
  def GET(self):
    path = 'index.html'
    if not os.path.exists(path):
      raise web.notfound()
    else:
      return open(path, 'rb').read()

class Request(object):
  def POST(self):
    form_data = web.input()
    host = urlparse.urlparse(form_data.url)[1]
    conn = httplib.HTTPConnection(host)
    path = form_data.url[form_data.url.find(host) + len(host):]
    headers = {}
    for line in form_data.headers.splitlines():
      k = line[:line.index(':')]
      v = line[line.index(':')+2:]
      headers[k.strip()] = v.strip()
    conn.request(form_data.method, path, form_data.body.encode("utf-8"), headers)
    response = conn.getresponse()
    response_headers = response.getheaders()
    headers = "HTTP %s %s\n" % (response.status, response.reason)
    headers += "\n".join(["%s:%s" % (k, v) for k, v in response_headers])
    response_body = response.read()
    render = web.template.render('templates')
    return render.result("%s %s\n%s" % (form_data.method, path, form_data.headers), form_data.body, headers, response_body)

class TestPost(object):
  def POST(self):
    return web.data()

urls = ('/', Home, '/request', Request, '/test', TestPost)

app = web.application(urls, globals())
if __name__ == '__main__':
  app.run()
