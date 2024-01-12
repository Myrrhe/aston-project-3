$(document).ready(function() {
    const blockOutputId = '#block-output';

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

                const lenMatch = Math.min(len1, len2);

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

                // Logging
                $(blockOutputId).empty();
                if ($(blockOutputId).hasClass('d-none')) {
                    $(blockOutputId).removeClass('d-none');
                }

                const firstErrPlayer1 = data['stderr'][0].shift();
                const firstErrPlayer2 = data['stderr'][1].shift();

                let startWrite = false;

                if (firstErrPlayer1.length > 0 || firstErrPlayer2.length) {
                    const blockOneOutput = $('<div></div>');

                    const blockRound = $(`<div class='text-color-fore pb-2 fw-bold fs-6'>0/${lenMatch}</div>`);
                    blockRound.appendTo(blockOneOutput);

                    // 1
                    const blocStderr1 = $('<div class=\'pb-1\'></div>');

                    const errorTitlePlayer1 = $('<div class=\'text-color-bright fw-bold\'>Sortie d\'erreur :</div>');
                    errorTitlePlayer1.appendTo(blocStderr1);

                    const blocStderrContent1 = $('<div class=\'text-color-alert\'></div>');
                    if (firstErrPlayer1.length > 0) {
                        for (const err of firstErrPlayer1) {
                            if (err !== null) {
                                const lineError = $(`<div class='output-line'>${err}</div>`);
                                lineError.appendTo(blocStderrContent1);
                            }
                        }
                    }

                    blocStderrContent1.appendTo(blocStderr1);
                    blocStderr1.appendTo(blockOneOutput);

                    // 2
                    const blocStderr2 = $('<div class=\'pb-1\'></div>');

                    const errorTitlePlayer2 = $('<div class=\'text-color-bright-alt fw-bold\'>Sortie d\'erreur :</div>');
                    errorTitlePlayer2.appendTo(blocStderr2);

                    const blocStderrContent2 = $('<div class=\'text-color-alert\'></div>');
                    if (firstErrPlayer2.length > 0) {
                        for (const err of firstErrPlayer2) {
                            if (err !== null) {
                                const lineError = $(`<div class='output-line'>${err}</div>`);
                                lineError.appendTo(blocStderrContent2);
                            }
                        }
                    }

                    blocStderrContent2.appendTo(blocStderr2);
                    blocStderr2.appendTo(blockOneOutput);

                    blockOneOutput.appendTo(blockOutputId);

                    startWrite = true;
                }

                for (let i = 0; i < lenMatch; i++) {
                    const blockOneOutput = $('<div></div>');

                    if (startWrite) {
                        const separatorLine = $('<hr class=\'hr\' />');
                        separatorLine.appendTo(blockOneOutput);
                    }

                    const blockRound = $(`<div class='text-color-fore pb-2 fw-bold fs-6'>${i + 1}/${lenMatch}</div>`);
                    blockRound.appendTo(blockOneOutput);

                    // 1
                    const blockPlayer1 = $('<div class=\'pb-1\'></div>');
                    const blocStderr1 = $('<div class=\'pb-1\'></div>');

                    const errorTitlePlayer1 = $('<div class=\'text-color-bright fw-bold\'>Sortie d\'erreur :</div>');
                    errorTitlePlayer1.appendTo(blocStderr1);

                    const blocStderrContent1 = $('<div class=\'text-color-alert\'></div>');
                    if (i < data['stderr'][0].length) {
                        for (const err of data['stderr'][0][i]) {
                            if (err !== null) {
                                const lineError = $(`<div class='output-line'>${err}</div>`);
                                lineError.appendTo(blocStderrContent1);
                            }
                        }
                    }

                    blocStderrContent1.appendTo(blocStderr1);
                    blocStderr1.appendTo(blockPlayer1);

                    const blocStdout1 = $('<div class=\'pb-1\'></div>');
                    const outputTitlePlayer1 = $('<div class=\'text-color-bright fw-bold\'>Sortie standard :</div>');
                    outputTitlePlayer1.appendTo(blocStdout1);

                    const lineOutputPlayer1 = $(`<div class='text-color-fore output-line'>${data['stdout'][0][i]}</div>`);
                    lineOutputPlayer1.appendTo(blocStdout1);

                    blocStdout1.appendTo(blockPlayer1);

                    blockPlayer1.appendTo(blockOneOutput);

                    // 2
                    const blockPlayer2 = $('<div class=\'pb-1\'></div>');
                    const blocStderr2 = $('<div class=\'pb-1\'></div>');

                    const errorTitlePlayer2 = $('<div class=\'text-color-bright-alt fw-bold\'>Sortie d\'erreur :</div>');
                    errorTitlePlayer2.appendTo(blocStderr2);

                    const blocStderrContent2 = $('<div class=\'text-color-alert\'></div>');
                    if (i < data['stderr'][1].length) {
                        for (const err of data['stderr'][1][i]) {
                            if (err !== null) {
                                const lineError = $(`<div class='output-line'>${err}</div>`);
                                lineError.appendTo(blocStderrContent2);
                            }
                        }
                    }

                    blocStderrContent2.appendTo(blocStderr2);
                    blocStderr2.appendTo(blockPlayer2);

                    const blocStdout2 = $('<div class=\'pb-1\'></div>');
                    const outputTitlePlayer2 = $('<div class=\'text-color-bright-alt fw-bold\'>Sortie standard :</div>');
                    outputTitlePlayer2.appendTo(blocStdout2);

                    const lineOutputPlayer2 = $(`<div class='text-color-fore output-line'>${data['stdout'][1][i]}</div>`);
                    lineOutputPlayer2.appendTo(blocStdout2);

                    blocStdout2.appendTo(blockPlayer2);

                    blockPlayer2.appendTo(blockOneOutput);

                    blockOneOutput.appendTo(blockOutputId);

                    startWrite = true;
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
