#!/usr/bin/python

import os,sys
from random import randint

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from django.utils import simplejson as json

from models import Payment

class PaymentHandler(webapp.RequestHandler):    
    def __init__(self):
        self.commandMap = {
            "CreatePayment" : self.CreatePayment ,
            "FetchPayment" : self.FetchPayment,
            "PaymentStatus" : self.PaymentStatus,
            "DoPayment": self.DoPayment
        }
    
    def get(self,command,argument=''):
        self.commandMap[command](self.request.get('token'))
        
            
    def post(self,command,argument=''):        
                    
        try:
            self.commandMap[command](json.loads(self.request.body))
        except:
            self.response.out.write("cannot create payment:" + str(sys.exc_info()[:]))
    
    def CreatePayment(self,details):
                        
        p = Payment()
        p.amount = details["amount"]
        p.company = details["company"]
        p.complete = False
        p.token = str(self.GenerateToken())        
        p.put()
        
        resp = {
            "success" : True ,
            "token" : p.token
        }        
        self.response.out.write(json.dumps(resp))
                
        return True
    
    def FetchPayment(self,token):
        q = Payment.all()
        q.filter("token =", token)
        p = q.fetch(1)[0]
    
        values = {
            "company" : p.company,
            "amount" : p.amount,
            "token" : p.token
        }
        
        path = os.path.join(os.path.dirname(__file__), 'templates/payment_details.html')
        self.response.out.write(template.render(path, values))
    
            
    def DoPayment(self,token):        
        q = Payment.all()
        q.filter("token = ",token)
        p = q.fetch(1)[0]
        
        if p:
            p.complete = True
            p.put()
        
        values = {
            "confirmation_code" : str(self.GenerateToken())
        }
        
        path = os.path.join(os.path.dirname(__file__), 'templates/payment_complete.html')
        self.response.out.write(template.render(path, values))
        
    def PaymentStatus(self,token):
        q = Payment.all()
        q.filter("token = ",token)
        p = q.fetch(1)[0]
        
        resp = {
            "token" : token,
            "isComplete" : p.complete
        }
        
        self.response.out.write(json.dumps(resp))
    
    def GenerateToken(self):
        #TODO: fix this shit
        return randint(10e7,10e8)
        
        
        
        