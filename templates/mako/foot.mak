%if context.get('offset') and offset > 0:
    <div id="prev-button">
		%if offset == num_entries:
			<a href="${pagename}">previous ${num_entries} &lt;&lt;</a><br>
		%else:
			<a href="${pagename}?offset=${offset - num_entries}">previous ${num_entries} &lt;&lt;</a><br>
		%endif
    </div>
%endif

%if context.get('keywordatom', None):
  <a href="${keywordatom}">Atom feed for keyword "${keyword}"</a>
%endif

%if context.get('offset_next'):
    <div id="next-button">
        <a href="${pagename}?offset=${offset_next}">next ${num_entries} &gt;&gt;</a>
        &nbsp; &nbsp;
    </div>
%endif

	</div></div></div> <!-- end yui-g, yui-b, yui-main -->
	
	<div class="yui-b"><img src="static/logo.png" id="logo" /><br>
   	<a href="mailto:bill.mill@gmail.com">contact</a> |
	<a href="elsewhere.html">elsewhere</a>
	</div>

	</div> <!-- end bd -->


	<div id="ft">footer</div>
</div> <!-- end yui-t7 -->
</body>
</html>
