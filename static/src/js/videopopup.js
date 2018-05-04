/*
 * Author: Sławomir Netteria.NET https://netteria.net
 */
(function ($) {

    $.fn.VideoPopUp = function (options) {
        var defaults = {
            // backgroundColor: "#000000",
            opener: "video",
            maxweight: "640",
            pausevideo: false,
            idvideo: ""
        };

        var patter = this.attr('id');

        var settings = $.extend({}, defaults, options);

        var video = document.getElementById(settings.idvideo);

        function stopVideo() {
            video.pause();
            video.currentTime = 0;
        }

        $('#' + patter + '').css("display", "none");
        $('#' + patter + '').append('<div id="VideoFill"></div>');

        $('#VideoFill').css("background", settings.backgroundColor);
        $('#' + patter + '').css("z-index", "100001");
        $('#' + patter + '').css("position", "fixed");
        $('#' + patter + '').css("top", "0");
        $('#' + patter + '').css("bottom", "0");
        $('#' + patter + '').css("right", "0");
        $('#' + patter + '').css("left", "0");
        $('#' + patter + '').css("padding", "auto");
        $('#' + patter + '').css("text-align", "center");
        $('#' + patter + '').css("background", "none");
        $('#' + patter + '').css("vertical-align", "vertical-align");

        $("#videCont").css("z-index", "100002");
        $('#' + patter + '').append('<div id="videoBoxCloser"> <svg class="icon icon--close"><use href="/shabaka_website/static/src/img/sprite/sprite.svg#close"></use></svg></div>');
        $("#" + settings.opener + "").on('click', function () {
            $('#' + patter + "").show();
            $('#' + settings.idvideo + '').trigger('play');
        });
        $("#videoBoxCloser").on('click', function () {
            if (settings.pausevideo == true) {
                $('#' + settings.idvideo + '').trigger('pause');
            } else {
                stopVideo();
            }
            $('#' + patter + "").hide();
        });
        return this.css({});
    };

}(jQuery));