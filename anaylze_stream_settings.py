# Inspired by https://github.com/LearnedVector/A-Hackers-AI-Voice-Assistant/

import pyaudio
import threading
import time
import wave
import argparse
import os


class Listener:
    '''
    sr - sample rate - typ. 8000
    chunk - number of samples (chunks) provided directly from audio card. - typ. 1024
    dt - data type of samples - typ. pyaudio.paInt8 (audio cards tend to be 8-bit)
    nchan - number of channels of audio to recordd. - typ. 1
    '''
    def __init__(self, sr, dt, chunk, nchan):
        self.chunk_size = chunk
        self.sample_rate = sr
        self.sample_datatype = dt
        self.nchannels = nchan
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.sample_datatype,
                                  channels=self.nchannels,
                                  rate=self.sample_rate,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=self.chunk_size)

    def listen(self, queue):
        while True:
            data = self.stream.read(self.chunk_size, exception_on_overflow=False)
            queue.append(data)
            time.sleep(0.01)

    def run(self, queue):
        thread = threading.Thread(target=self.listen, args=(queue,), daemon=True)
        thread.start()
        print("I am now listening... \n")


class SpeechRecognitionEngine:
    '''
    sr - sample rate - typ. 8000
    chunk - number of samples (chunks) provided directly from audio card. - typ. 1024
    dt - data type of samples - typ. pyaudio.paInt8 (audio cards tend to be 8-bit)
    nchan - number of channels of audio to recordd. - typ. 1
    '''
    def __init__(self, sr, dt, chunk, nchan, filepath, postfix = ''):
        self.listener = Listener(sr=sr, dt=dt, chunk=chunk, nchan=nchan)
        self.audio_q = list()
        self.sample_rate = sr
        self.sample_data_type = dt
        self.nchannels = nchan
        self.filepath = filepath
        self.filename_postfix = (lambda x: '' if x == '' else ('_'+x))(postfix)

    def run(self, qdepth):
        self.listener.run(self.audio_q)
        thread = threading.Thread(target=self.inference_loop, args=(qdepth,), daemon=True)
        thread.start()

    def save(self, waveforms, fname="temp.wav"):
        wf = wave.open(fname, "wb")
        # set the channels
        wf.setnchannels(self.nchannels)
        # set the sample format
        wf.setsampwidth(self.listener.p.get_sample_size(self.sample_data_type))
        # set the sample rate
        wf.setframerate(self.sample_rate)
        # write the frames as bytes
        wf.writeframes(b"".join(waveforms))
        # close the file
        wf.close()

        return fname

    def inference_loop(self, qdepth):
        i = 0
        while True:
            if len(self.audio_q) < qdepth:
                continue
            else:
                pred_q = self.audio_q.copy()
                self.audio_q.clear()
                print('Transcribe Text Here.')
                self.save(pred_q, f'{self.filepath}/test{str(i)}{self.filename_postfix}.wav')
                i += 1

            # time.sleep(0.05)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Testing running pyaudio to support streaming audio.")
    parser.add_argument('--filepath', '-p', type=str, default=None, required=True,
                        help='file location where we will save samples  file names are test<#>.wav where # \
                              is the number in a sequence of saved chunks from the sound card.')
    args = parser.parse_args()

    for pyaudio_datatype in [pyaudio.paInt8, pyaudio.paInt16, pyaudio.paInt32]:
        SAMPLE_DATATYPE = pyaudio_datatype
        if pyaudio_datatype == pyaudio.paInt8:
            pyaudio_datatype_str = 'int8'
        elif pyaudio_datatype == pyaudio.paInt16:
            pyaudio_datatype_str = 'int16'
        elif pyaudio_datatype == pyaudio.paInt32:
            pyaudio_datatype_str = 'int32'
        else:
            print('WHOOPS')

        SAMPLE_RATE = 16000
        CHUNK_SIZE = 1024
        QUEUE_DEPTH = 16 # 1 second of data
        NCHANNELS = 1
        window_size = CHUNK_SIZE * QUEUE_DEPTH / SAMPLE_RATE
        print(f'Sample from audio card and save off data every {window_size}s')

        # remove old files following the pattern test<#>.wav
        #   ask the user before removing.
        #   check if files exist.
        #   remove them.
        #   iterate through and find all the files
        files = []
        lst = os.listdir(args.filepath)
        for filename in lst:
            if "test" in filename and 'wav' in filename:
                files.append(filename)
        files.sort()

        """
        # if some files are found that look like old ones, ask to remove them.
        if len(files) > 0:
            rsp = input(
                f'The following files were found in {args.filepath}: {files}.  Would you like to remove them? [Y/n] ')
            if rsp.lower() == '' or rsp.lower() == 'y':
                for file in files:
                    print(f'Removing {file}.')
                    os.remove(f'{args.filepath}/{file}')
            else:
                print('Leaving program.  Remove files to run to completion.')
                exit()
        """

        try:
            asr_engine = SpeechRecognitionEngine(SAMPLE_RATE, SAMPLE_DATATYPE, CHUNK_SIZE, NCHANNELS, args.filepath, postfix=pyaudio_datatype_str)
            asr_engine.run(QUEUE_DEPTH)
            threading.Event().wait()

        except KeyboardInterrupt as e:
            print('Exiting...')
            #exit()
            continue
