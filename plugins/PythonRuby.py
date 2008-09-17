import cherrypy as cpy

class PythonRuby:
    def __init__(self, parent): pass

    @cpy.expose
    def index(self):
        return """<html><head><title>test</title></head>
<body>something</body>
<link type="text/css" rel="stylesheet" href="css/SyntaxHighlighter.css"></link>
<script language="javascript" src="js/shCore.js"></script>
<script language="javascript" src="js/shBrushCSharp.js"></script>
<script language="javascript" src="js/shBrushXml.js"></script>
</html>
