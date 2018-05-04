(function ($) {
    /* globals jQuery, window, console, NProgress */
    'use strict';
    $(document).on("click", ".jsQuantityDecrease", function () {
        var quantity = $(this).parent().find('input[name="add_qty"]').val();
        quantity = quantity * 1;
        var newQuantity = quantity - 1;
        $(this).parent().find('input[name="add_qty"]').attr('value', newQuantity);
        if (newQuantity < 2) {
            $(this).parent().find(".jsQuantityDecrease").addClass("disabled");
        } else {
            $(this).parent().find(".jsQuantityDecrease").removeClass("disabled");
        }
    }),

        $(document).on("click", ".jsQuantityIncrease", function () {
            var quantity = $(this).parent().find('input[name="add_qty"]').val();
            quantity = quantity * 1;
            var newQuantity = quantity + 1
            $(this).parent().find('input[name="add_qty"]').attr('value', newQuantity)
            if (newQuantity >= 2) {
                $(this).parent().find(".jsQuantityDecrease").removeClass("disabled");
            } else {
                $(this).parent().find(".jsQuantityDecrease").addClass("disabled");
            }

        })
    $(document).ready(function () {
        $('#plus_them').click(function (e) {
            e.preventDefault();
            var quantity = parseInt($('#count_product').val());
            $('#count_product').val(quantity + 1);

        });
        $('#moins_them').click(function (e) {
            e.preventDefault();
            var quantity = parseInt($('#count_product').val());
            if (quantity > 0) {
                $('#count_product').val(quantity - 1);
            }
        });
        // slide Home
        $('.owl-home').owlCarousel({
            autoplayHoverPause: false,
            autoplay: true,
            loop: true,
            nav: true,
            dots: false,
            items: 1,
            rtl: true,
            animateIn: 'animated fadeIn',
            navText: ["", "<svg class='icon  icon--arrowLeft'><use href='/shabaka_website/static/src/img/sprite/sprite.svg#arrowLeft'></use></svg>"],
            mouseDrag: false,
            touchDrag: false,
            margin: 0,
            smartSpeed: 150
        });
        // slide Book
        $('.owl-book').owlCarousel({
            autoplayHoverPause: false,
            autoplay: true,
            loop: true,
            nav: false,
            dots: false,
            items: 5,
            rtl: false,
            center: true,
            margin: 70,
            slideBy: 5,
            responsive: {
                0: {
                    items: 1
                },
                800: {
                    items: 2
                },
                1000: {
                    items: 3
                },
                1480: {
                    items: 5
                }
            }
        });
        // slide offer
        $('.owl-offer').owlCarousel({
            autoplayHoverPause: true,
            autoplay: true,
            loop: true,
            nav: true,
            dots: false,
            items: 4,
            rtl: true,
            navText: ["<svg class='icon  icon--arrowLeft'><use href='/shabaka_website/static/src/img/sprite/sprite.svg#arrowLeft'></use></svg>", "<svg class='icon  icon--arrowLeft'><use href='/shabaka_website/static/src/img/sprite/sprite.svg#arrowLeft'></use></svg>"],
            margin: 40,
            responsive: {
                0: {
                    items: 1
                },
                320: {
                    items: 2
                },
                960: {
                    items: 3
                },
                1480: {
                    items: 4
                }
            }
        });
        // popup
        $('#videoBox').VideoPopUp({
            backgroundColor: "#fff",
            opener: "OpenVideo",
            maxweight: "340",
            idvideo: "videOne"
        });
        // rate
        $(".rate").rateYo({
            rating: 3.2,
            rtl: true
        });


        // Tabs
        $('ul.tabs li a').click(function () {
            $('li a').removeClass("is-active");
            $(this).addClass("is-active");
        });
        $('ul.tabs--filled li a').click(function () {
            $('li a').removeClass("is-active");
            $(this).addClass("is-active");
        });

        $('ul.tab_ajax li a').click(function () {
            $('li a').removeClass("is-active");
            $(this).addClass("is-active");
        });


        $("ul.tab_ajax li a").click(function (event) {
            var link = $(this).attr("marker");
            $('.store .content').removeClass('is-active-content');
            $(link).addClass('is-active-content');
        });


        // Marker
        $('ul.marker li:first').addClass('activeMark');
        $(".tabs li a").click(function (event) {
            var link = $(this).attr("marker");
            var target = '#' + link;
            $('ul.marker li').removeClass('activeMark');
            $(target).addClass('activeMark');
        });
        // events
        $("ul.tabs--filled li a").click(function (event) {
            var link = $(this).attr("marker");
            $('.event .content').removeClass('is-active-content');
            $(link).addClass('is-active-content');
        });
        //cart
        $(".Card-delete").click(function (event) {
            var del = $(this).parent().parent().parent();
            del.hide();
        });
        // like Button
        $('.is-like input[type=checkbox]').change(function () {
            $(this).parent().toggleClass('is-checked');
        });
        // wow
        var wow = new WOW({
            boxClass: 'wow',
            animateClass: 'animated',
            offset: 0,
            mobile: true,
            live: true,
            callback: function (box) {
            }
        });
        wow.init();
        // masonry
        $('.grid').masonry({
            itemSelector: '.grid-item',
            isResizable: true,
            isRTL: true,
            originLeft: false,
            gutter: 20,
            // fitWidth: true
        });
        // tilt
        $('.grid-item, .Card--offer').tilt({
            perspective: 1000,
            easing: "cubic-bezier(.03,.98,.52,.99)",
        });

        const tilt = $('.Card--offer-two').tilt();
        // Destroy instance
        tilt.tilt.destroy.call(tilt);

        $('.Card--offer-two .Card-header').tilt({
            glare: true,
            perspective: 1000,
            easing: "cubic-bezier(.03,.98,.52,.99)",
        });

        $('.owl-book .Card-header, .owl-home .Card-header img, .product .Card-header img,.card--news .Card-header,.Card--long .Card-header,.card--product .Card-header').tilt({
            perspective: 1000,
            easing: "cubic-bezier(.03,.98,.52,.99)",
            glare: true
        });
        // Math Height
        $('.equal-offer,.equal-product,.equal-news,.equal-long').matchHeight({
            byRow: true,
            property: 'height',
            target: null,
            remove: false
        });
        // select
        $('.select').select2({
            width: '100%',
            dir: "rtl"
        });
        // dropdown
        $('ul li.dropdown').click(function (e) {
            $(this).toggleClass("hover");
        });
        $('ul li a.search,#search .is-close').click(function (e) {
            $("#search").toggleClass("is-open");
        });
        // okay
        var navigation = $('#nav-main').okayNav();
        $(window).on('load', function () {
            var navigation = $('#nav-main').okayNav();
            setTimeout(function () {
                NProgress.done();
            }, 2000);
            $('.equal-offer,.equal-product,.equal-news,.equal-long').matchHeight({
                byRow: true,
                property: 'height',
                target: null,
                remove: false
            });
        });
        $(window).on('resize', function () {
            var navigation = $('#nav-main').okayNav();
            $('.equal-offer,.equal-product,.equal-news,.equal-long').matchHeight({
                byRow: true,
                property: 'height',
                target: null,
                remove: false
            });
        });
        // END --------------------
    });

}(jQuery));


// ---------------------
// Java Script

// input number cart
var count = 1;
var countEl = document.getElementById("count");

function plus() {
    count++;
    countEl.value = count;
}

function minus() {
    if (count > 1) {
        count--;
        countEl.value = count;
    }
}