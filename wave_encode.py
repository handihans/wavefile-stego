'''
Hides a string of ASCII text in a specified .wav file.
For a standard framerate of 22050, about 2726 characters can
be stored per second of sound, and 11025 per 4 seconds of sound.

Hans
'''

import wave
from sys import argv

def write_string(string, data_list, start=0, space=1):
    for i in range(0, len(string)):
        data_index = start + i * space
        if data_list[data_index] % 2 == int(string[i]) % 2:
            pass
        else:
            # Prevents values in data from going out of range(0, 256)
            # and raising ValueError with bytes() function
            if data_list[data_index] >= 255:
                data_list[data_index] -= 1
            else:
                data_list[data_index] += 1
    return data_list

if argv[1] == '--help':
    print('Usage: python3 [SCRIPT] [TEXTFILE] [WAVEFILE]')
    print('[SCRIPT] is the name of this script')
    print('[TEXTFILE] must be in ASCII format.')
    print('[WAVEFILE] must be a .wav file.')
    print()
    print('For a standard framerate of 22050, about 2726 characters')
    print('can be stored per second of sound')
    print('or about 11025 characters per 4 seconds of sound.')

else:
    script, textfile, wavefile = argv

    print('Creating binary data of textfile...')
    textfile = open(textfile, 'r')
    instring  = ''
    for i in textfile:
        instring += i
    textfile.close()

    # Convert each item in 'instring' to 8 bit binary number
    instring = list(instring)
    for i in range(len(instring)):
        instring[i] = format(ord(instring[i]), '08b')

    # Create continuous binary string
    bin_string = ''
    for i in instring:
        bin_string += i

    # Create name of copy file in the form 'filename(x).wav'
    for i in range(1, 100):
        try:
            w = wave.open(wavefile[:-4] + '(' + str(i) + ')' + wavefile[-4:], 'rb')
            w.close()
        except FileNotFoundError:
            outfile = wavefile[:-4] + '(' + str(i) + ')' + wavefile[-4:]
            break

    print('Reading wavefile...')
    # Create empty .wav file with same properties as original file
    w = wave.open(wavefile, 'rb')
    data = w.readframes(w.getnframes())
    params = w.getparams()

    output = wave.open(outfile, 'wb')
    output.setparams(params)

    w.close()
    data = list(data)

    print('Editing wave data...')
    # Add 8 bit integer to beginning of data specifying
    # the spacing between each bit written to data
    spacing = int( (len(data)-8) / len(bin_string) )
    b_spacing = format(spacing, '08b')

    # Subtract 8 because first byte is used to store spacing
    if len(bin_string) > len(data) - 8:
        print('SizeError: Input string too long.')
    else:
        # Write data to least significant bits of wave data
        write_string(b_spacing, data)
        write_string(bin_string, data, 8, spacing)

    data = bytes(data)

    print('Writing data to new wavefile...')
    # Finish up
    output.writeframes(data)
    output.close()

