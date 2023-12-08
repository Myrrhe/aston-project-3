"use strict";


$("#content").on("change", function () {
    const converter = new showdown.Converter();
    const markdownTextSanitized = $(this).val()
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
    $("#preview-answer").html(converter.makeHtml(markdownTextSanitized));
});


$("#button-write").on("click", function () {
    if ($("#write-answer").hasClass("d-none")) {
        $("#write-answer").removeClass("d-none");
    }
    if (!$("#preview-answer").hasClass("d-none")) {
        $("#preview-answer").addClass("d-none");
    }
    if (!$("#button-write").hasClass("forum-link-selected")) {
        $("#button-write").addClass("forum-link-selected");
    }
    if ($("#button-preview").hasClass("forum-link-selected")) {
        $("#button-preview").removeClass("forum-link-selected");
    }
});

$("#button-preview").on("click", function () {
    if (!$("#write-answer").hasClass("d-none")) {
        $("#write-answer").addClass("d-none");
    }
    if ($("#preview-answer").hasClass("d-none")) {
        $("#preview-answer").removeClass("d-none");
    }
    if ($("#button-write").hasClass("forum-link-selected")) {
        $("#button-write").removeClass("forum-link-selected");
    }
    if (!$("#button-preview").hasClass("forum-link-selected")) {
        $("#button-preview").addClass("forum-link-selected");
    }
});
