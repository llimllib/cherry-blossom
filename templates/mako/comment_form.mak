<form method="post" action="${url}" name="comments_form">
<input type="hidden" name="secretToken" value="pleaseDontSpam" />
<input name="story" type="hidden" value="${story}" />
Name:<br />
<input maxlength="50" name="author" size="50" type="text" value="" />
<br /><br />
E-mail:<br />
<input maxlength="75" name="email" size="50" type="text" value="" />
<br /><br />
URL:<br />
<input maxlength="100" name="url" size="50" type="text" value="" />
<br /><br />
Comment:<br />
<textarea cols="50" name="comment" rows="12"></textarea>
<br /><br />
<input name="Submit" type="submit" value="Submit" />
</form>
