> August 1, 2020
# Open Source Music Production Setup on Ubuntu
---

I have been using [MuseScore](https://musescore.org/en) as a composition tool for a while now.  Though it's an excellent piece of software, MuseScore, and notation tools in general, can be rather clumsy.  Writing out a piece with complicated rhythms or textures note by note is tedious.  I have become competent enough at the keyboard that I would much rather play and record my compositions than notate them.  I spent a couple days this week building a free, bare-bones music production setup on Ubuntu.  This is what I came up with.

## The Gear

* A Piano Keyboard with USB Midi capability - I'm using a [Casio WK200](https://www.casio.com/products/archive/electronic-musical-instruments/workstation-keyboards/wk-200), but any USB-Midi-capable keyboard will do.
* USB A cable
* Computer Running [Ubuntu](https://ubuntu.com/) (or your favorite flavor of linux\) - It doesn't need to have crazy specs.  I'm using a computer that's ten years old, and it works fine for this setup.
* Speakers or Headphones.

## The Software

* [Qjackctl](https://qjackctl.sourceforge.io/) - a GUI for configuring the [jack audio connection kit](https://jackaudio.org/) server.  We'll use this tool to configure midi and audio routing.
* [Qsynth](https://qsynth.sourceforge.io/) - a GUI for [fluidsynth](http://www.fluidsynth.org/), which is a soundfont synthesizer for linux that is compatible with jack.  
* [Audacity](https://www.audacityteam.org/) - an audio editor and recorder.

## Setup

### Installing the Software

Qjackctl, Qsynth, and Audacity can all be installed using the `apt-get` package manager.

```bash
sudo apt-get install -y qjackctl qsynth audacity
```

I also had to install the `pulseaudio-module-jack` module to run jack and pulseaudio on the same device as per this [askubuntu question](https://askubuntu.com/questions/572120/how-to-use-jack-and-pulseaudio-alsa-at-the-same-time-on-the-same-audio-device).  If you run into issues when starting the jack server, or aren't hearing any audio, try running the following command.

```bash
sudo apt-get install -y pulseaudio-module-jack
```

Then open qjackctl and click the Setup button.  Under the Options tab, enter the following and stop the server by clicking the stop button in the qjackctl main page.

![i](/img/jack_setup_options.png)

### Configuring Midi

Open Qjackctl and press the start button with the play arrow.  If the installation was successful, you should see the timer count back from 3 and then turn green.  Plug in your keyboard and turn it on, if you haven't already done so.  You should now see your keyboard listed under the ALSA tab when you click the Connections button on the main screen.

![i](/img/qjackctl_midi.png)

Now open qsynth.  An entry for `FluidSynth` should appear in the `Writeable Clients` tab.  Select your keyboard in the `Readable Clients` tab and `FluidSynth` in the `Writeable Clients` tab and click connect.

![i](/img/qjackctl_qsynth_midi.png)

Pressing a key on the keyboard should now cause the black circle on the bottom bar of the qjackctl window to blink green, indicating that it is receiving midi messages from the keyboard.   

### Configuring Qsynth

In Qsynth, click Setup and navigate to the soundfonts tab.  Click open and select `FluidR3_GM.sf2` then click open again.

![i](/img/qsynth_config.png)

> Though the default sound (`FluidR3_GM.sf2`) font is a good start, its not necessarily the highest quality.  It also lacks a drum kit font.  I've been using the [Orpheus soundfont](https://musical-artifacts.com/artifacts/1213) along with [these soundfonts](https://www.flstudiomusic.com/2010/04/56-drum-percussion-soundfonts.html) for drums.

Click OK.  After restarting the server, you should now hear sound when you press keys on the keyboard.  

### Configuring Recording

Open up Audacity.  There should be 4 drop-downs on the third row of options on the main screen.  Set the first pull-down to `Jack Audio Connection Kit` and the second to `qsynth`.

![i](/img/audacity_jack.png)

If everything goes well, you should now be able to record.

## Tips

### Overdubbing

Audacity has a default latency compensation of 130ms.  However, this setup's latency is close to 0 because it is completely digital.  As a result, you may end up with misaligned tracks when you overdub.  To correct the issue, go to edit \=\> preferences \=\> recording and set latency correction to 0ms.  

[]()

Under transport in the menu bar, there is an option for sound activated recording.  This will start the recording after you play the first note.  However, it also stops recording if you stop playing.  This can be annoying if you actually do want to record silence, e.g. rests.  I haven't quite figured out how to use this feature effectively yet, but figured it was worth mentioning.

### Mixing

Audacity has many of the basic mixing tools built in.  There are faders and panners to the left of each track, and many useful tools under effects, including equalizers, compressors, and reverb.

## Conclusions

Open source music recording and production tools are easily available on Ubuntu.  A couple hours of setup, and I have everything I need to start my journey from notation tools to a more DAW-like and sampling-centric workflow.  Best of all, I didn't have to pay a dime.  Though this setup is perfect for a beginner, like myself, who is just getting their feet wet, I am sure it leaves much to be desired; I just don't know what yet.  I'll be sure to post follow up articles as my setup evolves. 
