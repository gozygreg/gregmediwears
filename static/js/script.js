// // Add button
// $(document).on('click', '#add-button', function (e) {
//     e.preventDefault();
//     $.ajax({
//         type: 'POST',
//         url: '{% url "bag-add" %}',
//         data: {
//             product_id: $('#add-button').val(),
//             product_quantity: $('#select option:selected').text(),
//             csrfmiddlewaretoken: "{{ csrf_token }}",
//             action: 'post'
//         },
//         success: function (json) {
//             document.getElementById("bag-qty").textContent = json.qty;
//             document.getElementById("redirect-url").value = window.location.pathname;
//             window.location.href = '/';

//         },
//         error: function (xhr, errmsg, err) {

//         }

//     });
// })