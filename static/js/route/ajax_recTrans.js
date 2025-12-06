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

        document.getElementById('button_search2').addEventListener('click', function() {

            let race = document.getElementById('raceId').value;
            let recipient = document.getElementById('recipientId').value;
            let sender = document.getElementById('senderId').value;
            let dateFrom = document.getElementById('dateFrom').value;
            let dateTo = document.getElementById('dateTo').value;
            let registration = document.getElementById('registrationId').value;

            let data = {
                "race": race,
                "recipient": recipient,
                "sender": sender,
                "dateFrom": dateFrom,
                "dateTo": dateTo,
                "registration": registration,
            };

            $.ajax({
                type: 'POST',
                url: url2,
                data: data,
                dataType: 'json',
                success: function (response)
                {
                    let div_answer = document.getElementById('div_answer2');
                    if(response.found)
                        div_answer.innerHTML = "(Мест - "+response.count+") (Вес - "+response.weight+")";
                    else
                        div_answer.innerHTML = "Ничего не найдено!";
                    return false;
                },
                error: function (response) {
                    console.log("error");
                }
            });
        })
        document.getElementById('button_search').addEventListener('click', function() {
            let bag_N = document.getElementById('bag_N').value;
            let routeForSearch = document.getElementById('routeForSearch').value;

            let data = {
                "bag_N": bag_N,
                "routeForSearch": routeForSearch,
            };

            $.ajax({
                type: 'POST',
                url: url1,
                data: data,
                dataType: 'json',
                success: function (response)
                {
                    if(response.answer) {

                        console.log(response.RecTransID);
                        let div = document.createElement('div');
                        const str = 'Номер Документа: <b id="RTIDsearch"> </b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp'+
                            '<a href="RecTransCont/' + parseInt(response.RecTransID) + '">Просмотр</a>'+
                            '&nbsp;&nbsp;&nbsp;&nbsp;'+
                            '<a href="update_RecTran/' + parseInt(response.RecTransID) + '">Редактировать</a>';

                        div.class = "col-sm-6";
                        div.innerHTML = str;

                        let div_answer = document.getElementById('div_answer');
                        div_answer.innerHTML = "";
                        div_answer.append(div);

                        const RTIDsearch = document.getElementById('RTIDsearch');
                        RTIDsearch.textContent = response.RecTransID;
                    }
                    else
                    {
                        let div = document.createElement('div');
                        const str = '<p> Ничего не найдено! </p>';

                        div.class = "col-sm-6";
                        div.innerHTML = str;

                        let div_answer = document.getElementById('div_answer');
                        div_answer.innerHTML = "";
                        div_answer.append(div);

                    }
                    return false;
                },
                error: function (response) {
                    console.log("error");
                }
            });
        })
    });