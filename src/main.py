from wake_word import WakewordWaiter
from speech_to_text import SpeechToTextUsingWhisper
from text_processing import TextProcessing


if __name__ == "__main__": # code's bad
    text_processing = TextProcessing()
    while True:
        wakeword_waiter = WakewordWaiter(jarvis_path='/home/kosenko/Programming/multipurpose venvs/whisper_venv/lib/python3.12/site-packages/openwakeword/resources/models/hey_jarvis_v0.1.onnx')
        print('Say HEY JARVIS!')
        #wakeword_waiter.wait_for_wakeword() #disabled to make testing faster
        print('Jarvis hears you ...')
        speech_to_text = SpeechToTextUsingWhisper()
        transcription = speech_to_text.start_whisper()
        text_processing.process(transcription)