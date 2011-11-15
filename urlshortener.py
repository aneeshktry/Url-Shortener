import random
import cgi


from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class Urldatas(db.Model):
	enteredurl=db.TextProperty()
	shorturl=db.TextProperty()
	link=db.TextProperty()


class Functions:
	def check(self,url,datas):
		for data in datas:
			if data.enteredurl==url:
				return data.link
	
	def random(self):
		s=''
		for x in range(0,4):
			s += chr(random.randint(96,122))
		return s	


class urlhandler(webapp.RequestHandler):
	def get(self):
		self.response.out.write(template.render('input.html',{}))
	
		
	
	

	def post(self):
		f=Functions()
		url=self.request.get("url")
		datas=db.GqlQuery("SELECT * FROM Urldatas")
		url1=f.check(url,datas)
		if url1:
			urllink=url1
		else:
			str1=f.random()
			urllink="http://www.pythonurlshortner.appspot.com/" + str1
			d = Urldatas() 
			d.enteredurl = url
			d.shorturl = str1
			d.link = urllink
			d.put()
		values={'shorturl':urllink}
		self.response.out.write(template.render('output.html',values))

class Redirect(webapp.RequestHandler):
	def get(self):
		var= self.request.path
		str1=var[1:]
		dbo=Urldatas.all()
		dbo=db.GqlQuery("SELECT * FROM Urldatas ")
		for x in dbo:
			if x.shorturl==str1:
		        	self.redirect(x.enteredurl)
		



application = webapp.WSGIApplication([('/',urlhandler),('/.+',Redirect)],debug=True)


def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
