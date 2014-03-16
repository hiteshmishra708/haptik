function trackGAEvent(category, eventName){
    _gaq.push(['_trackEvent', category, eventName]);
};

$(function () {


    function animateTweets() {
        var quotes = $(".quotes");
        var quoteIndex = -1;
        function showNextQuote() {
            ++quoteIndex;
            quotes.eq(quoteIndex % quotes.length)
                .fadeIn(2000).delay(4000).fadeOut(2000, showNextQuote);
        }
        showNextQuote();
    };

    $(document).ready(function(){
        animateTweets();
        //$.ajax({
        //     url: '/twitter_mentions/',
        //     type: "GET",
        //     headers: { "Content-Type": "application/json" },
        //     dataType: "JSON",
        //     success: function (result) {
        //        var arrayLength = result.length;
        //        for (var i = 0; i < arrayLength; i++) {
        //            tweet= '<h2 class="quotes"><span>@' + result[i]['user'] + ':</span><br>' + result[i]['text'] + '</h2>';
        //            $('.foottwit-lt').append(tweet);
        //        }
        //        animateTweets();
        //     },
        //     error: function (xhr, ajaxOptions, thrownError) {
        //        console.log('error');
        //     }
        // });
    });




    var divInput = $('div.input'); 

    var width = divInput.width();

    var outerWidth = divInput.parent().width() - (divInput.outerWidth() - width) - 0;

    var input = $('input#s');

    var submit = $('#searchSubmit');

    var txt = input.val();  

    var urlString2 = 'url(/static/img/newsite/grayicon.png)';

    var urlString1 = 'url(/static/img/newsite/search-icon.png)';







    input.bind('focus', function () {

        // alert("focus");


        if (input.val() === txt) {

            input.val('');



            document.getElementById("searchSubmit").style.backgroundImage = urlString2;

            document.getElementById("searchSubmit").style.display = 'block';

            document.getElementById("s").style.fontStyle = 'normal';

        }

        else {

            document.getElementById("searchSubmit").style.backgroundImage = urlString1;

            document.getElementById("searchSubmit").style.display = 'block';

            document.getElementById("s").style.fontStyle = 'normal';

        }



        $(this).animate({ color: '#000' }, 300); // text color

        $(this).parent().animate({

            width: outerWidth + 'px',

            marginLeft: '-25px'

        }, 300, function () {

            if (!(input.val() === '' || input.val() === txt)) {

                if (!($.browser.msie && $.browser.version < 9)) {

                    submit.fadeIn(300);

                } else {

                    submit.css({ display: 'block' });

                }

            }

        }).addClass('focus');

    }).bind('blur', function () {

        $(this).animate({ color: '#b4bdc4' }, 300); // text color

        $(this).parent().animate({

            width: width + 'px',

            marginLeft: '-25px'

        }, 300, function () {

            if (input.val() === '') {

                input.val(txt)

                document.getElementById("s").style.fontStyle = 'italic';

            }

        }).removeClass('focus');

        if (!($.browser.msie && $.browser.version < 9)) {

            //   submit.fadeOut(100);

        } else {

            //    submit.css({display: 'none'});

        }

    }).keyup(function () {



        if (input.val() === '') {



            if (!($.browser.msie && $.browser.version < 9)) {



                document.getElementById("searchSubmit").style.backgroundImage = urlString2;

                document.getElementById("s").style.fontStyle = 'italic';

                //submit.fadeOut(300);

            } else {



                document.getElementById("searchSubmit").style.backgroundImage = urlString2;

                //submit.css({ display: 'none' });

                document.getElementById("s").style.fontStyle = 'italic';

            }

        } else {

            if (!($.browser.msie && $.browser.version < 9)) {

                submit.fadeIn(300);

                document.getElementById("searchSubmit").style.backgroundImage = urlString1;

                document.getElementById("s").style.fontStyle = 'normal';

            } else {

                submit.css({ display: 'block' });

                document.getElementById("searchSubmit").style.backgroundImage = urlString1;

                document.getElementById("s").style.fontStyle = 'normal';

            }

        }

    });









    });









