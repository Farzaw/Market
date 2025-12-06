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

function SetRoute(id){
    $('#id_routeFrom').find('option').remove().end().append('<option>Загрузка...</option>');
    $('#routeTo').find('option').remove().end().append('<option>Загрузка...</option>');

    let val = document.getElementById(id).value;
    if(val) {
        $.ajax({
            type: 'POST',
            url: url,
            data: {'country_id': val},

            success: function (response) {

                let routes = response["routes"];
                let routeFromElem = document.getElementById('id_routeFrom');
                let routeToElem = document.getElementById('id_routeTo');

                $('#id_routeFrom').find('option').remove().end().append('<option value="-1">---------</option>');
                $('#id_routeTo').find('option').remove().end().append('<option value="-1">---------</option>');

                for (let r of routes) {

                    let option1 = document.createElement("option");
                    option1.text = r[1];
                    option1.value = r[0];
                    routeFromElem.add(option1);

                    let option2 = document.createElement("option");
                    option2.text = r[1];
                    option2.value = r[0];
                    routeToElem.add(option2);
                }
            },
            error: function (response) {
                // alert the error if any error occured
                console.log(response["error"]);
            }
        })
    }
}

function SetRoute2(id){
    $('#id_route').find('option').remove().end().append('<option>Загрузка...</option>');

    let val = document.getElementById(id).value;
    if(val) {
        $.ajax({
            type: 'POST',
            url: url,
            data: {'country_id': val},

            success: function (response) {

                let routes = response["routes"];
                let routeElem = document.getElementById('id_route');

                $('#id_route').find('option').remove().end().append('<option value="-1">---------</option>');

                for (let r of routes) {

                    let option1 = document.createElement("option");
                    option1.text = r[1];
                    option1.value = r[0];
                    routeElem.add(option1);

                }
            },
            error: function (response) {
                // alert the error if any error occured
                console.log(response["error"]);
            }
        })
    }
}

function OpenModal(clientID) {
    let direction = $('#id_direction').val();

    let data = {
        "direction": direction,
        "routes[]": $('#id_route').val(),
        "agent": $('#id_agent').val(),
        "clientID": clientID
    }

    if(direction)
     $.ajax({
        type: 'POST',
        url: url2,
        data: data,
        success: function (response) {
            $('#inf1').text(response["inf1"]);

            let L = response["L"];
            let total = response["total"];

            let tbody = document.getElementById("idBody");
            $("#idBody").empty();
            let tr,tn;

            for(let l of L){
                tr = document.createElement("tr");

                let td0 = document.createElement("td");
                tn = document.createTextNode(l[0]);
                td0.appendChild(tn);
                td0.align='center';
                tr.appendChild(td0);

                let td1 = document.createElement("td");
                tn = document.createTextNode(l[1]);
                td1.appendChild(tn);
                td1.align='center';
                tr.appendChild(td1);

                let td2 = document.createElement("td");
                tn = document.createTextNode(l[2]);
                td2.appendChild(tn);
                td2.align='center';
                tr.appendChild(td2);


                let td3 = document.createElement("td");
                tn = document.createTextNode(l[3]);
                td3.appendChild(tn);
                td3.align='center';
                tr.appendChild(td3);

                tbody.appendChild( tr);
            }

            tr = document.createElement("tr");
            tr.style.fontWeight = 'bold';
            let td_total = document.createElement("td");
            tn = document.createTextNode("Итого:");
            td_total.appendChild(tn);
            td_total.align='right';
            tr.appendChild(td_total);

            let td_total0 = document.createElement("td");
            tn = document.createTextNode(total[0]);
            td_total0.appendChild(tn);
            td_total0.align='center';
            tr.appendChild(td_total0);

            let td_total1 = document.createElement("td");
            tn = document.createTextNode(total[1]);
            td_total1.appendChild(tn);
            td_total1.align='center';
            tr.appendChild(td_total1);

            let td_total2 = document.createElement("td");
            tr.appendChild(td_total2);
            tbody.appendChild( tr);

            tr = document.createElement("tr");
            tr.style.fontWeight = 'bold';

            let td1 = document.createElement("td");
            tn = document.createTextNode(" Всего:");
            td1.appendChild(tn);
            td1.colSpan="2";
            td1.align='right';
            tr.appendChild(td1);


            let td2 = document.createElement("td");
            tn = document.createTextNode(total[0]+total[1]);
            td2.appendChild(tn);
            td2.align='center';
            tr.appendChild(td2);

            let td_t2 = document.createElement("td");
            tn = document.createTextNode(total[2]);
            td_t2.appendChild(tn);
            td_t2.align='center';
            tr.appendChild(td_t2);

            tbody.appendChild( tr);

            $('#modal-lg').modal('show');
        },
        error: function (response) {
            // alert the error if any error occured
            console.log(response);
        }
    })
}