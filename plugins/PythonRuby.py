import cherrypy as cpy

class PythonRuby:
    def __init__(self, parent): pass

    @cpy.expose
    def index(self):
        return """<html><head><title>test</title></head>
<body><pre name="code" class="python:nogutter:nocontrols">
class PythonRuby:
    def __init__(self, parent): pass
</pre>
<link type="text/css" rel="stylesheet" href="/static/SyntaxHighlighter/SyntaxHighlighter.css"></link>
<script language="javascript" src="/static/SyntaxHighlighter/shCore.js"></script>
<script language="javascript" src="/static/SyntaxHighlighter/shBrushPython.js"></script>
<script language="javascript" src="/static/SyntaxHighlighter/shBrushRuby.js"></script>
<script language="javascript">
dp.SyntaxHighlighter.ClipboardSwf = '/static/SyntaxHighlighter/clipboard.swf';
dp.SyntaxHighlighter.HighlightAll('code');
</script>
</body>
</html>"""
