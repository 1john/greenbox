function ageVerify() {
function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+d.toUTCString();
	document.cookie = cname + "=" + cvalue + "; " + expires +";path=/";
}

function getCookie(cname) {
	var name = cname + "=";
	var ca = document.cookie.split(';');
	
	for (var i=0; i < ca.length; i++) {
		var c = ca[i].trim();
		if (c.indexOf(name) === 0) return c.substring(name.length,c.length);
	}
}

function checkCookie() {
	var age = getCookie("ageVerify");
		
	if (age === "over21") {
		// Check cookie: if exists and age passes, allow user into site
		setCookie("ageVerify", "over21", 1);				
	} else {
		// If cookie value is under 21, or if cookie does not exist, create modal window and ask user to respond
		$('body').prepend("<div class=\"age-check\"><div class=\"text-wrapper\"><p>Are you over 21?</p><button class=\"confirm button\">Yes</button><button class=\"cancel button\">No</button></div></div>");

		// Get rid of modal once button is clicked
		$('.age-check button').on('click', function() {
			$('.age-check').hide();
		});

		$('button.confirm').on('click', function() {
			// If user responds yes, change age value
			age = "over21";
			setCookie("ageVerify", "over21", 1);
		});

		$('button.cancel').on('click', function() {
			// If user clicks cancel, direct user to /under-21 page
			setCookie("ageVerify", "under21", 1);
			window.location.replace("http://www.oregon.gov/olcc/marijuana/Pages/FAQs-Personal-Use.aspx");
		});
	}
}

$(function() {
	checkCookie();
});
}


