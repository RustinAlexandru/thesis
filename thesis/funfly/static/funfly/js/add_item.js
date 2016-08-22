/**
 * Created by alexandrurustin on 7/9/16.
 */

$(document).ready(function () {

    var page_href = window.location.href;

    $('[data-toggle="tooltip"]').tooltip();

    var dropdown_item_type = $('#id_item_type');
    if (dropdown_item_type.val() == 'Ninegag') {
        $("#div_id_text_area").hide();
        $("#div_id_source_url label").removeClass('requiredField');
        if ($("#div_id_source_url .asteriskField").length == 1) {
            $("#div_id_source_url .asteriskField").remove();
        }
    }


    $('#id_item_type').on('change', function () {
        if (this.value == 'Video') {
            $("#div_id_text_area").hide();
            $("#div_id_media_file").hide();

            $("#div_id_source_url label").addClass('requiredField');
            if ($("#div_id_source_url .asteriskField").length == 0) {
                $("#div_id_source_url label").append("<span class='asteriskField'>*</span>");
            }
        }
        else if (this.value == 'Joke') {
            $("#div_id_title").hide();
            $("#div_id_text_area").show();
            $("#div_id_media_file").hide();
            $("#div_id_source_url label").removeClass('requiredField');
            if ($("#div_id_source_url .asteriskField").length == 1) {
                $("#div_id_source_url .asteriskField").remove();
            }
        }
        else  //Ninegag
        {
            $("#div_id_text_area").hide();
            $("#div_id_media_file").show();
            $("#div_id_source_url label").removeClass('requiredField');
            if ($("#div_id_source_url .asteriskField").length == 1) {
                $("#div_id_source_url .asteriskField").remove();
            }
        }
    });

});