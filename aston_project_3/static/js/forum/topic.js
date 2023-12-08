"use strict";

$("#button-trigger-answer").on("click", function () {
    if ($("#block-anwer").hasClass("d-none")) {
        $("#block-anwer").removeClass("d-none");
    }
    if ($("#block-anwer").hasClass("opacity-0")) {
        $("#block-anwer").removeClass("opacity-0");
    }
    if ($("#empty-space").hasClass("d-none")) {
        $("#empty-space").removeClass("d-none");
    }
});

$("#button-close-answer").on("click", function () {
    if (!$("#block-anwer").hasClass("d-none")) {
        $("#block-anwer").addClass("d-none");
    }
    if (!$("#block-anwer").hasClass("opacity-0")) {
        $("#block-anwer").addClass("opacity-0");
    }
    if (!$("#empty-space").hasClass("d-none")) {
        $("#empty-space").addClass("d-none");
    }
});
