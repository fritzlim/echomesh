import analyse
import numpy
import pyaudio
import sys
import wave


READ = not False
CHUNK = 1024
INPUT_INDEX = int(sys.argv[1])

# Initialize PyAudio
pyaud = pyaudio.PyAudio()

if READ:

  # Open input stream, 16-bit mono at 44100 Hz
  # On my system, device 4 is a USB microphone
  stream = pyaud.open(
    format = pyaudio.paInt16,
    channels = 1,
    rate = 8000,
    input_device_index = INPUT_INDEX,
    input = True)

  while True:
    # Read raw microphone data
    rawsamps = stream.read(1024)
    # Convert raw data to NumPy array
    samps = numpy.fromstring(rawsamps, dtype=numpy.int16)
    # Show the volume and pitch
    print analyse.loudness(samps), analyse.musical_detect_pitch(samps)

else:


  if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

  wf = wave.open(sys.argv[1], 'rb')
  format = pyaud.get_format_from_width(wf.getsampwidth())
  stream = pyaud.open(format=format,
                      channels=wf.getnchannels(),
                      rate=wf.getframerate(),
                      output=True)

  data = wf.readframes(CHUNK)

  while data != '':
    stream.write(data)
    data = wf.readframes(CHUNK)

  stream.stop_stream()
  stream.close()

  pyaud.terminate()