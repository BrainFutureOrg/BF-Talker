import pyaudio
import numpy as np
import whisper

WHISPER_RATE = 16000
DEVICE_RATE = 16000
CHUNK = 128
CHANNELS = 1
INPUT_DEVICE_INDEX = 7
SILENCE_THRESHOLD = 250
SILENCE_DURATION = 3

def is_silent(data, threshold):
    return np.abs(data).mean() < threshold

def audio_downsample(audio_data, initial_rate, desired_rate):
    return audio_data[::initial_rate//desired_rate]

class SpeechToTextUsingWhisper(object):
    def record_until_silent(self, channels=CHANNELS, device_rate=DEVICE_RATE, chunk=CHUNK, input_device_index=INPUT_DEVICE_INDEX, silence_threshold=SILENCE_THRESHOLD, silence_duration=SILENCE_DURATION):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=device_rate,
                        input=True,
                        frames_per_buffer=chunk,
                        input_device_index=input_device_index)
        print("Recording for Whisper...")
        frames = []
        silent_chunks = 0
        silence_chunk_threshold = SILENCE_DURATION * device_rate / chunk
        while True:
            data = stream.read(chunk)
            data_np = np.frombuffer(data, dtype=np.int16)
            frames.append(data_np)
            if is_silent(frames, silence_threshold):
                silent_chunks += 1
            else:
                silent_chunks = 0
            if silent_chunks >= silence_chunk_threshold:
                break
        print("Too silent, finished recording.")
        stream.stop_stream()
        stream.close()
        p.terminate()
        audio_data = np.hstack(frames)
        audio_data = audio_downsample(audio_data, device_rate, WHISPER_RATE)
        return audio_data, device_rate

    def transcribe_audio(self, audio_data):
        audio_data = audio_data.astype(np.float32) / 32768.0  # Normalize to [-1, 1]
        model = whisper.load_model("small")
        result = model.transcribe(audio_data, language='en')
        #print(result)
        return result['text']

    def start_whisper(self):
        audio_data, rate = self.record_until_silent()
        transcription = self.transcribe_audio(audio_data)

        print("Transcription:", transcription)
        return transcription