'''
Hides a string of ASCII text in a specified .wav file.
For a standard framerate of 22050, about 2726 characters can
be stored per second of sound, and 11025 per 4 seconds of sound.

Hans
'''

import wave
from sys import argv

# 8-bit binary string 'b', wave bytearray data 'w'
def encode(b, w, start=0, step=1):
    for i, bit in enumerate(b):
            if bit == '0':
                w[start+i*step] = w[start+i*step] & 254
            else:
                w[start+i*step] = w[start+i*step] | 1
    return w

if argv[1] == '--help':
    print('Usage: python3 [SCRIPT] [TEXTFILE] [WAVEFILE]')
    print('[SCRIPT] is the path to this script')
    print('[TEXTFILE] must be in ASCII format.')
    print('[WAVEFILE] must be a .wav file.')
    print()
    print('For a standard framerate of 22050, about 2726 characters')
    print('can be stored per second of sound')
    print('or about 11025 characters per 4 seconds of sound.')

else:
    script, textfile, wavefile = argv
    
    print('Creating binary data of textfile...')
    f = open(textfile, 'r')
    string = f.read()
    f.close()

    # Convert intstring into 8-bit binary string
    bin_string = ''.join(format(i, '08b') for i in bytearray(string, 'ascii'))

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
    w = wave.open(wavefile, 'r')
    data = bytearray(w.readframes(w.getnframes()))
    params = w.getparams()
    w.close()
    output = wave.open(outfile, 'w')
    output.setparams(params)

    print('Editing wave data...')
    # Add 8 bit integer to beginning of data specifying
    # the spacing between each bit written to data
    spacing = int( (len(data)-8) / len(bin_string) )
    b_spacing = format(spacing, '08b')
    
    # Subtract 8 because first byte is used to store spacing
    if len(bin_string) > len(data) - 8:
        print('ERROR: Input file too big.')
    else:
        # Write data to least significant bits of wave data
        data = encode(b_spacing, data)
        data = encode(bin_string, data, 8, spacing)

        # Finish up
        print('Writing data to new wavefile...')
        output.writeframes(bytearray(data))
        
    output.close()

