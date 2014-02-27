var chatServerName = 'ec2-54-184-99-64.us-west-2.compute.amazonaws.com';

var chatServerBind = 'http://' + chatServerName + ':5280/http-bind';

var connectionUsername = 'agent@' + chatServerName;

var Athena = {
	connection: null,

    activeBusinessViaName : null,
    activeBusinessName: null,
    activeCollId: null,
    activeUserHandle: null,
    start_time: null,

	bindAllBusinesses: function(){
		$('.chat-business').live('click', function(){
			$('.chat-business').removeClass('selected');
			$(this).addClass('selected');
			var businessId = $(this).attr("id");
			var viaName = $(this).attr("via");
            Athena.activeBusinessViaName = viaName;
            Athena.activeBusinessName = $(this).attr("name");

            //Setting the user variables to nil
            // because once you click on a business no user is active
            Athena.activeCollId = null;
            Athena.activeUserHandle = null;
            $("#chat-area").html("");
            $.ajax({
                type: 'GET',
                url: '/collections_for_business/' + businessId + '/',
                success: function(data){
                    $("#userTable tr").remove();
                    $('#userTable tbody').append(data);
                    
                }
            })
		});
	},

    bindAllUsers: function(){
        $('.user-row').live('click', function(){
            $("#chat-area").html("");
            $('.user-row').removeClass('selected');
            $(this).addClass('selected');

            var coll_id = $(this).attr('coll_id');
            Athena.activeCollId = coll_id;
            Athena.activeUserHandle = $(this).attr('handle');
            console.log($(this).attr('handle'));
            console.log(Athena.activeUserHandle);

            $.ajax({
                type: 'GET',
                url: '/chats_by_collection/' + coll_id +'/',
                success: function(data){
                    /*$('#chat-area').append("<p>" + 
                            Athena.activeBusinessName + 
                            " is talking to " + 
                            Athena.activeUserHandle + 
                            "</p>");*/
                    $('#chat-area').append(data);
                    
                    $("#chat-messages").scrollTop($("#chat-messages")[0].scrollHeight);
                }
            })
        });
    },

    bindChatInput: function(){
        $('.chat-input').live('keypress', function(e){
            if (e.which === 13) {
                e.preventDefault();

                var body = $(this).val();
                // TODO: hard coding the user to be test. REMOVE IT
                //var jid = Athena.activeUserHandle + '@' + chatServerName;
                var jid = Athena.activeUserHandle.toLowerCase() + '@' + chatServerName;

                Athena.connection.send($msg({
                    to: jid,
                    "type": "chat",
                    "via": Athena.activeBusinessViaName
                }).c('body').t(body).up().c('subject').t(Athena.activeBusinessViaName));

                Athena.logMessage(body, false);
                $(this).parent().find('#chat-messages').append(                
                    "<p class='chat from-business'>" +
                    body +
                    "</p><div class='newline'></div>"
                );
                $(this).val('');
                $("#chat-messages").scrollTop($("#chat-messages")[0].scrollHeight);
                var $fromUser = $("tr[handle='" + Athena.activeUserHandle.toLowerCase() +"']");
                $fromUser.removeClass('unread');
            };
        })
    },

    messageReceived: function(message){
        console.log('message from user on the next line');
        console.log(message);
        var from = Strophe.getNodeFromJid($(message).attr('from'));
        //var via = $(message).attr('via');
        var via = $(message).find('subject').text();
        var body  = $(message).find('body').text();
        var $fromBusiness = $("tr[via='"+via+"']");

        // If the business is selected do user checks.
        // else show notification and update unread
        if ($fromBusiness.hasClass('selected')) {
            var $fromUser = $("tr[handle='" + from +"']");
            // if the user exists in the roster check if it is selected
            if ($fromUser.length) {
                // If the user is selected. Insert the row and 
                // to the chat place and scroll to bottom.
                if ($fromUser.hasClass('selected')) {
                    $('#chat-messages').append(
                            "<p class='chat from-user'>" +
                                    body +
                            "</p><div class='newline'></div>"
                        );
                    $("#chat-messages").scrollTop($("#chat-messages")[0].scrollHeight);
                }
                // else the user exists in the roster but is not active
                else{
                    //TODO: send alert and update user roster
                    $fromUser.prependTo($fromUser.parent());
                    $fromUser.addClass('unread');
                    $.notify(from + " just sent a message", {globalPosition: "top center", className: "success"});
                }
            }
            // Else its the first time the user has messaged the business
            else{
                $.ajax({
                    type: 'GET',
                    data: {user_name:from, via_name:via, business_handle:connectionUsername },
                    url: '/get_new_user_roster/',
                    success: function(data){
                       $.notify(from + " just sent a message", {globalPosition: "top center", className: "success"});
                       $('#user-roster').prepend(data);
                    },
                    error: function(data){
                        alert('Unable to get new user data. You will have to refresh the page');
                    }
                });
            }
        }
        else{
            //TODO: update business roster and update unread
            $fromBusiness.prependTo($fromBusiness.parent());
            $fromBusiness.addClass('unread');
            $.notify(via + " just received a message", {globalPosition: "top center", className: "success"});
        }
        return true;
    },

    logMessage: function(messageBody, fromUser){
        var k = {body: messageBody, coll_id: Athena.activeCollId};
        console.log(k);
        $.ajax({
            type: 'GET',
            data: {body: messageBody, coll_id: Athena.activeCollId},
            url: '/message_sent_from_business/',
            success: function(data){
                console.log('sucess');
            },
            error: function(data){
                console.log('error');
                console.log(data);
            }
        })
    },


    send_ping: function(to){
        var ping = $iq({
            to: to,
            type: "get",
            id: "ping1"}).c("ping", {xmlns: "urn:xmpp:ping"});

        console.log("Sengin ping to" + to + ".");
        Athena.start_time = (new Date()).getTime();

        Athena.connection.send(ping);
    },

    handle_pong: function(iq){
        var elapsed = (new Date()).getTime() - Athena.start_time;
        console.log("Received pong from server in "+ elapsed + " ms");
        
    },
};


$(document).ready(function (){
    jsSetup();
	$(document).trigger('connect', {});

	//activate tabs
	//$('#chat-area').tabs().find('.ui-tabs-nav').sortable({axis: 'x'});
});


$(document).bind('connect', function(ev, data){
	var conn = new Strophe.Connection(chatServerBind);

	conn.connect(connectionUsername, 'password', function(status){
		if (status == Strophe.Status.CONNECTED) {
			$(document).trigger('connected');
		}
		else if (status == Strophe.Status.DISCONNECTED) {
			$(document).trigger('disconnected');
		};
	});
	Athena.connection = conn;
});


$(document).bind('connected', function(){
    /*Athena.connection.addHandler(Athena.handle_pong, null, "iq", null, "ping1");
    var domain = Strophe.getDomainFromJid(Athena.connection.jid);

    Athena.send_ping(domain);*/
	Athena.bindAllBusinesses();
    Athena.bindAllUsers();
    Athena.bindChatInput();
    Athena.connection.addHandler(Athena.messageReceived, null, "message");
    Athena.connection.send($pres());
});


$(document).bind('disconnected', function(){
	//TODO: fill this part out
});


function jsSetup(){
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    console.log(csrftoken);

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }


    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("Content-Type", "application/json");
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}
