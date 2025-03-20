import pyaudio

pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16,
                 channels=1,
                 rate=16000,
                 input=True,
                 frames_per_buffer=1024)

print("Recording audio for 5 seconds...")
frames = []
for _ in range(0, int(16000 / 1024 * 5)):
    data = stream.read(1024)
    frames.append(data)
print("Recording complete.")

# Print the number of frames recorded and the length of the first frame (in bytes)
print(f"Recorded {len(frames)} frames.")
if frames:
    print(f"Length of first frame: {len(frames[0])} bytes")

stream.stop_stream()
stream.close()
pa.terminate()
