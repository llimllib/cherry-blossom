<table><tr>
    <form method="POST" name="edit_story" action="../update_story">
    <input type="hidden" value="${filename}" name="filename">
    <td>Title:</td>
    <td><input name="story_title" value="${story_title}" size="75"/><br/></td>
</tr><tr>
    <td>Body</td>
    <td><textarea name="story_body" rows=50 cols=75>${body}</textarea></td>
</tr><tr>
    <td></td>
    <td><input type="submit" text="submit"></td>
</tr></table>
</body>
</html>