$(function () {



    var divInput = $('div.input1');

    var width = divInput.width();

    var outerWidth = divInput.parent().width() - (divInput.outerWidth() - width) - 0;

    var input = $('input#s1');

    var submit = $('#searchSubmit1');

    var txt = input.val();

    var urlString2 = 'url(/static/img/newsite/grayicon.png)';

    var urlString1 = 'url(/static/img/newsite/search-icon.png)';



    input.bind('focus', function () {       

        if (input.val() === txt) {

            input.val('');



            document.getElementById("searchSubmit1").style.backgroundImage = urlString2;

            document.getElementById("searchSubmit1").style.display = 'block';

            document.getElementById("s1").style.fontStyle = 'normal';

        }

        else {

            document.getElementById("searchSubmit1").style.backgroundImage = urlString1;

            document.getElementById("searchSubmit1").style.display = 'block';

            document.getElementById("s1").style.fontStyle = 'normal';

        }



        $(this).animate({ color: '#000' }, 300); // text color

        $(this).parent().animate({

            width: outerWidth + 'px',

            marginLeft: '0px'

        }, 300, function () {

            if (!(input.val() === '' || input.val() === txt)) {

                if (!($.browser.msie && $.browser.version < 9)) {

                    submit.fadeIn(300);

                } else {

                    submit.css({ display: 'block' });

                }

            }

        }).addClass('focus1');

    }).bind('blur', function () {

        $(this).animate({ color: '#b4bdc4' }, 300); // text color

        $(this).parent().animate({

            width: width + 'px',

            marginLeft: '0px'

        }, 300, function () {

            if (input.val() === '') {

                input.val(txt)

                document.getElementById("s1").style.fontStyle = 'italic';

            }

        }).removeClass('focus1');

        if (!($.browser.msie && $.browser.version < 9)) {

            //   submit.fadeOut(100);

        } else {

            //    submit.css({display: 'none'});

        }

    }).keyup(function () {



        if (input.val() === '') {



            if (!($.browser.msie && $.browser.version < 9)) {



                document.getElementById("searchSubmit1").style.backgroundImage = urlString2;

                document.getElementById("s1").style.fontStyle = 'italic';

                //submit.fadeOut(300);

            } else {



                document.getElementById("searchSubmit1").style.backgroundImage = urlString2;

                //submit.css({ display: 'none' });

                document.getElementById("s1").style.fontStyle = 'italic';

            }

        } else {

            if (!($.browser.msie && $.browser.version < 9)) {

                submit.fadeIn(300);

                document.getElementById("searchSubmit1").style.backgroundImage = urlString1;

                document.getElementById("s1").style.fontStyle = 'normal';

            } else {

                submit.css({ display: 'block' });

                document.getElementById("searchSubmit1").style.backgroundImage = urlString1;

                document.getElementById("s1").style.fontStyle = 'normal';

            }

        }

    });











});



function docht(){

if(document.documentElement.clientHeight<document.documentElement.scrollHeight){

return document.documentElement.scrollHeight;

}else{

return document.documentElement.clientHeight;

}}

function godisplay()

{

document.getElementById('html_pop').style.display='block';

document.getElementById('pop_div').style.display="block";

document.getElementById('pop_div').style.height=docht()+"px";

}

function hide_div()

{

document.getElementById('pop_div').style.display="none";

document.getElementById('html_pop').style.display = 'none';

document.getElementById('pop_div1').style.display = "none";



}

function godisplay1() {

    document.getElementById('html_pop1').style.display = 'block';

    document.getElementById('pop_div1').style.display = "block";

    document.getElementById('pop_div1').style.height = docht() + "px";

}

function hide_div1() {

    document.getElementById('pop_div1').style.display = "none";

    document.getElementById('html_pop1').style.display = 'none';

}

    function trim(str) {

            return str.replace(/^\s+|\s+$/g, '');

        }    









