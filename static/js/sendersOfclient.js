$("#id_sender_form").submit(function (e) {
    e.preventDefault();

    var serializedData = $(this).serialize();
    $.ajax({
        type: 'POST',
        url: urlSender,
        data: serializedData,
        success: function (response) {
            $('#modal-lg').modal('hide');
            let total = document.getElementById('id_client_sender-TOTAL_FORMS').value;
            for(let prefix=0; prefix<total; prefix++){
                let el = document.getElementById('id_client_sender-' + prefix.toString() + '-sender');
                if(el){
                    let opt = document.createElement('option');
                    opt.value = response['pk'];
                    opt.text = response['fullname'];
                    el.appendChild(opt);
                }
            }
            alert('Отправитель успешно добавлен.');
        },
        error: function (response) {

            if("responseJSON" in response && "error" in response["responseJSON"])
            {
            if("fullname" in response["responseJSON"]["error"])
            {
                document.getElementById('id_fullname_error').textContent =
                    response["responseJSON"]["error"]["fullname"];
            }}
            else{
                alert("Произошла ошибка!!!");
            }

        }
    })
});

function load_senders(){
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
    $.ajax({
        type: 'POST',
        url: url2,
        data: {},
        success: function (response) {
            let senders = response['senders'];
            let last_prefix = document.getElementById('id_client_sender-TOTAL_FORMS').value - 1;

            let el = document.getElementById('id_client_sender-' + last_prefix.toString() + '-sender');

            if(el){
                let vals = [];
                for(let i=0; i<el.options.length; i++)
                    if(el.options[i].value)
                        vals.push(el.options[i].value);
                for(let i=0; i<senders.length; i++)
                {
                    if(!(vals.includes(senders[i]['pk'].toString())))
                    {
                        let opt = document.createElement('option');
                        opt.value = senders[i]['pk'];
                        opt.text = senders[i]['fullname'];
                        el.appendChild(opt);
                    }
                }
            }

        },
        error: function (response) {
            // alert the error if any error occured
            console.log(response["error"]);
        }
    })

}

