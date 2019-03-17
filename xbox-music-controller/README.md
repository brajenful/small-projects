# xbox-music-controller

A small script that lets you control media applications with your XBOX 360 or XBOX One controller. It does so by mapping the multimedia buttons to the controller's buttons.

### Dependencies

- [keyboard](https://github.com/boppreh/keyboard) for emulating the keyboard buttons.
- [inputs](https://github.com/zeth/inputs) for listening to controller keypresses.

### How to use

This is by no means a finished script, and never will be (which is part of the reason it doesn't have its own repository), but despite that, I wanted to share it anyway just in case someone can use some of it in their own projects, or if nothing else, just as example as to how you should not write proper code.

That being said, it doesn't have any error handling, the buttons are hard-coded, and its actual practical use is debatable at best. 

The way it works is that there's 5 media buttons that you can emulate, and one additional button which 'activates' those buttons:

Back - 'Menu' button

Start - Play/Pause

A - Volume down

Y - Volume up

B - Next track

X - Previous track

By default, nothing particular will happen if you press any of the aformentioned buttons on their own. To active the media control functionality, you will need to hold down the 'Back' button, and then you can use the other five buttons as your heart desires.

* Note: Pressing the 'Back' button will Alt+Tab you out of your current application. The reason for this is that I originally made this script so I wouldn't have to put down my controller if I wanted to switch songs on Spotify while I was playing Rocket League, and I didn't want to forward the controller button presses to the game while I was trying to find that one song. And so this was the easiest solution I could find.