function JSONTest() {

    var hostName = document.location.hostname;

    hostName = hostName.replace("www.", "");

    var urlString1 = 'url(/static/img/newsite/grayicon.png)';

    //alert(hostName);

    var urlString = 'url(/static/img/newsite/tick.png)';



    if (trim(document.getElementById("s").value) == "") {

        alert("Enter Mobile no");

        document.getElementById("s").focus();

        document.getElementById("searchSubmit1").style.backgroundImage = urlString1;

        return false;

    }

    if (isNaN(document.getElementById("s").value)) {

        alert("Enter only numeric");

        document.getElementById("s").focus();

        return false;

    }



    if (document.getElementById("s").value.length < 10) {



        alert("Enter a valid number");

        return false;

    }



    if (trim(document.getElementById("q").value) == "") {

        alert("Enter Country code");

        document.getElementById("s").focus();

        return false;

    }

    var countrycode = document.getElementById("q").value

    var mobileno = document.getElementById("s").value.trim();

    countrycode = countrycode.replace("+", "").trim();

    //var resultDiv = $("#resultDivContainer");

    // var url_ = "http://haptik.co/api/v1/website_signup/?format=json";

    var url_ = "/api/v1/website_signup/?format=json";

    $.ajaxSetup({

        beforeSend: function (jqXHR, options) {

            if (options.contentType == "application/json" && typeof options.data != "string") 

            {               

                options.data = JSON.stringify(options.data);

            }

        }

    });

    trackGAEvent('Home' , 'Submit Phone Number');

    $.ajax({

        url: url_,

        type: "POST",

        headers: { "Content-Type": "application/json" },

        data: JSON.stringify({ country_code: countrycode, number: mobileno, os_type: 0 }),

        dataType: "JSON",

        success: function (result) {

            //  document.getElementById("searchSubmit").style.backgroundImage = urlString;

           godisplay();

        },

        error: function (xhr, ajaxOptions, thrownError) {

           // document.getElementById("searchSubmit").style.backgroundImage = urlString;

            godisplay();

        }

    });

}



function Sendmail() {
    if (trim(document.getElementById("txtfname").value) == "") {
        alert("Enter first name");
        document.getElementById("txtfname").focus();
        return false;
    }

    if (trim(document.getElementById("txtcompany").value) == "") {
        alert("Enter company");
        document.getElementById("txtcompany").focus();
        return false;
    }

    if (document.getElementById("standard-dropdown").value == "" || document.getElementById("standard-dropdown").value == "1") 
    {
        alert("Enter function");
        document.getElementById("standard-dropdown").focus();
        return false;
    }

     if (trim(document.getElementById("txtpno").value) == "") {
        alert("Enter Phone Number");
        document.getElementById("txtpno").focus();
        return false;
    }

     if (isNaN(document.getElementById("txtpno").value)) {
        alert("Enter only numeric");
        document.getElementById("txtpno").focus();
        return false;
    }

    if (document.getElementById("txtpno").value.length < 10) 
    {
        alert("Enter a valid number");
        document.getElementById("txtpno").focus();
        return false;
    }

    if (document.getElementById("txtlname").value == "") 
    {
        alert("Enter last name");
        document.getElementById("txtlname").focus();
        return false;
    }

    if (document.getElementById("txttitle").value == "") 
    {
        alert("Enter title");
        document.getElementById("txttitle").focus();
        return false;
    }

    if (document.getElementById("txtemail").value.length > 0) {
        if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(document.getElementById("txtemail").value)) {
        }
        else {
            alert("Invalid E-mail Address! Please re-enter.");
            document.getElementById("txtemail").focus();
            document.getElementById("txtemail").select();
            return false;
        }
    }
    else {
        alert("Please enter your Email ID");
        document.getElementById("txtemail").focus();
        document.getElementById("txtemail").select();
        return false;
    }

    if (document.getElementById("txtmsg").value == "") {
        alert("Enter Message");
        document.getElementById("txtmsg").focus();
        return false;
    } 

    var fname = document.getElementById("txtfname").value;
    var lname = document.getElementById("txtlname").value;
    var company = document.getElementById("txtcompany").value;
    var funccontrol = document.getElementById("standard-dropdown");
    var func = funccontrol.options[funccontrol.selectedIndex].text;          
    var pno = document.getElementById("txtpno").value;
    var title = document.getElementById("txttitle").value;
    var email = document.getElementById("txtemail").value;
    var msg = document.getElementById("txtmsg").value;
    var oXmlHttp = zXmlHttp.createRequest();
    var params = "r=" + Math.random() + "&fname=" + fname+  "&lname=" + lname + "&company=" + company + "&func=" + func + "&pno=" + pno + "&title=" + title + "&email=" + email + "&msg=" + msg;

    data = {
        "fname" : fname,
        "lname" : lname,
        "company" : company,
        "func" : func,
        "pno" : pno,
        "title" : title,
        "email" : email,
        "msg" : msg
    };
    
    document.getElementById("intsubmit").style.display = "none";
    document.getElementById("divloader").style.display = "block";

    $.ajax({
        url: "/company_submit/",
        type: "GET",
        headers: {
            "Content-Type" : "application/json"
        },
        data : data,
        dataType: "JSON",
        success: function(response){
            document.getElementById("intsubmit").style.display = "block";
            document.getElementById("divloader").style.display = "none";
            window.scroll(0,50) ;
            godisplay();
        },
        error: function(response){
            document.getElementById("intsubmit").style.display = "block";
            document.getElementById("divloader").style.display = "none";
            console.log(response)
            alert('There was a problem. Please try again');
        }
    });

    // alert(params);
