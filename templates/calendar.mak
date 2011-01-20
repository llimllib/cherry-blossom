<table>
<tr> 
    <td align="center" colspan="7"><a href="/${year}/${month}">${monthname}</a> ${year}</td>
</tr>
%for week in cal:
    <tr>
    %for day, isEntry in week:
        <td>
        %if day != 0 and isEntry:
            <a href="/${year}/${month}/${day}">${day}</a>
        %elif day != 0:
            ${day}
        %else:
            &nbsp;
        %endif
        </td>
    %endfor
    </tr>
%endfor
</table>
