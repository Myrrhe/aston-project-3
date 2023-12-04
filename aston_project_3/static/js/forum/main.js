"use strict";

const templateURL = $("#link-section").attr("href");

function getCurrentURL() {
    return encodeURI(templateURL.replace("PLACEHOLDER_TYPE", $("#section-select option").val()));
    const section = $("#section-select option").val();
    const page = $("#main").attr("data-page");
    const category = $("#main").attr("data-category");
}

function updateURL() {
    $("#link-section").attr("href", getCurrentURL());
}

$("#section-select").on("change", function () {
    updateURL();
});

updateURL();
