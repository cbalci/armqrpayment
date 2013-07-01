#!/usr/bin/python

import os,sys

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

from paymentHandler import *

class MainHandler(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        self.response.out.write(template.render(path, template_values))
        
def main():
    application = webapp.WSGIApplication([
        ('/', MainHandler),
        (r'/qrpayment/(.*)',PaymentHandler)
        ], debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
