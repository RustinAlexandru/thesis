/**
 * Created by alexandrurustin on 7/18/16.
 */

var data = {};

$(document).ready(function () {

    $('[data-toggle="tooltip"]').tooltip();

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('.delete_item').click(function () {

        item_id = $(this).attr("data-item-id");
        item_type = $(this).attr("data-item-type");
        data_received = {
            "item_id": item_id,
            "item_type": item_type
        };
        var self = this;

        $.ajax({
            type: 'POST',
            url: '',
            data: {
                "data": JSON.stringify(data_received)
            },
            dataType: "html",
            success: function (data) {
                swal(
                    'Alright!',
                    'You deleted the item from your personal save list!',
                    'success'
                );

                $(self).tooltip('hide');

                $('#delete_item_' + item_id).remove();

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

    $("#filter_sort_form").on('submit', function (e) {
        // current_page = $('.endless_page_current > strong:nth-child(1)').text();
        // url = window.location.href + '?page=' + current_page + '&querystring_key=page'
        data['itemType'] = $('.selectpicker').val();
            $.ajax({
                url: '',
                type: 'GET',
                data: data,
                success: function (data) {
                    $(".saved_items_container").html(data)
                },
                error: function (err) {
                    console.log('err: ' + err);
                }
            });
            e.preventDefault();
        });

    $("#filter_sort_form").on('change', "[data-input]", function () {
        $("#filter_sort_form").submit()
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

