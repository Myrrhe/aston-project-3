"use strict";

$("#button-email").on("click", function () {
    if (!$("#block-email").hasClass("d-none")) {
        $("#block-email").addClass("d-none");
    }
    if ($("#form-email").hasClass("d-none")) {
        $("#form-email").removeClass("d-none");
    }
});

$("#cancel-email").on("click", function () {
    if ($("#block-email").hasClass("d-none")) {
        $("#block-email").removeClass("d-none");
    }
    if (!$("#form-email").hasClass("d-none")) {
        $("#form-email").addClass("d-none");
    }
});

$("#button-password").on("click", function () {
    if (!$("#block-password").hasClass("d-none")) {
        $("#block-password").addClass("d-none");
    }
    if ($("#form-password").hasClass("d-none")) {
        $("#form-password").removeClass("d-none");
    }
});

$("#cancel-password").on("click", function () {
    if ($("#block-password").hasClass("d-none")) {
        $("#block-password").removeClass("d-none");
    }
    if (!$("#form-password").hasClass("d-none")) {
        $("#form-password").addClass("d-none");
    }
});
