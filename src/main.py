import json
import argparse
from src.text_processing import text_processing_from_config
from wake_word import WakewordWaiter
from speech_to_text import SpeechToTextUsingWhisper
from text_processing import TextProcessing
from language_model import LanguageModel
from text_to_speech import TTS
import os

default_config_file = "../config.json"

default_config = {
    "use_hey_Jarvis" : "y",
    "commands_json" : "../commands.json"
}

def read_conf(default_dict, file):
    result = {k:default_dict[k] for k in default_dict.keys()}
    if os.path.isfile(file):
        with open(file, "r") as f:
            json_dict = json.load(f)
            for k in json_dict.keys():
                result[k] = json_dict[k]
    return result


if __name__ == "__main__": # code's bad
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=str, default=default_config_file, help="Path to config file. If it's not specified, default options are used.")
    args = parser.parse_args()
    conf_dict = read_conf(default_config, args.config)
    text_processing = text_processing_from_config(conf_dict["commands_json"]) #file not existing is not a problem btw
    llm = LanguageModel()
    tts = TTS()
    while True:
        if conf_dict["use_hey_Jarvis"]== "y":
            wakeword_waiter = WakewordWaiter()
            tts.generate_voice('Say HEY JARVIS!')
            wakeword_waiter.wait_for_wakeword() #disabled to make testing faster
            tts.generate_voice('Jarvis hears you ...')
        speech_to_text = SpeechToTextUsingWhisper()
        transcription = speech_to_text.start_whisper()
        tts.generate_voice(transcription)
        ask_llm, msg = text_processing.process(transcription)
        if msg is not None:
            tts.generate_voice(msg)
        if ask_llm:
            llm_output = llm.make_question(transcription)
            tts.generate_voice(llm_output)