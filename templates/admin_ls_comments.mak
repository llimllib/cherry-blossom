<form action="delete_comments" method="POST">
<table border=1>
	<tr><td>Delete?</td><td>Story Name</td><td>Author</td><td>Email</td>
	<td>Url</td><td>Comment</td></tr>
%for comment in comments:
	<tr><td><input type="checkbox" name="delete_filename" 
		value="${comment.filename}"></td>
	<td>${comment.story}</a></td>
	<td>${comment.author}</a></td>
	<td><a href="mailto:${comment.email}">${comment.email}</a></td>
	<td><a href="${comment.url}">${comment.url[7:20]}</a></td>
	<td>${comment.text}</td>
%endfor
</table>
<input type="submit" value="Delete Checked Comments">
</form>
