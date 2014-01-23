var whichQuote = true;
var debugging = false;
var abcase;
var inputText;
$("document").ready(function() {//$(window).load() must be used instead of $(document).ready() because of Webkit compatibility
	var query = get_query();
	if (query.debug === "true") {
		debugging = true;
	}
	abtesting();
	$("a#submitno").click(function(e) {
		e.preventDefault();
		submitNo();
	});

	$("input#s-head").enterKey(function() {
		submitNo();
	});

	$("input#s-head").focusin(function() {
		var currentValue = $(this).attr("value");
		if (currentValue === inputText)
			$(this).attr("value", "");
	});
	$("input#s-head").focusout(function() {
		var currentValue = parseInt($(this).attr("value").trim());
		if (currentValue === "")
			$(this).attr("value", inputText);
	})
	$("cite").hover(function(e) {
		$("li.callingCode").css("display", "block");
		$("h6.facebooklike").css("display", "none");
	}, function(e) {
		$("li.callingCode").css("display", "none");
		$("h6.facebooklike").css("display", "block");

	});
	$("ul#chooseCallingCode").hover(function(e) {
		$("li.callingCode").css("display", "block");
		$("h6.facebooklike").css("display", "none");
	}, function(e) {
		$("li.callingCode").css("display", "none");
		$("h6.facebooklike").css("display", "block");

	});
	$("article.hatein").hover(function(e) {
	}, function(e) {
	});
	$("li.callingCode").click(function(e) {
		e.preventDefault();
		var thisText = $(this).text();
		$("cite").text(thisText.substring(thisText.indexOf("+")));
		if (thisText.indexOf("India") != -1) {
			$("img#screenshot").attr("src", "/static/img/iphoneblack.png");
		} else {
			$("img#screenshot").attr("src", "/static/img/iphoneblackrow.png");
		}
	});
	setInterval(quoteTimer, 10000);
	getCountry();
});
function getImage(htmlString) {
	return $(htmlString).find("img:first").attr("src");
}

function getCountry() {
	log(codehelper_ip);
	if (codehelper_ip.Country === "IN") {
		$("img#screenshot").attr("src", "/static/img/iphoneblack.png");
		$("span#callingcode").text("+91");
	} else if (result.countryCode === "AE") {
		$("img#screenshot").attr("src", "/static/img/iphoneblackrow.png");
		$("span#callingcode").text("+971");
	} else if (result.countryCode === "SN") {
		$("img#screenshot").attr("src", "/static/img/iphoneblackrow.png");
		$("span#callingcode").text("+65");
	} else if (result.countryCode === "US") {
		$("img#screenshot").attr("src", "/static/img/iphoneblackrow.png");
		$("span#callingcode").text("+1");
	}
}

function abtesting() {
	abcase = Math.random();
	abcase = 1;
	//testing over for now
	if (abcase <= 0.5) {
		inputText = "Enter your mobile number for early access";
	} else {
		inputText = "Enter your mobile number for a chance to get early access";
	}
	$("input#s-head").attr("value", inputText);
}

function checkIfHuman(title) {
	$("h1#checkTitle").html(title);
	$("body").css("overflow", "hidden");
	$("div#checkIfHuman").css("display", "block");
	var first = Math.floor((Math.random() * 5) + 1);
	var second = Math.floor((Math.random() * 5) + 1);
	var sum = first + second;
	var option1 = sum - 1;
	var option2 = sum + 1;
	var option3 = sum + 2;
	var correct = Math.floor((Math.random() * 4) + 1);
	switch(correct) {
		case 1:
			$("div#answer1").html(sum);
			$("div#answer2").html(option1);
			$("div#answer3").html(option2);
			$("div#answer4").html(option3);
			break;
		case 2:
			$("div#answer2").html(sum);
			$("div#answer1").html(option1);
			$("div#answer3").html(option2);
			$("div#answer4").html(option3);
			break;
		case 3:
			$("div#answer3").html(sum);
			$("div#answer1").html(option1);
			$("div#answer2").html(option2);
			$("div#answer4").html(option3);
			break;
		case 4:
			$("div#answer4").html(sum);
			$("div#answer1").html(option1);
			$("div#answer2").html(option2);
			$("div#answer3").html(option3);
			break;
	}

	$("p#checkQuestion").html("What is the sum of " + first + " and " + second + "?");
	$("div#answers").css("display", "block");
	$("div.answers").unbind("click");
	$("div#outsideContainer").unbind("click");
	$("div.answers").click(function(e) {
		e.preventDefault();
		var answer = $(this).html();
		if (answer === sum + "") {
			sendNo();
		} else {
			checkIfHuman("Oops, you were wrong<br>Let's try that again");
		}
	});
	$("div#outsideContainer").click(function(e) {
		e.preventDefault();
		hideTest();
	})
}

