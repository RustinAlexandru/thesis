/**
 * Created by alexandrurustin on 7/27/16.
 */


$(document).ready(function () {


    page_href = window.location.href;

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $(document).on('click', '.follow', function () {

        profile_id = $(this).data("profile-id");

        url = page_href + 'follow/';

        data_sent = {
            "profile_id": profile_id,
        };
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                "data": JSON.stringify(data_sent)
            },
            dataType: "json",
            success: function (data) {
                if (!data["integrity_error"] && !data["self_follow_error"]) {
                    swal(
                        'Good job!',
                        'You are now following this user!',
                        'success'
                    )
                }
                else if (data["self_follow_error"]) {
                    swal(
                        'Oops..',
                        "We're sorry, you can't follow yourself. That doesn't make sense, does it?",
                        'error'
                    )
                }
                else {  // integrity_error message alert
                    sweetAlert(
                        'Oops...',
                        "We're sorry, you are already following this user!",
                        'error'
                    )
                }

            },
            error: function (data) {
                sweetAlert(
                    'Oops...',
                    'Something went wrong!',
                    'error'
                )
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

