"use strict";

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

$(document).ready(function () {
    if (!checkOneCookie("cookies_init")) {
        $("#modal_cookies").modal('show');
        setOneCookie("cookies_init", "1");
        setOneCookie("theme_save", "0");
        setOneCookie("lang_save", "0");
    }
});

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
