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
    // var all_link = $('#menu-sidebar a')
    // var current = location.href
    // var current_list = location.href.split('/')
    // console.log(current_list)
    // console.log(current)
    //
    // all_link.each(function () {
    //     var link_list = this.href.split('/')
    //     var link = $(this)
    //     if (link_list[3] === current_list[3] && link_list[4] === current_list[4]) {
    //         link.addClass('active')
    //     }
    // })
    // console.log(all_link)
    var current = $('#link-id').val()
    $(`#${current}`).addClass('active')
    console.log(current)
})