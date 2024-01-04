const getCurrentURL = function(page, category) {
    return encodeURI($(`#link-${page}-page-${category}-category`).attr('href')
        .replace('PLACEHOLDER_TYPE', $('#section-select').val()));
};

const updateURL = function() {
    $('.update-url').each((_, element) => $(element).attr('href', getCurrentURL($(element).attr('data-page'), $(element).attr('data-category'))));
};

$('#section-select').on('change', function () {
    updateURL();
});

updateURL();
