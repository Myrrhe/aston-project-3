"use strict";

// COOKIES

function getOneCookie(cname) {
    const name = cname + "=";
    const decodedCookie = decodeURIComponent(document.cookie);
    const ca = decodedCookie.split(";");
    for (let i = 0; i < ca.length; i++) {
        const c = ca[i].trim();
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function checkOneCookie(cname) {
    return getOneCookie(cname) !== "";
}

function setOneCookie(cname, cvalue, exdays = 365) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    let expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

// THEME

function getButtonTheme() {
    if ($("#night-button").hasClass("dark")) {
        return 0;
    } else if ($("#night-button").hasClass("light")) {
        return 1;
    } else {
        return 2;
    }
}

function setButtonTheme(theme) {
    if ($("#night-button").hasClass("dark")) {
        $("#night-button").removeClass("dark");
    }
    if ($("#night-button").hasClass("light")) {
        $("#night-button").removeClass("light");
    }
    if ($("#night-button").hasClass("lightdark")) {
        $("#night-button").removeClass("lightdark");
    }
    if (theme == 0) {
        $("#night-button").addClass("dark");
    } else if (theme == 1) {
        $("#night-button").addClass("light");
    } else {
        $("#night-button").addClass("lightdark");
    }
}

function switchButtonTheme() {
    setButtonTheme((getButtonTheme() + 1) % 3)
}

function getOsTheme() {
    return window.matchMedia("(prefers-color-scheme: dark)").matches;
}

function updateTheme() {
    if ($("body").hasClass("dark-mode")) {
        $("body").removeClass("dark-mode");
    }
    if ($("body").hasClass("light-mode")) {
        $("body").removeClass("light-mode");
    }
    let theme = 0;
    if (checkOneCookie("theme")) {
        theme = getOneCookie("theme");
    } else {
        theme = getButtonTheme();
    }
    if (theme == 0 || (theme == 2 && getOsTheme())) {
        $("body").addClass("dark-mode");
    } else {
        $("body").addClass("light-mode");
    }
}

// LANGUAGE

function getSelectLanguage() {
    return $("#language-select").val();
}

function setSelectLanguage(language) {
    $("#language-select").val(language);
}

// MODAL COOKIES

$(".button-cookie").on("click", function () {
    if ($(this).attr("id") === "button_cookie_required") {
        setOneCookie("theme_save", "0");
        setOneCookie("lang_save", "0");
    } else if ($(this).attr("id") === "button_cookie_accept_all") {
        setOneCookie("theme_save", "1");
        setOneCookie("lang_save", "1");
    } else {

    }
});

$(".switch-cookie").change(function () {
    switch ($(this).attr("id")) {
        case "switch-cookie-theme":
            setOneCookie("theme_save", $(this).prop("checked") ? "1" : "0")
            break;
        case "switch-cookie-lang":
            setOneCookie("lang_save", $(this).prop("checked") ? "1" : "0")
            break;
        default:
            break;
    }
});

// NIGHT BUTTON

$("#night-button").on("click", function () {
    switchButtonTheme();
    if (checkOneCookie("theme_save") && getOneCookie("theme_save") == "1") {
        setOneCookie("theme", getButtonTheme());
    }
    updateTheme();
});

// SELECT LANGUAGE

// $("#language-select").on("change", function () {
//     if (checkOneCookie("lang_save") && getOneCookie("lang_save") == "1") {
//         setOneCookie("language", getSelectLanguage());
//     }
//     // location.reload();
// });

$("#submit-language").on("click", function () {
    if (checkOneCookie("lang_save") && getOneCookie("lang_save") == "1") {
        setOneCookie("language", getSelectLanguage());
    }
});

// COUNTRY FLAG

function getFlagEmoji(countryCode) {
    const codePoints = countryCode
        .toUpperCase()
        .split("")
        .map(char => 127397 + char.charCodeAt());
    return String.fromCodePoint(...codePoints);
}

// PAGE LOAD

$(document).ready(function () {
    // Cookies
    if (!checkOneCookie("cookies_init")) {
        $("#modal_cookies").modal('show');
        setOneCookie("cookies_init", "1");
        setOneCookie("theme_save", "0");
        setOneCookie("lang_save", "0");
    }

    // Theme
    if (checkOneCookie("theme_save") && getOneCookie("theme_save") == "1") {
        if (!checkOneCookie("theme")) {
            setOneCookie("theme", "2");
        }
        setButtonTheme(getOneCookie("theme"));
    } else {
        setOneCookie("theme", "");
        setButtonTheme("2");
    }
    updateTheme();

    // Language
    // if (checkOneCookie("lang_save") && getOneCookie("lang_save") == "1") {
    //     if (!checkOneCookie("language")) {
    //         setOneCookie("language", "fr");
    //     }
    //     setSelectLanguage(getOneCookie("language"));
    // } else {
    //     setOneCookie("language", "");
    //     setSelectLanguage("fr");
    // }

    $.each($(".option-capitalize"), function (_, value) {
        const words = value.text.split(" ");
        if (words.length > 0) {
            words[0] = words[0].charAt(0).toUpperCase() + words[0].slice(1).toLowerCase();
        }
        value.text = words.join(" ");
    });
});
