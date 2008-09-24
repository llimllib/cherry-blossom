<!--TODO
* write an intro
* Explain symbols
* improve code sample typography
  * large space between [ and start of list
  * difficult to tell } from )
  * = looks like -
* break out into pages
* create a TOC
* fix HTML output (it works-ish now, but creates crappy HTML)
* list comprehensions
    * select/find_all/each/inject
* ! and ? methods
* <=> operator
* ranges (.. and ... operators)
* lack of nested functions
-->

<%def name="explain(header, text)">
</pre><tr><td colspan="2">
% if 0:
    <h2>${header}</h2>
% endif

% if text:
    <p>${text}</p>
% endif
</td></tr>
</%def>

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
<h1>Translating Selected Python idioms into Ruby</h1>
<table border="0" width="800">
${explain("None","The ruby equivalent of <code>None</code> is <code>nil</code>")}
${pycode()}None
${rubycode()}nil

${explain("print","The ruby equivalent of the print statement is the <code>puts()</code> function")}
${pycode()}>>> print "Twenty twelve"
Twenty twelve
${rubycode()}>>> puts "thirteen"
thirteen
=> nil

${explain("comments","Ruby comments begin with hashmarks and extend to the end of the line, just like in python")}
${pycode()}#this is a comment to the end of the line
${rubycode()}#so is this

${explain("assignment","""Assignments in ruby return a value. When showing interactive Ruby in this document
I will often omit these return values for clarity.""")}
${pycode()}>>> x = 12
${rubycode()}>>> x = 12
=> 12

${explain("boolean", """Ruby has boolean objects <code>true</code> and <code>false</code>""")}
${pycode()}>>> 42 == 42
True
>>> 42 == 43
False
${rubycode()}>>> 42 == 42
=> true
>>> 42 == 43
=> false

${explain("quotes", """Ruby strings may be enclosed in single or double quotes, just as in python, though double quotes
allow interpolation and single quotes don't; more on that later.""")}
${pycode()}>>> "spam" == 'spam'
True
${rubycode()}>>> "onyx" == 'onyx'
=> true

${explain("str()","The ruby equivalent of the <code>str()</code> function is the <code>to_s</code> method")}
${pycode()}>>> str(42)
"42"
${rubycode()}>>> 42.to_s
=> "42"

${explain("str()","Unsurprisingly, the ruby equivalent of the <code>int()</code> function is the <code>to_i</code> method")}
${pycode()}>>> int("42")
"42"
${rubycode()}>>> "42".to_i
=> 42

${explain("dir()","Use Ruby's <code>methods()</code> method where you'd use Python's <code>dir()</code>")}
${pycode()}>>> dir(12)
['__abs__', '__add__', '__and__', ...]
${rubycode()}>>> 12.methods()
=> ["method", "%", "between?", "send", ...]

${explain("unpacking","You may unpack lists in Ruby just like in Python")}
${pycode()}>>> a,b = [42, 43]
>>> a
42
>>> b
43
${rubycode()}>>> a,b = [42, 43]
=> [42, 43]
>>> a
=> 42
>>> b
=> 43

${explain("conditional assignment","Python has no operator equivalent to ruby's conditional assignment operator")}
${pycode()}if not x:
    x = 12
${rubycode()}x ||= 12

${explain("tuples","Ruby has no concept of tuples; simply use lists for the same purpose")}
${pycode()}("spam", 42)
${rubycode()}["emerald", 42]

${explain("Dictionaries","Ruby spells dictionary \"Hash\". You must call the Hash constructor with square brackets instead of parens.")}
${pycode()}>>> {1: 2, "alpha": "beta"}
{1: 2, "alpha": "beta"}
>>> dict([(1,2), ("alpha", "beta")])
{1: 2, 'alpha': 'beta'}
${rubycode()}>>> {1=> 2, "alpha"=> "beta"}
=> {"alpha"=>"beta", 1=>2}
>>> Hash[1, 2, "alpha", "beta"]
=> {"alpha"=>"beta", 1=>2}

${explain("tuple and list access","You may access elements of lists and hashes with square brackets, just like in python")}
${pycode()}>>> [1,2,3,4,5][2]
3
>>> {1: 2, "alpha": "beta"}["alpha"]
"beta"
${rubycode()}>>> [1,2,3,4,5][2]
=> 3
>>> {1: 2, "alpha": "beta"}["alpha"]
=> "beta"

${explain("id","Ruby's equivalent of Python's built-in <code>id()</code> function is the <code>object_id</code> method")}
${pycode()}>>> x = "spam"
>>> id(x)
19923360
${rubycode()}>>> x = "diamond"
=> "diamond"
>>> x.method_id
=> 192042

