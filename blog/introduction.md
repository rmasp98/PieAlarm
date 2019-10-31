# Introduction

This blog is a complete (as long as I remember) walk-through of my journey trying to make a Smart Alarm clock. By this I mean and regular alarm clock but with a screen to display additional information and a few more bells and whistles such as voice recognition, light control, etc.

I should warn you now that I have never programmed in Python before (the language the software is in), never done any UI design let alone used Qt (the ui library I am using), and never really done much with Raspberry Pi’s or hardware in general. If you are here expecting a consumer grade product, you are probably in the wrong place. However, if you are also a complete beginner and you want someone going through the same process, come join along.

Just some background: I am not a complete novice at programming. I have been programming in C++ in my spare time for about 8 years. I am in the middle of writing a game engine, a game and an operating system (bit of a pipe dream). My job involves a lot of interaction with code (especially python) so I have picked a few things up and wanted to give it a proper try myself.

The motivation for this was largely based around my partner continuously asking me what the weather was going to be like today. So I wanted something that would be able to answer her without me having to look it up and buying a home assistant seemed to easy. This was then serendipitously timed with Amazon advertising a smart alarm clock to me and as with all new technology, I wanted one. But instead of paying amazon ludicrous amounts of money for a smart alarm clock, I paid Amazon ludicrous amounts of money for the components of a smart alarm clock.

So overall, here are the general features I am looking to add to my Smart Alarm Clock:
* User Interface - display time/date, weather and alarms
  * Main screen will display the current time and date, the weather for the day or week, and the next alarm. There will also be a controllable background
  * Weather screen will give more detailed information of weather and can be reached by clicking on weather in main screen
  * Alarm screen will allow configuration of alarms and can be reached by clicking alarm on main screen
  * Settings screen to fine tune what is displayed, e.g. fonts, backgrounds, brightness, light thresholds etc.
  * Should be able to go into a dark theme at night emitting minimal light based on the ambient light (using a light sensor)
* Alarm
  * I want the alarm to be able to trigger a range of interesting things such as music, playlists, radio, light, etc.
  * I also want the alarm to sync with my phone so that I can set everything on my phone
  * I also want all phone alarms to be disabled when in vicinity of alarm (maybe through bluetooth)
  * I may also connect the alarm to the light to steadily illuminate the room as another incentive to get up.
* Weather is pretty straight forward and will likely just follow the patterns of most other weather apps
* Voice - control various aspects with voice commands
  * I want to be able to get the alarm to tell me the time and the weather from a voice command
  * I want to be able to snooze over voice (maybe with a voice controlled maths challenge)
  * I want to be able to turn the light on and off with voice

So as I have already mentioned, I am going to be building this using a Raspberry Pi, because it so easy to make things with; a touch screen, to display and interact with the information; a light sensor, for darkening the screen at night; a light, both for alarms and general usage; and speakers, for the alarm and responses. 

I have decided to write this in Python3 using Qt as a User Interface library because Python is really easy to use (apparently) and Qt seemed to be the simplest library for creating a UI. I have not yet researched what I will need for all the other functions, so I will elaborate on that in later blogs.


