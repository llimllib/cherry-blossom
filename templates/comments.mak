%for cmt in comments:
<div class="comment">
    <br />${cmt.text}<br />
    %if cmt.url:
        Posted by <a href=${cmt.url}>${cmt.author}</a>
    %else:
        Posted by ${cmt.author}
    %endif
    <br />
</div>
%endfor
<p>
