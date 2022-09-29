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
from ast import dump
from sys import stdout

# combines two nibbles into a byte
def byteNibbles(lsb,msb):
	b = lsb
	b |= (msb & 0xf) << 4 
	return b

# 
def ledOnOff(val):
	if val == 0:
		return ' '
	return '*'

#
def intOnOff(val):
	return int(bool(val))

# gets the program group number ABCD
def getOB8ProgramGroup(prog):

	groupString = ''
	groupNum = int(prog / 8) + 1
	if groupNum & 0x1:
		groupString += 'A'
	if groupNum & 0x2:
		groupString += 'B'
	if groupNum & 0x4:
		groupString += 'C'
	if groupNum & 0x8:
		groupString += 'D'
	return groupString

# gets the program number 1-8
def getOB8ProgramNumber(prog):
	return prog % 8 + 1

# creates a string with the program information
def dumpOB8ProgramsText(programsArray):

	# dump is the output string
	dump = ''

	for programDict in programsArray:

		# program number (ABCD-12345678)
		dump += '=== Program {}-{}  ({}) ===\n'.format(programDict['programGroup'],programDict['programNumber'],programDict['programIndex'])

		dump += 'Master: \n'
		dump += '  Program Volume:{}  Bend:{}\n'.format(programDict['volume'],programDict['bendAmount'])

		dump += 'Control: \n'
		dump += '  Portamento:{}  \n'.format(programDict['portAmt'])
		dump += '  Unison:{}  \n'.format(ledOnOff(programDict['unison']))
		dump += '  Osc2_Detune:{}  \n'.format(programDict['osc2Detune'])

		dump += 'Modulation: \n'
		dump += '  LFO_Rate:{: <2}  Mod_Depth_1:{: <2}  Mod_Depth_2:{: <2}  \n'.format(programDict['lfoFreq'],programDict['fmAmnt'],programDict['pwmAmnt'])
		dump += '  Wave_Tri:{}      Osc1_Frq:{}      Osc1_PWM:{}  \n'.format(ledOnOff(programDict['lfoWaveTri']),ledOnOff(programDict['osc1FM']),ledOnOff(programDict['osc1PWM']))
		dump += '  Wave_Sqr:{}      Osc2_Frq:{}      Osc2_PWM:{}  \n'.format(ledOnOff(programDict['lfoWaveSqr']),ledOnOff(programDict['osc2FM']),ledOnOff(programDict['osc2PWM']))
		dump += '  Wave_S/H:{}    Filter_Frq:{}    Volume_Mod:{}  \n'.format(ledOnOff(programDict['lfoWaveSnH']),ledOnOff(programDict['filterFM']),ledOnOff(programDict['vcaMod']))

		dump += 'Oscillators: \n'
		dump += '  Osc1_Frq:{: <2}                       Pulse_Width:{: <2}   Osc2_Frq:{}  \n'.format(programDict['vco1Freq'],programDict['oscPWM'],programDict['vco2Freq'])
		dump += '  Osc1_Wave_Tri:{}  Osc1_Wave_Sqr:{}  Sync:{}  F-Env:{}  Osc1_Wave_Tri:{}  Osc1_Wave_Sqr:{}  \n'.format(ledOnOff(programDict['osc1WaveTri']),ledOnOff(programDict['osc1WaveSqr']),ledOnOff(programDict['sync']),ledOnOff(programDict['fEnv']),ledOnOff(programDict['osc2WaveTri']),ledOnOff(programDict['osc2WaveSqr']))

		dump += 'Filter: \n'
		dump += '  Frequency:{: <2}            Resonance:{: <2}          Mod:ulation:{: <2}  \n'.format(programDict['vcfFreq'],programDict['vcfRes'],programDict['vcfMod'])
		dump += '  Osc1_On:{}  Osc2_Half:{}  Osc2_Full:{}  Noise:{}  4_Pole:{}  Kbd_Track:{}  \n'.format(ledOnOff(programDict['osc1On']),ledOnOff(programDict['osc2Half']),ledOnOff(programDict['osc2On']),ledOnOff(programDict['noise']),ledOnOff(programDict['fourPole']),ledOnOff(programDict['kbdTrack']))

		dump += 'Envelopes: \n'
		dump += '  VCF A:{: <2}  D:{: <2}  S:{: <2}  R:{: <2}  \n'.format(programDict['vcfAtk'],programDict['vcfDcy'],programDict['vcfSus'],programDict['vcfRel'])
		dump += '  VCA A:{: <2}  D:{: <2}  S:{: <2}  R:{: <2}  \n'.format(programDict['vcaAtk'],programDict['vcaDcy'],programDict['vcaSus'],programDict['vcaRel'])

		dump += '-- Page 2 -- \n'
		dump += 'Control: \n'
		dump += '  Portamento_Bend:{}  \n'.format(ledOnOff(programDict['portBend']))
		dump += '  Voice_Detune:{}  \n'.format(programDict['voiceDetune'])
		dump += 'Modulation: \n'
		dump += '  Trig_Wave_Tri:{}  Quantize_1:{}   Quantize_2:{}  \n'.format(ledOnOff(programDict['trigLfoWaveTri']),ledOnOff(programDict['fmQuant']),ledOnOff(programDict['pwmQuant']))
		dump += '  Trig_Wave_Sqr:{}    Invert_1:{}     Invert_2:{}  \n'.format(ledOnOff(programDict['trigLfoWaveSqr']),ledOnOff(programDict['fmDlyInvert']),ledOnOff(programDict['pwmDlyInvert']))
		dump += '  Trig_Wave_S/H:{}   LFO_Track:{}  LFO_Env_Mod:{}  \n'.format(ledOnOff(programDict['trigLfoWaveSnH']),ledOnOff(programDict['lfoTrack']),ledOnOff(programDict['lfoRateDelay']))
		dump += 'Oscillators: \n'
		dump += '  LFO Phase: 90:{}  180:{}  '.format(ledOnOff(programDict['_90']),ledOnOff(programDict['_180']))
		dump += 'Osc1_LFO_Mod_Invert: Freq:{}  PWM:{}  '.format(ledOnOff(programDict['vco1180']),ledOnOff(programDict['pw1180']))
		dump += 'Portamento: Match:{}  Quantize:{}  \n'.format(ledOnOff(programDict['portMatch']),ledOnOff(programDict['portQuant']))
		dump += 'Filter: \n'
		dump += '  Portamento: Legato:{}  Equal_Time:{}  Exponential:{}  \n'.format(ledOnOff(programDict['legato']),ledOnOff(programDict['constPort']),ledOnOff(programDict['expoPort']))
		dump += 'Envelopes: \n'
		dump += '  Delay_Mod_1:{}  Attack_Mod_1:{}  LFO_Trig_Point:{}  \n'.format(programDict['fmVibDelay'],programDict['fmVibRaise'],programDict['lfoTrigPoint'])
		dump += '  Delay_Mod_2:{}  Attack_Mod_2:{}   Pedal_Release:{}  \n'.format(programDict['pwmVibDelay'],programDict['pwmVibRaise'],programDict['pedalSustn'])

		dump += '\n'

	return dump

