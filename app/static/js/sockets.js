$(document).ready(function(){
    namespace = '/test'; // change to an empty string to use the global namespace

    // the socket.io documentation recommends sending an explicit package upon connection
    // this is specially important when using the global namespace
    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    // socket.on('connect', function() {
    //     socket.emit('my event', {data: 'I\'m connected!'});
    // });
    
    // event handler for server sent data
    // the data is displayed in the "Received" section of the page
    socket.on('my response', function(msg) {
        $('#messages').append(msg.data);
        //$('#messages').attr('scrollTop', $('#messages').attr('scrollHeight'));
        $('#message').val('');
        $("#messages").animate({ scrollTop: $("#messages")[0].scrollHeight}, 1000);
    });

    socket.emit('join', {room: $('#channelName').text()});

    // handlers for the different forms in the page
    // these send data to the server in a variety of ways
    $('form#messageForm').submit(function(event) {
        var message = $.trim($('#message').val());
        if (message != '') {
            socket.emit('my event', 
                {data: message,
                room: $('#channelName').text()});
        }
        
        return false;
    });

    $('#btnClear').bind('click', function() {
            $('#messages').html('');
            return false;
        });
    $('#leave').bind('click', function(event) {
        socket.emit('leave', {room: $('#channelName').text()});
        window.location.href = '/main';
        //return false;
    });

});
