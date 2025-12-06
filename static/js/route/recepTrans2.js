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

function ControllerSum()
{
    let sumP=0.0, sumS=0.0;
    for(let i=0; i<8; i++)
    {
        let idPriceIV = 'id_services_set-'+ i.toString() +'-priceIV';
        let idPriceSom = 'id_services_set-'+ i.toString() +'-priceSom';
        let idSumPriceIV = 'id_services_set-'+ i.toString() +'-sumPriseIV';
        let idSumSom = 'id_services_set-'+ i.toString() +'-sumSom';
        let idStatus = 'id_services_set-'+ i.toString() +'-status';
        let idCount = 'id_services_set-'+ i.toString() +'-count';

        let sumPriceIV = document.getElementById(idSumPriceIV);
        let sumSom = document.getElementById(idSumSom);
        let status = document.getElementById(idStatus);
        let countV = document.getElementById(idCount).value;
        let priceIV = document.getElementById(idPriceIV).value;
        let priceSom = document.getElementById(idPriceSom).value;

        priceIV = priceIV.replace(',','.');
        priceSom = priceSom.replace(',','.');
        countV = countV.replace(',','.');
        if(countV && priceIV && sumPriceIV)
            sumPriceIV.value = parseFloat(countV)*parseFloat(priceIV);
        else
            sumPriceIV.value = '0.0';

        if(countV && priceSom && sumSom) {
            sumSom.value = parseFloat(countV) * parseFloat(priceSom);
        }
        else {
            sumSom.value = '0.0';
        }
        if (sumSom && sumSom.value  && sumPriceIV && sumPriceIV.value) {
            if (status.checked)
                sumS = sumS + parseFloat(sumSom.value);
            else
                sumP = sumP + parseFloat(sumPriceIV.value);
        }
    }
    document.getElementById('id_remainder').value= sumP;
    document.getElementById('id_paid').value = sumS;
}

$('#id_route').on('change', function() { jsFunction(); })

function jsFunction()
{
    const val = document.getElementById('id_route').value;

    let v = parseInt(document.querySelector("#id_productp_set-TOTAL_FORMS").value);

    for(let j=0; j<v; j++) {
        const element = document.getElementById('id_productp_set-' + j.toString() + '-bag_number');
        if (element)
        if(element.parentElement.parentElement.parentElement.style.display !== 'none')
        {
            element.value=0;
        }
    }
    CounterBagNumber();

    if(val) {
        $.ajax({
            type: 'POST',
            url: url2,
            data: {'route_id': val},
            success: function (response) {
                document.getElementById('currency_recipient').value = response['currency_name'];
                document.getElementById('currency_Som').value = response['currency'];

                let currency_Som = parseFloat(response['currency']);

                for(let i=0; i<8; i++)
                {
                    let id_priceIV = 'id_services_set-' + i.toString() + '-priceIV';
                    let id_priceSom = 'id_services_set-' + i.toString() +'-priceSom';
                    let price = parseFloat(response['Services'][i]);
                    let el_priceIV = document.getElementById(id_priceIV);
                    let el_priceSom = document.getElementById(id_priceSom);

                    if(el_priceIV && el_priceSom) {
                        el_priceIV.value = price;
                        el_priceSom.value = (currency_Som * price).toFixed(2);
                    }
                }
                ControllerSum();
            },
            error: function (response) {
                // alert the error if any error occured
                console.log(response["error"]);
            }
        })
    }
    else{
        for(let i=0; i<8; i++)
        {
            let id_priceIV = 'id_services_set-' + i.toString() + '-priceIV';
            let id_priceSom = 'id_services_set-' + i.toString() +'-priceSom';

            let el_priceIV = document.getElementById(id_priceIV);
            let el_priceSom = document.getElementById(id_priceSom);

            if(el_priceIV && el_priceSom) {
                el_priceIV.value = 0.0;
                el_priceSom.value = 0.0;
            }
        }
        ControllerSum();
    }

}


function onblurBagNumber(id){
    const bagNVal = document.getElementById(id).value;
    const route_ID = document.getElementById('id_route').value;
    if(bagNVal && route_ID) {
        $.ajax({
            type: 'POST',
            url: url,
            data: {'routeID': route_ID, 'val': bagNVal},
            success: function (response) {
                if(response['answer'])
                {
                    alert('Такой номер сумки уже существует!');
                    document.getElementById(id).value=0;
                }
            },
            error: function (response) {
                // alert the error if any error occured
                console.log(response["error"]);
            }
        })
    }
    CounterBagNumber();
}

function CounterBagNumber(){
    let x = document.getElementById('id_productp_set-TOTAL_FORMS').value;
    const arr = [];
    for(let i=0; i<x; i++)
    {
        let name = 'id_productp_set-'+ i.toString() +'-bag_number';
        let element = document.getElementById(name);
        if (element != null && element.value) {
            if(element.parentElement.parentElement.parentElement.style.display !== 'none')
                if(element.value && element.value > 0)
                    if(!arr.includes(element.value))
                        arr.push(element.value);
        }
    }

    jQuery('#p_bag_number_count').text(arr.length);
    jQuery('#id_bag_number_count').val(arr.length);
    jQuery('#id_services_set-1-count').val(arr.length);
    ControllerSum();
}

