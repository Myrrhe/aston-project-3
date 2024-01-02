$('#save-cookies-settings').on('click', function () {
    if ($('#switch-cookie-theme-page').prop('checked')) {
        window.setOneCookie('theme_save', '1');
    } else {
        window.setOneCookie('theme_save', '0');
    }
    if ($('#switch-cookie-lang-page').prop('checked')) {
        window.setOneCookie('lang_save', '1');
    } else {
        window.setOneCookie('lang_save', '0');
    }
    if (window.getOneCookie('theme_save') !== '1') {
        window.setOneCookie('theme', '');
    }
    if (window.getOneCookie('lang_save') !== '1') {
        window.setOneCookie('language', '');
    }
    $('.toast').toast('show');
});