# dumps a JS Dictionay of the parameters
def dumpOB8ProgramDictToJS(programDict):
	dump = 'program = {' 
	dump += 'programIndex:{},'.format(programDict['programIndex'])
	dump += 'programGroup:\'{}\','.format(programDict['programGroup'])
	dump += 'programNumber:{},'.format(programDict['programNumber'])
	dump += 'vcfRel:{},'.format(programDict['vcfRel'])
	dump += 'lfoWave:{},'.format(programDict['lfoWave'])
	dump += 'vcaRel:{},'.format(programDict['vcaRel'])
	dump += 'unison:{},'.format(programDict['unison'])
	dump += 'lfoWave:{},'.format(programDict['lfoWave'])
	dump += 'lfoWaveTri:{},'.format(programDict['lfoWaveTri'])
	dump += 'lfoWaveSqr:{},'.format(programDict['lfoWaveSqr'])
	dump += 'lfoWaveSnH:{},'.format(programDict['lfoWaveSnH'])
	dump += 'vcfDcy:{},'.format(programDict['vcfDcy'])
	dump += 'filterFM:{},'.format(programDict['filterFM'])
	dump += 'osc2FM:{},'.format(programDict['osc2FM'])
	dump += 'vcaDcy:{},'.format(programDict['vcaDcy'])
	dump += 'osc2Wave:{},'.format(programDict['osc2Wave'])
	dump += 'osc2WaveTri:{},'.format(programDict['osc2WaveTri'])
	dump += 'osc2WaveSqr:{},'.format(programDict['osc2WaveSqr'])
	dump += 'vcfAtk:{},'.format(programDict['vcfAtk'])
	dump += 'osc1Wave:{},'.format(programDict['osc1Wave'])
	dump += 'osc1WaveTri:{},'.format(programDict['osc1WaveTri'])
	dump += 'osc1WaveSqr:{},'.format(programDict['osc1WaveSqr'])
	dump += 'vcaAtk:{},'.format(programDict['vcaAtk'])
	dump += 'osc2PWM:{},'.format(programDict['osc2PWM'])
	dump += 'osc1PWM:{},'.format(programDict['osc1PWM'])
	dump += 'vcfSus:{},'.format(programDict['vcfSus'])
	dump += 'noise:{},'.format(programDict['noise'])
	dump += 'fourPole:{},'.format(programDict['fourPole'])
	dump += 'vcaSus:{},'.format(programDict['vcaSus'])
	dump += 'osc2On:{},'.format(programDict['osc2On'])
	dump += 'osc2Half:{},'.format(programDict['osc2Half'])
	dump += 'vcfMod:{},'.format(programDict['vcfMod'])
	dump += 'osc1On:{},'.format(programDict['osc1On'])
	dump += 'kbdTrack:{},'.format(programDict['kbdTrack'])
	dump += 'vcfRes:{},'.format(programDict['vcfRes'])
	dump += 'pw1180:{},'.format(programDict['pw1180'])
	dump += 'vco1180:{},'.format(programDict['vco1180'])
	dump += 'oscPWM:{},'.format(programDict['oscPWM'])
	dump += 'vcaMod:{},'.format(programDict['vcaMod'])
	dump += 'fEnv:{},'.format(programDict['fEnv'])
	dump += 'lfoFreq:{},'.format(programDict['lfoFreq'])
	dump += 'sync:{},'.format(programDict['sync'])
	dump += 'osc1FM:{},'.format(programDict['osc1FM'])
	dump += 'fmAmnt:{},'.format(programDict['fmAmnt'])
	dump += 'pwmAmnt:{},'.format(programDict['pwmAmnt'])
	dump += 'portAmt:{},'.format(programDict['portAmt'])
	dump += 'volume:{},'.format(programDict['volume'])
	dump += 'osc2Detune:{},'.format(programDict['osc2Detune'])
	dump += 'vcfFreq:{},'.format(programDict['vcfFreq'])
	dump += 'vco2Freq:{},'.format(programDict['vco2Freq'])
	dump += 'vco2PW:{},'.format(programDict['vco2PW'])
	dump += 'vco1Freq:{},'.format(programDict['vco1Freq'])
	dump += 'spare:{},'.format(programDict['spare'])
	dump += 'legato:{},'.format(programDict['legato'])
	dump += 'lfoTrigPoint:{},'.format(programDict['lfoTrigPoint'])
	dump += 'pedalSustn:{},'.format(programDict['pedalSustn'])
	dump += 'portBend:{},'.format(programDict['portBend'])
	dump += 'trigLfoWave:{},'.format(programDict['trigLfoWave'])
	dump += 'trigLfoWaveTri:{},'.format(programDict['trigLfoWaveTri'])
	dump += 'trigLfoWaveSqr:{},'.format(programDict['trigLfoWaveSqr'])
	dump += 'trigLfoWaveSnH:{},'.format(programDict['trigLfoWaveSnH'])
	dump += 'fmVibRaise:{},'.format(programDict['fmVibRaise'])
	dump += 'lfoTrack:{},'.format(programDict['lfoTrack'])
	dump += 'fmDlyInvert:{},'.format(programDict['fmDlyInvert'])
	dump += 'pwmVibRaise:{},'.format(programDict['pwmVibRaise'])
	dump += 'portQuant:{},'.format(programDict['portQuant'])
	dump += 'portMatch:{},'.format(programDict['portMatch'])
	dump += 'fmVibDelay:{},'.format(programDict['fmVibDelay'])
	dump += '_180:{},'.format(programDict['_180'])
	dump += '_90:{},'.format(programDict['_90'])
	dump += 'pwmVibDelay:{},'.format(programDict['pwmVibDelay'])
	dump += 'pwmDlyInvert:{},'.format(programDict['pwmDlyInvert'])
	dump += 'pwmQuant:{},'.format(programDict['pwmQuant'])
	dump += 'voiceDetune:{},'.format(programDict['voiceDetune'])
	dump += 'expoPort:{},'.format(programDict['expoPort'])
	dump += 'constPort:{},'.format(programDict['constPort'])
	dump += 'bendAmount:{},'.format(programDict['bendAmount'])
	dump += 'lfoRateDelay:{},'.format(programDict['lfoRateDelay'])
	dump += 'fmQuant:{},'.format(programDict['fmQuant'])
	dump += '}\n'
	return dump

