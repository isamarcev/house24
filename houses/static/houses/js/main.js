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
    var all_link = $('#menu-sidebar a')
    var current_list = location.href.split('/')
        if (current_list[4] === 'cabinet') {
        all_link.each(function () {
        var link_list = this.href.split('/')
        var link = $(this)
        if (link_list[5] === current_list[5]) {
            link.addClass('active')
        }
    })
    }
    var current = $('#link-id').val()
    $(`#${current}`).addClass('active')
    console.log(current)
})

$('#sidebar-overlay').click(function () {
    $('#dropleft').click()
})