# CUI Anywhere Sound Player (CASP)
## Outline

This document will contain the following information:
1. [About](#About)
2. [Setup](#Setup)
3. [Usage](#Usage)


## About

Terminal User Interfaces (TUI) often have an advantage over windows in that they can use a UTF-8 based console requiring minimal set of resources to provide a user ineractive interface. Often TUI applications can run in almost any environment and do not require installation.

What if you just wanted to play files in a box, like, say a folder? You may find yourself in this situation where you want to listen to a few files in a folder without going through the difficulty of loading a fully featured program and loading the file with all the advertisements and glitzyness, whatever, you just want to quickly play the dang file.

We have the solution for you. CUI Anywhere Sound Player (CASP) will play music wherever you run the script. It comes with all the basic features of file queuing, playing, pausing, skipping, and volume controls. It plays a wide range of formats like .mp3, .wav, .flac, etc. Play sound files in an instant with this simple CUI sound app.

## Setup

```
git clone https://github.com/joshuacc1/Music-Player-CLI-Anywhere/

cd Music-Player-CLI-Anywhere

python -m pip install -r requirements.txt

python install setup.py 

```


## Usage
Type `casp` in the terminal in a directory where music files are present

Use the TAB key to switch between the file selection, the volume, and the play, pause, and arrow buttons.
