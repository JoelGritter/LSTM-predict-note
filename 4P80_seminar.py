# -*- coding: utf-8 -*-
"""4P80_Seminar

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_LxG1cSVyaKEmU93ZLvF8SVfwt7X--Tj

Joel Gritter & Kindeep Singh Kargil

COSC 4P80 - Seminar Demo

March 29, 2021
"""

# Music output
!sudo apt-get install fluidsynth
!pip install midi2audio
!pip install mingus
from mingus.containers import Note, NoteContainer, Track
from mingus.midi.midi_file_out import write_NoteContainer, write_Track
from midi2audio import FluidSynth

fsy = FluidSynth()

# imports for data manipulation
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# imports for machine learning
import keras
from keras.models import Sequential
from keras.layers import Dense, LSTM

# read in the notes, make an array with 0's, except for the current note
def read_and_format(input_filepath):
  input_data = []
  with open(input_filepath) as input_file:
    for line in input_file:
      values = line.split(",")
      for value in values:
        tmp = [0.0] * 88
        v = int(value)
        tmp[v-1] = 1.0
        input_data.append(tmp)
  
  return input_data
  

input_data = read_and_format("k330-allegro-moderato.csv")

# get the previous 20 notes, predict the next note
def generate_datasets(input_array, n_prev = 20):
  temp_x = [input_array[i:i+n_prev] for i in range(len(input_array) - n_prev)]
  temp_y = [input_array[i+n_prev] for i in range(len(input_array) - n_prev)]

  return np.array(temp_x), np.array(temp_y)

x, y = generate_datasets(input_data)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, shuffle=True)

print(x_train.shape, y_train.shape)
print(x_test.shape, y_test.shape)
print(y_train[0])

# build the model itself
model = Sequential()
model.add(LSTM(30))
model.add(Dense(88, activation="softmax"))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# train the model
model.fit(x_train, y_train, batch_size=10, epochs=100, validation_split=0.05)

# test the model
model.evaluate(x_test, y_test)

# See incorrectly predicted 
predictions = model.predict(x_test)
incorrect_indices = []
for (index, (prediction, target)) in enumerate(zip(predictions, y_test)):
  pred = np.argmax(prediction)
  tar = np.argmax(target)
  if pred != tar:
    incorrect_indices.append(index)

print(", ".join(map(str, incorrect_indices)))

# Predict song
test_in = x_test[0]
test_out = y_test[0]
# initial - provide inital 20 notes
# n - how many predicted notes to add (i.e. expand by this number)
def make_big_song(initial, n):
  res =[ x for x in initial]
  for _ in range(n):
    next = model.predict(np.array([res[-20:],]))[0]
    res.append(next)

  return np.array(res)

test = make_big_song(test_in, 60)
print(test.shape)

# Expects n x 88
def vector_to_midi(arr, filename="nice.midi"):
  track = Track()
  for note_arr in arr:
    note_num = int(np.argmax(note_arr))
    note = Note()
    note.from_int(note_num - 3)
    track.add_notes(note)
  write_Track(filename, track)
  print("Done!")
  
vector_to_midi(test)

def predict_to_file(first_20_notes, expected, filename="nice"):
  next = model.predict(np.array([first_20_notes]))
  actual_next = np.array([expected])
  next_file = filename + "_predicted_note"
  actual_next_file = filename + "_actual_note"
  orig_file = filename + "_first_20_notes"

  vector_to_midi(next, next_file + ".midi")
  vector_to_midi(actual_next, actual_next_file + ".midi")
  vector_to_midi(first_20_notes, orig_file + ".midi")

  # This conversion not seem to work
  # fsy.midi_to_audio(next_file + ".midi", next_file + ".mp3")
  # fsy.midi_to_audio(actual_next_file + ".midi", actual_next_file + ".mp3")
  # fsy.midi_to_audio(orig_file + ".midi",  orig_file + ".mp3")

predict_to_file(test_in, test_out)

inci = incorrect_indices[0]
predict_to_file(x_test[inci], y_test[inci], 'first_incorrect')