<html><head>
<link rel="alternate" type="application/rss+xml" title="billmill.org RSS Feed" href="http://billmill.org/Rss/" />
<link rel="shortcut icon" href="static/favicon.ico" type="image/x-icon">
<link rel="icon" href="static/favicon.ico" type="image/x-icon">
<link href="/static/styles.css" rel="stylesheet" type="text/css" />
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

<title>${blog_title} - ${context.get('title', '')}</title>
</head>
<body>

<div id="box"><!-- Begin Container Box -->
<!--<div id="header"></div>-->
<div id="main"><!-- Begin Main Content -->

%if context.get('offset') and offset > 0:
    <div id="prev-button">
		%if offset == num_entries:
			<a href="${pagename}">previous ${num_entries} &lt;&lt;</a><br>
		%else:
			<a href="${pagename}?offset=${offset - num_entries}">previous ${num_entries} &lt;&lt;</a><br>
		%endif
    </div>
%endif

%if context.get('keywordrss', None):
  <a href="${keywordrss}">Rss for keyword</a>
%endif
