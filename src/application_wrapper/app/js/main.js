/*
Twitter Widget
*/
twttr = (function(d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0],
    t = window.twttr || {};
  if (d.getElementById(id)) return t;
  js = d.createElement(s);
  js.id = id;
  js.src = "https://platform.twitter.com/widgets.js";
  fjs.parentNode.insertBefore(js, fjs);

  t._e = [];
  t.ready = function(f) {
    t._e.push(f);
  };

  return t;
}(document, "script", "twitter-wjs"));

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
	consumer_key:         'XLuTfzcgjUtlZs4dzGM3W2tq6',
	consumer_secret:      'FfTFPxwhiI97wuy9TOe6Lq8Sgl8phJRFQNaukQbEXg6oblyuzJ',
	access_token:         '1179141952794583042-IPNL6nE2SdzZnG26p3Ld5TgpBSNfA9',
	access_token_secret:  'ptuUKpOGbUZIg8alVapQdXg3ibPdoBMwGT5LBDW4DRcgK',
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

				for (i=0; i<5; i++){
					let tweet = data.statuses[i];

					console.log(tweet);
					document.getElementById("user").innerHTML = tweet.user.name;
					document.getElementById("tweetbody").innerHTML = tweet.text;
					document.getElementById("tweeturl").innerHTML = "Http://www.Twitter.com/" +tweet.user.screen_name +"/status/" +tweet.id_str;
				
					let request = new XMLHttpRequest();
					request.open("GET", "https://publish.twitter.com/oembed?url=Http://www.Twitter.com/" +tweet.user.screen_name +"/status/" +tweet.id_str);
					request.send();
					request.onload = () => {
						console.log(request);
						if (request.status === 200){
							var response = JSON.parse(request.response);
							newTweetDiv = document.getElementById("tweetEmbed1").cloneNode(true);
							newTweetDiv.innerHTML = response.html
							document.getElementById('tweetHolder1').appendChild(newTweetDiv)
							twttr.widgets.load(newTweetDiv);
							console.log(response.html);
						} else{
							console.log("ERROR: " +request.statusText);
						}
					}
				}

				for (i=6; i<11; i++){
					let tweet = data.statuses[i];

					console.log(tweet);
					document.getElementById("user").innerHTML = tweet.user.name;
					document.getElementById("tweetbody").innerHTML = tweet.text;
					document.getElementById("tweeturl").innerHTML = "Http://www.Twitter.com/" +tweet.user.screen_name +"/status/" +tweet.id_str;
				
					let request = new XMLHttpRequest();
					request.open("GET", "https://publish.twitter.com/oembed?url=Http://www.Twitter.com/" +tweet.user.screen_name +"/status/" +tweet.id_str);
					request.send();
					request.onload = () => {
						console.log(request);
						if (request.status === 200){
							var response = JSON.parse(request.response);
							newTweetDiv = document.getElementById("tweetEmbed2").cloneNode(true);
							newTweetDiv.innerHTML = response.html
							document.getElementById('tweetHolder2').appendChild(newTweetDiv)
							twttr.widgets.load(newTweetDiv);
							console.log(response.html);
						} else{
							console.log("ERROR: " +request.statusText);
						}
					}
				}
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
