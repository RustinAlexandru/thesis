/**
 * Created by alexandrurustin on 7/27/16.
 */


var orderByDate = 'Default';
var orderByTitle = 'Default';

var data = {
    date_orderBy: orderByDate,
    title_orderBy: orderByTitle
};

function sendRequest(data) {

    $.ajax({
        url: '',
        type: 'GET',
        data: data,
        success: function (data) {
            $(".endless_page_template").html(data)
        },
        error: function (err) {
            console.log('err: ' + err);
        }
    });
}


$(document).ready(function () {

    $("body").tooltip({
        selector: '[data-toggle="tooltip"]'
    });

    var date_orderby_selector = '#date_orderby';
    var title_orderby_selector =  '#title_orderby';

    $(date_orderby_selector + ' li').on('click', function () {
        $(date_orderby_selector).find('.selected').removeClass('selected');
        $(this).addClass('selected');
        data['date_orderBy'] = $(this).children(':first').data('sort');
        sendRequest(data);

    });

    $(title_orderby_selector + ' li').on('click', function () {
        $(title_orderby_selector).find('.selected').removeClass('selected');
        $(this).addClass('selected');
        data['title_orderBy'] = $(this).children(':first').data('sort');
        sendRequest(data);

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

        data = {
            "item_id": item_id,
            "item_type": item_type
        };
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                "data": JSON.stringify(data)
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

