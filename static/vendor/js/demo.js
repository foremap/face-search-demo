$(function () {
    'use strict';
    // Load demo images:
    $.ajax({
        url: "/all-images",
        dataType:"json"
    }).done(function (result) {
        // console.log ( result.photos );
        var linksContainer = $('#links'),
            baseUrl; 
        // Add the demo images as links with thumbnails to the page:
        $.each(result.photos, function (index, photo) {
            baseUrl = photo.url;
            $('<a/>')
                .append($('<img>').prop('src', baseUrl).prop('width', 100))
                .prop('href', baseUrl.replace("lfw-small", "lfw-large"))
                .prop('title', photo.name)
                .attr('data-gallery', '')
                .appendTo(linksContainer);
        });
    });
});
