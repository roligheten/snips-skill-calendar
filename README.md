# Snips Calendar App
Calendar skill for the Snips voice assistant platform that interfaces with your Google Calendar (And hopefully more later) and allows you to ask event related questions.

# Installation
You can find this app on the Snips App Store under the name "Calendar", to use it simply add the app to your assistant and update it.

During deployment of your assistant it will ask you to provide "google_token", this token can be retrieved here:

[Link to Google sign-in](https://accounts.google.com/o/oauth2/auth?scope=https://www.googleapis.com/auth/calendar&response_type=code&redirect_uri=urn:ietf:wg:oauth:2.0:oob&client_id=173155842276-rfbrtra35u55rug7jtc85i50r9grunbg.apps.googleusercontent.com)

**It is important that the timezone on your Snips device is correct**, if it is not the app will malfunction. If you are running stock Raspbian this can be changed via the "raspi-config" command

# Supported intents:
## Events on specific date
Examples:
* What am I doing tomorrow?
* What am I doing 25th of July at 15 pm?
* What was I doing yesterday?
* What am I doing today at noon?

# Future work
The following features are not currently implement but will be looked into in the future:
* Support for "next event on my calendar" type queries
* Microsoft Outlook support
* iCloud calendar support
* Other providers if there is interest

# Contibuting
Code contributions are highly appreciated, if you wish to contibute features please feel free to contact me. 
