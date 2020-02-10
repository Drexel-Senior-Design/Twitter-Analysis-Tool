/*
Event Listeners
 */
document.addEventListener("DOMContentLoaded", function(){
	var hashtag_grab_btn = document.getElementById("hashtag_btn");
	hashtag_grab_btn.onclick = Get_Tweets_in_Hashtag;
	if (T) {
		document.getElementById("tweet_connection_status").innerHTML = "Yep";
	}
});

/*
variables
*/
var fakeDataX = [4, 2, 5, 20, 20, 1, 5, 3];

// Establish Twitter Connection
let Twit = require("twit");
var T = new Twit({
	consumer_key:         '',
	consumer_secret:      '',
	access_token:         '',
	access_token_secret:  '',
});

function Get_Tweets_in_Hashtag(){
	let hashtag = document.getElementById("user_hashtag").value;
	// TODO: Better input validation on Hashtag
	if (hashtag.length > 140 || hashtag.search("#") !== -1){
		alert("Bad input, too long or invalid characters");
		throw "Get_Tweets_in_Hashtag(): Input Too long or Invalid Chars";
	}
	T.get('search/tweets',
		{ q: '#'+hashtag, count: 100 },
		function(err, data, response) {
			// TODO: Error Handling
			if (!err) {
				let tweet = data.statuses[0];
				document.getElementById("user").innerHTML = tweet.user.name;
				document.getElementById("tweetbody").innerHTML = tweet.text;
			}
		}
	);
}

/*
scrape hashtag that the user enters
*/
function Get_User_Hashtag() {
	var x = document.getElementById("user_hashtag").value;
	document.getElementById("report_display").innerHTML = x;
}