function hideTest() {
	$("div#checkIfHuman").css("display", "none");
	$("body").css("overflow", "inherit");
	$("input#s-head").attr("value", "Enter your mobile number for early access");
}

function submitNo() {
	var no = $("input#s-head").attr("value");
	if (!isNaN(no)) {
		checkIfHuman("Just double-checking that you are human");
	} else {
		$("input#s-head").attr("value", "Please enter a valid number");
		$("input#s-head").blur();
	}
}

function sendNo() {
	var no = ($("input#s-head").attr('value'));
	no = no.trim();
	var countrycode = $("cite").text();
	countrycode = countrycode.replace("+", "").trim();
	var data = {
		"country_code" : countrycode,
		"number" : no,
		"os_type" : 0
	};
	$("h1#checkTitle").html("Sending...");
	$("p#checkQuestion").html("");
	$("div#answers").css("display", "none");
	log(data);
	$.ajaxSetup({
		beforeSend : function(jqXHR, options) {
			if (options.contentType == "application/json" && typeof options.data != "string") {
				options.data = JSON.stringify(options.data);
			}
		}
	});

	$.ajax({
		url : "/api/v1/website_signup/?format=json",
		type : "POST",
		headers : {
			"Content-Type" : "application/json",
		},
		data : JSON.stringify(data),
		dataType : "JSON",
		success : function(response) {
			log(response);
			$("h1#checkTitle").html("Thank you for signing up!");
			$("p#checkQuestion").html("We have sent an SMS with further details to your number. Please share with your friends to make their lives easier too.<br><br> Click anywhere outside this box to close it.<br>" + '<a id="facebook" target="_blank" href="https://www.facebook.com/sharer/sharer.php?u=http://goo.gl/OfOqqN" class="shareButton"></a>' + '<a id="twitter" target="_blank" href="http://twitter.com/share?url=http://goo.gl/igP5gB" class="shareButton"></a>' + '<a id="google" target="_blank" href="https://plusone.google.com/_/+1/confirm?hl=en&url=http://goo.gl/RTfYm2" class="shareButton"></a>');
			if (abcase <= 0.5) {
				_gaq.push(['_trackEvent', 'signup', 'new', 'short']);
			} else {
				_gaq.push(['_trackEvent', 'signup', 'new', 'long']);
			}
		},
		error : function(error) {
			log(error);
			if (error.status == 500) {
				if (error.responseText.indexOf("1062")) {
					$("h1#checkTitle").html("Your number was already registered previously!");
					$("p#checkQuestion").html("We will be sending you a text with a download link once we open up more beta slots. Until then, please do share Haptik with your friends to make their lives easier!<br><br> Click anywhere outside this box to close it.<br>" + '<a id="facebook" target="_blank" href="https://www.facebook.com/sharer/sharer.php?u=http://goo.gl/OfOqqN" class="shareButton"></a>' + '<a id="twitter" target="_blank" href="http://twitter.com/share?text=Hate calling companies? Sign up here so you can text them. @hellohaptik&url=http://goo.gl/igP5gB" class="shareButton"></a>' + '<a id="google" target="_blank" href="https://plusone.google.com/_/+1/confirm?hl=en&url=http://goo.gl/RTfYm2" class="shareButton"></a>');
					if (abcase <= 0.5) {
						_gaq.push(['_trackEvent', 'signup', 'old', 'short']);
					} else {
						_gaq.push(['_trackEvent', 'signup', 'old', 'long']);
					}
				} else {
					checkIfHuman("Oops, we encountered an error on our end. Please try once more");
					if (abcase <= 0.5) {
						_gaq.push(['_trackEvent', 'signup', 'error', '500']);
					} else {
						_gaq.push(['_trackEvent', 'signup', 'error', '500']);
					}
				}
			} else {
				checkIfHuman("Oops, we encountered an error on our end. Please try once more");
				if (abcase <= 0.5) {
					_gaq.push(['_trackEvent', 'signup', 'error', error.responseText]);
				} else {
					_gaq.push(['_trackEvent', 'signup', 'error', error.responseText]);
				}
			}
		}
	});
}

