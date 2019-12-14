# Parental oversight on Spotify
CS410 Text Information Systems Project 

Sam Parmar, Vijay Mishra, Pragya Mishra
## Function of tool:
The project focuses on parental oversight with Spotify. Parents with access and control over their son or daughter’s Spotify accounts will be equipped with a simple tool to analyze trends in listening history and conduct sentiment analysis on the listening choices (listened to songs) of their son or daughter. 
## Software implementation documentation:
1. Angular UI - front end code (all under angular-app)
directory - angular-app  
ng serve --host 0.0.0.0 --port 4200 --disable-host-check

1. App Server (4201) - Backend Server which does all the heavy lifting. this is one which calls spotify, genius and sentiment analysis.
python3 app-server.py  
   1. User song data pull with Spotify api
   1. Lyrics data pull Genius api pull (using song info obtained form Spotify api)
   1. Sentiment analysis (using lyrics data obtained from Genius api)
 
1. Login server (4202) (borrowed Obscurify) this implements the oauth flow for Spotify - we are using implicit authorization.
directory - angular-app
node login_server.js <client id> <secret>
   1. Note: The OAuth 2.0 Implicit Grant type is utilized for authentication w/ short lived access tokens.

## Software usage documentation:
1. Visit the following link in your web browser: 
1. Login with Spotify account
   1. Authorize access to proceed.
1. 

## Contribution of each team member:
* All team members collectively came up with the idea for the project
* Sam Parmar was the team leader for the project. Sam led work with the Spotify and Genius APIs to pull/parse song and lyrics data. He  assisted Pragya and Vijay in the web programming, and he outlined the presentation and maintained documentation. 
* Vijay Mishra developed the sentiment analysis model to assess emotions conveyed in text. Vijay also led the  web programming for the project by developing the app server and login server on AWS. Vijay developed the UI, persistent caching, and website security certificates to avoid browser privacy error. 
* Pragya Mishra assisted in the web programming defining the JSON format data and ensured the sub-programs effectively linked together.

## Acknowledgement and References:
* The login servered was based on the recently released Obscurity project (https://github.com/alexolivero/Obscurify).
* The glitch spotify implicit grant template was consulted for OAuth implementation (https://glitch.com/~spotify-implicit-grant).