def dumpOB8TopBoilerplateHTML():
	dump = '<!DOCTYPE html>\n'
	dump += '<html>\n'
	dump += '<head>\n'
	dump += '<style>\n'
	dump += '	body {\n'
	dump += '		background-color: black;\n'
	dump += '		color: white;\n'
	dump += '	}\n'
	dump += '	table {\n'
	dump += '		font-family: \'Handel Gothic\', \'Lucida Sans\', \'Lucida Sans Regular\', \'Lucida Grande\', \'Lucida Sans Unicode\', Geneva, Verdana, sans-serif;\n'
	dump += '		padding: 0 1em;\n'
	dump += '	}\n'
	dump += '	.panel {\n'
	dump += '		background-image: linear-gradient(#050570 1px, transparent 1px);\n'
	dump += '		background-size: 100% 1em;\n'
	dump += '	}\n'
	dump += '	thead {\n'
	dump += '		font-weight: bold;\n'
	dump += '		font-size: larger;\n'
	dump += '	}\n'
	dump += '	h1 {\n'
	dump += '		background-color: black;\n'
	dump += '		font-family: \'Handel Gothic\', \'Lucida Sans\', \'Lucida Sans Regular\', \'Lucida Grande\', \'Lucida Sans Unicode\', Geneva, Verdana, sans-serif;\n'
	dump += '		padding-left: 20px;\n'
	dump += '	}\n'
	dump += '	h2 {\n'
	dump += '		background-color: black;\n'
	dump += '		font-family: \'Handel Gothic\', \'Lucida Sans\', \'Lucida Sans Regular\', \'Lucida Grande\', \'Lucida Sans Unicode\', Geneva, Verdana, sans-serif;\n'
	dump += '		padding: 0.5em 20px;\n'
	dump += '		border: solid white 1px;\n'
	dump += '	}\n'
	dump += '	tr {\n'
	dump += '		vertical-align: top;\n'
	dump += '	}\n'
	dump += '	td {\n'
	dump += '		font-weight: light;\n'
	dump += '		text-align: center;\n'
	dump += '		padding: .5em .5em 0;\n'
	dump += '		width: 10em;\n'
	dump += '	}\n'
	dump += '	.label polyline {\n'
	dump += '		fill: none;\n'
	dump += '		stroke: white;\n'
	dump += '		stroke-width: 1\n'
	dump += '	}\n'
	dump += '	.page2label {\n'
	dump += '		color:#66aaff;\n'
	dump += '		font-weight:light;\n'
	dump += '		font-size: small;\n'
	dump += '	}\n'
	dump += '	.button rect {\n'
	dump += '		fill: black;\n'
	dump += '		stroke: #050570;\n'
	dump += '		stroke-width: 1\n'
	dump += '	}\n'
	dump += '	.knob circle {\n'
	dump += '		fill: black;\n'
	dump += '		stroke: #050570;\n'
	dump += '		stroke-width: 1\n'
	dump += '	}\n'
	dump += '	.knob polygon {\n'
	dump += '		fill: white;\n'
	dump += '	}\n'
	dump += '	.knob td {\n'
	dump += '		padding: 0\n'
	dump += '	}\n'
	dump += '	.button td {\n'
	dump += '		padding: 0\n'
	dump += '	}\n'
	dump += '</style>\n'
	dump += '</head>\n'
	dump += '<body>\n'
	dump += '<script>\n'
	dump += '	function makeTriangleSVG() {\n'
	dump += '		return \'<svg class="label" height="1em" width="2em" viewBox="0 -1 20 12"><polyline <polyline points="0,10 10,0 20,10"/>/></svg>\'\n'
	dump += '	}\n'
	dump += '	function makeSquareSVG() {\n'
	dump += '		return \'<svg class="label" height="1em" width="2em" viewBox="0 -1 20 12"><polyline points="0,10 0,0 10,0 10,10 20,10"/></svg>\'\n'
	dump += '	}\n'
	dump += '	function makeThreeWaveSVG() {\n'
	dump += '		return \'<svg class="label" height="1em" width="8em" viewBox="10 -1 70 12">\\n'
	dump += '								<polyline points="0,20 20,0, 20,20"/>\\n'
	dump += '								<polyline points="30,10 40,0 50,10"/>\\n'
	dump += '								<polyline points="60,10 60,0 70,0 70,10 80,10"/>\\n'
	dump += '							</svg>\'\n'
	dump += '	}\n'
	dump += '	function makeTableCell(cellText, cellClass, doubleWide = false) {\n'
	dump += '		var cell = document.createElement(\'td\');\n'
	dump += '		cell.innerHTML = cellText;\n'
	dump += '		cell.className = cellClass;\n'
	dump += '		if (doubleWide) {\n'
	dump += '			cell.colSpan = 2;\n'
	dump += '		}\n'
	dump += '		return cell;\n'
	dump += '	}\n'
	dump += '	function makeLabelCell(label, doubleWide = false) {\n'
	dump += '		return makeTableCell(label, \'label\', doubleWide);\n'
	dump += '	}\n'
	dump += '	function makeLabelRow(columnArray, doubleWide = false) {\n'
	dump += '		var row = document.createElement(\'tr\');\n'
	dump += '		row.className = \'label\';\n'
	dump += '		columnArray.forEach(label => {\n'
	dump += '			row.appendChild(makeLabelCell(label, doubleWide));\n'
	dump += '		});\n'
	dump += '		return row;\n'
	dump += '	}\n'
	dump += '	function makeLabelRow2(columnArray, doubleWide = false) {\n'
	dump += '		var row = document.createElement(\'tr\');\n'
	dump += '		row.className = \'page2label\';\n'
	dump += '		columnArray.forEach(label => {\n'
	dump += '			row.appendChild(makeLabelCell(label, doubleWide));\n'
	dump += '		});\n'
	dump += '		return row;\n'
	dump += '	}\n'
	dump += '	function makeKnobCell(value, doubleWide) {\n'
	dump += '		// rotation 0 points straight up, 180 points straight down\n'
	dump += '		// values from 0-63 should be -145 to +145\n'
	dump += '		rotationValue = value * 290 / 62 - 145;\n'
	dump += '		var cell = document.createElement(\'td\');\n'
	dump += '		cell.innerHTML = \'<svg class="knob" height="4em" width="4em" viewBox="-1 -1 32 32">\\n'
	dump += '			<circle r="15" cx="15" cy="15"/>\\n'
	dump += '			<circle r="7" cx="15" cy="15"/>\\n'
	dump += '			<circle r="5" cx="15" cy="15"/>\\n'
	dump += '			<polygon points="15,0 18,8 12,8" transform="rotate(\'\n'
	dump += '			+ rotationValue +\n'
	dump += '			\', 15, 15)"/></svg>\';\n'
	dump += '		if (doubleWide) {\n'
	dump += '			cell.colSpan = 2;\n'
	dump += '		}\n'
	dump += '		return cell;\n'
	dump += '	}\n'
	dump += '	function makeKnobRow(valueArray, doubleWide = false) {\n'
	dump += '		var row = document.createElement(\'tr\');\n'
	dump += '		row.className = \'knob\';\n'
	dump += '		valueArray.forEach(value => {\n'
	dump += '			if (value == null) {\n'
	dump += '				row.appendChild(makeLabelCell(\'\', doubleWide));\n'
	dump += '			}\n'
	dump += '			else {\n'
	dump += '				row.appendChild(makeKnobCell(value, doubleWide));\n'
	dump += '			}\n'
	dump += '		});\n'
	dump += '		return row;\n'
	dump += '	}\n'
	dump += '	function makeButtonSVG(value) {\n'
	dump += '		led = \'\';\n'
	dump += '		if (value) {\n'
	dump += '			led = \'<circle style="fill:red" r="4" cx="15" cy="8"/>\';\n'
	dump += '		}\n'
	dump += '		return \'<svg class="button" height="3em" width="3em" viewBox="-1 -1 32 32">\\n'
	dump += '			<rect width="30" height="30"/>\\n'
	dump += '			<rect x="2" y="14" width="26" height="14"/>\'\n'
	dump += '			+ led + \'</svg>\';\n'
	dump += '	}\n'
	dump += '	function makeButtonCell(value) {\n'
	dump += '		var cell = document.createElement(\'td\');\n'
	dump += '		cell.innerHTML = makeButtonSVG(value);\n'
	dump += '		return cell;\n'
	dump += '	}\n'
	dump += '	function makeButtonRow(columnArray) {\n'
	dump += '		var row = document.createElement(\'tr\');\n'
	dump += '		row.className = \'button\';\n'
	dump += '		columnArray.forEach(value => {\n'
	dump += '			if (value == null) {\n'
	dump += '				row.appendChild(makeLabelCell(\'\'));\n'
	dump += '			}\n'
	dump += '			else if (value == 0 || value == 1) {\n'
	dump += '				row.appendChild(makeButtonCell(value));\n'
	dump += '			}\n'
	dump += '			else if (Array.isArray(value)) {\n'
	dump += '				var cell = document.createElement(\'td\');\n'
	dump += '				if (value[0] == \'triangle\') {\n'
	dump += '					cell.innerHTML = makeTriangleSVG() + makeButtonSVG(value[1]);\n'
	dump += '				}\n'
	dump += '				else if (value[0] == \'square\') {\n'
	dump += '					cell.innerHTML = makeSquareSVG() + makeButtonSVG(value[1]);\n'
	dump += '				}\n'
	dump += '				else if (value[0] == \'s/h\') {\n'
	dump += '					cell.innerHTML = \'S/H\' + makeButtonSVG(value[1]);\n'
	dump += '				}\n'
	dump += '				row.appendChild(cell);\n'
	dump += '			}\n'
	dump += '		});\n'
	dump += '		return row;\n'
	dump += '	}\n'
	dump += '	function makeParameterGroupTable() {\n'
	dump += '		return document.createElement(\'table\');\n'
	dump += '	}\n'
	dump += '	function makeMasterTable(program) {\n'
	dump += '		var table = makeParameterGroupTable();\n'
	dump += '		table.appendChild(makeLabelRow([\'MASTER<br/>VOLUME\', \'\', \'PROGRAM<br/>VOL/BAL\']));\n'
	dump += '		table.appendChild(makeKnobRow([0, null, program.volume]));\n'
	dump += '		table.appendChild(makeLabelRow([\'AUTO<br/>TUNE\', \'<br/>HOLD\', \'CHORD/<br/>PAGE&nbsp;2\']));\n'
	dump += '		table.appendChild(makeButtonRow([0, 0, 0]));\n'
	dump += '		table.appendChild(makeLabelRow([\'\', \'MASTER<br/>TUNE\', \'\']));\n'
	dump += '		table.appendChild(makeKnobRow([null, 31, null]));\n'
	dump += '		return table;\n'
	dump += '	}\n'
	dump += '	function makeControlTable(program) {\n'
	dump += '		var table = makeParameterGroupTable();\n'
	dump += '		table.appendChild(makeLabelRow([\'<br/>PORTAMENTO\']));\n'
	dump += '		table.appendChild(makeKnobRow([program.portAmt]));\n'
	dump += '		table.appendChild(makeLabelRow([\'<br/>UNISON\']));\n'
	dump += '		table.appendChild(makeButtonRow([program.unison]));\n'
	dump += '		table.appendChild(makeLabelRow([\'<br/>OSC&nbsp;2&nbsp;DETUNE\']));\n'
	dump += '		table.appendChild(makeKnobRow([program.osc2Detune]));\n'
	dump += '		return table;\n'
	dump += '	}\n'
	dump += '	function makeModulationTable(program) {\n'
	dump += '		var table = makeParameterGroupTable();\n'
	dump += '		table.appendChild(makeLabelRow([\'LFO<br/>RATE\', \'MODULATION<br/>DEPTH 1\', \'MODULATION<br/>DEPTH&nbsp;2\']));\n'
	dump += '		table.appendChild(makeKnobRow([program.lfoFreq, program.fmAmnt, program.pwmAmnt]));\n'
	dump += '		table.appendChild(makeLabelRow([\'WAVEFORM\', \'OSC&nbsp;1&nbsp;FRQ\', \'OSC&nbsp;1&nbsp;PWM\']));\n'
	dump += '		table.appendChild(makeButtonRow([[\'triangle\', program.lfoWaveTri], program.osc1FM, program.osc1PWM]));\n'
	dump += '		table.appendChild(makeLabelRow([\'\', \'OSC&nbsp;2&nbsp;FRQ\', \'OSC&nbsp;2&nbsp;PWM\']));\n'
	dump += '		table.appendChild(makeButtonRow([[\'square\', program.lfoWaveSqr], program.osc2FM, program.osc2PWM]));\n'
	dump += '		table.appendChild(makeLabelRow([\'\', \'FILTER&nbsp;FRQ\', \'VOLUME&nbsp;MOD\']));\n'
	dump += '		table.appendChild(makeButtonRow([[\'s/h\', program.lfoWaveSnH], program.filterFM, program.vcaMod]));\n'
	dump += '		return table;\n'
	dump += '	}\n'
	dump += '	function makeOscillatorsTable(program) {\n'
	dump += '		var table = makeParameterGroupTable();\n'
	dump += '		table.appendChild(makeLabelRow([\'OSC&nbsp;1<br/>FREQUENCY\', \'1&nbsp;AND&nbsp;2<br/>PULSE&nbsp;WIDTH\', \'OSC&nbsp;2<br/>FREQUENCY\'], true));\n'
	dump += '		table.appendChild(makeKnobRow([program.vco1Freq, program.oscPWM, program.vco2Freq], true));\n'
	dump += '		table.appendChild(makeLabelRow([\'WAVEFORM<br/>\' + makeThreeWaveSVG(), \'OSC&nbsp;2<br/>SYNC&nbsp;F-ENV\', \'WAVEFORM<br/>\' + makeThreeWaveSVG()], true));\n'
	dump += '		table.appendChild(makeButtonRow([program.osc1WaveTri, program.osc1WaveSqr, program.sync, program.fEnv, program.osc2WaveTri, program.osc2WaveSqr]));\n'
	dump += '		return table;\n'
	dump += '	}\n'
	dump += '	function makeFilterTable(program) {\n'
	dump += '		var table = makeParameterGroupTable();\n'
	dump += '		table.appendChild(makeLabelRow([\'<br/>FREQUENCY\', \'<br/>RESONANCE\', \'<br/>MODULATION\'], true));\n'
	dump += '		table.appendChild(makeKnobRow([program.vcfFreq, program.vcfRes, program.vcfMod], true));\n'
	dump += '		table.appendChild(makeLabelRow([\'OSC&nbsp;1<br/>ON\', \'OSC&nbsp;2<br/>HALF\', \'<br/>FULL\', \'NOISE<br/>ON\', \'<br/>4&nbsp;POLE\', \'KBD<br/>TRACK\']));\n'
	dump += '		table.appendChild(makeButtonRow([program.osc2On, program.osc2Half, program.osc2On, program.noise, program.fourPole, program.kbdTrack]));\n'
	dump += '		return table;\n'
	dump += '	}\n'
	dump += '	function makeEnvelopesTable(program) {\n'
	dump += '		var table = makeParameterGroupTable();\n'
	dump += '		table.appendChild(makeLabelRow([\'FILTER<br/>ATTACK\', \'<br/>DECAY\', \'<br/>SUSTAIN\', \'<br/>RELEASE\']));\n'
	dump += '		table.appendChild(makeKnobRow([program.vcfAtk, program.vcfDcy, program.vcfSus, program.vcfRel]));\n'
	dump += '		table.appendChild(makeLabelRow([\'VOLUME<br/>ATTACK\', \'<br/>DECAY\', \'<br/>SUSTAIN\', \'<br/>RELEASE\']));\n'
	dump += '		table.appendChild(makeKnobRow([program.vcaAtk, program.vcaDcy, program.vcaSus, program.vcaRel]));\n'
	dump += '		return table;\n'
	dump += '	}\n'
	dump += '	\n'
	dump += '	function makeMasterTable2(program) {\n'
	dump += '		var table = makeParameterGroupTable();\n'
	dump += '		table.appendChild(makeLabelRow2([\'\', \'\', \'\']));\n'
	dump += '		return table;\n'
	dump += '	}\n'
	dump += '	function makeControlTable2(program) {\n'
	dump += '		var table = makeParameterGroupTable();\n'
	dump += '		table.appendChild(makeButtonRow([program.portBend]));\n'
	dump += '		table.appendChild(makeLabelRow2([\'PORTAMENTO<br/>BEND\']));\n'
	dump += '		table.appendChild(makeKnobRow([program.voiceDetune]));\n'
	dump += '		table.appendChild(makeLabelRow2([\'VOICE&nbsp;DETUNE\']));\n'
	dump += '		return table;\n'
	dump += '	}\n'
	dump += '	function makeModulationTable2(program) {\n'
	dump += '		var table = makeParameterGroupTable();\n'
	dump += '		table.appendChild(makeButtonRow([[\'triangle\',  program.trigLfoWaveTri], program.fmQuant, program.pwmQuant]));\n'
	dump += '		table.appendChild(makeLabelRow2([\'\', \'QUANTIZE&nbsp;1<br/>&nbsp;\', \'QUANTIZE&nbsp;2<br/>&nbsp;\']));\n'
	dump += '		table.appendChild(makeButtonRow([[\'square\', program.trigLfoWaveSqr], program.fmDlyInvert, program.pwmDlyInvert]));\n'
	dump += '		table.appendChild(makeLabelRow2([\'\', \'INVERT&nbsp;1<br/>&nbsp;\', \'INVERT&nbsp;2<br/>&nbsp;\']));\n'
	dump += '		table.appendChild(makeButtonRow([[\'s/h\', program.trigLfoWaveSnH], program.lfoTrack, program.lfoRateDelay]));\n'
	dump += '		table.appendChild(makeLabelRow2([\'TRIG<br/>WAVEVORM\', \'LFO&nbsp;TRACK\', \'LFO&nbsp;ENV&nbsp;MOD\']));\n'
	dump += '		return table;\n'
	dump += '	}\n'
	dump += '	function makeOscillatorsTable2(program) {\n'
	dump += '		var table = makeParameterGroupTable();\n'
	dump += '		table.appendChild(makeButtonRow([program._90, program._180, program.vco1180, program.pw1180, program.portMatch, program.portQuant]));\n'
	dump += '		table.appendChild(makeLabelRow2([\'90º\', \'180º\',\'FREQUENCY\',\'PULSE&nbsp;WIDTH\', \'MATCH\', \'QUANTIZE\']));\n'
	dump += '		table.appendChild(makeLabelRow2([\'LFO&nbsp;PHASE\',\'OSC&nbsp;1&nbsp;LFO&nbsp;MOD&nbsp;INVERT\', \'PORTAMENTO\'],true));\n'
	dump += '		return table;\n'
	dump += '	}\n'
	dump += '	function makeFilterTable2(program) {\n'
	dump += '		var table = makeParameterGroupTable();\n'
	dump += '		table.appendChild(makeButtonRow([program.legato, program.constPort, program.expoPort]));\n'
	dump += '		table.appendChild(makeLabelRow2([\'LEGATO\', \'EQUAL&nbsp;TIME\', \'EXPONENTIAL\']));\n'
	dump += '		table.appendChild(makeLabelRow2([\'-\',\'PORTAMENTO\',\'-\']));\n'
	dump += '		return table;\n'
	dump += '	}\n'
	dump += '	function makeEnvelopesTable2(program) {\n'
	dump += '		var table = makeParameterGroupTable();\n'
	dump += '		table.appendChild(makeKnobRow([program.fmVibDelay, program.fmVibRaise, program.vcfSus, program.lfoTrigPoint]));\n'
	dump += '		table.appendChild(makeLabelRow2([\'DELAY MOD 1\', \'ATTACK MOD 1\', \'\', \'LFO TRIG POINT\']));\n'
	dump += '		table.appendChild(makeKnobRow([program.vcaAtk, program.pwmVibDelay, program.pwmVibRaise, program.pedalSustn]));\n'
	dump += '		table.appendChild(makeLabelRow2([\'DELAY MOD 2\', \'ATTACK MOD 2\', \'\', \'PEDAL RELEASE\']));\n'
	dump += '		return table;\n'
	dump += '	}\n'
	dump += '	function appendColumnWithTable(tableBodyRow, table) {\n'
	dump += '		var tableBodyColumn = document.createElement(\'td\');\n'
	dump += '		tableBodyColumn.appendChild(table);\n'
	dump += '		tableBodyRow.appendChild(tableBodyColumn);\n'
	dump += '	}\n'
	dump += '	function appendProgramHeading(program) {\n'
	dump += '		var heading = document.createElement(\'h2\');\n'
	dump += '		heading.innerHTML = \'Program \' + program.programGroup + \'-\' + program.programNumber + \' (\' + program.programIndex + \')\';\n'
	dump += '		document.body.appendChild(heading);\n'
	dump += '	}\n'
	dump += '	function appendProgramTable(program) {\n'
	dump += '		var programTable = document.createElement(\'table\');\n'
	dump += '		programTable.className = \'panel\';\n'
	dump += '		document.body.appendChild(programTable);\n'
	dump += '		var tableHead = document.createElement(\'thead\');\n'
	dump += '		programTable.appendChild(tableHead);\n'
	dump += '		tableHead.appendChild(makeTableCell("MASTER", "category"));\n'
	dump += '		tableHead.appendChild(makeTableCell("CONTROL", "category"));\n'
	dump += '		tableHead.appendChild(makeTableCell("MODULATION", "category"));\n'
	dump += '		tableHead.appendChild(makeTableCell("OSCILLATORS", "category"));\n'
	dump += '		tableHead.appendChild(makeTableCell("FILTER", "category"));\n'
	dump += '		tableHead.appendChild(makeTableCell("ENVELOPES", "category"));\n'
	dump += '		var tableBody = document.createElement(\'tbody\');\n'
	dump += '		programTable.appendChild(tableBody);\n'
	dump += '		var tableBodyRow = document.createElement(\'tr\');\n'
	dump += '		tableBody.appendChild(tableBodyRow);\n'
	dump += '		appendColumnWithTable(tableBodyRow, makeMasterTable(program));\n'
	dump += '		appendColumnWithTable(tableBodyRow, makeControlTable(program));\n'
	dump += '		appendColumnWithTable(tableBodyRow, makeModulationTable(program));\n'
	dump += '		appendColumnWithTable(tableBodyRow, makeOscillatorsTable(program));\n'
	dump += '		appendColumnWithTable(tableBodyRow, makeFilterTable(program));\n'
	dump += '		appendColumnWithTable(tableBodyRow, makeEnvelopesTable(program));\n'
	dump += '		var tableBodyRow = document.createElement(\'tr\');\n'
	dump += '		tableBody.appendChild(tableBodyRow);\n'
	dump += '		appendColumnWithTable(tableBodyRow, makeMasterTable2(program));\n'
	dump += '		appendColumnWithTable(tableBodyRow, makeControlTable2(program));\n'
	dump += '		appendColumnWithTable(tableBodyRow, makeModulationTable2(program));\n'
	dump += '		appendColumnWithTable(tableBodyRow, makeOscillatorsTable2(program));\n'
	dump += '		appendColumnWithTable(tableBodyRow, makeFilterTable2(program));\n'
	dump += '		appendColumnWithTable(tableBodyRow, makeEnvelopesTable2(program));\n'
	dump += '	}\n'
	return dump

