const blockAnswerId = '#block-answer';
const emptySpaceId = '#empty-space';

$('#button-trigger-answer').on('click', function () {
    if ($(blockAnswerId).hasClass('d-none')) {
        $(blockAnswerId).removeClass('d-none');
    }
    if ($(blockAnswerId).hasClass('opacity-0')) {
        $(blockAnswerId).removeClass('opacity-0');
    }
    if ($(emptySpaceId).hasClass('d-none')) {
        $(emptySpaceId).removeClass('d-none');
    }
});

$('#button-close-answer').on('click', function () {
    if (!$(blockAnswerId).hasClass('d-none')) {
        $(blockAnswerId).addClass('d-none');
    }
    if (!$(blockAnswerId).hasClass('opacity-0')) {
        $(blockAnswerId).addClass('opacity-0');
    }
    if (!$(emptySpaceId).hasClass('d-none')) {
        $(emptySpaceId).addClass('d-none');
    }
});
