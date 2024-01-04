$(document).ready(function() {
    $('#submit-edit-bot').click(function(event) {
        event.preventDefault();
        const csrfTokenElement = $('#form-create-bot [name="csrfmiddlewaretoken"]');
        $.ajax({
            url: $(this).attr('data-url'),
            type: 'POST',
            dataType: 'json',
            data: {
                csrfmiddlewaretoken: csrfTokenElement.val(),
                'create_bot_form-bot_id': $(this).attr('data-bot-id'),
                'create_bot_form-name': $('#name').val(),
                'create_bot_form-code': $('#id_create_bot_form-code').val(),
                create_bot_form: 'create_bot',
            },
            success(_data) {
            },
            error(error) {
                console.log('Une erreur s\'est produite:', error);
            },
        });
    });

    $('#button-publish').click(function(event) {
        event.preventDefault();
        const csrfTokenElement = $('#form-toggle-publish [name="csrfmiddlewaretoken"]');
        const button = $(this);
        $.ajax({
            url: $(this).attr('data-url'),
            type: 'POST',
            dataType: 'json',
            data: {
                csrfmiddlewaretoken: csrfTokenElement.val(),
                'toggle_publish_bot_form-bot_id': $(this).attr('data-bot-id'),
                toggle_publish_bot_form: 'toggle_publish_bot',
            },
            success(data) {
                const brightClass = 'button-bright';
                const darkClass = 'button-dark';
                if (data.posted) {
                    button.val(button.attr('data-message-published'));
                    if (button.hasClass(brightClass)) {
                        button.removeClass(brightClass);
                    }
                    if (!button.hasClass(darkClass)) {
                        button.addClass(darkClass);
                    }
                } else {
                    button.val(button.attr('data-message-unpublished'));
                    if (button.hasClass(darkClass)) {
                        button.removeClass(darkClass);
                    }
                    if (!button.hasClass(brightClass)) {
                        button.addClass(brightClass);
                    }
                }
            },
            error(error) {
                console.log('Une erreur s\'est produite:', error);
            },
        });
    });
});
