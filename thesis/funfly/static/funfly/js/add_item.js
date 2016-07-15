/**
 * Created by alexandrurustin on 7/9/16.
 */

$(document).ready(function () {

    $('[data-toggle="tooltip"]').tooltip();
    
    var dropdown_item_type = $('#id_item_type');
    if (dropdown_item_type.val() == 'Ninegag') {
        $("#div_id_text_area").hide();
    }


    $('#id_item_type').on('change', function () {
        if (this.value == 'Video') {
            $("#div_id_text_area").hide();
            $("#div_id_media_file").hide();
        }
        else if (this.value == 'Joke') {
            $("#div_id_text_area").show();
            $("#div_id_media_file").hide();
        }
        else  //Ninegag
        {
            $("#div_id_text_area").hide();
            $("#div_id_media_file").show();
        }
    });

    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
    });

    $('[data-toggle="tooltip"]').click(function() {
        item_id = $(this).attr("data-item-id");
        item_type = $(this).attr("data-item-type");
        url = $("this").attr("href");
        data_received = {
                "item_id": item_id,
                "item_type": item_type
            };

        $.ajax({
            type: 'POST',
            url: '',
            data: {
                "data": JSON.stringify(data_received)
            },
            dataType: "json",
            success: function (data) {
                alert(data.plm);
                alert("Works");
            },
            error: function(data) {
                alert("Something went wrong!");
            }
        });
    });

});


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
