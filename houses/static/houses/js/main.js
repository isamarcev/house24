var big_photo = $('.brand-link')

$('#dropleft').click(function (){
    var big_photo = $('#big-photo')
    var small_photo = $('#small-photo')
    if (big_photo.css('display') == 'none') {
        console.log('fasdfasdf')
        big_photo.css('display', 'block')
        small_photo.css('display', 'none')

    }
    else if (big_photo.css('display') == 'block'){
        big_photo.css('display', 'none')
        small_photo.css('display', 'block')

    }
    }
)

$(function () {
    var IDEAL = $('#current')
    console.log(IDEAL.val())
    // var location = window.location.href;
    // var cur_url = '/' + location.split('/').pop();
    //     console.log(location)
    // console.log(cur_url)
    // $('#menu-sidebar li').each(function () {
    //     var element = $(this).children('a')
    //     var link = element.attr('href');
    //     if (cur_url === link) {
    //         $(this).addClass('active')
    //     } else {
    //         $(this).removeClass('active')
    //     }
    // })


})