def dumpOB8ProgramsHeaderHTML(fileReader):
	dump = 'document.title = \'OB-8 Programs from {}\'\n'.format(fileReader.name)
	dump += 'heading = document.createElement(\'h1\')\nheading.innerHTML=\'OB-8 Programs from {}\'\ndocument.body.appendChild(heading)\n'.format(fileReader.name)
	return dump

def dumpOB8ProgramHTML(programDict):
	dump = dumpOB8ProgramDictToJS(programDict)
	dump += 'appendProgramHeading(program);\nappendProgramTable(program);\n'
	return dump

# creates a string with the program information
def dumpOB8ProgramsHTML(programsArray):
	dump = ''
	for programDict in programsArray:
		dump += dumpOB8ProgramHTML(programDict)
	return dump

# creates a string with the program information
def dumpOB8BottomBoilerplateHTML():
	dump = '</script></body></html>'
	return dump

# creates a string with the program information
def getOB8Programs(buf):

	programsArray = []
	
	for i in range(int(len(buf)/60)):
	
		programDict = {}
		programsArray.append(programDict)

		programIndex = buf[i*60+4]
		programDict['programIndex'] = programIndex+1
		programDict['programGroup'] = getOB8ProgramGroup(programIndex)
		programDict['programNumber'] = getOB8ProgramNumber(programIndex)

		# program data begins at byte 5
		# 0
		progDataOffset = i*60+5 
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		vcfRel 		= d >> 2
		lfoWave 	= (d & 0x3) << 1
		programDict['vcfRel']=vcfRel

		# 1
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		vcaRel 		= d >> 2
		unison 		= intOnOff(d & 0x1)
		lfoWave 	= lfoWave | ((d >> 1) & 0x1)
		lfoWaveTri = intOnOff(lfoWave & 0x1)
		lfoWaveSqr = intOnOff(lfoWave & 0x2)
		lfoWaveSnH = intOnOff(lfoWave & 0x4)
		programDict['vcaRel']=vcaRel
		programDict['unison']=unison
		programDict['lfoWave']=lfoWave
		programDict['lfoWaveTri']=lfoWaveTri
		programDict['lfoWaveSqr']=lfoWaveSqr
		programDict['lfoWaveSnH']=lfoWaveSnH

		# 2
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		vcfDcy 		= d >> 2
		filterFM	= intOnOff(d & 0x2)
		osc2FM		= intOnOff(d & 0x1)
		programDict['vcfDcy']=vcfDcy
		programDict['filterFM']=filterFM
		programDict['osc2FM']=osc2FM

		# 3
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		vcaDcy 		= d >> 2
		osc2Wave	= d & 0x3
		osc2WaveTri = intOnOff(osc2Wave & 0x1)
		osc2WaveSqr = intOnOff(osc2Wave & 0x2)
		programDict['vcaDcy']=vcaDcy
		programDict['osc2Wave']=osc2Wave
		programDict['osc2WaveTri']=osc2WaveTri
		programDict['osc2WaveSqr']=osc2WaveSqr

		# 4
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		vcfAtk 		= d >> 2
		osc1Wave	= d & 0x3
		osc1WaveTri = intOnOff(osc1Wave & 0x1)
		osc1WaveSqr = intOnOff(osc1Wave & 0x2)
		programDict['vcfAtk']=vcfAtk
		programDict['osc1Wave']=osc1Wave
		programDict['osc1WaveTri']=osc1WaveTri
		programDict['osc1WaveSqr']=osc1WaveSqr

		# 5
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		vcaAtk 		= d >> 2
		osc2PWM		= intOnOff(d & 0x2)
		osc1PWM 	= intOnOff(d & 0x1)
		programDict['vcaAtk']=vcaAtk
		programDict['osc2PWM']=osc2PWM
		programDict['osc1PWM']=osc1PWM

		# 6
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		vcfSus 		= d >> 2
		noise		= intOnOff(d & 0x2)
		fourPole 	= intOnOff(d & 0x1)
		programDict['vcfSus']=vcfSus
		programDict['noise']=noise
		programDict['fourPole']=fourPole

		# 7
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		vcaSus 		= d >> 2
		osc2On		= intOnOff(d & 0x2)
		osc2Half 	= intOnOff(d & 0x1)
		programDict['vcaSus']=vcaSus
		programDict['osc2On']=osc2On
		programDict['osc2Half']=osc2Half

		# 8
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		vcfMod 		= d >> 2
		osc1On		= intOnOff(d & 0x2)
		kbdTrack 	= intOnOff(d & 0x1)
		programDict['vcfMod']=vcfMod
		programDict['osc1On']=osc1On
		programDict['kbdTrack']=kbdTrack

		# 9
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		vcfRes 		= d >> 2
		pw1180		= intOnOff(d & 0x2)
		vco1180 	= intOnOff(d & 0x1)
		programDict['vcfRes']=vcfRes
		programDict['pw1180']=pw1180
		programDict['vco1180']=vco1180

		# 10
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		oscPWM 		= d >> 2
		vcaMod		= intOnOff(d & 0x2)
		fEnv	 	= intOnOff(d & 0x1)
		programDict['oscPWM']=oscPWM
		programDict['vcaMod']=vcaMod
		programDict['fEnv']=fEnv

		# 11
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		lfoFreq 	= d >> 2
		sync		= intOnOff(d & 0x2)
		osc1FM	 	= intOnOff(d & 0x1)
		programDict['lfoFreq']=lfoFreq
		programDict['sync']=sync
		programDict['osc1FM']=osc1FM

		# 12
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		fmAmnt 		= d >> 2
		volume		= (d & 0x3) << 4
		programDict['fmAmnt']=fmAmnt

		# 13
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		pwmAmnt 	= d >> 2
		volume		= volume | (d & 0x3) << 2
		programDict['pwmAmnt']=pwmAmnt

		# 14
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		portAmt 	= d >> 2
		volume		= volume | (d & 0x3)
		programDict['portAmt']=portAmt
		programDict['volume']=volume

		# 15
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		osc2Detune 	= d >> 2
		vco2PW		= (d & 0x3) << 4
		programDict['osc2Detune']=osc2Detune

		# 16
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		vcfFreq 	= d >> 2
		vco2PW		= vco2PW | (d & 0x3) << 2
		programDict['vcfFreq']=vcfFreq

		# 17
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		vco2Freq 	= d >> 2
		vco2PW		= vco2PW | (d & 0x3)
		programDict['vco2Freq']=vco2Freq
		programDict['vco2PW']=vco2PW

		# 18
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		vco1Freq	= d >> 2
		spare		= intOnOff(d & 0x2)
		legato 		= intOnOff(d & 0x1)
		programDict['vco1Freq']=vco1Freq
		programDict['spare']=spare
		programDict['legato']=legato

		# 19
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		lfoTrigPoint= d >> 2
		trigLfoWave	= (d & 0x3) << 1
		programDict['lfoTrigPoint']=lfoTrigPoint
		programDict['trigLfoWave']=trigLfoWave

		# 20
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		pedalSustn	= d >> 2
		portBend	= intOnOff(d & 0x1)
		trigLfoWave	= trigLfoWave | ((d >> 1) & 0x1)
		trigLfoWaveTri = intOnOff(trigLfoWave & 0x1)
		trigLfoWaveSqr = intOnOff(trigLfoWave & 0x2)
		trigLfoWaveSnH = intOnOff(trigLfoWave & 0x4)
		programDict['pedalSustn']=pedalSustn
		programDict['portBend']=portBend
		programDict['trigLfoWave']=trigLfoWave
		programDict['trigLfoWaveTri']=trigLfoWaveTri
		programDict['trigLfoWaveSqr']=trigLfoWaveSqr
		programDict['trigLfoWaveSnH']=trigLfoWaveSnH

		# 21
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		fmVibRaise	= d >> 2
		lfoTrack	= intOnOff(d & 0x2)
		fmDlyInvert	= intOnOff(d & 0x1)
		programDict['fmVibRaise']=fmVibRaise
		programDict['lfoTrack']=lfoTrack
		programDict['fmDlyInvert']=fmDlyInvert

		# 22
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		pwmVibRaise	= d >> 2
		portQuant	= intOnOff(d & 0x2)
		portMatch	= intOnOff(d & 0x1)
		programDict['pwmVibRaise']=pwmVibRaise
		programDict['portQuant']=portQuant
		programDict['portMatch']=portMatch

		# 23
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		fmVibDelay	= d >> 2
		_180		= intOnOff(d & 0x2)
		_90			= intOnOff(d & 0x1) 
		programDict['fmVibDelay']=fmVibDelay
		programDict['_180']=_180
		programDict['_90']=_90

		# 24
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		pwmVibDelay	= d >> 2
		pwmDlyInvert= intOnOff(d & 0x2)
		pwmQuant	= intOnOff(d & 0x1)
		programDict['pwmVibDelay']=pwmVibDelay
		programDict['pwmDlyInvert']=pwmDlyInvert
		programDict['pwmQuant']=pwmQuant

		# 25
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		voiceDetune	= d >> 2
		expoPort	= intOnOff(d & 0x2)
		constPort	= intOnOff(d & 0x1)
		programDict['voiceDetune']=voiceDetune
		programDict['expoPort']=expoPort
		programDict['constPort']=constPort

		# 26
		progDataOffset += 2
		d = byteNibbles(buf[progDataOffset],buf[progDataOffset+1])
		bendAmount	= d >> 2
		lfoRateDelay= intOnOff(d & 0x2)
		fmQuant		= intOnOff(d & 0x1)
		programDict['bendAmount']=bendAmount
		programDict['lfoRateDelay']=lfoRateDelay
		programDict['fmQuant']=fmQuant

	return programsArray

