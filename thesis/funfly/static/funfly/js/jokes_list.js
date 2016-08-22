/**
 * Created by alexandrurustin on 7/26/16.
 */
/**
 * Created by alexandrurustin on 7/26/16.
 */


var orderByDate = 'Default';
var orderByLikes = 'Default';
var orderByDislikes = 'Default';
var jokeCategory = 'Any';

var data = {
    joke_category: jokeCategory,
    date_orderBy: orderByDate,
    likes_orderBy: orderByLikes,
    dislikes_orderBy: orderByDislikes
};

function sendRequest() {


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
    var likes_orderby_selector = '#likes_orderby';
    var dislikes_orderby_selector = '#dislikes_orderby';

    $(date_orderby_selector + ' li').on('click', function () {
        $(date_orderby_selector).find('.selected').removeClass('selected');
        $(this).addClass('selected');
        data['date_orderBy'] = $(this).children(':first').data('sort');
        sendRequest();

    });

    $(likes_orderby_selector + ' li').on('click', function () {
        $(likes_orderby_selector).find('.selected').removeClass('selected');
        $(this).addClass('selected');
        data['likes_orderBy'] = $(this).children(':first').data('sort');
        sendRequest();

    });

    $(dislikes_orderby_selector + ' li').on('click', function () {
        $(dislikes_orderby_selector).find('.selected').removeClass('selected');
        $(this).addClass('selected');
        data['dislikes_orderBy'] = $(this).children(':first').data('sort');
        sendRequest();

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

        data_received = {
            "item_id": item_id,
            "item_type": item_type
        };
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                "data": JSON.stringify(data_received)
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

    $(document).on('click', '.like_item', function () {
        item_id = $(this).attr("data-item-id");
        item_type = $(this).attr("data-item-type");

        $("#likes").toggleClass('text-primary');
        $(this).toggleClass('text-primary');

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
                'data': JSON.stringify(data_sent)
            },
            dataType: "json",
            success: function (data) {
                $('#likes_number_'+ item_id).html(data['likes']);
                $("#likes_user_list_" + item_id).html("");
                data['likes_list'].forEach(function (item) {
                    $("#likes_user_list_" + item_id).append("<li class='list-group-item'>" + item['username'] + "</li>");
                });
                if (data["message"] == "You disliked this")
                {
                    swal('Alright, ',
                        'You removed your like!',
                        'success')
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


    $("#filter_sort_form").on('submit', function (e) {
        current_page = $('.endless_page_current > strong:nth-child(1)').text();
        // url = window.location.href + '?page=' + current_page + '&querystring_key=page'
        data['joke_category'] = $('.selectpicker').val();
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

