$(document).ready(function () {
    //var params = getSearchParameters();

    //var base_grant_url = decodeURIComponent(params.base_grant_url);
    console.log("Page ready");


    // Handle sma form data when submit is clicked
    $('#login_form').on('submit', function (event) {
        event.preventDefault();
        handleLoginForm();
    });

    function handleLoginForm() {
        d3.json('http://127.0.0.1:8000/splash/api/login/', {
            method: "POST",
            body: JSON.stringify({
                email: $('#email').val(),
                name: $('#name').val(),
            }),
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-type": "application/json; charset=UTF-8"
            }
        }).then(function (data) {

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

    function getSearchParameters() {
        var prmstr = window.location.search.substr(1);
        return prmstr != null && prmstr != "" ? transformToAssocArray(prmstr) : {};
    }

    function transformToAssocArray(prmstr) {
        var params = {};
        var prmarr = prmstr.split("&");
        for (var i = 0; i < prmarr.length; i++) {
            var tmparr = prmarr[i].split("=");
            params[tmparr[0]] = tmparr[1];
        }
        return params;
    }
});