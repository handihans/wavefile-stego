'''
Hides a string of ASCII text in a specified .wav file.
For a standard framerate of 22050, about 2726 characters can
be stored per second of sound, and 11025 per 4 seconds of sound.

Hans
'''

import wave
from sys import argv

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
    
    textfile = open(textfile, 'r')
    instring  = ''
    for i in textfile:
        instring += i
    textfile.close()

    instring = list(instring)
    # Convert each item in 'instring' to binary
    for i in range(len(instring)):
        # Chop off first 2 places of the binary number because of
        # formatting of the bin() function output
        instring[i] = bin(ord(instring[i]))[2:]

    # Pad each value in instring with 0's so that it is an 8 bit string
    for i in range(len(instring)):
        while True:
            if len(instring[i]) < 8:
                instring[i] = '0' + instring[i]
            else:
                break

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

        
    # Create empty .wav file with same properties as original file
    w = wave.open(wavefile, 'rb')
    data = w.readframes(w.getnframes())
    params = w.getparams()

    output = wave.open(outfile, 'wb')
    output.setparams(params)

    w.close()


    # Manipulate data before writing to copy file
    data = list(data)

    if len(bin_string) > len(data):
        print('SizeError: Input string too long.')
    else:
        # Write data to least significant bits of wave data
        for i in range(len(bin_string)):
            if data[i] % 2 == int(bin_string[i]) % 2:
                pass
            else:
                # Prevents values in data from going out of range(0, 256) and causing ValueError with bytes()
                if data[i] >= 255:
                    data[i] -= 1
                else:
                    data[i] += 1
            
    data = bytes(data)

    # Finish up
    output.writeframes(data)
    output.close()
    
