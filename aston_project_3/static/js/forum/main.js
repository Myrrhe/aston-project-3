"use strict";

const templateURL = $("#link-section").attr("href");

function getCurrentURL() {
    return templateURL.replace("PLACEHOLDER_TYPE", $("#section-select option").val());
}

function updateURL() {
    $("#link-section").attr("href", getCurrentURL());
}

$("#section-select").on("change", function () {
    updateURL();
});

updateURL();
