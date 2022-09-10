# OB8 ob8syxtool

## What This Script Does
This Python script prints the program parameters for
Oberheim OB-8 programs from system exclusive dumps created by the OB-8 firmware B5, as documented in the OB-8 service manual August 15, 1984.

## Why This Script
I wanted to understand the OB-8 factory preset programs and document my own programs. I could not find another free way to do this.

## What You Need
This script requires a file with Oberheim system exclusive dumps. 
It expects the first four bytes of the file to be `F0100101`, and then prints one or more 60-byte programs that follow in the file.

To dump a program from an OB-8:
- Select a **stored** program
- Enable MIDI program change and dump messages by turning on the 'A' switch on Page 2 (it is always off at power-on)
- Briefly hold the 'Write' switch on Page 2

## Help
Here is the output of `python3 ob8syxtool.py -h` :
```
usage: ob8syxtool.py [-h] file [file ...]

Dumps the patch settings contained in Oberheim OB-8 sysex files

positional arguments:
  file        OB-8 sysex input files

optional arguments:
  -h, --help  show this help message and exit
```