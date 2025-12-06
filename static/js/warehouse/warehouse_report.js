$(document).ready(function()
{
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                } } }
        return cookieValue;
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });


    document.getElementById('id_direction').addEventListener('change', function() {

        let country = document.getElementById('id_direction').value;
        let routeFromEl = document.getElementById('id_routeFrom');
        let routeToEl = document.getElementById('id_routeTo');

        let length1 = routeFromEl.options.length;
        for (let i = length1-1; i >= 0; i--)
            routeFromEl.options[i] = null;

        let length2 = routeToEl.options.length;
        for (let i = length2-1; i >= 0; i--)
            routeToEl.options[i] = null;

        if(country) {
            $.ajax({
                type: 'POST',
                url: url,
                data: {'country': country},
                dataType: 'json',
                success: function (response) {
                    const routes = response["routes"];

                    let optionE1 = document.createElement("option");
                    let optionE2 = document.createElement("option");
                    routeFromEl.add(optionE1);
                    routeToEl.add(optionE2);

                    for (let i = 0; i < routes.length; i++) {
                        let option1 = document.createElement("option");
                        option1.text = routes[i].text;
                        option1.value = routes[i].pk;
                        routeFromEl.add(option1);

                        let option2 = document.createElement("option");
                        option2.text = routes[i].text;
                        option2.value = routes[i].pk;
                        routeToEl.add(option2);
                    }
                },
                error: function (response) {
                    console.log("error");
                }
            });
        }

    });
        }
    );


