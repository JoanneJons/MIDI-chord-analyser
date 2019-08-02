import rtmidi
import enum
from music21 import *
note_list = []

class Status(enum.Enum) :
    note_on = 1
    note_off = 2
    other = 16

def analyse (note_list):
    # Function which takes a list as an argument, does harmony analisys and returns the analysed chord.
    c = chord.Chord (note_list)
    h = harmony.chordSymbolFigureFromChord (c)
    return h

def add_to_note_list (note) :
    # Function to add the given note to the note_list after checking whether note already exists in note_list
    f = 0
    for i in note_list :
        if (i == note) :
            f += 1
    if (f == 0) :    
        note_list.append (note)

def delete_from_note_list (note) :
    # Function to remove note from note_list after checking whether note exist in note_list
    f = 0
    for i in note_list :
            if (i == note) :
                f += 1
    if (f != 0) :
        note_list.remove (note)

midi_in = rtmidi.MidiIn()
available_ports = midi_in.get_ports()


midi_port = '' # text to display a label on the MIDI port status

if available_ports: # if MIDI ports available, open the first port
    index = 0
    for p in available_ports :
        print('{} : {}'.format(index, p))
        index += 1

    print ("Select port ")
    selected_port = input()
    midi_in.open_port(int(selected_port))
    midi_port =  'MIDI port: ' + midi_in.get_ports()[int(selected_port)]
    print(midi_port)
else:
    print("MIDI Port not found!")
    midi_port = "MIDI port not found!"


running = False

def start_analysis():
    global running
    running = True
    print ("Running ...")
    print ("Press Ctrl-C to exit")

def task():
    try :
        previous = ""
        while(True) :
            
            global running
            
            if (running):
                message = midi_in.get_message()
                
                if message :
                    m = message[0][0] & 0xF0
                    v = message[0][2]
                    status = Status.other

                    if m == 0x90 :
                        if v != 0 :
                            status = Status.note_on
                        elif v == 0 :
                            status = Status.note_off

                    elif (m == 0x80) :
                        status = Status.note_off


                    if (status == Status.note_on) :
                        add_to_note_list (message[0][1])

                    elif (status == Status.note_off) :
                        delete_from_note_list (message[0][1])

                    if (len(note_list) > 2) :
                        h = analyse (note_list)
                        if (h != 'Chord Symbol Cannot Be Identified'):
                            if (h != previous) :
                                print(h)
                                previous = h
    except KeyboardInterrupt :
        pass

start_analysis()
task()

