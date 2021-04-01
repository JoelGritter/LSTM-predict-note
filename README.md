# LSTM-predict-note
LSTM model to predict next note in a song

Try it on Google Colab: https://colab.research.google.com/drive/1_LxG1cSVyaKEmU93ZLvF8SVfwt7X--Tj?usp=sharing

## Background Question
Given the notes preceding, can we build an LSTM model to predict the next note in a song?

## Conclusion
LSTM model had an observed **72.31%** rate of getting the next note _exactly_ correct.

## Background Information
- Trained on Mozart's Sonata No. 10 in C Major, K. 330
- Model was built using Keras, and executed on Google Colab

## File Structure
- Training data: `./data/`
- Raw sheet music: `./assets/`
- Presentation deck: `./Presentation.pdf`
- Jupyter Notebook: `./4P80_Seminar.ipynb`
- Python file: `./4P80_Seminar.py`

## Data
### Data Gathering:
Data was manually transcribed from sheet music for Mozart's Sonata No. 10 in C Major, in particular the allegro moderato movement of that composition. The sheet music is available under `./assets/sheet-music/`.

Each of the notes were transcribed using a system in comparison to middle C. The note itself was first noted, then the octave difference from middle C's octave. \(More specifically, the octave from middle C to the B above middle C\)

e.g. C#++ indicates C sharp, two octaves above middle C.

Only the very top note \(the melody, in most cases\), was transcribed for the purposes of this data.

### Data Pre-processing:
Once in the note+octave notation, a Python script was used to convert those notes into a number in the range \[0, 88\). \(Available under `./data/convert-notes-to-numbers.py`\) This number indicated which note was being played in that particular moment.

Then once this data was received on the Keras side of things, it converts this number index into an 88-ary binary array, where the only true index is the current number. \(This array similarly indicates which note is being played in the particular moment, just easier to digest for the Keras model\)

### Training/Testing Data:
- For X \(input\): take the previous 20 88-ary arrays
- For Y \(output\): take the current 88-ary array
- 80% training data, 20% testing data
- Data was shuffled

## Using Colab for demo

1. Create a copy of https://colab.research.google.com/drive/1_LxG1cSVyaKEmU93ZLvF8SVfwt7X--Tj?usp=sharing to your drive
![image](https://user-images.githubusercontent.com/32722218/113331909-810e4580-92ee-11eb-9096-c63e19d1158d.png)
2. Add the data file, download https://raw.githubusercontent.com/JoelGritter/LSTM-predict-note/main/data/numbers/k330-allegro-moderato.csv (You can use this link: https://downgit.github.io/#/home?url=https://github.com/JoelGritter/LSTM-predict-note/blob/main/data/numbers/k330-allegro-moderato.csv, or use wget)
3. Upload this file to colab, make sure the filename is "k330-allegro-moderato.csv"
![image](https://user-images.githubusercontent.com/32722218/113332406-21fd0080-92ef-11eb-9801-b553ef117fcc.png)
4. You're done with setup! Use runtime > run all to run all steps, you can also use your own input files instead.


## Credits
Joel Gritter and Kindeep Singh Kargil

COSC 4P80 - Brock University - March 29, 2021
