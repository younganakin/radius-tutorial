$(document).ready(function () {
    $('#payment_modal').modal('hide');
    $('#payment_form').on('submit', function (event) {
        var ws4redis = WS4Redis({
            uri: 'ws://localhost:8000/ws/foobar?subscribe-broadcast&publish-broadcast&echo',
            connecting: on_connecting,
            connected: on_connected,
            receive_message: receiveMessage,
            disconnected: on_disconnected,
            heartbeat_msg: null
        });

        function on_connecting() {
            console.log('Websocket is connecting...');
        }

        function on_connected() {
            console.log("Connection has been established.")
        }

        function sendMessage() {
            ws4redis.send_message('A message');
        }

        function on_disconnected(evt) {
            console.log('Websocket was disconnected: ' + JSON.stringify(evt));
        }

        // receive a message though the websocket from the server
        function receiveMessage(msg) {
            $("#payment_modal_body > p").text(msg);
            $('#payment_modal').modal('show');
        }
    });
});