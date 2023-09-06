odoo.define('website_project_snippet.s_latest_projects', ['web.ajax'], function (require) {
    'use strict';
    
    var ajax = require('web.ajax');
    $(document).ready(function () {
        var container = document.getElementById("ref_post");
        var img_cover = document.getElementById("ref_cover");
        var container_url = document.getElementById("ref_url");

        if (container) {
            container.innerHTML = "";
        
            ajax.jsonRpc('/get_references', 'call', {}).then(function(data){
                container.innerHTML = "";
                img_cover.innerHTML = "";
                container_url.innerHTML = "";

                for (var i=0; i < data.length; i++){
                    container.innerHTML += data[i].short_description.slice(0,120);
                    img_cover.innerHTML += '<img class="card-img-top" src="' + data[i].cover + '" style="object-fit: cover;height:230px;" alt="Latest Projects"/>'
                    container_url.innerHTML += '<a href="/references/' + data[i].post_url +'" class="btn btn-primary btn-sm o_default_snippet_text">Lees Meer</a>'
                }
            });
        }
    });
});