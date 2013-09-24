var whichQuote = true;
$("document").ready(function() {//$(window).load() must be used instead of $(document).ready() because of Webkit compatibility
	$(".photosgallery-std").sliderkit({
		mousewheel : false,
		circular : true,
		shownavitems : 1,
		scroll : 1,
		panelbtnshover : true,
		auto : true,
		navscrollatend : false,
		counter : true
	});
	var myGallery = $('.photosgallery-std').data('sliderkit');
	var myPaginStr = '';
	var myPaginCount = 0;
	// Building the pagination tag
	$('li', myGallery.navUL).each(function() {
		myPaginStr += '<li><a href="#" rel="' + myPaginCount + '">' + (myPaginCount + 1) + '</a></li>';
		myPaginCount++;
	});
	//myGallery.domObj.before('<div id="myPagination1" class="sliderkit-pagination"><ul>'+myPaginStr+'</ul></div>');
	// Selecting first item
	var myPaginTag = $('#myPagination1'), myPaginItems = $('li', myPaginTag);
	myPaginItems.eq(myGallery.options.start).addClass('selected');
	// Pagination items click event
	$('a', myPaginTag).click(function() {
		var $a = $(this);
		if (! $a.parent().hasClass('selected')) {
			myGallery.changeWithId($a.attr('rel'));
		}
		return false;
	});
	// Selecting current pagination item
	myGallery.options.panelfxbefore = function() {
		myPaginItems.removeClass('selected');
		myPaginItems.eq(myGallery.currId).addClass('selected');
	}
	$('#playbtn').click(function() {
		if (myGallery.isPlaying != null) {
			myGallery.autoScrollStop();
		} else {
			myGallery.autoScrollStart();
			myGallery._autoScrollHoverStop();
		}
		return false;
	});
	$('#startslide').click(function() {
		myGallery._wrapPanels();
		myGallery.imageFx.remove();
		myGallery.options.panelfx = 'sliding';
		myGallery.options.panelfxeasing = 'easeInOutExpo';
		myGallery.stepForward();
		return false;
	});
	$('#startfancy').click(function() {
		myGallery.options.panelfx = 'fancy';
		myGallery.options.imagefx = {
			fxType : 'random'
		};
		myGallery.imageFx.init();
		return false;
	});

	$("a#submitno").click(function(e) {
		e.preventDefault();
		submitNo();
	});

	$("input#s-head").enterKey(function() {
		submitNo();
	});

	$("input#s-head").focusin(function() {
		$(this).attr("value", "");
	});
	$("cite").hover(function(e) {
		$("li.callingCode").css("display", "block");
		$("h6.facebooklike").css("display", "none");
	}, function(e) {
		//console.log("out");
		$("li.callingCode").css("display", "none");
		$("h6.facebooklike").css("display", "block");

	});
	$("ul#chooseCallingCode").hover(function(e) {
		$("li.callingCode").css("display", "block");
		$("h6.facebooklike").css("display", "none");
	}, function(e) {
		//console.log("out");
		$("li.callingCode").css("display", "none");
		$("h6.facebooklike").css("display", "block");

	});
	$("article.hatein").hover(function(e) {
		//console.log("in");
	}, function(e) {
	});
	$("li.callingCode").click(function(e) {
		e.preventDefault();
		var thisText = $(this).text();
		$("cite").text(thisText.substring(thisText.indexOf("+")));
	});
	setInterval(quoteTimer, 5000);
});
function getImage(htmlString) {
	return $(htmlString).find("img:first").attr("src");
}

function checkIfHuman(title) {
	$("h1#checkTitle").html(title);
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
			//console.log("correct");
			sendNo();
		} else {
			//console.log("wrong");
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
}

function submitNo() {
	var no = $("input#s-head").attr("value");
	//console.log(no);
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
	countrycode = countrycode.replace("+", "");
	var data = {
		"country_code" : countrycode,
		"number" : no,
		"os_type" : 0
	};
	$("h1#checkTitle").html("Sending...");
	$("p#checkQuestion").html("");
	$("div#answers").css("display", "none");
	//console.log(data);
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
			//console.log(response);
			$("h1#checkTitle").html("Thank you for signing up!");
			$("p#checkQuestion").html("We have sent an SMS with further details to your number. Please share with your friends to make their lives easier too.<br><br> Click anywhere outside this box to close it.<br>" + '<a id="facebook" target="_blank" href="https://www.facebook.com/sharer/sharer.php?u=http://goo.gl/OfOqqN" class="shareButton"></a>' + '<a id="twitter" target="_blank" href="http://twitter.com/share?url=http://goo.gl/igP5gB" class="shareButton"></a>' + '<a id="google" target="_blank" href="https://plusone.google.com/_/+1/confirm?hl=en&url=http://goo.gl/RTfYm2" class="shareButton"></a>');
		},
		error : function(error) {
			//console.log(error);
			if (error.status == 500) {
				if (error.responseText.indexOf("1062")) {
					$("h1#checkTitle").html("Your number was already registered previously!");
					$("p#checkQuestion").html("To download the app again, visit haptik.co/download on your mobile device. And please do share it with your friends to make their lives easier.<br><br> Click anywhere outside this box to close it.<br>" + '<a id="facebook" target="_blank" href="https://www.facebook.com/sharer/sharer.php?u=http://goo.gl/OfOqqN" class="shareButton"></a>' + '<a id="twitter" target="_blank" href="http://twitter.com/share?text=Hate calling companies? Sign up here so you can text them. @hellohaptik&url=http://goo.gl/igP5gB" class="shareButton"></a>' + '<a id="google" target="_blank" href="https://plusone.google.com/_/+1/confirm?hl=en&url=http://goo.gl/RTfYm2" class="shareButton"></a>');

				} else
					checkIfHuman("Oops, we encountered an error on our end. Please try once more");
			}
		}
	});
}

function generateParas(text) {
	return '<p>' + text + '</p>';
}

function generateAlsoRead(postEntry) {
	return '<li><a target="_blank" href="' + postEntry.url + '">' + postEntry['regular-title'] + '</a></li>';
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
				$("h2#blogTitle").html(data.posts[0]['regular-title']);
				var postHTML = data.posts[0]['regular-body'];
				$("div#postImage").css("background-image", 'url(' + $(postHTML).find('img:first').attr("src") + ')');
				$("p#slug").text($(postHTML).text());
				$("a#fullStory").attr("href", data.posts[0].url);
				$("a#fullStory").attr("href", data.posts[0].url);
				$(".ellipsis").ellipsis();
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
