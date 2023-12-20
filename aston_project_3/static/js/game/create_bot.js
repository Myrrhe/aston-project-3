"use strict";

$(document).ready(function() {
    $('#button-duplicate').click(function(event) {
        event.preventDefault();
        const csrfTokenElement = $('#form-toggle-publish [name="csrfmiddlewaretoken"]');
        const button = $(this);
        $.ajax({
            url: $(this).attr("data-url"),
            type: 'POST',
            dataType: 'json',
            data: {
                csrfmiddlewaretoken: csrfTokenElement.val(),
                "toggle_publish_bot_form-bot_id": $(this).attr("data-bot-id"),
                toggle_publish_bot_form: "toggle_publish_bot"
            },
            success: function(data) {
                if (data.posted) {
                    button.val(button.attr("data-message-published"));
                } else {
                    button.val(button.attr("data-message-unpublished"));
                }
            },
            error: function(error) {
                console.log('Une erreur s\'est produite:', error);
            },
        });
    });
});
