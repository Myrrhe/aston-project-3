const idBlockEmail = '#block-email';
const idFormEmail = '#form-email';
const idBlockPassword = '#block-password';
const idFormPassword = '#form-password';

$('#button-email').on('click', function () {
    if (!$(idBlockEmail).hasClass('d-none')) {
        $(idBlockEmail).addClass('d-none');
    }
    if ($(idFormEmail).hasClass('d-none')) {
        $(idFormEmail).removeClass('d-none');
    }
});

$('#cancel-email').on('click', function () {
    if ($(idBlockEmail).hasClass('d-none')) {
        $(idBlockEmail).removeClass('d-none');
    }
    if (!$(idFormEmail).hasClass('d-none')) {
        $(idFormEmail).addClass('d-none');
    }
});

$('#button-password').on('click', function () {
    if (!$(idBlockPassword).hasClass('d-none')) {
        $(idBlockPassword).addClass('d-none');
    }
    if ($(idFormPassword).hasClass('d-none')) {
        $(idFormPassword).removeClass('d-none');
    }
});

$('#cancel-password').on('click', function () {
    if ($(idBlockPassword).hasClass('d-none')) {
        $(idBlockPassword).removeClass('d-none');
    }
    if (!$(idFormPassword).hasClass('d-none')) {
        $(idFormPassword).addClass('d-none');
    }
});