function log(message) {
	if (debugging) {
		console.log(message);
	}
}

function generateParas(text) {
	return '<p>' + text + '</p>';
}

function generateAlsoRead(postEntry) {
	return '<li><a target="_blank" href="' + postEntry["url-with-slug"] + '">' + postEntry['regular-title'] + '</a></li>';
}

function quoteTimer() {
	whichQuote = !whichQuote;
	var quote = "Advertisers struggle to be heard through the noise.<br><br> Customer service reps, on the other hand, can whisper.<br><br>";
	if (whichQuote) {
		quote = "I think the single factor that is killing  consumers and that is under the company’s control is this: the desire to perform all customer service in real time.<br><br>";
	}
	$("span#quote").animate({
		"opacity" : "0"
	}, 1000, function() {
		$("span#quote").html(quote);
		$("span#quote").animate({
			"opacity" : "1"
		}, 1000, function() {
		});
	});
}

function setBlog(data) {
	var ulHTML = "";
	if (data.posts[0].type === "regular") {
		$("h2#blogTitle").html(data.posts[0]['regular-title']);
		var postHTML = data.posts[0]['regular-body'];
		$("div#postImage").css("background-image", 'url(' + $(postHTML).find('img:first').attr("src") + ')');
		$("p#slug").text($(postHTML).text());
		$("a#fullStory").attr("href", data.posts[0]["url-with-slug"]);
		$(".ellipsis").ellipsis();
	}
	else if (data.posts[0].type === "video"){
		$("p#slug").html(data.posts[0]['video-caption']);
		$("div#postImage").html(data.posts[0]["video-source"]);
		$("a#fullStory").attr("href", data.posts[0]["url-with-slug"]);
	}
	if (data.posts.length == 1) {
		$("#morePosts").css("display", "none");
	}
	for (var i = 1; i < data.posts.length; i++) {
		ulHTML += generateAlsoRead(data.posts[i]);
	}
	$("ul#morePosts").html(ulHTML);
}

$.fn.enterKey = function(fnc) {
	return this.each(function() {
		$(this).keypress(function(ev) {
			var keycode = (ev.keyCode ? ev.keyCode : ev.which);
			if (keycode == '13') {
				fnc.call(this, ev);
			}
		})
	})
}
function vai_a(id, v) {
	for ( i = 1; i <= 3; i++) {
		document.getElementById("home" + i).className = "ahome" + i;
	}
	//document.getElementById("home" + v).className = "home" + v;
	$('html,body').animate({
		scrollTop : $("#" + id).offset().top - 96
	}, 600);
}

/**
 * Used to get the query part of the URL
 * @return {Object} result result is a JSONObject containing the different query parameters in the URL
 */
function get_query() {
	var url = location.href;
	var qs = url.substring(url.indexOf('?') + 1).split('&');
	for (var i = 0, result = {}; i < qs.length; i++) {
		qs[i] = qs[i].split('=');
		result[qs[i][0]] = qs[i][1];
	}
	return result;
}