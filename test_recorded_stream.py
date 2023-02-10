# Inspired by https://github.com/LearnedVector/A-Hackers-AI-Voice-Assistant/
import argparse
import wave
import pyaudio
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Testing running pyaudio to support streaming audio from laptop.")
    parser.add_argument('--filepath', '-p', type=str, default=None, required=True,
                        help='file location where we will save samples  file names are test<#>.wav where # \
                              is the number in a sequence of saved chunks from the sound card.')
    args = parser.parse_args()
    p = pyaudio.PyAudio()

    datatype = pyaudio.paInt16
    SAMPLE_RATE = 8000
    CHUNK_SIZE = 1024
    QUEUE_DEPTH = 15
    window_size = CHUNK_SIZE*QUEUE_DEPTH/SAMPLE_RATE
    print(f'Sample from audio card and save off data every {window_size}s')

    # iterate through and find all the files
    files = []
    lst = os.listdir(args.filepath)
    for filename in lst:
        if "test" in filename and 'wav' in filename:
            files.append(filename)
    files.sort()

    # read files into memory
    b = []
    for file in files:
        wf = wave.open(f'{args.filepath}/{file}')
        while True:
            # bits - type bytes / binary string
            bits = wf.readframes(CHUNK_SIZE)
            # when
            b.extend(bits)

            if len(bits) == 0:
                print(f'Read all bytes from {file}')
                break

    wf = wave.open(f'{args.filepath}/big.wav', "wb")
    # set the channels
    wf.setnchannels(1)
    # set the sample format
    wf.setsampwidth(p.get_sample_size(datatype))
    # set the sample rate
    wf.setframerate(SAMPLE_RATE)
    # write the frames as bytes

    wf.writeframes(bytes(b))
    # close the file
    wf.close()

    # now print in matplotlib...
    # plt.plot(b)
