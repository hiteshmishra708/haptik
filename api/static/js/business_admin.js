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

