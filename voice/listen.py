
import sounddevice as sd
import speech_recognition as sr
import io
import wave


class JarvisListener:

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.sample_rate = 16000

    def listen(self):

        print("\nListening... Speak now!")

        try:
            recording = sd.rec(
                int(5 * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                dtype="int16"
            )

            sd.wait()

            audio_buffer = io.BytesIO()

            with wave.open(audio_buffer, "wb") as wav:
                wav.setnchannels(1)
                wav.setsampwidth(2)
                wav.setframerate(self.sample_rate)
                wav.writeframes(recording.tobytes())

            audio_buffer.seek(0)

            with sr.AudioFile(audio_buffer) as source:
                audio = self.recognizer.record(source)

            print("Processing speech...")

            text = self.recognizer.recognize_google(
                audio,
                language="en-IN"
            )

            print(f"You: {text}")
            return text

        except sr.UnknownValueError:
            print("I couldn't understand that.")
            return None

        except sr.RequestError:
            print("Speech recognition service unavailable.")
            return None

        except Exception as error:
            print(f"Microphone error: {error}")
            return None
