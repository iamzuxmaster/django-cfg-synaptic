var socket = io.connect();
socket.on('connect', function() {
    socket.emit('my_connect', {req_id: $('input[name="req_id"]').val()});
});
req_id = $('input[name="req_id"]').val()

function openChatModal(element){
$('#chatmessages').html("");
$("#chatModal").modal("toggle")
$("#chatModal").modal("show")
let json =  {
    req_id: req_id,
    acc_id: element.dataset.include
}
axios.post("/control/chat/all/messages/", json, {      
    headers: {"X-CSRFToken": csrfToken, 'Content-Type': 'application/json'}
}).then(response => {
    
    $(".ijKlmNo").text(`${$(".col.text-center .app-title").text()}`)
    $("input[name='room_id']").val(`${response.data.chat.id}`)
    socket.emit("join_room", {room_id:$("input[name='room_id']").val()})
    response.data.messages.forEach(message => {
    let $messages = $('#chatmessages');
    if (message.message.account.id == $('input[name="req_id"]').val()) {
        $messages.append(`<div class='bg-success mb-3 p-2 rounded' style='width:80%;margin-left:auto; color:white;'>${message.message.message}</div>`)
    } else {
        $messages.append(`<div class='bg-success mb-3 p-2 rounded' style='width:80%;margin-right:auto; color:white;'>${message.message.message}</div>`)
    }
    })
    
})
}
socket.on('joined_room', function(data) {
});

socket.on('disconnect', function() {
$('.is_online').text("Вы Офлайн");
});
socket.on('my_connect_response', function(msg) {
    $('.is_online').text("Вы Онлайн");
});

$('button#sendMessage').click(function(event) {
let inputMessage = $("textarea.messageArea")
if (inputMessage.val() != '') {
    socket.emit('sendmessage', {room_id: $('input[name="room_id"]').val(), message: $(".messageArea").val(), account_id:$('input[name="req_id"]').val() });
} 
});

socket.on("addmessage", (data)=>{
let $messages = $('#chatmessages');
let inputMessage = $("textarea.messageArea")
if (data.message.account.id == $('input[name="req_id"]').val()) {
$messages.append(`<div class='bg-success mb-3 p-2 rounded' style='width:80%;margin-left:auto; color:white;'>${data.message.message}</div>`)
} else {
$messages.append(`<div class='bg-success mb-3 p-2 rounded' style='width:80%;margin-right:auto; color:white;'>${data.message.message}</div>`)
}
inputMessage.val('')
})


$('form#emit').submit(function(event) {
    socket.emit('my_event', {data: $('#emit_data').val()});
    return false;
});
$('form#broadcast').submit(function(event) {
    socket.emit('my_broadcast_event', {data: $('#broadcast_data').val()});
    return false;
});
$('form#join').submit(function(event) {
    socket.emit('join', {room: $('#join_room').val()});
    return false;
});
$('form#leave').submit(function(event) {
    socket.emit('leave', {room: $('#leave_room').val()});
    return false;
});
$('form#send_room').submit(function(event) {
    socket.emit('my_room_event', {room: $('#room_name').val(), data: $('#room_data').val()});
    return false;
});
$('form#close').submit(function(event) {
    socket.emit('close_room', {room: $('#close_room').val()});
    return false;
});
$('form#disconnect').submit(function(event) {
    socket.emit('disconnect_request');
    return false;
});