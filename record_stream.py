# Inspired by https://github.com/LearnedVector/A-Hackers-AI-Voice-Assistant/

import pyaudio
import threading
import time
import wave
import argparse
import os

class Listener:

    def __init__(self, sample_rate=8000, record_seconds=2):
        self.chunk = 1024
        self.sample_rate = sample_rate
        self.record_seconds = record_seconds
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt8,
                        channels=1,
                        rate=self.sample_rate,
                        input=True,
                        output=True,
                        frames_per_buffer=self.chunk)

    def listen(self, queue):
        while True:
            data = self.stream.read(self.chunk , exception_on_overflow=False)
            import pdb
            pdb.set_trace()
            queue.append(data)
            time.sleep(0.01)

    def run(self, queue):
        thread = threading.Thread(target=self.listen, args=(queue,), daemon=True)
        thread.start()
        print("I am now listening... \n")


class SpeechRecognitionEngine:

    def __init__(self, sr, file_location):
        self.listener = Listener(sample_rate=sr)
        self.audio_q = list()
        self.sr = sr
        self.file_location = file_location

    def run(self):
        self.listener.run(self.audio_q)
        thread = threading.Thread(target=self.inference_loop, daemon=True)
        thread.start()

    def save(self, waveforms, fname="temp.wav"):

        wf = wave.open(fname, "wb")
        # set the channels
        wf.setnchannels(1)
        # set the sample format
        wf.setsampwidth(self.listener.p.get_sample_size(pyaudio.paInt8))
        # set the sample rate
        wf.setframerate(self.sr)
        # write the frames as bytes
        wf.writeframes(b"".join(waveforms))
        # close the file
        wf.close()

        return fname

    def inference_loop(self):
        i = 0
        while True:
            if len(self.audio_q) < 15:
                continue
            else:
                pred_q = self.audio_q.copy()
                self.audio_q.clear()
                print('Predicting Text.')
                self.save(pred_q, f'{self.file_location}/test{str(i)}.wav')
                i += 1

            # time.sleep(0.05)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Testing running pyaudio to support streaming audio from laptop.")
    parser.add_argument('--file_location', '-f', type=str, default=None, required=True,
                        help='file location where we will save samples  file names are test<#>.wav where # \
                              is the number in a sequence of saved chunks from the sound card.')
    args = parser.parse_args()
    sample_rate = 8000
    # TODO: add Chunk and frame params


    # remove old files following the pattern test<#>.wav
    #   ask the user before removing.
    #   check if files exist.
    #   remove them.
    #   iterate through and find all the files
    files = []
    lst = os.listdir(args.file_location)
    for filename in lst:
        if "test" in filename and 'wav' in filename:
            files.append(filename)
    files.sort()
    if len(files) > 0:
        rsp = input(f'The following files were found in {args.file_location}: {files}.  Would you like to remove them? [Y/n] ')
        if rsp.lower() == '' or rsp.lower() == 'y':
            for file in files:
                print(f'Removing {file}.')
                os.remove(f'{args.file_location}/{file}')
        else:
            print('Leaving program.  Remove files to run to completion.')
            exit()


    try:
        asr_engine = SpeechRecognitionEngine(sample_rate, args.file_location)
        print(f'Prediction Window is {1024 * 15 / sample_rate}s.')
        asr_engine.run()
        threading.Event().wait()

    except KeyboardInterrupt as e:
        print('Exiting...')
        exit()