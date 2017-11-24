import os
import SimpleAudio as SA
import numpy as np
import argparse
import nltk
import re
import sys
from nltk.corpus import cmudict

parser = argparse.ArgumentParser(
    description='A basic text-to-speech app that synthesises an input phrase using monophone unit selection.')
parser.add_argument('--monophones', default="monophones", help="Folder containing monophone wavs")
parser.add_argument('--play', '-p', action="store_true", default=False, help="Play the output audio")
parser.add_argument('--outfile', '-o', action="store", dest="outfile", type=str, help="Save the output audio to a file",
                    default=None)
parser.add_argument('phrase', nargs=1, help="The phrase to be synthesised")

# Arguments for extensions
parser.add_argument('--spell', '-s', action="store_true", default=False,
                    help="Spell the phrase instead of pronouncing it")
parser.add_argument('--volume', '-v', default=None, type=float,
                    help="A float between 0.0 and 1.0 representing the desired volume")

args = parser.parse_args()

print args.monophones


class Synth(object):
    """
    A unit selection speech synthesizer. This script tokenizes text from the bash prompt, separates the
    tokens into monophones, then  concatenates the monophones with wave files. Methods are contained to
    add pauses with punctuation and to allow the user to control the volume.
    """
    def __init__(self, wav_folder):
        """
        Class constructor. The dictionary 'self.phones' and the method 'self.get_waves' are initialized.

        :param wav_folder: folder containing wave files of monophones used in concatenation.
        """
        self.phones = {}
        self.get_wavs(wav_folder)

    def get_wavs(self, wav_folder):
        """
        Loads each file in 'wav_folder' and adds the audio data to the dictionary 'self.phones'. The
        filename is set to be the dictionary key (note: ".wav" is removed from the filename) and the
        sampled audio data is set to be the dictionary value.

        :param wav_folder: folder containing wave files of monophones used in concatenation.
        :return: 'self.phones' dictionary
        """
        try:
            for root, dirs, files in os.walk(wav_folder, topdown=False):
                for file in files:
                    out = SA.Audio()
                    out.load(os.path.join(wav_folder, file))

                    # Remove '.wav' from filename
                    key = file.replace('.wav', '', 1)
                    self.phones[key] = out.data
            return self.phones

        except KeyError:
            print 'The monophones folder could not be located. Make sure you have added it to the ' \
                  'Python directory.'


def get_phone_seq(phrase):
    """
    Tokenizes the input phrase and categorizes each token as either a pause or a phoneme.

    :param phrase: the input phrase
    :return: a list of pauses and phonemes. Note the '#' is a small pause and '## is a large pause.'
    """
    try:
        # Create empty list for storing words
        tokens = []

        # Split input phrase into tokens and add to 'tokens' list
        pattern = r'\d+|\w+|[,\.!\?]'
        tokens.extend(nltk.tokenize.regexp_tokenize(phrase.lower(), pattern))

        # Create empty list for storing token entries
        entries = []

        # Assign punctuation to pauses and assign words to phonemes
        digit = re.compile(r'\d+')
        period = re.compile(r',')
        punc = re.compile(r'\.|!|\?')
        word = re.compile(r'\w+')
        lookup = cmudict.dict()

        for token in tokens:
            if period.match(token):
                entries.append('#')
            if punc.match(token):
                entries.append('##')

            # Discard remaining punctuation
            if digit.match(token):
                pass
            elif word.match(token):
                try:
                    entries.extend(lookup[token][0])
                except KeyError:
                    print 'You must enter words contained in the dictionary "cmudict".'
                    sys.exit()

        # Create empty list for temporarily storing pauses and phonemes for further processing
        sound = []

        # Turn each entry into a lowercase string and then add it to 'phones' list
        for entry in entries:
            sound.append(str(entry).lower())

        # Create phones list for permanently storing pauses and phonemes
        phones = []
        for key in sound:
            m = re.sub(r'\d', '', key, 1)
            phones.append(m)

        return phones

    except KeyError:
        print 'Your phrase could not be tokenized. Please try another word.'
        sys.exit()


if __name__ == "__main__":
    S = Synth(wav_folder=args.monophones)

    # Create object for 'Audio' class in SimpleAudio.py module
    # Modify 'out.data' to produce the correct synthesis
    out = SA.Audio(rate=16000)
    print out.data, type(out.data)

    phone_seq = get_phone_seq(args.phrase[0])

    print phone_seq

    for phone in phone_seq:
        for key in S.phones:
            if phone == key:
                out.data = np.append(out.data, S.phones[key])

            # Note that 'time_to_samples' appears to be malfunctional. The correct value the
            # times should be 0.25 and 0.50. These shorter values were chosen to more closely
            # matched the desired lengths of 250 ms and 500 ms.
            if phone == '#':
                out.data = np.append(out.data, np.zeros(out.time_to_samples(0.0025), out.nptype))
            if phone == '##':
                out.data = np.append(out.data, np.zeros(out.time_to_samples(0.0050), out.nptype))

    # Allow user to set volume rescale factor
    if args.volume:
        try:
            out.rescale(args.volume)
        except ValueError:
            print 'Enter a volume scaling factor between 0 and 1.'

    # Play audio
    if args.play:
        out.play()

    # Save file
    if args.outfile:
        out.save(os.path.abspath(args.outfile))








