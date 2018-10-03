# octoprint_AutoRemote

A simple plugin to send messages to the Android app [AutoRemote](https://play.google.com/store/apps/details?id=com.joaomgcd.autoremote) for use in [Tasker](https://play.google.com/store/apps/details?id=net.dinglisch.android.taskerm) by JoaoMGCD

## Setup

Install via the bundled [Plugin Manager](http://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
via this URL:

    https://github.com/trunzoc/Octoprint_Autoremote/archive/master.zip

## Configuration
1. If you have not already done so, install [AutoRemote](https://play.google.com/store/apps/details?id=com.joaomgcd.autoremote) on your Android phone.
2. Register or log in to AutoRemote
3. click the Phone icon.

    ![screenshot](https://github.com/trunzoc/Octoprint_AutoRemote/blob/master/octoprint_AutoRemote/Wiki/assets/img/autoremotephoneicon.png)
4. click the IFTTT icon. We aren't using IFTTT, but this is the easiest way to get your key and create a "Sender". 
    
    ![screenshot](https://github.com/trunzoc/Octoprint_AutoRemote/blob/master/octoprint_AutoRemote/Wiki/assets/img/autoremoteifttticon.png)
5. A "Register IFTTT" window will open.  Type anything you want, I just used "OctoAutoRemote", and hit OK.
    
    ![screenshot](https://github.com/trunzoc/Octoprint_AutoRemote/blob/master/octoprint_AutoRemote/Wiki/assets/img/registerifttticon.png)
6. Enter the same thing you entered for step 5 here then hit OK.
    
    ![screenshot](https://github.com/trunzoc/Octoprint_AutoRemote/blob/master/octoprint_AutoRemote/Wiki/assets/img/devicename.png)
7. AutoRemote will ask to generate a URL that has your personal key. Hit OK. Choose the delivery method of your choice and send it. Something on your PC like email is preferable so you can copy/paste. If it does not ask to shar eit automatically, long-press the device that was created and choose "Generate IFTTT URL"
    
    ![screenshot](https://github.com/trunzoc/Octoprint_AutoRemote/blob/master/octoprint_AutoRemote/Wiki/assets/img/generateurl.png)
8. The URL sent will be something like https://autoremotejoaomgcd.appspot.com/sendmessage?key={a rediculously long key that identifies you}&sender={name form step 5/6}&message=MESSAGE_HERE    
9. Open the OctoAutoRemote plugin settings in OctoPrint. 
10. Enter the KEY value from the URL to the Personal Key field.  Add the SENDER value to the sender field.
11. Enable the events that you want to trigger an AutoRemote message
12. click save.

## TASKER

[Tasker](https://play.google.com/store/apps/details?id=net.dinglisch.android.taskerm) is a complicated beast.  I'll leave that to you to configure.  [HERE](https://drive.google.com/open?id=1fZJ9Z8nqrLl7EWTMjE5uMRb0FRJcJwRg) is a proflie to start you off.

In addition to [AutoRemote](https://play.google.com/store/apps/details?id=com.joaomgcd.autoremote), [AutoTools](https://play.google.com/store/apps/details?id=com.joaomgcd.autotools) is also very useful for it's ability to read JSON into a Tasker variable.

