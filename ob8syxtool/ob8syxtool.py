#
# MIT License
#
# Copyright (c) 2022 Christian-E! / Ten by Ten Software
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

#
# This script will print the program parameters for
# an Oberheim OB-8 sysex file
#

import argparse

# combines two nibbles into a byte
def byteNibbles(lsb,msb):
	b = lsb
	b |= (msb & 0xf) << 4 
	return b

# 
def onOff(val):
	if val == 0:
		return ' '
	return '*'

# dumps the program number in format ABCD-12345678
def dumpOB8ProgramNumber(prog):
	dump = '=== Program '

	groupNum = int(prog / 8) + 1
	if groupNum & 0x1:
		dump += 'A'
	if groupNum & 0x2:
		dump += 'B'
	if groupNum & 0x4:
		dump += 'C'
	if groupNum & 0x8:
		dump += 'D'

	progNum = prog % 8 + 1

	dump += '-{}  ({}) ===\n'.format(progNum,prog+1)

	return dump

# creates a string with the program information
def dumpOB8Programs(buf):

	# dump is the output string
	dump = ''
	
	for i in range(int(len(buf)/60)):
	
		# program number (ABCD-12345678)
		dump += dumpOB8ProgramNumber(buf[i*60+4])

		# program data begins at byte 5
		# 0
		progDataOffset = i*60+5 
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		vcfRel 		= d >> 2
		lfoWave 	= (d & 0x3) << 1

		# 1
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		vcaRel 		= d >> 2
		unison 		= onOff(d & 0x1)
		lfoWave 	= lfoWave | ((d >> 1) & 0x1)
		lfoWaveTri = onOff(lfoWave & 0x1)
		lfoWaveSqr = onOff(lfoWave & 0x2)
		lfoWaveSnH = onOff(lfoWave & 0x4)

		# 2
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		vcfDcy 		= d >> 2
		filterFM	= onOff(d & 0x2)
		osc2FM		= onOff(d & 0x1)

		# 3
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		vcaDcy 		= d >> 2
		osc2Wave	= d & 0x3
		osc2WaveTri = onOff(osc2Wave & 0x1)
		osc2WaveSqr = onOff(osc2Wave & 0x2)

		# 4
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		vcfAtk 		= d >> 2
		osc1Wave	= d & 0x3
		osc1WaveTri = onOff(osc1Wave & 0x1)
		osc1WaveSqr = onOff(osc1Wave & 0x2)

		# 5
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		vcaAtk 		= d >> 2
		osc2PWM		= onOff(d & 0x2)
		osc1PWM 	= onOff(d & 0x1)

		# 6
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		vcfSus 		= d >> 2
		noise		= onOff(d & 0x2)
		fourPole 	= onOff(d & 0x1)

		# 7
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		vcaSus 		= d >> 2
		osc2On		= onOff(d & 0x2)
		osc2Half 	= onOff(d & 0x1)

		# 8
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		vcfMod 		= d >> 2
		osc1On		= onOff(d & 0x2)
		kbdTrack 	= onOff(d & 0x1)

		# 9
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		vcfRes 		= d >> 2
		pw1180		= onOff(d & 0x2)
		vco1180 	= onOff(d & 0x1)

		# 10
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		oscPWM 		= d >> 2
		vcaMod		= onOff(d & 0x2)
		fEnv	 	= onOff(d & 0x1)

		# 11
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		lfoFreq 	= d >> 2
		sync		= onOff(d & 0x2)
		osc1FM	 	= onOff(d & 0x1)

		# 12
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		fmAmnt 		= d >> 2
		volume		= (d & 0x3) << 4

		# 13
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		pwmAmnt 	= d >> 2
		volume		= volume | (d & 0x3) << 2

		# 14
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		portAmt 	= d >> 2
		volume		= volume | (d & 0x3)

		# 15
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		osc2Detune 	= d >> 2
		vco2PW		= (d & 0x3) << 4

		# 16
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		vcfFreq 	= d >> 2
		vco2PW		= vco2PW | (d & 0x3) << 2

		# 17
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		vco2Freq 	= d >> 2
		vco2PW		= vco2PW | (d & 0x3)

		# 18
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		vco1Freq	= d >> 2
		spare		= onOff(d & 0x2)
		legato 		= onOff(d & 0x1)

		# 19
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		lfoTrigPoint= d >> 2
		trigLfoWave	= (d & 0x3) << 1

		# 20
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		pedalSustn	= d >> 2
		portBend	= onOff(d & 0x1)
		trigLfoWave	= trigLfoWave | ((d >> 1) & 0x1)
		trigLfoWaveTri = onOff(trigLfoWave & 0x1)
		trigLfoWaveSqr = onOff(trigLfoWave & 0x2)
		trigLfoWaveSnH = onOff(trigLfoWave & 0x4)

		# 21
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		fmVibRaise	= d >> 2
		lfoTrack	= onOff(d & 0x2)
		fmDlyInvert	= onOff(d & 0x1)

		# 22
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		pwmVibRaise	= d >> 2
		portQuant	= onOff(d & 0x2)
		portMatch	= onOff(d & 0x1)

		# 23
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		fmVibDelay	= d >> 2
		_180		= onOff(d & 0x2)
		_90			= onOff(d & 0x1) 

		# 24
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		pwmVibDelay	= d >> 2
		pwmDlyInvert= onOff(d & 0x2)
		pwmQuant	= onOff(d & 0x1)

		# 25
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		voiceDetune	= d >> 2
		expoPort	= onOff(d & 0x2)
		constPort	= onOff(d & 0x1)

		# 26
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		bendAmount	= d >> 2
		lfoRateDelay= onOff(d & 0x2)
		fmQuant		= onOff(d & 0x1)

		dump += 'Master: \n'
		dump += '  Program Volume:{}  Bend:{}\n'.format(volume,bendAmount)

		dump += 'Control: \n'
		dump += '  Portamento:{}  \n'.format(portAmt)
		dump += '  Unison:{}  \n'.format(unison)
		dump += '  Osc2_Detune:{}  \n'.format(osc2Detune)

		dump += 'Modulation: \n'
		dump += '  LFO_Rate:{: <2}  Mod_Depth_1:{: <2}  Mod_Depth_2:{: <2}  \n'.format(lfoFreq,fmAmnt,pwmAmnt)
		dump += '  Wave_Tri:{}      Osc1_Frq:{}      Osc1_PWM:{}  \n'.format(lfoWaveTri,osc1FM,osc1PWM)
		dump += '  Wave_Sqr:{}      Osc2_Frq:{}      Osc2_PWM:{}  \n'.format(lfoWaveSqr,osc2FM,osc2PWM)
		dump += '  Wave_S/H:{}    Filter_Frq:{}    Volume_Mod:{}  \n'.format(lfoWaveSnH,filterFM,vcaMod)

		dump += 'Oscillators: \n'
		dump += '  Osc1_Frq:{: <2}                       Pulse_Width:{: <2}   Osc2_Frq:{}  \n'.format(vco1Freq,oscPWM,vco2Freq)
		dump += '  Osc1_Wave_Tri:{}  Osc1_Wave_Sqr:{}  Sync:{}  F-Env:{}  Osc1_Wave_Tri:{}  Osc1_Wave_Sqr:{}  \n'.format(osc1WaveTri,osc1WaveSqr,sync,fEnv,osc2WaveTri,osc2WaveSqr)

		dump += 'Filter: \n'
		dump += '  Frequency:{: <2}            Resonance:{: <2}          Mod:ulation:{: <2}  \n'.format(vcfFreq,vcfRes,vcfMod)
		dump += '  Osc1_On:{}  Osc2_Half:{}  Osc2_Full:{}  Noise:{}  4_Pole:{}  Kbd_Track:{}  \n'.format(osc1On,osc2Half,osc2On,noise,fourPole,kbdTrack)

		dump += 'Envelopes: \n'
		dump += '  VCF A:{: <2}  D:{: <2}  S:{: <2}  R:{: <2}  \n'.format(vcfAtk,vcfDcy,vcfSus,vcfRel)
		dump += '  VCA A:{: <2}  D:{: <2}  S:{: <2}  R:{: <2}  \n'.format(vcaAtk,vcaDcy,vcaSus,vcaRel)

		dump += '-- Page 2 -- \n'
		dump += 'Control: \n'
		dump += '  Portamento_Bend:{}  \n'.format(portBend)
		dump += '  Voice_Detune:{}  \n'.format(voiceDetune)
		dump += 'Modulation: \n'
		dump += '  Trig_Wave_Tri:{}  Quantize_1:{}   Quantize_2:{}  \n'.format(trigLfoWaveTri,fmQuant,pwmQuant)
		dump += '  Trig_Wave_Sqr:{}    Invert_1:{}     Invert_2:{}  \n'.format(trigLfoWaveSqr,fmDlyInvert,pwmDlyInvert)
		dump += '  Trig_Wave_S/H:{}   LFO_Track:{}  LFO_Env_Mod:{}  \n'.format(trigLfoWaveSnH,lfoTrack,lfoRateDelay)
		dump += 'Oscillators: \n'
		dump += '  LFO Phase: 90:{}  180:{}  '.format(_90,_180)
		dump += 'Osc1_LFO_Mod_Invert: Freq:{}  PWM:{}  '.format(vco1180,pw1180)
		dump += 'Portamento: Match:{}  Quantize:{}  \n'.format(portMatch,portQuant)
		dump += 'Filter: \n'
		dump += '  Portamento: Legato:{}  Equal_Time:{}  Exponential:{}  \n'.format(legato,constPort,expoPort)
		dump += 'Envelopes: \n'
		dump += '  Delay_Mod_1:{}  Attack_Mod_1:{}  LFO_Trig_Point:{}  \n'.format(fmVibDelay,fmVibRaise,lfoTrigPoint)
		dump += '  Delay_Mod_2:{}  Attack_Mod_2:{}   Pedal_Release:{}  \n'.format(pwmVibDelay,pwmVibRaise,pedalSustn)

		dump += '\n'

	return dump

# main
parser = argparse.ArgumentParser(description='Dumps the patch settings contained in Oberheim OB-8 sysex files')
parser.add_argument('inputFile',
type=argparse.FileType('rb'), nargs='+',  metavar='file', help='OB-8 sysex input files')
args = parser.parse_args()

for f in args.inputFile:
	buf = f.read()
	if (len(buf) % 60) or (buf[:4] != b'\xf0\x10\x01\x01'):
		print('This does not appear to be an OB-8 sysex file')
		parser.print_usage()
		continue
	else:
		print(f.name)
		print(dumpOB8Programs(buf))