${explain("strings","Ruby has mutable strings, while Python has immutable ones")}
${pycode()}>>> x = "spam"
>>> y = x
>>> x[1] = "c"
>>> x
"scam"
>>> y
"spam"
${rubycode()}>>> x = "opal"
>>> y = x
>>> x[1] = "c"
>>> x
=> "ocal"
>>> y
=> "ocal"

${explain("symbols","""Ruby has a concept of \"symbols\", which are somewhat like 
<a href=\"http://docs.python.org/lib/non-essential-built-in-funcs.html\">interned</a> strings. Note that
python automatically interns strings which look like identifiers, which can be a bit surprising.""")}
${pycode()}>>> a = "!"
>>> b = "!"
>>> c = intern("!")
>>> d = intern("!")
>>> id(a) != id(b) and id(c) == id(d)
True
${rubycode()}>>> a = "topaz"
>>> b = "topaz"
>>> c = :topaz
>>> d = :topaz
>>> a.object_id != b.object_id && c.object_id == d.object_id
=> true

${explain("Functions", """Simple functions are defined almost identically by ruby and python. In ruby, whitespace
is not significant, and empty functions simply return nil.""")}
${pycode()}
def f():
    pass
${rubycode()}
def f()
end

${explain("Function calls","Ruby function calls do not always require parentheses; we'll revisit this more later")}
${pycode()}def f():
    return "spam"

>>> f()
'spam'
>>> f
&lt;function f at 0x000000&gt;
${rubycode()}def f()
    return "why?"
end

>>> f()
=> "why?"
>>> f
=> "why?"

${explain("Functions", """Standard positional arguments function the same way in python and ruby""")}
${pycode()}
def f(a, b, c):
    print a, b, c

f("alpha", 12, 'beta')
${rubycode()}
def f(a, b, c)
    puts a, b, c
end

#these two calls are identical
f("alpha", 12, 'beta')
f "alpha", 12, 'beta'

${explain("return","""Ruby has a return statement, but it will return the result of the last expression
in a function if one is not present""")}
${pycode()}def f():
    return "silly walk"
${rubycode()}def f()
    return "pearl"
end
def g()
    "pearl"
end

>>> f() == g()
=> true

${explain("rest","Ruby supports arbitrary argument lists similarly to Python")}
${pycode()}def f(a, *rest):
    return rest

>>> f(1,2,3,4)
(2,3,4)
${rubycode()}def f(a, *rest)
    rest
end

>>> f(1,2,3,4)
=> [2,3,4]

${explain("splat","Ruby also has a splat operator that works just like Python's")}
${pycode()}def f(a, b, c):
    return a + b + c

>>> f(*[1,2,3])
6
${rubycode()}def f(a, b, c)
    a + b + c
end

>>> f(*[1,2,3])
=> 6

${explain("Keyword Arguments","Ruby has no concept of keyword parameters; instead, one often passes a hash of options to a function.")}
${pycode()}def f(a=1, b=2, c=3):
	return a + b + c
${rubycode()}def f(params)
    params[:a] ||= 1
	params[:b] ||= 2
	params[:c] ||= 3

	params[:a] + params[:b] + params[:c]

${explain("blocks", """A Ruby block is just an anonymous function. One way to create one is with curly braces
delimiting the block and pipes delimiting the function's argument. A block may not be passed inside parentheses.""")}
${pycode()}>>> x = [['a', 99], ['a', 1]]

>>> x.sort(lambda x, y: cmp(x[1], y[1]))
>>> x
[['a', 1], ['a', 99]]
${rubycode()}>>> x = [['a', 99], ['a', 1]]

>>> x.sort {|x,y| x[1] <=> y[1]} 
=> [["a", 1], ["a", 99]]
>>> x.sort({|x,y| x[1] <=> y[1]})
SyntaxError: compile error

${explain("blocks contd", """There is an alternative, equivalent, "do/end" syntax for blocks.""")}
${pycode()}>>> x = [['a', 99], ['a', 1]]
>>> x.sort(lambda x, y: cmp(x[1], y[1]))
>>> x
[['a', 1], ['a', 99]]
${rubycode()}>>> [['a', 99], ['a', 1]].sort do |x,y|
    x[1] <=> y[1]
end
=> [["a", 1], ["a", 99]]

${explain("List Comprehensions","""There is no exact equivalent to python's list comprehensions in Ruby. A few
examples and equivalents follow:""")}
${pycode()}[x**2 for x in range(6)]
[x**2 for x in range(6) if x%2 == 0]
[x+y for x in ["a", "b", "c"] for y in ["d", "e"]]
${rubycode()}(1...6).map { |x| x**2 }
(1...6).select({|x| x%2 == 0}).map({|x| x**2})
["a", "b", "c"].map {|x| ["d", "e"].map {|y| x+y}}.flatten

</td></tr>
</table>
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
