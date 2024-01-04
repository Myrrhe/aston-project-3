// COOKIES

const getOneCookie = function(cname) {
    const name = cname + '=';
    const decodedCookie = decodeURIComponent(document.cookie);
    const ca = decodedCookie.split(';');
    for (const value of ca) {
        const c = value.trim();
        if (c.startsWith(name)) {
            return c.substring(name.length, c.length);
        }
    }
    return '';
};

const checkOneCookie = function(cname) {
    return getOneCookie(cname) !== '';
};

const setOneCookie = function(cname, cvalue, exdays = 365) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    document.cookie = `${cname}=${cvalue};expires=${d.toUTCString()};path=/;SameSite=Strict`;
};

// THEME

const nightButtonId = '#night-button';
const lightModeName = 'light-mode';
const numberThemes = 3;

const getButtonTheme = function() {
    if ($(nightButtonId).hasClass('dark')) {
        return '0';
    } else if ($(nightButtonId).hasClass('light')) {
        return '1';
    } else {
        return '2';
    }
};

const setButtonTheme = function(theme) {
    if ($(nightButtonId).hasClass('dark')) {
        $(nightButtonId).removeClass('dark');
    }
    if ($(nightButtonId).hasClass('light')) {
        $(nightButtonId).removeClass('light');
    }
    if ($(nightButtonId).hasClass('lightdark')) {
        $(nightButtonId).removeClass('lightdark');
    }
    if (theme === '0') {
        $(nightButtonId).addClass('dark');
    } else if (theme === '1') {
        $(nightButtonId).addClass('light');
    } else {
        $(nightButtonId).addClass('lightdark');
    }
};

const switchButtonTheme = function() {
    setButtonTheme(((parseInt(getButtonTheme(), 10) + 1) % numberThemes).toString());
};

const getOsTheme = function() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
};

const updateTheme = function() {
    if ($('body').hasClass('dark-mode')) {
        $('body').removeClass('dark-mode');
    }
    if ($('body').hasClass(lightModeName)) {
        $('body').removeClass(lightModeName);
    }
    let theme;
    if (checkOneCookie('theme')) {
        theme = getOneCookie('theme');
    } else {
        theme = getButtonTheme();
    }
    if (theme === '0' || (theme === '2' && getOsTheme())) {
        $('body').addClass('dark-mode');
    } else {
        $('body').addClass(lightModeName);
    }
};

// LANGUAGE

const getSelectLanguage = function() {
    return $('#language-select').val();
};

const setSelectLanguage = function(language) {
    $('#language-select').val(language);
};

// MODAL COOKIES

$('.button-cookie').on('click', function () {
    if ($(this).attr('id') === 'button_cookie_required') {
        setOneCookie('theme_save', '0');
        setOneCookie('lang_save', '0');
    } else if ($(this).attr('id') === 'button_cookie_accept_all') {
        setOneCookie('theme_save', '1');
        setOneCookie('lang_save', '1');
    } else {
        // Nothing to do here
    }
});

$('.switch-cookie').change(function () {
    switch ($(this).attr('id')) {
        case 'switch-cookie-theme':
            if ($(this).prop('checked')) {
                setOneCookie('theme_save', '1');
            } else {
                setOneCookie('theme_save', '0');
            }
            break;
        case 'switch-cookie-lang':
            if ($(this).prop('checked')) {
                setOneCookie('lang_save', '1');
            } else {
                setOneCookie('lang_save', '0');
            }
            break;
        default:
            break;
    }
});

// NIGHT BUTTON

$(nightButtonId).on('click', function () {
    switchButtonTheme();
    if (checkOneCookie('theme_save') && getOneCookie('theme_save') === '1') {
        setOneCookie('theme', getButtonTheme());
    }
    updateTheme();
});

// SELECT LANGUAGE

// $('#language-select').on('change', function () {
//     if (checkOneCookie('lang_save') && getOneCookie('lang_save') === '1') {
//         setOneCookie('language', getSelectLanguage());
//     }
//     // location.reload();
// });

$('#submit-language').on('click', function () {
    if (checkOneCookie('lang_save') && getOneCookie('lang_save') === '1') {
        setOneCookie('language', getSelectLanguage());
    }
});

// COUNTRY FLAG

const aCharacterIndexMinusUTF16A = 127397;

const getFlagEmoji = function(countryCode) {
    const codePoints = countryCode
        .toUpperCase()
        .split('')
        .map(char => aCharacterIndexMinusUTF16A + char.charCodeAt());
    return String.fromCodePoint(...codePoints);
};

// PAGE LOAD

$(document).ready(function () {
    // Cookies
    if (!checkOneCookie('cookies_init')) {
        $('#modal_cookies').modal('show');
        setOneCookie('cookies_init', '1');
        setOneCookie('theme_save', '0');
        setOneCookie('lang_save', '0');
    }

    // Theme
    if (checkOneCookie('theme_save') && getOneCookie('theme_save') === '1') {
        if (!checkOneCookie('theme')) {
            setOneCookie('theme', '2');
        }
        setButtonTheme(getOneCookie('theme'));
    } else {
        setOneCookie('theme', '');
        setButtonTheme('2');
    }
    updateTheme();

    // Language
    // if (checkOneCookie('lang_save') && getOneCookie('lang_save') === '1') {
    //     if (!checkOneCookie('language')) {
    //         setOneCookie('language', 'fr');
    //     }
    //     setSelectLanguage(getOneCookie('language'));
    // } else {
    //     setOneCookie('language', '');
    //     setSelectLanguage('fr');
    // }

    $.each($('.option-capitalize'), function (_, value) {
        const words = value.text.split(' ');
        if (words.length > 0) {
            words[0] = words[0].charAt(0).toUpperCase() + words[0].slice(1).toLowerCase();
        }
        value.text = words.join(' ');
    });
});
