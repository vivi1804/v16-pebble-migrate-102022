odoo.define('website_blog_snippet.s_latest_posts', ['web.ajax'], function (require) {
    'use strict';
    
    var ajax = require('web.ajax');
    
    $(document).ready(function () {
        var container = document.getElementById("blog_post");
        var img_cover = document.getElementById("blog_cover");
        var container_url = document.getElementById("blog_url");

        if (container) {
            container.innerHTML = "";
        
            ajax.jsonRpc('/get_blog_posts', 'call', {}).then(function(post){
                container.innerHTML = "";
                img_cover.innerHTML = "";
                container_url.innerHTML = "";

                for (var i=0; i < post.length; i++){
                    container.innerHTML +=  post[i].content.slice(0,120);
                    img_cover.innerHTML += '<img class="card-img-top" src="' + post[i].cover + '" style="object-fit: cover;height:230px;" alt="Latest News"/>'
                    container_url.innerHTML += '<a href="/blog/' + post[i].post_url +'" class="btn btn-primary btn-sm o_default_snippet_text">Lees Meer</a>'
                }
            });
        }
    });
});