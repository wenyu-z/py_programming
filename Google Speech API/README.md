## Using Google Speech API
Notes from writing slb_er.ipynb, transcribing SLB 2017 Q2 earnings call
### 1. Do Not use MP3 files
Per [Google Cloud Speech API Best Practices](https://cloud.google.com/speech/docs/best-practices):
>Using mp3, m4a, mu-law, a-law or other lossy codecs during recording or transmission may reduce accuracy. If your audio is already in an encoding not supported by the API, transcode it to lossless FLAC or LINEAR16.

It is found from [this link](https://www.magellanic-clouds.com/blocks/en/guide/cloud-speech-api-audio-encoding/) that SoX ([download here](http://sox.sourceforge.net/)) can be used. However, separate dll files, libmad-0.dll and lbmp3lame-0.dll, are needed per [this link](https://stackoverflow.com/questions/3537155/sox-fail-util-unable-to-load-mad-decoder-library-libmad-function-mad-stream) and downloaded [here](https://stackoverflow.com/questions/3537155/sox-fail-util-unable-to-load-mad-decoder-library-libmad-function-mad-stream)

`sox <filename>.mp3 --rate 16k --bits 16 --channels 1 output.flac` at command line to convert mp3 to a flac (or perhaps wav) file

Read more about audio encoding on Google Cloud site [here](https://cloud.google.com/speech/docs/encoding)

### 2. Launching datalab
Reference: https://codelabs.developers.google.com/codelabs/cpb100-datalab/index.html
Option 2 used.

### 3. Writing the Request
A couple of references are used here:
* [Using notebook on Datalab](https://github.com/GoogleCloudPlatform/training-data-analyst/blob/master/CPB100/lab4c/mlapis.ipynb) (also included: example of how to extract data from the response return)
* [Using cloud shell CLI](https://codelabs.developers.google.com/codelabs/cloud-speech-intro/index.html?index=..%2F..%2Findex#6)

But in these examples above, the audio clip is shorter than 1 minute. The earnings call clip is longer than 1 minute (actually way longer), and therefore needs ["asynchronous speech recognition"](https://cloud.google.com/speech/docs/async-recognize). 
