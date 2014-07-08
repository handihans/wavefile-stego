
import wave
from sys import argv


if argv[1] == '--help':
    print('Usage: python3 [SCRIPT] [WAVEFILE] [OUTFILE]')
    print('[SCRIPT] is the name of this script')
    print('[WAVEFILE] must be a .wav file.')
    print('[OUTFILE] must be an empty textfile.')

else:
    script, inwave, outfile = argv

    print('Reading wave data...')
    w = wave.open(inwave, 'rb')
    data = list(w.readframes(w.getnframes()))
    w.close()

    print('Reading least significant bits...')
    # Get bit spacing from LSB of the first 8 bytes
    spacing = ''
    for i in data[:8]:
        spacing += str(i % 2)
    spacing = int(spacing, 2)

    # Create list of least significant bits from wave data
    bitdata = []
    for i in range(8, len(data), spacing):
        bitdata.append(data[i] % 2)


    # Create list of byte-sized chunks
    byte_string = ''
    for i in bitdata:
        byte_string += str(i)

    byte_chunks = []
    for i in range(int(len(byte_string) / 8)):
        byte_chunks.append(byte_string[i*8:i*8+8])

    end_string = ''
    for i in byte_chunks:
        if int(i, 2) < 256   and int(i, 2) >= 10:
            end_string += chr(int(i, 2))
        else:
            break

    print('Writing to dumpfile...')
    # Dump 'end_string' to 'outfile'
    f = open(outfile, 'w')
    f.write(end_string)
    f.close()
