"use strict";

$("#button-trigger-answer").on("click", function () {
    if ($("#block-anwer").hasClass("d-none")) {
        $("#block-anwer").removeClass("d-none");
    }
    if ($("#block-anwer").hasClass("opacity-0")) {
        $("#block-anwer").removeClass("opacity-0");
    }
});

$("#button-close-answer").on("click", function () {
    if (!$("#block-anwer").hasClass("d-none")) {
        $("#block-anwer").addClass("d-none");
    }
    if (!$("#block-anwer").hasClass("opacity-0")) {
        $("#block-anwer").addClass("opacity-0");
    }
});

$("#content").on("change", function () {
    const converter = new showdown.Converter();
    const markdownText = $(this).val();
    const markdownTextSanitized = markdownText
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
