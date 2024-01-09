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
            success(data) {
                const positions = data['match_movements'].split('|').map(s =>
                    s.split(';').map(function(p) {
                        const [x, y] = p.split(',');
                        return {'x': parseInt(x, 10), 'y': parseInt(y, 10)};
                }));

                const len1 = positions[0].length;
                const len2 = positions[1].length;

                if (len1 > len2) {
                    positions[0].splice(len2 - len1);
                } else if (len2 > len1) {
                    positions[1].splice(len1 - len2);
                } else {
                    // The arrays are already the same size
                }

                if (data['match_result'] !== '') {
                    if (data['match_result']) {
                        $('#fight-result').html(`${data['bot_name']} a gagné !`);
                    } else {
                        $('#fight-result').html(`${data['bot_name']} a perdu :(`);
                    }
                }

                triggerMatch(positions[0], positions[1]);
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
