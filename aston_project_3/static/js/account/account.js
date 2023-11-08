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
