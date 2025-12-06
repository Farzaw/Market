function SetListName(id){
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

    let val = document.getElementById(id).value;
    if(val) {
        $.ajax({
            type: 'POST',
            url: url,
            data: {'category_id': val},
            success: function (response) {
                let listName = response['listName'];

                let nameId = id.replace('category', 'name');
                let nameEl = document.getElementById(nameId);

                if (nameEl) {
                    let length = nameEl.options.length;
                    for (let i = length - 1; i >= 0; i--)
                        nameEl.options[i] = null;

                    let option = document.createElement("option");
                    option.text = '';
                    option.value = '';
                    nameEl.add(option);

                    for (let i = 0; i < listName.length; i++) {
                        let option = document.createElement("option");
                        option.text = listName[i]['listNameTitle'];
                        option.value = listName[i]["listNameID"];
                        nameEl.add(option);
                    }
                }

            },
            error: function (response) {
                // alert the error if any error occured
                console.log(response["error"]);
            }
        })
    }
    else{
        let nameId = id.replace('category', 'name');
        let nameEl = document.getElementById(nameId);

        if (nameEl) {
            let length = nameEl.options.length;
            for (let i = length - 1; i >= 0; i--)
                nameEl.options[i] = null;
        }

    }
}

function controllerSumWarehouse()
{

    let form_total = document.getElementById('id_warehouseoperationinner_set-TOTAL_FORMS').value;

    let total_sum = 0.0

    for(let i=0; i<form_total; i++){
        let id_sum = 'id_warehouseoperationinner_set-' + i.toString() + '-sum';

        let sum = document.getElementById(id_sum);

        if(sum && sum.value)
            if (sum.parentNode.parentNode.parentNode.style.display !== "none") {
                total_sum += parseFloat(sum.value.replace(',','.'));
            }
    }
    document.getElementById('id_sum').value = total_sum;
}

window.onload = function() {
    controllerSumWarehouse();
};
