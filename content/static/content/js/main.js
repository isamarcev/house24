$(document).ready(function(){
    $('.slider').slick({
        // autoplay: true,
        autoplaySpeed: 3000,
        dots: true,
        prevArrow: '<i class="fas fa-chevron-circle-left fa-3x slick-prev"></i>',
        nextArrow: '<i class="fas fa-chevron-circle-right fa-3x slick-next"></i>'
    });
});


$(function () {
    var all_link = $('#navbarScroll a')
    var current_list = location.href.split('/')
    all_link.each(function () {
        var link_list = this.href.split('/')
        var link = $(this)
        if (link_list[3] === current_list[3]) {
            link.addClass('active-link')
        }
    })
})
