<?xml version="1.0" ?>
<rss version="2.0" xmlns:admin="http://webns.net/mvcb/" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:creativeCommons="http://backend.userland.com/creativeCommonsRssModule" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:html="http://www.w3.org/1999/html" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:slash="http://purl.org/rss/1.0/modules/slash/">
    <channel>
        <title>${blog_title}</title>
        <link>${base_url}</link>
        <description>${blog_desc}</description>
        <language>${blog_lang}</language>
        <dc:creator>${blog_author} ${blog_email}</dc:creator>
%for e in entries:
        <item>
            <title>${e.title}</title>
            <guid isPermaLink="false">${e.relpath}</guid>
            <link>${e.link}</link>
            <description><![CDATA[${e.desc}]]></description>
            <content:encoded><![CDATA[${e.text}]]></content:encoded>
            <category domain="${base_url}">${e.relpath}</category>
            <dc:date>${e.time}</dc:date>
        </item>
%endfor
    </channel>
</rss>
