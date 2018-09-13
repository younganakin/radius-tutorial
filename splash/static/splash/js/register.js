$(document).ready(function () {
    $('#register_form').on('submit', function (event) {
        event.preventDefault();
        handleRegistrationForm();
    });

    function handleRegistrationForm() {
        d3.json('http://127.0.0.1:8000/splash/api/register/', {
            method: "POST",
            body: JSON.stringify({
                uname: $('#user_name').val(),
                fname: $('#first_name').val(),
                lname: $('#last_name').val(),
                email: $('#email').val(),
                contact: $('#phone_number').val(),
            }),
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-type": "application/json; charset=UTF-8"
            }
        }).then(function (data) {
            console.log(data);
        });
    }

    /**
    function initiateSTKPush() {
        d3.json('http://pay.brandfi.co.ke:8301/api/stkpush', {
            method: "POST",
            body: JSON.stringify({
                clientId: $('#clientId').val(),
                transactionType: "CustomerPayBillOnline",
                phoneNumber: $('#phone_number').val(),
                amount: "1",
                callbackUrl: "http://pay.brandfi.co.ke/payfi-success",
                accountReference: "demo",
                transactionDesc: "Test"
            }),
            headers: {
                "Postman-Token": getCSRFToken(),
                "Content-type": "application/json",
                "Accept": "application/json",
                "Cache-Control": "no-cache",
                "mode": "no-cors"
            }
        }).then(function (data) {
            console.log(data);
        });
    }
     */

    function queryStatusOfSTKPush() {
        d3.json('http://pay.brandfi.co.ke:8301/api/stkpushquery', {
            method: "POST",
            body: JSON.stringify({
                clientId: $('#clientId').val(),
                transactionType: "CustomerPayBillOnline",
                phoneNumber: $('#phone_number').val(),
                amount: "1",
                callbackUrl: "http://pay.brandfi.co.ke/payfi-success",
                accountReference: "demo",
                transactionDesc: "Test"
            }),
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-type": "application/json",
                "Accept": "application/json",
                "Cache-Control": "no-cache"
            }
        }).then(function (data) {
            console.log(data);
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