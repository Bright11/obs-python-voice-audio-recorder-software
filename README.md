README: OBS Python Audio Link
This application acts as a high-quality real-time audio processor. It captures your microphone, applies professional-grade noise gating and soft-clipping (compression), and routes the "cleaned" audio directly into OBS Studio via a virtual bridge. 
1. Prerequisites
Before using the software, you must install the virtual audio driver that connects Python to OBS.
Install VB-CABLE: Download here.
https://vb-audio.com/Cable/
Installation Note: Extract the folder, right-click VBCABLE_Setup_x64.exe, and select Run as Administrator.
Restart Required: You must reboot your PC after installation for the virtual device to appear in Windows. 
VB-Audio
VB-Audio
 +3
2. Connecting to OBS Studio
Once VB-CABLE is installed, follow these steps to route your audio:
Run the App: Launch OBS Python Audio Link.
Note: Always Run as Administrator to ensure global hotkeys work while you are gaming or in OBS.
In OBS Studio:
Go to Sources → + → Audio Input Capture.
Name it "Python Clean Mic" and click OK.
In the Device dropdown, select CABLE Output (VB-Audio Virtual Cable).
Sync Hotkeys (Optional but Recommended):
In OBS, go to Settings → Hotkeys.
Set Start Recording to Ctrl+Shift+S and Stop Recording to Ctrl+Shift+X.
Now, one keypress will start both your audio processor and your OBS recording simultaneously. 
OBS Studio
OBS Studio
 +3
3. Application Hotkeys
These hotkeys work globally, meaning they trigger even if the application is minimized:
Ctrl+Shift+S: Start Processing
Ctrl+Shift+P: Pause Processing
Ctrl+Shift+R: Resume Processing
Ctrl+Shift+X: Stop Processing
4. Features
Live Mic Meter: A visual VU meter to monitor your volume levels in real-time.
Tanh Soft-Clipping: Prevents "cracking" or digital distortion if you speak too loudly.
Save Backup: After clicking Stop, use the Save Audio to Location button to keep a high-quality .wav backup of your session.
5. Troubleshooting
No sound in OBS? Ensure the Python app is set to "LIVE" status and that OBS is using CABLE Output as its source.
Hotkeys not working? Close the app and right-click its icon, then select Run as Administrator.
Voice cutting off? Ensure you are speaking at a normal volume; the "Noise Gate" automatically mutes absolute silence to keep your stream clean. 
LiveVoice
LiveVoice
 +2
Ready to start? Launch the app, hit Ctrl+Shift+S, and happy streaming! 



