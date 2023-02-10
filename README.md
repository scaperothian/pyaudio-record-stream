# pyaudio-record-stream
## Program to learn how to continuously record audio streams.

Inspired by https://github.com/LearnedVector/A-Hackers-AI-Voice-Assistant/
  
<img width="497" alt="Screenshot 2023-02-09 at 11 11 02 PM" src="https://user-images.githubusercontent.com/4464787/217998813-548bd016-5fd0-41b2-b68c-04b853a55467.png">

Save to a file.  Convention is test#.wav. Where # is the number given to the audio queue.  The numbers are ordered, so reassembly of the queues would result in time ordered samples.


```
python record_stream.py -f <filepath>
```

```
python test_recorded_stream.py -f <filepath>
```

## Requirements

Tested with Python 3.10 and pyaudio.  See requirements.txt (this is mostly it!)
