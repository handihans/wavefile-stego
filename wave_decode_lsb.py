
import wave
from sys import argv


if argv[1] == '--help':
    print('Usage: python3 [SCRIPT] [WAVEFILE] [OUTFILE]')
    print('ORIGINAL and MODIFIED must be .wav files.')
    print('OUTFILE must be an empty textfile.')
    
else:
    script, inwave, outfile = argv

    w = wave.open(inwave, 'rb')
    data = list(w.readframes(w.getnframes()))
    w.close()

    # Create list of least significant bits from wave data
    bitdata = []
    for i in data:
        bitdata.append(i % 2)
    

    # Create list of byte-sized chunks
    byte_string = ''
    for i in bitdata:
        byte_string += str(i)
        
    byte_chunks = []
    for i in range(int(len(byte_string) / 8)):
        byte_chunks.append(byte_string[i*8:i*8+8])

    end_string = ''
    for i in byte_chunks:
        end_string += chr(int(i, 2))
    
    # Dump 'end_string' to 'outfile'
    f = open(outfile, 'w')
    f.write(end_string)
    f.close()

    

    
    

    

    
