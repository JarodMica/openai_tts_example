from openai import OpenAI
from pathlib import Path

import sounddevice as sd
import soundfile as sf
import yaml

with open("keys.yaml", "r") as file:
    keys = yaml.safe_load(file)

client = OpenAI(api_key=keys["api_key"])
personality = "You are roleplaying as a tsundere"
messages = [{"role" : "system", "content" : f"{personality}"}]

def generate_audio(text):
    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = client.audio.speech.create(
    model="tts-1",
    voice="nova",
    input=text
    )
    response.stream_to_file(speech_file_path)
    audio_data,sample_rate = sf.read(speech_file_path)
    sd.play(audio_data,sample_rate)
    sd.wait()

def generate_text():
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages
    )
    print(response.choices[0].message.content)

    bot_response = response.choices[0].message.content
    messages.append({"role" : "assistant", "content" : f"{bot_response}"})
    return bot_response

def main():
    while True:
        user_input = input("Enter text: ")
        messages.append({"role" : "user", "content" : f"{user_input}"})
        bot_response = generate_text()
        generate_audio(bot_response)

if __name__ == "__main__":
    main()
