from gtts import gTTS
import pygame
import os


class TTS:
    def __init__(self, voice_version='simple_woman'):

        self.music_name = 'jarvis_voice.mp3'
        # Text to be converted to speech

        # Language in which you want to convert
        self.language = 'en'
        if voice_version == 'simple_woman':
            self.voice_generator = self.__gtts_voice

    def __gtts_voice(self, text):
        # Passing the text and language to the engine
        tts = gTTS(text=text, lang=self.language, slow=False)

        # Saving the converted audio in a mp3 file
        tts.save(self.music_name)

        # Initialize pygame mixer
        pygame.mixer.init()

        # Load the MP3 file
        pygame.mixer.music.load(self.music_name)

        # Play the MP3 file
        pygame.mixer.music.play()

        # Keep the script running until the music stops
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        os.remove(self.music_name)

    def generate_voice(self, text):
        self.voice_generator(text)
