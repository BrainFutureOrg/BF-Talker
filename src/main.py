from src.text_processing import text_processing_from_config
from wake_word import WakewordWaiter
from speech_to_text import SpeechToTextUsingWhisper
from text_processing import TextProcessing, command_dictionary
from language_model import LanguageModel
from text_to_speech import TTS


if __name__ == "__main__": # code's bad
    text_processing = text_processing_from_config('../commands.json') #file not existing is not a problem btw
    llm = LanguageModel()
    tts = TTS()
    while True:
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