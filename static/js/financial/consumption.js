function controllerSum_count(id){

    let count = document.getElementById(id).value;
    count = parseFloat(count.replace(',','.'));

    let id_price = id.replace('count','price');
    let price = document.getElementById(id_price).value;
    price = parseFloat(price.replace(',','.'));

    let id_sum = id.replace('count','sum');
    let sum_el = document.getElementById(id_sum);

    if(count && price)
        sum_el.value = (count * price).toFixed(2);
    else
        sum_el.value = 0.0;
    Set_total();
}

function controllerSum_price(id){

    let price = document.getElementById(id).value;
    price = parseFloat(price.replace(',','.'));

    let id_count = id.replace('price', 'count');
    let count = document.getElementById(id_count).value;
    count = parseFloat(count.replace(',','.'));

    let id_sum = id.replace('price', 'sum');
    let sum_el = document.getElementById(id_sum);

    if(count && price)
        sum_el.value = (count * price).toFixed(2);
    else
        sum_el.value = '0.0';

    Set_total();
}

function Set_total()
{
    let form_total = document.getElementById('id_operationsinner_set-TOTAL_FORMS').value;

    let total_count = 0.0
    let total_sum = 0.0
    for(let i=0; i<form_total; i++){
        let id_count = 'id_operationsinner_set-' + i.toString() + '-count';
        let id_sum = 'id_operationsinner_set-' + i.toString() + '-sum';


        let count = document.getElementById(id_count);

        if (count && count.value)
            if (count.parentNode.parentNode.parentNode.style.display !== "none") {
                total_count += parseFloat(count.value.replace(',','.'));
            }

        let sum = document.getElementById(id_sum);

        if(sum && sum.value)
            if (sum.parentNode.parentNode.parentNode.style.display !== "none") {
                total_sum += parseFloat(sum.value.replace(',','.'));
            }
    }
    document.getElementById('count_total').value = total_count;
    document.getElementById('id_sum').value = total_sum;
}
window.onload = function() {
    Set_total();
};