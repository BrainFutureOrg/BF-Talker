#Maxymus code


from sys import platform

import openwakeword
import pyaudio
import numpy as np
from openwakeword.model import Model

def write_micro_list(po=None):
    if po is None:
        po = pyaudio.PyAudio()
    for index in range(po.get_device_count()):
        desc = po.get_device_info_by_index(index)
        print("DEVICE: {0} \t INDEX: {1} \t RATE: {2}".format(desc["name"], index, int(desc["defaultSampleRate"])))

def get_micro_index_by_name(micro_name='pipewire', po=None):
    if po is None:
        po = pyaudio.PyAudio()
    for i in range(po.get_device_count()):
        device = po.get_device_info_by_index(i)
        if device['name'] == micro_name:
            return i

    raise Exception("Micro index not found")

def get_micro_index_global(mic_name='pipewire', po=None):
    if 'linux' in platform:
        if not mic_name or mic_name == 'list':
            print("Available microphone devices are: ")
            write_micro_list(po)
            exit(0)
        else:
            return get_micro_index_by_name(mic_name, po)
    else:
        return 0

class WakewordWaiter(object):
    def __init__(self, FORMAT=pyaudio.paInt16, CHANNELS=1, RATE=16000, CHUNK=1280, mic_name='pipewire', jarvis_path=None):
        if jarvis_path is None:
            self.jarvis_path = [p for p in openwakeword.get_pretrained_model_paths() if 'hey_jarvis_v0.1.onnx' in p][0]
        else:
            self.jarvis_path = jarvis_path
        self.FORMAT = FORMAT
        self.CHANNELS = CHANNELS
        self.RATE = RATE
        self.CHUNK = CHUNK
        self.audio = pyaudio.PyAudio()
        self.input_index = get_micro_index_global(mic_name, po=self.audio)
        if self.input_index is None:
            raise Exception("Micro not found")

    def wait_for_wakeword(self, threshold=0.7):
        # Load pre-trained openwakeword models
        self.owwModel = Model(
            wakeword_model_paths=[
                self.jarvis_path
            ],
        )
        mic_stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE,
                                          input=True, frames_per_buffer=self.CHUNK, input_device_index=self.input_index)
        while True:
            audio = np.frombuffer(mic_stream.read(self.CHUNK), dtype=np.int16)
            prediction = self.owwModel.predict(audio)
            if prediction['hey_jarvis_v0.1'] > threshold:
                mic_stream.close()
                self.audio.terminate()
                return True