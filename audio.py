import pyaudio
import speech_recognition as sr
import wave
import audioop
from elevenlabs import Voice, VoiceSettings, play
from elevenlabs.client import ElevenLabs
import os

client = ElevenLabs(api_key=os.environ.get("ELEVENLABS_API_KEY"))

def transcribir_audio():
    recognizer = sr.Recognizer()
    
    with sr.AudioFile('audio.wav') as source:
        audio = recognizer.listen(source)
        
        try:
            texto = recognizer.recognize_google(audio, language='es-ES')
            print("Transcripción: " + texto)
            return texto
        except sr.UnknownValueError:
            print("No se pudo entender el audio")
        except sr.RequestError as e:
            print(f"Error en el servicio de Google Speech Recognition; {e}")

def grabar_audio(): #Funcion extraida de https://github.com/GojiBL/wAIfu
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 2  # Duración máxima de grabación en silencio (segundos)
    THRESHOLD = 1000  # Umbral de amplitud para detectar sonido
    WAVE_OUTPUT_FILENAME = "audio.wav"

    p = pyaudio.PyAudio()

    # Configurar los parámetros de grabación de audio
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    print("Grabando audio...")

    frames = []
    silent_frames = 0  # Contador de frames sin sonido

    # Capturar audio del micrófono y almacenar los frames en una lista
    while True:
        data = stream.read(CHUNK)
        frames.append(data)

        # Obtener la amplitud del audio actual
        rms = audioop.rms(data, 2)  # 2 representa el ancho de muestra en bytes (16 bits)

        # Si la amplitud es menor que el umbral, incrementar el contador de frames sin sonido
        if rms < THRESHOLD:
            silent_frames += 1
        else:
            silent_frames = 0  # Restablecer el contador si se detecta sonido

        # Si se alcanza el límite de frames sin sonido, detener la grabación
        if silent_frames >= int(RATE / CHUNK * RECORD_SECONDS):
            break

    print("Grabación finalizada.")

    # Detener y cerrar el stream de audio
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Guardar los frames de audio en un archivo WAV
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
def hablar(texto):
    audio = client.generate(
    text=texto,
    voice=Voice(
        voice_id="jZQup0S2SnymAZXAOLOU",
        settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
    )
    )
    play(audio)
    
def main():
    hablar("Hola, soy un bot de prueba")

if __name__ == "__main__":
    main()