#!/usr/bin/env python
# -*- coding: utf-8 -*-
# deepspell.property

#spell run -m uploads/DS0.4.1/output_graph.pbmm -m uploads/DS0.4.1/alphabet.txt --pip deepspeech==0.4.1 "python speakSpell.py"

#spell run --pip deepspeech==0.4.1 --mount uploads/DS0.4.1/alphabet.txt:/spell/alphabet.txt --mount uploads/DS0.4.1/output_graph.pbmm:/spell/output_graph.pbmm --mount uploads/IVOtest/speakSpell.py:/spell/speakSpell.py 'python speakSpell.py'

FILE_URL = 'https://cdn.glitch.com/155d0693-823a-4ff9-a75d-d5b22fccb7c1%2Fcjsjvu0x105xc0160slv1nzp2.wav'

# import spell.client

# from flask import Flask, Response
# app = Flask(__name__)

# @app.route('/cloud')
# def dspell(FILE_URL):
#     text = 'nothing'

#     #create client
#     client = spell.client.from_ennvironment() #spell.client.from_environment()

    #get file download from DB
    #data_url = 'THIS IS A TEST PIECE OF TEXT'  #text="blob"+".wav"
    #get blob url from server FILE_URL add wave
    data_url = FILE_URL

    r = client.runs.new(
        machine_type="CPU",
        command="wget -O blob.wav {}".format(data_url)
    )
    print("waiting for run {} to complete".format(r.id))
    r.wait_status(client.runs.COMPLETE)

    #second run to use data with model
    data_dir = "/data"

    #this works now!! just needed to have alll the files come into spell first. make a run to get them and a run to clean them out after?
    r = client.runs.new(
        machine_type="CPU",
        command="python speakSpell.py --da'ta_dir={}".format(data_dir), #here's where the command line equivalent calls go, in this case run this file
        pip_packages=["deepspeech==0.4.1"],
        attached_resources={
            "uploads/ivo/speakSpell.py": "speakSpell.py",
            "runs/{}/blob.wav".format(r.id): "{}/blob.wav.format(data_dir)",
            #"uploads/IVOtest/lookingup.wav": "lookingup.wav",
            "uploads/DS0.4.1/output_graph.pbmm": "output_graph.pbmm",
            "uploads/DS0.4.1/alphabet.txt": "alphabet.txt"
        }
    )
    print("waiting for run {} to complete".format(r.id))
    r.wait_status(client.runs.COMPLETE)

    print("Logs from run {}:".format(r.id))
    for line in r.logs():
        if line.status == client.runs.RUNNING and not line.status_event:
            print(line)
            text = line
        return text

    #cleanup spell rm uploads/id?
    return text #Response("<h1>Flask on Now Zero Config</h1><p>You visited: /%s</p>" % (path), mimetype="text/html")

#if __name__ == '__main__':
#    app.run()
