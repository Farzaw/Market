$( document ).ready(function() {
    SetArticle();
});

function SetArticle() {
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

    let typeOper = $('#id_type').val();
    console.log("typeOper ", typeOper);

    let articleElm = $('#id_article');
    articleElm.find('option').remove();

    if(typeOper === "1" || typeOper === "2")
    {
        $.ajax({
            type: 'POST',
            url: url,
            data: {'typeO': typeOper},
            success: function (response) {
            console.log('success');

            let art = response["articles"];

            let optE = document.createElement('option');
            articleElm.append(optE);

            for(let ob of art)
            {
                let opt = document.createElement('option');
                opt.value = ob.pk;
                opt.text = ob.name
                articleElm.append(opt);
            }
            },
            error: function (response) {
                // alert the error if any error occured
                console.log(response);
            }
        })
    }
}