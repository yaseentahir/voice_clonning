import soundfile as sf  # Import soundfile for audio writing
from TTS.api import TTS
import os
from pydub import AudioSegment
import librosa
import numpy as np
import torch
from torchaudio.transforms import Resample

# Define the paths for the input audio files
audio_files = [
    r"C:\Users\hussa\OneDrive\Desktop\VCha\couqi-ai-voice-cloning-main\dataset\yaseen1.mp3",
    r"C:\Users\hussa\OneDrive\Desktop\VCha\couqi-ai-voice-cloning-main\dataset\yaseen2.mp3",
    r"C:\Users\hussa\OneDrive\Desktop\VCha\couqi-ai-voice-cloning-main\dataset\yaseen3.mp3"  # Add paths for input audio
]

# Output directory
output_dir = r"C:\Users\hussa\OneDrive\Desktop\VCha\couqi-ai-voice-cloning-main\output_cloned"
os.makedirs(output_dir, exist_ok=True)

# Initialize the TTS model
print("Loading XTTS model...")
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

# Text to synthesize
text_to_speak = (
    "The sun dipped below the horizon, casting a warm golden hue across the sky. The gentle breeze rustled the leaves of the trees, creating a soothing melody that seemed to harmonize with the distant chirping of birds."
)

# Prepare the final list of speaker WAV paths
final_speaker_wavs = []
for i, audio_path in enumerate(audio_files):
    if not os.path.exists(audio_path):
        print(f"Audio file does not exist: {audio_path}")
        continue

    # Convert MP3 to WAV if needed
    if audio_path.endswith(".mp3"):
        print(f"Converting {audio_path} to WAV...")
        mp3_audio = AudioSegment.from_mp3(audio_path)
        wav_path = os.path.join(output_dir, f"converted_audio_{i}.wav")
        mp3_audio.export(wav_path, format="wav")
        final_speaker_wavs.append(wav_path)
    else:
        # If it's already a WAV file, use it directly
        final_speaker_wavs.append(audio_path)

# Generate the cloned voice using the prepared speaker WAVs
if final_speaker_wavs:
    print("Generating speech with combined voice...")
    intermediate_output = os.path.join(output_dir, "cloned_voice_combined.wav")
    tts.tts_to_file(
        text=text_to_speak,
        file_path=intermediate_output,
        speaker_wav=final_speaker_wavs,
        language="en"
    )
    print(f"Intermediate cloned voice saved to: {intermediate_output}")

    # Perform voice conversion on the generated file
    print("Performing voice conversion for realism...")
    y, sr = librosa.load(intermediate_output, sr=None)

    # Resample audio to 16kHz for conversion
    resample_transform = Resample(orig_freq=sr, new_freq=16000)
    y_resampled = resample_transform(torch.tensor(y).unsqueeze(0))

    # Simulate voice conversion (replace with your VC model or method)
    # Placeholder: Adjust pitch to speaker's range
    pitch_shift = 2  # Positive/negative values to adjust pitch
    y_converted = librosa.effects.pitch_shift(
        y_resampled.squeeze().numpy(), sr=16000, n_steps=pitch_shift
    )

    # Save the voice-converted file
    final_output = os.path.join(output_dir, "cloned_voice_converted.wav")
    sf.write(final_output, y_converted, samplerate=16000)
    print(f"Voice-converted file saved to: {final_output}")
else:
    print("No valid input files were found. Please check the provided paths.")

print("Voice cloning and conversion process completed!")

