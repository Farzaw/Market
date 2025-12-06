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

function change_location(id_route, elem) {

    if (['Формируется', 'Отправлен', 'Прибыл'].includes(elem.value)) {
        if (confirm("Вы действительно хотите изменить статус рейса?")) {
            $.ajax({
                type: 'POST',
                url: url,
                data: {'route_id': id_route},

                success: function (response) {
                    elem.value = response["location"];
                },

                error: function (response) {
                    alert('Ошибка сервера. Не удалось выполнить запрос.');
                }
            })
        }
    }
}