# pyaudio-record-stream
## Program to learn how to continuously record audio streams.

Inspired by https://github.com/LearnedVector/A-Hackers-AI-Voice-Assistant/
  
<img width="983" alt="Screenshot 2023-02-09 at 11 37 31 PM" src="https://user-images.githubusercontent.com/4464787/218001961-f74952c1-bde6-4496-a69f-8ec83b806986.png">

Save to a file.  Convention is test#.wav. Where # is the number given to the audio queue.  The numbers are ordered, so reassembly of the queues would result in time ordered samples.


```
python record_stream.py -p <filepath>
```

```
python test_recorded_stream.py -p <filepath>
```

## Requirements

Tested with Python 3.10 and pyaudio.  See requirements.txt (this is mostly it!)
