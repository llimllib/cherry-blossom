%if context.get('offset_next'):
    <div id="next-button">
        <a href="${pagename}?offset=${offset_next}">next ${num_entries} &gt;&gt;</a>
        &nbsp; &nbsp;
    </div>
%endif
	<!--<div id="footer"></div> Empty right now! -->
</div> <!-- end main content -->
<div id="right-menu">
<div id="navcontainer"> <!--begin side navigation -->
    <div id="logo">
        <img src="/static/billmill_blu.gif">
    </div>
    <ul id="right-navlist">
        <li>
        <a href="/">blog</a> &bull;
        <a href="http://groups.google.com/group/billmillorg-discussion/topics?hl=en">discuss</a> &bull;
        <a href="/code.html">code</a> &bull;
        <a href="http://flickr.com/photos/llimllib">photos</a> &bull;
        <a href="/Atom/">Atom</a> &bull;
        <a href="http://www.last.fm/user/llimllib">music</a> &bull;
        <a href="http://del.icio.us/llimllib">bookmarks</a> &bull;
        <a href="http://bloglines.com/public/llimllib">blogroll</a> &bull;
        <a href="http://reddit.com/user/llimllib">reddit</a> &bull;
        <a href="http://billmill.org/static/medmen">Medicine Men Ultimate</a> &bull;
        <a href="mailto:bill.mill@gmail.com">email</a>
        </li>
    </ul>
</div><!-- end side navigaion -->

<!-- begin more info -->
<div id="more-info"><!--<h2 class="sideheader">My Name Rhymes</h2>-->
		<p></p>
		<p>I'm a programmer for a small company in 
        Baltimore, Maryland, USA. Besides programming, I play competitive 
        <a href="http://en.wikipedia.org/wiki/Ultimate_%28sport%29">ultimate</a>. 
        I blog at irregular intervals about various programming topics, but mostly
        Python.
        </p>
		<div id="blog-buttons">
			<p><a href="http://ronpaul2008.com"><img border=0 src="static/ronpaul.png"></a></p>
		</div>
</div><!-- end more info -->

</div><!--end main box div-->
</body>
</html>
