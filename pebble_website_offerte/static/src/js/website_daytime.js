odoo.define('website_daytime.website_daytime', ['web.ajax'], function (require) {
    'use strict';

    var ajax = require('web.ajax');
    $(document).ready(function () {
        var container = document.getElementById("website_daytime_container");
        var date = document.getElementById("daytime_date")
        var day = document.getElementById("daytime_day")
        var sunrise = document.getElementById("daytime_sunrise")
        var sunset = document.getElementById("daytime_sunset")
        var daylength = document.getElementById("daylength")

        // floating div
        var container_float = document.getElementById("daytime_float_main_div");
        var sunrise_float = document.getElementById("sunrise_float")
        var sunset_float = document.getElementById("sunset_float")
        var date_float = document.getElementById("date_float")

        if (container) {
            ajax.jsonRpc('/update_daytime', 'call', {}).then(function(data) {
                date.innerHTML = "";
                day.innerHTML = "";
                sunrise.innerHTML = "";
                sunset.innerHTML = "";
                daylength.innerHTML = "";
                date.innerHTML += data[0].date;
                day.innerHTML += data[0].day;
                sunrise.innerHTML += data[0].sunrise;
                sunset.innerHTML += data[0].sunset;
                daylength.innerHTML += data[0].daylength;
            });
        }

        if (container_float) {
            ajax.jsonRpc('/update_daytime', 'call', {}).then(function(data) {
                sunrise_float.innerHTML = "";
                sunset_float.innerHTML = "";
                date_float.innerHTML = "";
                date_float.innerHTML += data[0].date;
                sunrise_float.innerHTML += data[0].sunrise;
                sunset_float.innerHTML += data[0].sunset;
            });
        }

    });
});
