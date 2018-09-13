$(document).ready(function () {
    $('#register_form').on('submit', function (event) {
        event.preventDefault();
        initiateSTKPush();
    });

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