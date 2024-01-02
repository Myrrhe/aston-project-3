const previewAnswerId = '#preview-answer';
const buttonWriteId = '#button-write';
const writeAnswerId = '#write-answer';
const buttonPreviewId = '#button-preview';
const forumLinkSelectedClass = 'forum-link-selected';
const dNoneClass = 'd-none';

$('#content').on('change', function () {
    const converter = new window.showdown.Converter();
    const markdownTextSanitized = $(this).val()
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    $(previewAnswerId).html(converter.makeHtml(markdownTextSanitized));
});


$(buttonWriteId).on('click', function () {
    if ($(writeAnswerId).hasClass(dNoneClass)) {
        $(writeAnswerId).removeClass(dNoneClass);
    }
    if (!$(previewAnswerId).hasClass(dNoneClass)) {
        $(previewAnswerId).addClass(dNoneClass);
    }
    if (!$(buttonWriteId).hasClass(forumLinkSelectedClass)) {
        $(buttonWriteId).addClass(forumLinkSelectedClass);
    }
    if ($(buttonPreviewId).hasClass(forumLinkSelectedClass)) {
        $(buttonPreviewId).removeClass(forumLinkSelectedClass);
    }
});

$('#button-preview').on('click', function () {
    if (!$(writeAnswerId).hasClass(dNoneClass)) {
        $(writeAnswerId).addClass(dNoneClass);
    }
    if ($(previewAnswerId).hasClass(dNoneClass)) {
        $(previewAnswerId).removeClass(dNoneClass);
    }
    if ($(buttonWriteId).hasClass(forumLinkSelectedClass)) {
        $(buttonWriteId).removeClass(forumLinkSelectedClass);
    }
    if (!$(buttonPreviewId).hasClass(forumLinkSelectedClass)) {
        $(buttonPreviewId).addClass(forumLinkSelectedClass);
    }
});
