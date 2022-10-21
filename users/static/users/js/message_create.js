
let elemtnts = document.querySelectorAll("input[type='text']")
for (var i = 0; i < elemtnts.length; ++i) {
    elemtnts[i].addEventListener('change', function(e) {
        this.parentNode.classList.add('has-success');
    });
}

let selects = document.querySelectorAll("select")
for (var x = 0; x < selects.length; ++x) {
    selects[x].addEventListener('blur', function(e) {
        this.parentNode.classList.add('has-success');
    });
}
var house = $('#id_message_address_house_id');
var section = $('#id_message_address_section_id');
var floor = $('#id_message_address_floor_id');
var flat = $('#id_message_address_flat_id');
var empty_value = "<option value='all'>Всем...</option>";

function get_sections_floors_flats () {
    section.empty().append(empty_value)
    floor.empty().append(empty_value)
    flat.empty().append(empty_value)
    if (house.val() !== "all") {
        $.ajax({
            url: UrlGetSectionsFloorsFlats,
            type: 'GET',
            data: {
                'house': house.val()
            },
            success: (data) => {
                $(data.section).each(function (index, value) {
                    section.append("<option value='"+value.id+"'>"+value.title + "</option>");
                })
                $(data.floor).each(function (index, value) {
                    floor.append("<option value='"+value.id+"'>"+value.title + "</option>");
                })
                $(data.flat).each(function (index, value) {
                    flat.append("<option value='"+value.id+"'>№"+value.title + "</option>");
                })
            }
        })
    }
}

function get_flats_by_section () {
    flat.empty().append(empty_value)
    if (section.val() !== 'all') {
        $.ajax({
            url: UrlGetFlatsBySection,
            type: 'GET',
            data: {
                'section': section.val(),
                'floor': floor.val()
            },
            success: (data) => {
                $(data.flat).each(function (index, value) {
                    flat.append("<option value='"+value.id+"'>№"+value.title + "</option>");
                })
            }
        })
    }
}

$(document).ready(function () {
    house.on('change', get_sections_floors_flats);
    section.on('change', get_flats_by_section);
    floor.on('change', get_flats_by_section);
})

// AJAX
