<ul>
%for e in essays:
	<li><a href="/${e.relpath}.html">${e.title}</a><br>
		<p><div id="firstp">${e.first_para}</div>
	</li>
%endfor
</ul>
