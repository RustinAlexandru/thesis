/**
 * Created by alexandrurustin on 7/9/16.
 */


$(document).ready(function () {

    $("body").tooltip({
        selector: '[data-toggle="tooltip"]'
    });

    page_href = window.location.href;

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $(document).on('click', '.save_item', function () {

        item_id = $(this).attr("data-item-id");
        item_type = $(this).attr("data-item-type");

        itemType = $(this).attr("data-item-type");

        url = page_href;
        if (url.indexOf("page") !== -1) { //  url contains 'page' in it, needs adjustment
            // get_params_pos= url.indexOf("?")  // insert 'add_to_savelist' before get parameters
            if (url.indexOf("ninegags") !== -1) {
                url = url.replace("/ninegags/", "/ninegags/add_to_savelist/");
            } else if (url.indexOf("videos") !== -1) {
                url = url.replace("/videos/", "/videos/add_to_savelist/");
            } else if (url.indexOf("jokes") !== -1) {
                url = url.replace("/jokes/", "/videos/add_to_savelist/");
            }
        } else {
            url = page_href + 'add_to_savelist/'; // first page in a paginated list, url doesnt contain 'page' in it
        }

        data_sent = {
            "item_id": item_id,
            "item_type": item_type
        };
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                "data": JSON.stringify(data_sent)
            },
            dataType: "json",
            success: function (data) {
                if (!data["integrity_error"]) {
                    swal(
                        'Good job!',
                        'You added the item to your personal save list!',
                        'success'
                    )
                }
                else {  // integrity_error message alert
                    sweetAlert(
                        'Oops...',
                        "We're sorry, you've already added this item, you cannot add the same item twice!",
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

    $(document).on('click', '.like_button_wrap', function () {
        item_id = $(this).attr("data-item-id");
        item_type = $(this).attr("data-item-type");


        url = page_href;
        if (url.indexOf("page") !== -1) { //  url contains 'page' in it, needs adjustment
            // get_params_pos= url.indexOf("?")  // insert 'add_to_savelist' before get parameters
            if (url.indexOf("ninegags") !== -1) {
                url = url.replace("/ninegags/", "/ninegags/like/");
            } else if (url.indexOf("videos") !== -1) {
                url = url.replace("/videos/", "/videos/like/");
            } else if (url.indexOf("jokes") !== -1) {
                url = url.replace("/jokes/", "/videos/like/");
            }
        } else {
            url = page_href + 'like/'; // first page in a paginated list, url doesnt contain 'page' in it
        }

        data_sent = {
            "item_id": item_id,
            "item_type": item_type
        };
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                "data": JSON.stringify(data_sent)
            },
            dataType: "json",
            success: function (data) {
                if (data["integrity_error"]) {
                    sweetAlert(
                        'Oops...',
                        "We're sorry, you've already added this item, you cannot add the same item twice!",
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

    $(document).on('click', '.add_point', function () {
        item_id = $(this).attr("data-item-id");
        item_type = $(this).attr("data-item-type");

        $("#likes").toggleClass('text-primary');
        $(this).toggleClass('text-primary');

        url = page_href;
        if (url.indexOf("page") !== -1) { //  url contains 'page' in it, needs adjustment
            // get_params_pos= url.indexOf("?")  // insert 'add_to_savelist' before get parameters
            if (url.indexOf("ninegags") !== -1) {
                url = url.replace("/ninegags/", "/ninegags/add_point/");
            } else if (url.indexOf("videos") !== -1) {
                url = url.replace("/videos/", "/videos/add_point/");
            } else if (url.indexOf("jokes") !== -1) {
                url = url.replace("/jokes/", "/videos/add_point/");
            }
        } else {
            url = page_href + 'add_point/'; // first page in a paginated list, url doesnt contain 'page' in it
        }

        data_sent = {
            "item_id": item_id,
            "item_type": item_type
        };
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'data': JSON.stringify(data_sent)
            },
            dataType: "json",
            success: function (data) {
                $('#points').html(data['points']);
                selector = "i[data-item-id=" + item_id + "]";
                add_point_button = $(selector).parents()[0];
                $('.add_point').tooltip('hide');
                add_point_button.remove();
                button = 'button' + item_id;
                sessionStorage.setItem(button, "deleted")


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


    function hideAddPointButtons() {
        $.each(sessionStorage, function (key, value) {

            key_string = key;
            if (key_string.startsWith("button") && value == 'deleted') {
                var numberPattern = /\d+/g;
                id = key.match(numberPattern);
                selector = "i[data-item-id=" + id + "]";
                if (add_point_button = $(selector).parents()[0]) {
                    add_point_button.remove()
                }
            }

            $.each($('.add_point'), function () {
                $(this).removeClass('hidden');
            })

        });
    }

    hideAddPointButtons();


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

