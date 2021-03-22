import sys

# middle C is the 40th note on an 88 key piano
adjustment = 40

# converts note from the [note][octave_adjustment] format to a number
def convert_note(note):
    global adjustment

    notes = {
        "C": 0, 
        "C#": 1, 
        "Db": 1,
        "D": 2,
        "D#": 3,
        "Eb": 3,
        "E": 4,
        "E#": 5,
        "Fb": 5,
        "F": 5,
        "F#": 6,
        "Gb": 6,
        "G": 7,
        "G#": 8,
        "Ab": 8,
        "A": 9,
        "A#": 10,
        "Bb": 10,
        "B": 11,
        "B#": 12,
        "Cb": 12
    }

    temp_result = 0
    
    if len(note) >= 2:
        if len(note) == 2 and note[1] != "+" and note[1] != '-':
            # note is either a sharp or a flat note
            temp_result = notes[note]
        else:
            # note needs to be adjusted for octave
            if len(note) == 2:
                # note with no sharp/flat, adjusted for octave
                if note[1] == "+":
                    temp_result = notes[note[0]] + 12
                else:
                    temp_result = notes[note[0]] - 12
            else:
                # note with sharp/flat, adjusted for octave
                if note[2] == "+":
                    split_note = note.split("+")
                    temp_result = notes[split_note[0]] + (12 * (len(split_note) - 1))
                else:
                    split_note = note.split("-")
                    temp_result = notes[split_note[0]] - (12 * (len(split_note) - 1))
    else:
        # note is a "normal" note
        temp_result = notes[note]

    return temp_result + adjustment


# parses file, from notes to numbers
def parse(in_file, out_file):
    out_values = []

    with open(in_file) as input_file:
        for line in input_file:
            notes = line.strip().split(",")
            for note in notes:
                out_values.append(convert_note(note))
    
    print("INFO: " + str(len(out_values)) + " notes converted")

    with open(out_file, "a+") as output_file:
        for i in range(0, len(out_values)):
            if i != len(out_values) - 1:
                output_file.write(str(out_values[i]) + ",")
            else:
                output_file.write(str(out_values[i]))
        
        output_file.write("\n")
    
    print("INFO: successfully written to " + out_file)



if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print("usage: python3 convert-notes-to-numbers.py [input_file] [output_file]")
        exit(0)
    
    in_file = sys.argv[1]
    out_file = sys.argv[2]

    parse(in_file, out_file)
    exit(0)