$(document).on('click', '#add-button', function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: '{% url "bag-add" %}',
        data: {
            product_id: $('#add-button').val(),
            product_quantity: $('#select option:selected').text(),
            csrfmiddlewaretoken: "{{ csrf_token }}",
            action: 'post'
        },
        success: function (json) {
            console.log(json)
        },
        error: function (xhr, errmsg, err) {

        }

    });
})