//    try {
//        var url = "http://180.149.245.242/HaptikSendmail/SendUserMail.aspx";
//        oXmlHttp.open("POST", url, true);
//        oXmlHttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
//        oXmlHttp.setRequestHeader("Content-length", params.length);
//        oXmlHttp.setRequestHeader("Connection", "close");
//        oXmlHttp.onreadystatechange = function () {
//            if (oXmlHttp.readyState == 4) {
//                //alert(oXmlHttp.responseText);
//                if (oXmlHttp.responseText != "" && oXmlHttp.responseText != null) {
//                    var myString = oXmlHttp.responseText;
//                    var mySplitResult = myString.split("*");
//                    if (mySplitResult[0] == "1") {
//                        document.getElementById("intsubmit").style.display = "block";
//                        document.getElementById("divloader").style.display = "none";
//            window.scroll(0,50) ;
//                        godisplay();
//                    }
//                    else {
//                        document.getElementById("intsubmit").style.display = "block";
//                        document.getElementById("divloader").style.display = "none";
//            window.scroll(0,50) ;
//                        godisplay();
//                    }
//                }
//            }
//        };
//        oXmlHttp.send(params);
//        document.getElementById("intsubmit").style.display = "none";
//        document.getElementById("divloader").style.display = "block";
//    }
//    catch (ex) {
//        document.getElementById("intsubmit").style.display = "block";
//        document.getElementById("divloader").style.display = "none";
//        window.scroll(0,50) ;
//    }

}





function JSONTest1() {

    var hostName = document.location.hostname;

    hostName = hostName.replace("www.", "");

    //alert(hostName);



    var urlString1 = 'url(/static/img/newsite/grayicon.png)';



    if (trim(document.getElementById("s1").value) == "") {

        alert("Enter Mobile no");

        document.getElementById("s1").focus();

        document.getElementById("searchSubmit1").style.backgroundImage = urlString1;

        return false;

    }

    if (isNaN(document.getElementById("s1").value)) {

        alert("Enter only numeric");

        document.getElementById("s1").focus();

        return false;

    }



    if (document.getElementById("s1").value.length < 10) {



        alert("Enter a valid number");

        return false;

    }



    if (trim(document.getElementById("q1").value) == "") {

        alert("Enter Country code");

        document.getElementById("s1").focus();

        return false;

    }

    var countrycode = document.getElementById("q1").value

    var mobileno = document.getElementById("s1").value.trim();

    countrycode = countrycode.replace("+", "").trim();

    //var resultDiv = $("#resultDivContainer");

    // var url_ = "http://haptik.co/api/v1/website_signup/?format=json";

    var url_ = "/api/v1/website_signup/?format=json";

    $.ajaxSetup({

        beforeSend: function (jqXHR, options) {

            if (options.contentType == "application/json" && typeof options.data != "string") {

                options.data = JSON.stringify(options.data);

            }

        }

    });

    trackGAEvent('Get the App', 'Submit Number');

    $.ajax({

        url: url_,

        type: "POST",

        crossdomain: true,

        headers: {"Content-Type": "application/json" },

        data: JSON.stringify({ country_code: countrycode, number: mobileno, os_type: 0 }),

        dataType: "JSON",

        success: function (result) {

            //  document.getElementById("searchSubmit").style.backgroundImage = urlString;



            godisplay();

            document.getElementById("html_pop1").style.display = "none";



        },

        error: function (xhr, ajaxOptions, thrownError) {

            // document.getElementById("searchSubmit").style.backgroundImage = urlString;

            godisplay();

            document.getElementById("html_pop1").style.display = "none";

        }

    });

}