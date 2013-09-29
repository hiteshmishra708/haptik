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
        console.log('IN BEFORE SEND');
        console.log(settings);
        xhr.setRequestHeader("Content-Type", "application/json");
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            console.log('set cookie');
            console.log(xhr);
        }
        console.log(settings);
    }
});


$(function () { 
    $('.arrow, [class^=arrow-]').bootstrapArrows();
});

$(function(){
        $('#add_business').click(function(){
            window.location='/add_business'
        });
});

$(function(){
    $("#business_row").click(function(){
        var value = $(this).attr('value');
        window.location = '/add_business/'+value+'/';
    })
});

$(function(){
    $("#show_faqs").click(function(){
        var value = $(this).attr('value');
        window.location = '/business_faqs/'+value+'/';
    })
});

$(function(){
    $("#add_faq").click(function(){
        var value = $(this).attr('value');
        window.location = '/add_faqs/'+value+'/';
    })
});

$(function(){
    $("#back_to_business").click(function(){
        var value = $(this).attr('value');
        window.location = '/add_business/'+value+'/';
    })
});

$(function(){
    $("#back_to_admin").click(function(){
        window.location = '/business_admin/';
    })
});

$(function(){
    $("#back_to_faqs").click(function(){
        var value = $(this).attr('value');
        window.location = '/business_faqs/'+value+'/';
    })
});

$(function(){
    $("#send_message").click(function(){
        var business_id = $(this).attr("value");
        var message = $("textarea#message").val();
        console.log('sending message');
        $.ajax({
            type: 'POST',
            url: '/ajax_send_message/',
            data: JSON.stringify({ 'business_id' : business_id , 'message' : message}),
            headers: {
                "Content-Type" : "application/json"
            },
            success: function(data){
                alert('Sent');
                window.location = '/business_admin/'
            },
            error: function(data){
                alert('There was some problem sending');
            },
        });
        
    })
});



$(function(){
    $(".up,.down").click(function(){
        var row = $(this).parents("tr:first");
        var faqId = parseInt(row.attr("id"));
        if ($(this).is(".up")) {
            var newRelevance = parseInt(row.attr("relevance")) + 1;
            $.ajax({
                type: "PUT",
                url: "/api/v1/faqs/"+faqId+"/?format=json",
                data: '{"relevance" : '+newRelevance+'}',
                success: function(data){
                    console.log('success');
                    console.log(data);
                },
                error: function(data){
                    console.log('error');
                    console.log(data.responseText);
                }
            });
            var prevRowRelevance = parseInt(row.prev().attr("relevance"));
            row.attr("relevance", newRelevance);
            row.find("#relevance").find("#relevance-value").text(newRelevance);
            while(newRelevance > prevRowRelevance){
                row.insertBefore(row.prev());
                prevRowRelevance = parseInt(row.prev().attr("relevance"));
            }
        } else {
            var newRelevance = parseInt(row.attr("relevance")) - 1;
            if(newRelevance >= 0){
                $.ajax({
                    type: "PUT",
                    url: "/api/v1/faqs/"+faqId+"/?format=json",
                    data: '{"relevance" : '+newRelevance+'}',
                    success: function(data){
                        console.log('success');
                    },
                    error: function(data){
                        console.log('error');
                        console.log(data.responseText);
                    }
                });
                var nextRowRelevance = parseInt(row.next().attr("relevance"));
                row.attr("relevance", newRelevance);
                row.find("#relevance").find("#relevance-value").text(newRelevance);
                while(newRelevance < nextRowRelevance){
                    row.insertAfter(row.next());
                    nextRowRelevance = parseInt(row.next().attr("relevance"));
                }
            }
        }
    })
});

