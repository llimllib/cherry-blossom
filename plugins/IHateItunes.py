import cherrypy as cpy
import twitter
from time import time

class IHateItunes:
    def __init__(self, parent):
        self.twit = twitter.Api(username="IHateItunes", password="foobar")
        self.last_check = time()
        self.replies = self.twit.GetReplies()

    def getReplies(self):
        if self.last_check - time() > 30:
            self.replies = self.twit.GetReplies()
            self.last_check = time()
        return self.replies

    @cpy.expose
    def index(self):
        return """<html><head><title>I Hate iTunes</title></head>
<body>
<p>I Hate iTunes is a resources for all those who have gripes with iTunes. To use it,
simply <a href="http://twitter.com/IHateItunes">tweet IHateItunes</a> with the
annoyance that's getting to you today.</p>
<p><h3>I Hate iTunes because:</h3><p><ul>
        """ + "".join("<li>%s</li> - <a href='http://twitter.com/%s>%s</a>" %  \
                       (msg.text, msg.user.name, msg.user.name)                    \
                       for msg in self.getReplies()) +                         \
        "</ul></body></html>"
