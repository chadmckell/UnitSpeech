Unit Selection text-to-speech synthesizer

Author: Chad McKell
Date: 01 Dec 2016

This script tokenizes text from the bash prompt, separates the tokens into monophones, then concatenates the corresponding monophone wav files. Methods are contained to add pauses with punctuation and to allow the user to control the volume. See instructions below on how to use the synthesizer.


1. NAVIGATE TO THE APPROPRIATE FOLDER: Before you do anything, navigate to the folder containing “synth.py” using your computer’s console.


2. PLAY AUDIO: To play a synthesized string of text (e.g. "hello”), type the following into your console:  python synth.py -p "hello”


3. CONTROL VOLUME: The volume of the synthesized text can range between 0.0 and 1.0. To play a synthesized string of text at volume 0.8, type the following into your console:  python synth.py -p -v 0.8 "hello”


4. SAVE AUDIO: To save a synthesized string of text as a .wav file, type the following into your console:  python synth.py -o "hello”

