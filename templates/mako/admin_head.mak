<html><head><title>${title}</title>
<body>
Actions: 
%for mod in modules:
	<a href="/Admin/${mod['link']}">${mod['title']}</a> &nbsp;
%endfor
<br/><br/>