function CounterCount()
{
    let x = document.getElementById('id_productp_set-TOTAL_FORMS').value;

    let sum=0;

    for(let i=0; i<=x; i++)
    {
        let name = 'id_productp_set-'+ i.toString() +'-count';
        let element = document.getElementById(name);
        if (element && element.value)
            if(element.parentElement.parentElement.parentElement.style.display !== 'none')
                sum = sum + parseInt(element.value);
    }

    jQuery('#p_count_sum').text(sum);
    jQuery('#id_count_sum').val(sum);

}
function CounterWeight()
{
    let x = document.getElementById('id_productp_set-TOTAL_FORMS').value;
    let sum=0;
    for(let i=0; i<=x; i++)
    {
        let name = 'id_productp_set-' + i.toString() + '-weight';
        let element = document.getElementById(name);
        if (element && element.value)
            if(element.parentElement.parentElement.parentElement.style.display !== 'none')
                sum = sum + parseInt(element.value);
    }
    jQuery('#p_weight_sum').text(sum);
    jQuery('#id_weight_sum').val(sum);
    jQuery('#id_services_set-0-count').val(sum);
    ControllerSum();
}

function EventPriceIV(id){
    let id_priceSom = id.replace('priceIV', 'priceSom');
    let priceIVV = document.getElementById(id).value;
    let el_priceSom = document.getElementById(id_priceSom);
    let currency_SomV = document.getElementById('currency_Som').value;
    currency_SomV = currency_SomV.replace(',','.');
    priceIVV = priceIVV.replace(',','.');
    if(priceIVV && currency_SomV)
        el_priceSom.value = parseFloat(priceIVV)*parseFloat(currency_SomV);
    else
        el_priceSom.value = '0.0';
    ControllerSum();
}

function EventPriceSom(id){
    let id_priceIV = id.replace('priceSom', 'priceIV');
    let priceSomV = document.getElementById(id).value;
    let el_priceIV = document.getElementById(id_priceIV);
    let currency_SomV = document.getElementById('currency_Som').value;
    currency_SomV = currency_SomV.replace(',','.');
    priceSomV = priceSomV.replace(',','.');
    if(priceSomV && currency_SomV)
        el_priceIV.value = parseFloat(priceSomV)/parseFloat(currency_SomV);
    else
        el_priceIV.value = '0.0';
    ControllerSum();
}

function checkingNumberBags(){
    let pogruzka = parseInt(document.getElementById('id_services_set-1-count').value);
    let sum = 0;
    for(let i=3; i<7; i++)
    {
        let id_count = 'id_services_set-'+ i.toString() + '-count';
        let countV = document.getElementById(id_count).value;
        countV = parseFloat(countV.replace(',','.'));
        sum += countV;
    }

    sum===pogruzka? $("#id_submit_but").click() : document.getElementById('id_error').textContent= 'КОЛИЧЕСТВО МЕШКОВ НЕ СОВПАДАЕТ!!!';
}

function SetLastBagNumber(){
    let lp = parseInt(document.querySelector("#id_productp_set-TOTAL_FORMS").value);
    let val=0;
    //let index = null;

    for(let j=lp-1; j>=0; j--) {
        const element = document.getElementById('id_productp_set-' + j.toString() + '-bag_number');
        if (element)
        if(element.parentElement.parentElement.parentElement.style.display !== 'none')
        {
            if(element.value<=0) val=0;
            else val = parseInt(element.value) + 1;
           // index = j;
            break;
        }
    }
    if(val)
    {
        $("#product_add_form").click();
        document.getElementById('id_productp_set-'+ lp.toString() +'-bag_number').value = val;
        onblurBagNumber('id_productp_set-'+ lp.toString() +'-bag_number');
        CounterBagNumber();

    }
    else alert('Номер сумки не указан');
}

function SetLastProduct(){
    let v = parseInt(document.querySelector("#id_productp_set-TOTAL_FORMS").value);

    let prefix = 0;

    for(let j=v-1; j>=0; j--) {
        const element = document.getElementById('id_productp_set-' + j.toString() + '-bag_number');
        if (element)
        if(element.parentElement.parentElement.parentElement.style.display !== 'none')
        {
            prefix = j;
            break;
        }
    }

    let bag_numberV = document.getElementById('id_productp_set-'+ prefix.toString() +'-bag_number').value;
    let productV = parseInt(document.getElementById('id_productp_set-'+ prefix.toString() +'-product').value);

    if(bag_numberV<=0) alert('Номер сумки не указан');
    else if(bag_numberV && productV)
    {
        $("#product_add_form").click();
        document.getElementById('id_productp_set-' + (v).toString() + '-bag_number').value = parseInt(bag_numberV) + 1;
        document.getElementById('id_productp_set-' + (v).toString() + '-product').value = productV;
        onblurBagNumber('id_productp_set-'+ v.toString() +'-bag_number');
        CounterBagNumber();
    }
    else if(bag_numberV) alert('Товар не выбран');
    else if(productV) alert('Номер сумки не указан');
    else alert('Товар и номер сумки не указан');
}


function DuplicateLastBagNumber(){
    let lp = parseInt(document.querySelector("#id_productp_set-TOTAL_FORMS").value);
    let val=0;

    for(let j=lp-1; j>=0; j--) {
        const element = document.getElementById('id_productp_set-' + j.toString() + '-bag_number');
        if (element)
        {
            if(element.value<=0) val=0;
            else val = parseInt(element.value);
            break;
        }
    }

    if(val)
    {
        $("#product_add_form").click();
        document.getElementById('id_productp_set-'+ lp.toString() +'-bag_number').value = val;
        CounterBagNumber();
    }
    else alert('Номер сумки не указан');
}
