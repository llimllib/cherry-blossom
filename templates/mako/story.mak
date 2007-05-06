    <div id="entry">
    <h1>${title}
<br>${tmstr}</h1><br>
${text}
<p>
%if n_comments is not UNDEFINED:
	%try:
		%if int(n_comments) == 1:
			<% attributes['commentstr'] = ' (1 Comment)' %>
		%else:
			<% attributes['commentstr'] = ' (%s Comments)' % (n_comments) %>
		%endif
	%except ValueError:
		<% attributes['commentstr'] = '' %>
	%endtry
%endif

%if context.get('attributes'):
	[<a href="${base_url}${relpath}.html">#${attributes.get('commentstr', '')}</a>] 
%else:
	[<a href="${base_url}${relpath}.html">#</a>] 
%endif

${context.get('keywords', '')}
</div>
