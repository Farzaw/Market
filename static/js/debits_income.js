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


function SetClientOfAgent(id){
    id = id.replace('-inner', '-client');
    let element = document.getElementById(id);

    if (element)
        for (let i = element.options.length - 1; i >= 0; i--)
            element.options[i] = null;

    let val = document.getElementById('id_agent').value;

    if(val) {
        $.ajax({
            type: 'POST',
            url: url,
            data: {'agent_id': val},

            success: function (response) {
                let clients = response["clients"];

                if (element) {
                    let option = document.createElement("option");
                    option.text = '';
                    option.value = '';
                    element.add(option);

                    for(const [key, value] of Object.entries(clients)) {
                            let option = document.createElement("option");
                            option.text = value['client'];
                            option.value = value["pk"];
                            element.add(option);

                        }
                }
            },
            error: function (response) {
                console.log(response["error"]);
            }
        })
    }
}

$('#id_agent').on('change', function()
{

    let id = "id_agent";
    let x = document.getElementById('id_incomedebitsinner_set-TOTAL_FORMS').value;

    for(let i=0; i<x; i++) {
        let element = document.getElementById("id_incomedebitsinner_set-" + i.toString() + "-client");
        if (element)
            for (let i = element.options.length - 1; i >= 0; i--)
                element.options[i] = null;
    }

    let val = document.getElementById(id).value;
    if(val) {
        $.ajax({
            type: 'POST',
            url: url,
            data: {'agent_id': val},

            success: function (response) {
                let clients = response["clients"];
                console.log("clients");
                console.log(clients);
                console.log("clients");
                let x = document.getElementById('id_incomedebitsinner_set-TOTAL_FORMS').value;

                for(let i=0; i<x; i++)
                {
                    let element = document.getElementById("id_incomedebitsinner_set-"+ i.toString()+"-client");
                    id = "id_incomedebitsinner_set-"+ i.toString()+"-client";
                    if (element) {

                        let option = document.createElement("option");
                        option.text = '';
                        option.value = '';
                        element.add(option);

                        for(const [key, value] of Object.entries(clients)) {
                            let option = document.createElement("option");
                            option.text = value['client'];
                            option.value = value["pk"];
                            element.add(option);

                        }
                    }
                }
                console.log(response);
            },
            error: function (response) {
                // alert the error if any error occured
                console.log(response["error"]);
            }
        })
    }
})

function SetRoute(id)
{
    let id_route = id.replace('-client', '-route');
    let val = document.getElementById(id).value;
    let element = document.getElementById(id_route);
    if (element)
        for (let i = element.options.length - 1; i >= 0; i--)
            element.options[i] = null;

    if(val) {
        $('#' + id).attr("data-original-title", "Обрабатывается...").tooltip("show");

        $.ajax({
            type: 'POST',
            url: url2,
            data: {'client_id': val},

            success: function (response) {
                console.log(response);

                let routes = response["routes"];

                if (element) {

                    for (let i = element.options.length - 1; i >= 0; i--)
                        element.options[i] = null;

                    let option = document.createElement("option");
                    option.text = '';
                    option.value = '';
                    element.add(option);

                    for (let i = 0; i < routes.length; i++) {
                        let option = document.createElement("option");
                        option.text = routes[i]['text'];
                        option.value = routes[i]["pk"];
                        element.add(option);
                    }

                    console.log('------------------------');
                    console.log(routes);
                    console.log('------------------------');
                }
                $('#' + id).attr("data-original-title", "Долг: "+ response["remainder"]).tooltip("show");
            },
            error: function (response) {
                // alert the error if any error occured
                console.log(response["error"]);
            }
        })
    }
    else
    {

        $('#' + id).tooltip('dispose');
    }
}


function showDebits(prefix)
{

    let val = $('#id_'+ prefix + '-client').val();

    if(val) {
        $.ajax({
            type: 'POST',
            url: url3,
            data: {'client_id': val},

            success: function (response) {
                let dict = response["dict"]
                let income = response["income"]
                document.getElementById("inf_client").innerHTML=response["client"]
                document.getElementById("remainder_debt").innerHTML=
                    response["total1"]-response["total2"];


                let tbody = document.getElementById("idBody");
                $("#idBody").empty();
                let tr,tn;
                for(let k in dict){
                    tr = document.createElement("tr");
                    let td0 = document.createElement("td");
                    tn = document.createTextNode(k);
                    td0.appendChild(tn);
                    td0.align='center';
                    tr.appendChild(td0);

                    let td1 = document.createElement("td");
                    tn = document.createTextNode(dict[k][0]);
                    td1.appendChild(tn);
                    td1.align='center';
                    tr.appendChild(td1);

                    let td2 = document.createElement("td");
                    tn = document.createTextNode(dict[k][1]);
                    td2.appendChild(tn);
                    td2.align='center';
                    tr.appendChild(td2);
                    tbody.appendChild( tr);
                }

                tr = document.createElement("tr");
                tr.style.fontWeight = 'bold';
                let td_total = document.createElement("td");
                tn = document.createTextNode("Итого:");
                td_total.appendChild(tn);
                td_total.align='right';
                td_total.colSpan="2";
                tr.appendChild(td_total);

                let td_total0 = document.createElement("td");
                tn = document.createTextNode(response["total1"]);
                td_total0.appendChild(tn);
                td_total0.align='center';
                tr.appendChild(td_total0);

                tbody.appendChild( tr);

                let tbody2 = document.getElementById("idBody2");
                $("#idBody2").empty();

                for(let i of income) {
                    tr = document.createElement("tr");

                    let td0 = document.createElement("td");
                    tn = document.createTextNode(i[0]);
                    td0.appendChild(tn);
                    td0.align = 'center';
                    tr.appendChild(td0);

                    let td1 = document.createElement("td");
                    tn = document.createTextNode(i[1]);
                    td1.appendChild(tn);
                    td1.align = 'center';
                    tr.appendChild(td1);

                    let td2 = document.createElement("td");
                    tn = document.createTextNode(i[2]);
                    td2.appendChild(tn);
                    td2.align = 'center';
                    tr.appendChild(td2);
                    tbody2.appendChild(tr);
                }

                tr = document.createElement("tr");
                tr.style.fontWeight = 'bold';
                let td_total2 = document.createElement("td");
                tn = document.createTextNode("Итого:");
                td_total2.appendChild(tn);
                td_total2.align='right';
                td_total2.colSpan="2";
                tr.appendChild(td_total2);

                let td_total20 = document.createElement("td");
                tn = document.createTextNode(response["total2"]);
                td_total20.appendChild(tn);
                td_total20.align='center';
                tr.appendChild(td_total20);

                tbody2.appendChild( tr);
                $('#modal-lg').modal('show');

            },
            error: function (response) {
                // alert the error if any error occured
                console.log(response["error"]);
            }
        })
    }
}

function controllerDebitsSum()
{
    let form_total = document.getElementById('id_incomedebitsinner_set-TOTAL_FORMS').value;

    let total_sum = 0.0

    for(let i=0; i<form_total; i++){
        let id_sum = 'id_incomedebitsinner_set-' + i.toString() + '-sum';

        let sum = document.getElementById(id_sum);

        if(sum && sum.value)
            if (sum.parentNode.parentNode.parentNode.style.display !== "none") {
                total_sum += parseFloat(sum.value.replace(',','.'));
            }
    }
    document.getElementById('id_sum').value = total_sum;
}