"use strict";

$("#save-cookies-settings").on("click", function () {
    setOneCookie("theme_save", $("#switch-cookie-theme-page").prop("checked") ? "1" : "0");
    setOneCookie("lang_save", $("#switch-cookie-lang-page").prop("checked") ? "1" : "0");
    if (getOneCookie("theme_save") != "1") {
        setOneCookie("theme", "");
    }
    if (getOneCookie("lang_save") != "1") {
        setOneCookie("language", "");
    }
    $(".toast").toast("show");
});
