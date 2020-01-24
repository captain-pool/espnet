import csv
import itertools
import os
import re
import sys
import tqdm

csv_files = {
    'train': 'train_meta.csv',
    'test': 'test_meta.csv'
}
if len(sys.argv) != 3:
  exit(f"python {sys.argv[0]} <audio_root> <data_root>")

if __name__ == "__main__":
  audio_root, data_root = sys.argv[1:]
  count = itertools.count()
  for x in tqdm.tqdm(['train', 'test'], position=0):
    with open(os.path.join(audio_root, csv_files[x])) as csv_f, \
         open(os.path.join(data_root, x, 'text'), 'w') as text_f, \
         open(os.path.join(data_root, x, 'utt2spk'), 'w') as utt2spk_f, \
         open(os.path.join(data_root, x, 'wav.scp'), 'w') as wav_scp_f:
      text_f.truncate()
      utt2spk_f.truncate()
      wav_scp_f.truncate()
      csv_file = csv.reader(csv_f)
      for wav, transcript in tqdm.tqdm(csv_file, position=1):
        utt_id = next(count)
        text_f.write(f"{utt_id:04d} {transcript}\n")
        wav_scp_f.write(f"{utt_id:04d} ffmpeg -i {os.path.realpath(audio_root)}/wavs/{wav} -ac 1 -ar 16000 -f wav - |\n")
        utt2spk_f.write(f"{utt_id:04d} 0\n")
