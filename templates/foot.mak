<div>
%if context.get('offset') and offset > 0:
		%if offset == num_entries:
			&laquo; <a href="${pagename}">previous ${num_entries}</a> &nbsp;
		%else:
			&laquo; <a href="${pagename}?offset=${offset - num_entries}">previous ${num_entries}</a> &nbsp;
		%endif
%endif

%if context.get('keywordatom', None):
  <a href="${keywordatom}">Atom feed for keyword "${keyword}"</a>
%endif

%if context.get('offset_next'):
        <a href="/${pagename}?offset=${offset_next}">next ${num_entries} &raquo;</a>
%endif
</div>

</div>
</body>
</html>
