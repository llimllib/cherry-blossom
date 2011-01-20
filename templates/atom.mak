<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
	<link rel="self" href="/Atom/" />
	<id>${base_url}</id>
	<title>${blog_title}</title>
	<subtitle>${blog_desc}</subtitle>
	<updated>${last_updated}</updated>
	<author>
		<name>${blog_author}</name>
		<email>${blog_email}</email>
		<uri>${base_url}</uri>
	</author>
	<link href="${base_url}" />
%for e in entries:
	<entry>
		<title>${e.title}</title>
		<link href="${e.link}" />	
		<id>${e.link}</id>
		<updated>${e.time}</updated>
		<summary type="html">${e.desc}</summary>
		<content type="html">${e.text}</content>
	</entry>
%endfor
</feed>
