function controllerSum()
{
    let form_total = document.getElementById('id_operationsinner_set-TOTAL_FORMS').value;
    let total_sum = 0.0

    for(let i=0; i<form_total; i++){
        let id_sum = 'id_operationsinner_set-' + i.toString() + '-sum';

        let sum = document.getElementById(id_sum);

        if(sum && sum.value)
            if (sum.parentNode.parentNode.parentNode.style.display !== "none") {
                total_sum += parseFloat(sum.value.replace(',','.'));
            }
    }
    document.getElementById('id_sum').value = total_sum;
}
