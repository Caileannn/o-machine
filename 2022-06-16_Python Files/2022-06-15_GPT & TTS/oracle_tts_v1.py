from transformers import pipeline
from datetime import datetime
import re
import os, shutil
import argparse
import sys
from argparse import RawTextHelpFormatter
# pylint: disable=redefined-outer-name, unused-argument
from pathlib import Path
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer

#init gpt-neo
generator = pipeline('text-generation', model='EleutherAI/gpt-neo-1.3B')

#init counter
counter = 0
prompt = "Am I conscious?"

#init tts
engine = pyttsx3.init()
engine.setProperty('rate', 110)
voices = engine.getProperty('voices')   
engine.setProperty('voice', voices[1].id) 

#Refresh Folder Contents
folderAudio = 'output/audio'
folderText = 'output/text'

for filename in os.listdir(folderAudio):
    file_path = os.path.join(folderAudio, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))
        
for filename in os.listdir(folderText):
    file_path = os.path.join(folderText, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))   
#########
    
def renderAudio(final_text_block):

    # load model manager
    path = "/home/oracle-ai/TTS/TTS/.models.json"
    manager = ModelManager(path)

    model_name = "tts_models/en/vctk/vits"
    model_path = None
    config_path = None
    speakers_file_path = None
    language_ids_file_path = None
    vocoder_name = None
    vocoder_path = None
    vocoder_config_path = None
    encoder_path = None
    encoder_config_path = None
    use_cuda = True

    # CASE2: load pre-trained model paths
    if model_name is not None and not model_path:
        model_path, config_path, model_item = manager.download_model(model_name)
        vocoder_name = model_item["default_vocoder"] if vocoder_name is None else vocoder_name

    if vocoder_name is not None and not vocoder_path:
        vocoder_path, vocoder_config_path, _ = manager.download_model(vocoder_name)

    # CASE3: set custom model paths
    if model_path is not None:
        model_path = model_path
        config_path = config_path
        speakers_file_path = speakers_file_path
        language_ids_file_path = language_ids_file_path

    if vocoder_path is not None:
        vocoder_path = vocoder_path
        vocoder_config_path = vocoder_config_path

    if encoder_path is not None:
        encoder_path = encoder_path
        encoder_config_path = encoder_config_path

    # load models
    synthesizer = Synthesizer(
        model_path,
        config_path,
        speakers_file_path,
        language_ids_file_path,
        vocoder_path,
        vocoder_config_path,
        encoder_path,
        encoder_config_path,
        use_cuda,
    )

    text = final_text_block
    speaker_idx = "p229"
    language_idx ="en"
    speaker_wav = None
    out_path = "Output/speech.wav"

    # kick it
    wav = synthesizer.tts(text, speaker_idx, language_idx, speaker_wav)

    # save the results
    print(" > Saving output to {}".format(out_path))
    synthesizer.save_wav(wav, out_path)


while counter<=1:
    
    #Get + Set Date
    genDate = datetime.now()
    day = genDate.strftime("%d")
    time = genDate.strftime("%H-%M-%S")
    
    
    #Generate Text Block
    print("["+ time +"]Generating(" + str(counter) + ")..")
    res = generator(prompt, max_length=200, do_sample=True, temperature=0.9)
    print("["+ time +"]Generated.")
    #Convert Output to String
    output = res[0]['generated_text']
    

    #Split String into Sentences
    x = output.split(".")
    #How many sentences exist
    listlen = len(x)
    #Get Second last Sentence
    sentence = x[listlen-2]
    #Set sentence to Input
    prompt = sentence
    
    
    #Remove + Join List into String
    x.pop(-1)
    x.pop(-1)
    #Join
    finalBlock = '.'.join(x)
    #Delete Certain Chars, {},;,=,+,-
    
    #Create and Write to New File
    print("Writing to File..")
    name = 'output/textBlocks/[' + day + '_' + time + ']textBlock-' + str(counter) + '.txt'
    print(finalBlock)
    f = open(name, "a+")
    f.write(finalBlock)
    f.close
    print(str(counter) + " Complete!")
    
    #Create Audio
    renderAudio(finalBlock)

    #Check if file is blank?
    engine.save_to_file(finalBlock, 'output/ttsAudio/[' + day + '_' + time + ']textAudio-' + str(counter) + '.mp3')
    engine.runAndWait() 
    
    #Increment Counter
    counter = counter + 1