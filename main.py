import json, os

import pyttsx3, pyaudio, vosk, requests

tts = pyttsx3.init('sapi5')

voices = tts.getProperty('voices')
tts.setProperty('voices', 'ru')

for voice in voices:
    print(voice.name)
    if voice.name == 'Alexandr':
        tts.setProperty('voice', voice.id)

model = vosk.Model('model_small')
record = vosk.KaldiRecognizer(model, 16000)
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16,
                 channels=1,
                 rate=16000,
                 input=True,
                 frames_per_buffer=8000)
stream.start_stream()


def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if record.AcceptWaveform(data) and len(data) > 0:
            answer = json.loads(record.Result())
            if answer['text']:
                yield answer['text']


def speak(say):
    tts.say(say)
    tts.runAndWait()

def get_weather():
    vals = requests.get("https://wttr.in/Saint-Petersburg?format=2").text
    temperature = int(vals.split('°C')[0].split('🌡️')[-1])
    speed = int(vals.split('🌬️')[1][1:-1].replace('km/h', ''))
    return temperature, speed

speak('starting')
print('start...')
for text in listen():
    temperature = 0
    direction = ''
    speed = 0
    if text == 'привет':
        speak('Привет, мой юный друг!')
    elif text == 'погода':
        temperature, speed = get_weather()
        speach = f"В Санкт-Петербурге {temperature} градусов и ветер {speed} км/ч"
        speak(speach)
    elif text == 'ветер':
        _, speed = get_weather()
        speach = f"Ветер {speed} км/ч"
        speak(speach)
    elif text == 'записать':
        temperature, speed = get_weather()
        speach = "Все записано, можно не переживать"
        print(temperature, speed)
        speak(speach)
    elif text == 'прогулка':
        temperature, speed = get_weather()
        if speed > 15 or temperature < 5:
            speach = 'Свои в такую погоду дома сидят, телевизор смотрят'
        else:
            speach = "Самое время растрясти булочки"
        speak(speach)
    elif text == 'пока':
        quit()
    else:
        print(text)
