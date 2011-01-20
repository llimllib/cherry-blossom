<style>
a img {
border: 0;
}

</style>
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js"></script>
<script>
photo_url = "http://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=6c6e7d67a4f5d77f00569dcaa6337be9&user_id=64114626@N00&format=json&jsoncallback=?";

photos = null;
photo_idx = 0;
function next_photo_src() {
    var p = photos.photo[photo_idx++];
    return "http://farm" + p.farm + ".static.flickr.com/" + p.server + "/" + p.id + "_" + p.secret + ".jpg";
}

function link(href, text) {
	return '<a href="' + href + '">' + text + '</a>';
}

function img(src) {
	return '<img src="' + src + '">';
}

function next() {
    $("#photo").html(link('#" onclick="next()', img(next_photo_src())) + "<br>" +
					 link("#", img("http://billmill.org/static/flickr_logo.gif")));
}

$(document).ready(function(){
    page = window.location.href.match(/page=(\d+)/);
    if (page) {
        page = parseInt(page[1]);
        //TODO: what to do with the page?
    }

    $.getJSON(photo_url, function(data) {
        photos = $(data)[0].photos;
		next();
    });
});
</script>
<div id="photo" style="img { border: 0; }">
</div>
