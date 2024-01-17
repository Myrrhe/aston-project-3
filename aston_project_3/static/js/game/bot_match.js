$(document).ready(function() {
    const csrfTokenElement = $('#block-request [name="csrfmiddlewaretoken"]');
    $.ajax({
        url: $('#block-request').attr('data-url'),
        type: 'GET',
        dataType: 'json',
        success(data) {
            positions = setupMatch(data);

            triggerMatch(positions[0], positions[1]);
        },
        error(error) {
            console.log('Une erreur s\'est produite:', error);
        },
    });
});
