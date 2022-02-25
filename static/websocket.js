var username = {{ username }};
alert("In websocket.js")

    var chatSocket = new ReconnectingWebSocket(
        'ws://'
        + window.location.host
        + '/ws/'
	);

	chatSocket.onmessage = function(e){
		var data = JSON.parse(e.data);
		if (data['command'] === 'messages'){
			// alert("onmessage -> command=messages");
			for (let i=0; i<data['messages'].length; i++){
				createMessage(data['messages'][i]);
			}
		}
		else if (data['command'] === 'new_message'){
			createMessage(data['message']);
		}
	};

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#chat-message-input').onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#chat-message-submit').click();
        }
    };

    document.querySelector('#chat-message-submit').onclick = function(e) {
        var messageInputDom = document.querySelector('#chat-message-input');
		var message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
			'command': 'new_message',
			'message': message,
			'sender': username,
			'receiver': selected_contact
		}));
		messageInputDom.value = '';
	};

	function fetchMessages(){
		chatSocket.send(JSON.stringify({
			'command': 'fetch_messages'
		}));
	}

	function createMessage(data){
		var sender = data['sender'];
		var receiver = data['receiver']

		if (((sender==username)||(sender==selected_contact)) && ((receiver==username)||(receiver==selected_contact))){
			var msgListTag = document.createElement('li');
			var imgTag = document.createElement('img');
			var pTag = document.createElement('p');
			pTag.textContent = data.message;
			if (sender == username){
				msgListTag.className = 'sent';
				var userAvatar = "{{ user.avatar }}";
				// To remove added amp; which is done automatically by URLAction
				userAvatar = userAvatar.replaceAll("&amp;", "&");
				imgTag.src = userAvatar;
			}
			else{
				msgListTag.className = 'replies';
				imgTag.src = selected_contact_avatar;
			}
			msgListTag.appendChild(imgTag);
			msgListTag.appendChild(pTag);
			document.querySelector('#chat-log').appendChild(msgListTag);

			// To scroll to the bottom of the page when a message is created
			const message_div = document.querySelector('.messages')
			message_div.scrollTop = message_div.scrollHeight
		}
    };