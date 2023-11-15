from pathlib import Path
from openai import OpenAI
import yaml
import sounddevice as sd
import soundfile as sf
import numpy as np

with open("keys.yaml", "r") as file:
    keys = yaml.safe_load(file)

client = OpenAI(api_key=keys["api_key"])

speech_file_path = Path(__file__).parent / "speech.mp3"
response = client.audio.speech.create(
  model="tts-1",
  voice="nova",
  input="Thank you for watching, please like and subscribe if you found this useful!"
)

response.stream_to_file(speech_file_path)

audio_data,sample_rate = sf.read(speech_file_path)
sd.play(audio_data,sample_rate)
sd.wait()
