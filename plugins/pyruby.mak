<%def name="pycode()">
<tr><td>
<pre name="code" class="python:nogutter:nocontrols">
</%def>

<%def name="rubycode()">
</pre></td><td>
<pre name="code" class="ruby:nogutter:nocontrols">
</%def>

<html><head><title>test</title></head>
<body>
<table border=0>
${pycode()}
class PythonRuby:
    def __init__(self, parent): pass
${rubycode()}
class PythonRuby
    def initialize(parent)
    end
end</pre>
<link type="text/css" rel="stylesheet" href="/static/SyntaxHighlighter/SyntaxHighlighter.css"></link>
<script language="javascript" src="/static/SyntaxHighlighter/shCore.js"></script>
<script language="javascript" src="/static/SyntaxHighlighter/shBrushPython.js"></script>
<script language="javascript" src="/static/SyntaxHighlighter/shBrushRuby.js"></script>
<script language="javascript">
dp.SyntaxHighlighter.ClipboardSwf = '/static/SyntaxHighlighter/clipboard.swf';
dp.SyntaxHighlighter.HighlightAll('code');
</script>
</body>
</html>
