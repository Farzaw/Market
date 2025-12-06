function OpenModal(empID) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

    let data = {
        "currency": $('#id_currency').val(),
        "dateFrom": $('#id_dateFrom').val(),
        "dateTo": $('#id_dateTo').val(),
        "inspection": $('#id_inspection').val(),
        "packing": $('#id_packing').val(),
        "loading": $('#id_loading').val(),
        "empID": empID,
    }
    $.ajax({
        type: 'POST',
        url: url,
        data: data,
        success: function (response) {

            $('#inf1').text(response["inf1"]);
            $('#inf2').text(response["inf2"]);

            let dict = response["dict"];
            let total = response["total"];

            let tbody = document.getElementById("idBody");
            $("#idBody").empty();
            let tr,tn;
            for(let k in dict){

                tr = document.createElement("tr");
                let td = document.createElement("td");
                tn = document.createTextNode(k);
                td.appendChild(tn);
                tr.appendChild(td);

                let td0 = document.createElement("td");
                tn = document.createTextNode(dict[k][0]);
                td0.appendChild(tn);
                td0.align='center';
                tr.appendChild(td0);

                let td1 = document.createElement("td");
                tn = document.createTextNode(dict[k][1]);
                td1.appendChild(tn);
                td1.align='center';
                tr.appendChild(td1);

                let td2 = document.createElement("td");
                tn = document.createTextNode(dict[k][2]);
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
            tn = document.createTextNode(total[2]);
            td_total2.appendChild(tn);
            td_total2.align='center';
            tr.appendChild(td_total2);
            tbody.appendChild( tr);


            tr = document.createElement("tr");
            tr.style.fontWeight = 'bold';
            let td0 = document.createElement("td");
            td0.colSpan="2";
            tr.appendChild(td0);

            let td1 = document.createElement("td");
            tn = document.createTextNode(" Сумма:");
            td1.appendChild(tn);
            td1.align='right';
            tr.appendChild(td1);


            let td2 = document.createElement("td");
            tn = document.createTextNode(response["sum"]);
            td2.appendChild(tn);
            td2.align='center';
            tr.appendChild(td2);
            tbody.appendChild( tr);

            $('#modal-lg').modal('show');
        },
        error: function (response) {
            // alert the error if any error occured
            console.log(response);
        }
    })
}

function OpenModalEdit(empID){
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
                }
            }
        }
        return cookieValue;
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

    let data = {
        "salaryID": PK,
        "empID": empID,
    }
    $.ajax({
        type: 'POST',
        url: url1,
        data: data,
        success: function (response) {

            $('#inf1').text(response["inf1"]);
            $('#inf2').text(response["inf2"]);

            let dict = response["dict"];
            let total = response["total"];

            let tbody = document.getElementById("idBody");
            $("#idBody").empty();
            let tr,tn;
            for(let k in dict){

                tr = document.createElement("tr");
                let td = document.createElement("td");
                tn = document.createTextNode(k);
                td.appendChild(tn);
                tr.appendChild(td);

                let td0 = document.createElement("td");
                tn = document.createTextNode(dict[k][0]);
                td0.appendChild(tn);
                td0.align='center';
                tr.appendChild(td0);

                let td1 = document.createElement("td");
                tn = document.createTextNode(dict[k][1]);
                td1.appendChild(tn);
                td1.align='center';
                tr.appendChild(td1);

                let td2 = document.createElement("td");
                tn = document.createTextNode(dict[k][2]);
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
            tn = document.createTextNode(total[2]);
            td_total2.appendChild(tn);
            td_total2.align='center';
            tr.appendChild(td_total2);
            tbody.appendChild( tr);


            tr = document.createElement("tr");
            tr.style.fontWeight = 'bold';
            let td0 = document.createElement("td");
            td0.colSpan="2";
            tr.appendChild(td0);

            let td1 = document.createElement("td");
            tn = document.createTextNode(" Сумма:");
            td1.appendChild(tn);
            td1.align='right';
            tr.appendChild(td1);


            let td2 = document.createElement("td");
            tn = document.createTextNode(response["sum"]);
            td2.appendChild(tn);
            td2.align='center';
            tr.appendChild(td2);
            tbody.appendChild( tr);

            $('#modal-lg').modal('show');
        },
        error: function (response)
        {
            console.log(response);
        }
    })
}

$( document ).ready(function() {
    let t = parseInt($('#id_salaryinner_set-TOTAL_FORMS').val())
    for(let prefix=0; prefix<t; prefix++)
        SalaryTotalSL("id_salaryinner_set-" + prefix.toString() + "-totalSL");
})

