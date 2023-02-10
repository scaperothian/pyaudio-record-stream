# Inspired by https://github.com/LearnedVector/A-Hackers-AI-Voice-Assistant/
import argparse
import wave
import pyaudio
import os


def save(self, waveforms, fname="temp.wav"):
    wf = wave.open(fname, "wb")
    # set the channels
    wf.setnchannels(1)
    # set the sample format
    wf.setsampwidth(self.listener.p.get_sample_size(pyaudio.paInt16))
    # set the sample rate
    wf.setframerate(self.sr)
    # write the frames as bytes
    wf.writeframes(b"".join(waveforms))
    # close the file
    wf.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Testing running pyaudio to support streaming audio from laptop.")
    parser.add_argument('--file_location', '-f', type=str, default=None, required=True,
                        help='file location where we will save samples  file names are test<#>.wav where # \
                              is the number in a sequence of saved chunks from the sound card.')
    args = parser.parse_args()
    p = pyaudio.PyAudio()
    sr = 8000

    # iterate through and find all the files
    files = []
    lst = os.listdir(args.file_location)
    for filename in lst:
        if "test" in filename and 'wav' in filename:
            files.append(filename)
    files.sort()

    # read files into memory
    b = []
    for file in files:
        wf = wave.open(f'{args.file_location}/{file}')
        while True:
            # bits - type bytes / binary string
            bits = wf.readframes(1024)
            # when
            b.extend(bits)

            if len(bits) == 0:
                print(f'Read all bytes from {file}')
                break

    wf = wave.open(f'{args.file_location}/big.wav', "wb")
    # set the channels
    wf.setnchannels(1)
    # set the sample format
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    # set the sample rate
    wf.setframerate(sr)
    # write the frames as bytes

    wf.writeframes(bytes(b))
    # close the file
    wf.close()

    # concatenate them together
