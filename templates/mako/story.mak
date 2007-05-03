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
[<a href="${base_url}${relpath}">#${context.get('commentstr', '')}</a>] 
${context.get('keywords', '')}
</div>
