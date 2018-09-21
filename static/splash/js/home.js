$(document).ready(function () {
    $('#feedback_modal').modal('hide');
    var host_name = window.location.hostname;
    var host_port = window.location.port;
    feedback_url = "http://" + host_name + ':' + host_port + '/splash/api/feedback/';
    // Handle sma form data when submit is clicked
    $('#feedback_form').on('submit', function (event) {
        event.preventDefault();
        handleFeebackForm()
    });

    function handleFeebackForm() {
        d3.json(feedback_url, {
            method: "POST",
            body: JSON.stringify({
                service: $('[name="service"]').val(),
                food: $('[name="food"]').val(),
                atmosphere: $('[name="atmosphere"]').val(),
                comment: $('[name="comment"]').val(),
            }),
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-type": "application/json; charset=UTF-8"
            }
        }).then(function (data) {
            console.log(data['message']);
            if (data['message'] === 'Success') {
                $("#feedback_form").trigger("reset");
                $('#feedback_modal').modal('show');
            } else {

            }
        });
    }

    // Get CSRF token from cookie
    function getCSRFToken() {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, 10) == ('csrftoken' + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(10));
                    break;
                }
            }
        }
        return cookieValue;
    }
});