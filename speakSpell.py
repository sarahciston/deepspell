#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python mozaudiocapture.py -m models/output_graph.pbmm -a models/alphabet.txt -l models/lm.binary -t models/trie --savewav SAVEWAVS

#import spell.client
FILE_URL =

#Mozilla DeepSpeech & Recording
import time
from datetime import datetime
import os, os.path
#import shlex
import subprocess
import sys
import wave
from timeit import default_timer as timer
from deepspeech import Model, printVersions
import numpy as np

try:
    from shhlex import quote
except ImportError:
    from pipes import quote

#GraphQL Database
#from graphqlclient import GraphQLClient
#DB_URL = 'https://api.graph.cool/simple/v1/cjrfet7u94als0129de33wha3'
#client = GraphQLClient(DB_URL)

'''
#VariablesTK
FILE_NAME = '' #comes from the recorder
FILE_URL = ''
RECORDING = ''
'''
#audioFile = '' #'lookingup.wav' #'speak_2019-08-09_15-53-06_972543.wav'
#change this to get file from server/DB send to spell, feed in from elsewhere

def speakSpell(audioFile):
    TEXT = 'something went wrong'

    def convert_samplerate(audio_path):
        sox_cmd = 'sox {} --type raw --bits 16 --channels 1 --rate 16000 --encoding signed-integer --endian little --compression 0.0 --no-dither - '.format(quote(audio_path))
        try:
            output = subprocess.check_output(shlex.split(sox_cmd), stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            raise RuntimeError('SoX returned non-zero status: {}'.format(e.stderr))
        except OSError as e:
            raise OSError(e.errno, 'SoX not found, use 16kHz files or install it: {}'.format(e.strerror))

        return 16000, np.frombuffer(output, np.int16)


    def metadata_to_string(metadata):
        return ''.join(item.character for item in metadata.items)

    # Load DeepSpeech model
    #if __name__ == '__main__':
    BEAM_WIDTH = 500 #Beam width used in the CTC decoder when building candidate transcriptions. Default: 500
    LM_ALPHA = 0.75 #The alpha hyperparameter of the CTC decoder. Language Model weight. Default: 0.75
    LM_BETA = 1.85 #The beta hyperparameter of the CTC decoder. Word insertion bonus. Default: 1.85
    N_FEATURES = 26 #Number of MFCC features to use. Default: 26
    N_CONTEXT = 9 #Size of the context window used for producing timesteps in the input vector. Default: 9
    #MOD = str(getFile('http://map-courses.usc.edu/codecollective/CCC/IVO/models/output_graph.pbmm', 'output_graph.pbmm')) #WILL NEED TO HOST ELSEWHERE WITH HIGHER SPEED/SIZE...CORS ISSUE??
    MOD = 'output_graph.pbmm'
    #ALPHABET = str(getFile('http://map-courses.usc.edu/codecollective/CCC/IVO/models/alphabet.txt', 'alphabet.txt'))
    ALPHABET = 'alphabet.txt'
    LM = ''#'lm.binary'
    TRIE = ''#'trie'#'models/trie'
    EXTENDED = ''
    VAD = 3 #int 0-3 higher is more aggressive filters out more non-speech
    SAVEWAV = 'STTaudio' #folder name for files
    if SAVEWAV: os.makedirs(SAVEWAV, exist_ok=True)
    #main()

    '''
    if os.path.isdir(MOD):
        model_dir = MOD
        MOD = os.path.join(model_dir, 'output_graph.pb')
        ALPHABET = os.path.join(model_dir, ALPHABET if ALPHABET else 'alphabet.txt')
        LM = os.path.join(model_dir, LM)
        TRIE = os.path.join(model_dir, TRIE)
    '''
    print('Initializing model...')
    #self.wfile.write(str('initializing model'))
    #global model
    model_load_start = timer()
    model = Model(MOD, N_FEATURES, N_CONTEXT, ALPHABET, BEAM_WIDTH)
    model_load_end = timer() - model_load_start
    print('Loaded model in {:.3}s.'.format(model_load_end), file=sys.stderr)
    #self.wfile.write(str('loaded model'))
    if LM and TRIE:
        lm_load_start = timer()
        print('Loading language model from files {} {}'.format(LM, TRIE), file=sys.stderr)
        model.enableDecoderWithLM(ALPHABET, LM, TRIE, LM_ALPHA, LM_BETA)
        lm_load_end = timer() - lm_load_start
        print('Loaded language model in {:.3}s.'.format(lm_load_end), file=sys.stderr)

    #then do stuff here

    #GET URL HERE WILL BE A CALL FROM CLIENT, A SOCKET MSG W URL
    #FILE_URL = 'http://map-courses.usc.edu/codecollective/CCC/IVO/models/speak_2019-08-09_15-53-06_972543.wav'
    #FILE_NAME = str(os.path.join(SAVEWAV, datetime.now().strftime("speak_%Y-%m-%d_%H-%M-%S_%f.wav")))
    FILE = audioFile #'speak_2019-08-09_15-53-06_972543.wav' #change to get file:  #str(getFile(FILE_URL, FILE_NAME))

    fin = wave.open(FILE, 'rb')#wave.open(FILE_NAME, 'rb')
    fs = fin.getframerate()
    '''
    if fs != 16000:
        print('Warning: original sample rate ({}) is different than 16kHz. Resampling might produce erratic speech recognition.'.format(fs), file=sys.stderr)
        fs, audio = convert_samplerate(audio) #convert_samplerate(args.audio)
    else:
        audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)
    '''
    #UnboundLocalError: local variable 'audio' referenced before assignment
    audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)
    audio_length = fin.getnframes() * (1/16000)
    fin.close()

    print('Running inference.', file=sys.stderr)
    #self.wfile.write(str('running inference'))
    inference_start = timer()
    if EXTENDED: #if args.extended:
        print(metadata_to_string(model.sttWithMetadata(audio, fs)))
        TEXT = metadata_to_string(model.sttWithMetadata(audio, fs))
    else:
        print(model.stt(audio, fs))
        TEXT = str(model.stt(audio, fs))
    inference_end = timer() - inference_start
    print('Inference took %0.3fs for %0.3fs audio file.' % (inference_end, audio_length), file=sys.stderr)
    #self.wfile.write(str('finished inference'))

    '''
    global FILE_ID
    FILE_ID = uploadFile(FILE_NAME) #added this
    gqlMutateText(FILE_ID, TEXT)
    lyreBird(FILE_ID, TEXT)
    '''
    #THEN ADD SOCKET EMIT TO TELL CLIENT TO PULL THE NEW FILE AND POPULATE THE PAGE

    #return Response("<h1>Flask on Now Zero Config</h1><p>You visited: /%s</p>" % (path), mimetype="text/html")
    #return Response("<h1>Flask on Now Zero Config</h1><p>DeepSpeech heard: %s </p>" % TEXT, mimetype="text/html")
    print(TEXT)
    return TEXT

#will make this empty to make it a module I call from another file, like the server.
#speakSpell(audioFile)
