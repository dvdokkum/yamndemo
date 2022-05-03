from os.path import dirname, join as pjoin
import scipy
from scipy.io import wavfile

def ensure_sample_rate(original_sample_rate, waveform,
                       desired_sample_rate=16000):
  """Resample waveform if required."""
  if original_sample_rate != desired_sample_rate:
    desired_length = int(round(float(len(waveform)) /
                               original_sample_rate * desired_sample_rate))
    waveform = scipy.signal.resample(waveform, desired_length)
  return desired_sample_rate, waveform

# test_wav_file_name = 'test.wav'
# media_dir = pjoin(dirname(__file__), 'media')
# test_wav_file_name = pjoin(media_dir,'test.wav')
# sample_rate, wav_data = wavfile.read(test_wav_file_name, 'rb')
# sample_rate, wav_data = ensure_sample_rate(sample_rate, wav_data)

# Show some basic information about the audio.
# duration = len(wav_data)/sample_rate
# print(f'Sample rate: {sample_rate} Hz')
# print(f'Total duration: {duration:.2f}s')
# print(f'Size of the input: {len(wav_data)}')

def process_audio(filename):
  media_dir = pjoin(dirname(__file__), 'static', 'uploads')
  file_name = pjoin(media_dir,filename)
  sample_rate, wav_data = wavfile.read(file_name, 'rb')
  sample_rate, wav_data = ensure_sample_rate(sample_rate, wav_data)
  return wav_data