function SalaryTotalSL(id){

    let oklad = document.getElementById(id.replace('totalSL', 'oklad')).value.replace(',','.');
    let premiums = document.getElementById(id.replace('totalSL', 'premiums')).value.replace(',','.');
    let other = document.getElementById(id.replace('totalSL', 'other')).value.replace(',','.');
    let interest = document.getElementById(id.replace('totalSL', 'interest')).value.replace(',','.');
    let services = document.getElementById(id.replace('totalSL', 'services')).value.replace(',','.');


    let advance = document.getElementById(id.replace('totalSL', 'advance')).value.replace(',','.');
    let fine = document.getElementById(id.replace('totalSL', 'fine')).value.replace(',','.');
    let debt = document.getElementById(id.replace('totalSL', 'debt')).value.replace(',','.');
    let issuance = document.getElementById(id.replace('totalSL', 'issuance')).value.replace(',','.');

    let totalSL = document.getElementById(id);
    let remainder = document.getElementById(id.replace('totalSL', 'remainder'));
    let total = document.getElementById(id.replace('totalSL', 'total'));

    if(oklad && premiums && other && interest && services &&
        advance && fine && debt && issuance)
    {
        let tSL = parseFloat(oklad)+parseFloat(premiums)+parseFloat(other)+parseFloat(interest)+parseFloat(services);
        totalSL.value = (tSL).toFixed(3);

        let r = parseFloat(totalSL.value) + parseFloat(debt) - (parseFloat(advance) + parseFloat(fine));
        remainder.value = (r).toFixed(3);

        let t = parseFloat(remainder.value) - parseFloat(issuance);
        total.value =  (t).toFixed(3);
    }
    else
    {
        totalSL.value = "";
        remainder.value = "";
        total.value = "";
    }
}

function salaryOklad(id){
    SalaryTotalSL(id.replace('oklad', 'totalSL'));}

function salaryPremiums(id)
{
    SalaryTotalSL(id.replace('premiums', 'totalSL'));
}

function salaryOther(id){
    SalaryTotalSL(id.replace('other', 'totalSL'));
}

function salaryInterest(id){
    SalaryTotalSL(id.replace('interest', 'totalSL'));
}

function salaryDebt(id){
    let debt = document.getElementById(id).value.replace(',','.');
    let remainder = document.getElementById(id.replace('debt', 'remainder'));
    let total = document.getElementById(id.replace('debt', 'total'));
    let issuance = document.getElementById(id.replace('debt', 'issuance')).value.replace(',','.');

    let advance = document.getElementById(id.replace('debt', 'advance')).value.replace(',','.');
    let fine = document.getElementById(id.replace('debt', 'fine')).value.replace(',','.');
    let totalSL = document.getElementById(id.replace('debt', 'totalSL')).value.replace(',','.');

    if(debt && issuance && advance && fine && totalSL)
    {
        let r = parseFloat(totalSL) - (parseFloat(advance) + parseFloat(fine)) + (parseFloat(debt));
        remainder.value = (r).toFixed(3);
        let t = parseFloat(remainder.value) - parseFloat(issuance);
        total.value = (t).toFixed(3);
    }

    else
    {
        let oklad = document.getElementById(id.replace('debt', 'oklad')).value.replace(',','.');
        let premiums = document.getElementById(id.replace('debt', 'premiums')).value.replace(',','.');
        let other = document.getElementById(id.replace('debt', 'other')).value.replace(',','.');
        let interest = document.getElementById(id.replace('debt', 'interest')).value.replace(',','.');
        let services = document.getElementById(id.replace('debt', 'services')).value.replace(',','.');

        let totalSL = document.getElementById(id.replace('debt', 'totalSL'));
        let remainder = document.getElementById(id.replace('debt', 'remainder'));
        let total = document.getElementById(id.replace('debt', 'total'));

        if(oklad && premiums && other && interest && services)
        {
            let t = parseFloat(oklad)+parseFloat(premiums)+parseFloat(other)+parseFloat(interest)+parseFloat(services);
            totalSL.value = (t).toFixed(3);
        }
        else
            totalSL.value = "";

        remainder.value = "";
        total.value = "";
    }
}

function salaryIssuance(id){

    let issuance = document.getElementById(id).value.replace(',','.');

    let remainder = document.getElementById(id.replace('issuance', 'remainder')).value.replace(',','.');

    let total = document.getElementById(id.replace('issuance', 'total'));

    if(issuance && remainder)
        total.value = parseFloat(remainder) - parseFloat(issuance);
    else
        total.value = "";
}