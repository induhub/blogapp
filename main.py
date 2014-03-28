#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))


class BlogPost(ndb.Model):
    subject = ndb.StringProperty(required=True)
    content = ndb.TextProperty(required=True)
    


class RunHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('yahoo.html')
        context = {}
        html = template.render(context)
        self.response.write(html)
    def post(self):
        new_subject = self.request.get("subject")
        new_content = self.request.get("content")
        new_blog_post = BlogPost(subject=new_subject, content = new_content)
        post_key  = new_blog_post.put()
        post_id = post_key.id()
        self.redirect("/blog/"+str(post_id)) # /blog/84369
                                   
                                
class PostHandler(webapp2.RequestHandler):
    def get(self, post_id):
        blog_post = BlogPost.get_by_id(int(post_id))
        context = {'blog_post': blog_post}
        template = jinja_environment.get_template('post.html')
        html = template.render(context)
        self.response.write(html)

class MainHandler(webapp2.RequestHandler):
    def get(self) :
        query_object = BlogPost.query()
        top_10 = query_object.fetch(10)
        context = {'posts': top_10}
        template = jinja_environment.get_template('blog.html')
        html = template.render(context)
        self.response.write(html)
       

        
app = webapp2.WSGIApplication([
    ('/blog', MainHandler),('/blog/newpost',RunHandler),('/blog/(?P<post_id>.*)',PostHandler)
], debug=True)
