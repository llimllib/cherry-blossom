<html><head><title>${title}</title>
<body>
Actions: 
%for url, name in modules:
	<a href="/Admin/${url}">${name}</a> &nbsp;
%endfor
<br/><br/>