# main
parser = argparse.ArgumentParser(description='Dumps the patch settings contained in Oberheim OB-8 sysex files')
parser.add_argument('inputFile', type=argparse.FileType('rb'), nargs='+',  metavar='inFile', help='OB-8 sysex input files')
parser.add_argument('-o', '--outputFile', type=argparse.FileType('w'), metavar='outFile', help='output file')
parser.add_argument('--html', action='store_true', help='output as pretty html')
args = parser.parse_args()

# write to stdout or file
outputFile = stdout
if args.outputFile:
	outputFile = args.outputFile

if args.html:
	outputFile.write(dumpOB8TopBoilerplateHTML())

for f in args.inputFile:
	buf = f.read()
	if (len(buf) % 60) or (buf[:4] != b'\xf0\x10\x01\x01'):
		print('This does not appear to be an OB-8 sysex file')
		parser.print_usage()
		continue
	else:
		programsDict = getOB8Programs(buf)
		if args.html:
			outputFile.write(dumpOB8ProgramsHeaderHTML(f))
			outputFile.write(dumpOB8ProgramsHTML(programsDict))
		else:
			outputFile.write(f.name + '\n')
			outputFile.write(dumpOB8ProgramsText(programsDict))

if args.html:
	outputFile.write(dumpOB8BottomBoilerplateHTML())
