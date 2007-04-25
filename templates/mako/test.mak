<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <link rel="shortcut icon" href="static/favicon.ico" type="image/x-icon">
    <link rel="icon" href="static/favicon.ico" type="image/x-icon">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>${context.get('blog_title', '')}
%if title is not UNDEFINED:
    - ${title}
%endif
</title>
<link href="/static/styles.css" rel="stylesheet" type="text/css" />
<style type="text/css">
</style>
</head>
<body>

<div id="box"><!-- Begin Container Box -->
<!--<div id="header"></div>-->
<div id="main"><!-- Begin Main Content -->

%if context.get('keywordrss', None):
  <a href="${keywordrss}">Rss for keyword</a>
%endif
