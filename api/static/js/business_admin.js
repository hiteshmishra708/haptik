$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("Content-Type", "application/json");
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

