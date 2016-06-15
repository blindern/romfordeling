#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: Henrik Steen

# generate image with:
# $ python gendot.py utlysninger.txt bytter.txt >file.dot
# $ dot -n -Tpng file.dot >file.png

import re
import sys

if len(sys.argv) < 2:
	sys.stderr.write("Mangler argumenter!\n")
	sys.exit(1)

file_utlysninger = sys.argv[1]
file_bytter = ""
if len(sys.argv) > 2:
	file_bytter = sys.argv[2]

# settes ved load_bytter
has_semesters = False

# definisjon av romkartet
table = {
	"100a": {
		"x": 3,
		"y": 1.9,
		"nodes": [
			[101, .6],
			[103, .5, .4],
			[105, .5],
			[107, .5],
			[109, .5],
			[111, .5],
			[113, .5],
			[115, .5],
			[117, .5],
			[119, .5],
			["121G", .5],
			["121M", .5],
			[123, .6]
		]
	},
	"100b": {
		"x": 2,
		"y": 2.4,
		"nodes": [
			[102, .5],
			["104G", .5],
			["104M", .5],
			[106, .5],
			[108, .5],
			[110, .5],
			["HVV", .5],
			[112, .5],
			[114, .5],
			["116G", .5],
			["116M", .5],
			[118, .5],
			[120, .5],
			[122, .9]
		]
	},
	"200a": {
		"x": 5.5,
		"y": 1.9,
		"nodes": [
			[201, .6],
			[203, .5, .4],
			[205, .5],
			[207, .5],
			[209, .5],
			[211, .5],
			[213, .5],
			[215, .5],
			[217, .5],
			[219, .5],
			["221G", .5],
			["221M", .5],
			[223, .6]
		]
	},
	"200b": {
		"x": 4.5,
		"y": 2.4,
		"nodes": [
			[202, .5],
			[204, .5],
			["206M", .5],
			["206G", .5],
			[208, .5],
			["210M", .5],
			["210G", .5],
			[212, .5],
			[214, .5],
			["216G", .5],
			["216M", .5],
			[218, .5],
			[220, .5],
			[222, .9],
		]
	},
	"300a": {
		"x": 8,
		"y": 2.4,
		"nodes": [
			[301, .5],
			[303, .5],
			[305, .5],
			[307, .5],
			[309, .5],
			[311, .5],
			[313, .5],
			[315, .5],
			[317, .5],
			[319, .5],
			[321, .5],
			[323, .5]
		]
	},
	"300b": {
		"x": 7,
		"y": 2.9,
		"nodes": [
			[302, .5],
			[304, .5],
			[306, 1],
			[308, .5],
			[310, .5],
			[312, .5],
			[314, .5],
			[316, .5],
			[318, .5],
			[320, .5],
		]
	},
	"300c": {
		"x": 7.5,
		"y": 9,
		"nodes": [
			["322k", .4]
		]
	},
	"400a": {
		"x": -3,
		"y": 1.9,
		"nodes": [
			[402, .6],
			[404, .5, .4],
			[406, .5],
			[408, .5],
			[410, .5],
			[412, .5],
			[414, .5],
			[416, .5],
			[418, .5],
			[420, .5],
			["422G", .5],
			["422M", .5],
			[424, .6]
		]
	},
	"400b": {
		"x": -2,
		"y": 2.4,
		"nodes": [
			[401, .5],
			["403G", .5],
			["403M", .5],
			[405, .5],
			[407, .5],
			[409, .5],
			["HVØ", .5],
			[411, .5],
			[413, .5],
			["415G", .5],
			["415M", .5],
			[417, .5],
			[419, .5],
			[421, .9]
		]
	},
	"500a": {
		"x": -5.5,
		"y": 1.9,
		"nodes": [
			[502, .6],
			[504, .5, .4],
			[506, .5],
			[508, .5],
			[510, .5],
			[512, .5],
			[514, .5],
			[516, .5],
			[518, .5],
			[520, .5],
			["522G", .5],
			["522M", .5],
			[524, .6]
		]
	},
	"500b": {
		"x": -4.5,
		"y": 2.4,
		"nodes": [
			[501, .5],
			["503G", .5],
			["503M", .5],
			[505, .5],
			["507M", .5],
			["507G", .5],
			[509, .5],
			[511, .5],
			[513, .5],
			[515, .5],
			["517M", .5],
			["517G", .5],
			[519, .5],
			[521, .9],
		]
	},
	"600a": {
		"x": -8,
		"y": 2.4,
		"nodes": [
			[602, .5],
			[604, .5],
			[606, .5],
			[608, .5],
			[610, .5],
			[612, .5],
			[614, .5],
			[616, .5],
			[618, .5],
			[620, .5],
			[622, .5],
			[624, .5]
		]
	},
	"600b": {
		"x": -7,
		"y": 2.9,
		"nodes": [
			[601, .5],
			[603, .5],
			[605, 1],
			[607, .5],
			[609, .5],
			[611, .5],
			[613, .5],
			[615, .5],
			[617, .5],
			[619, .5],
		]
	},
	"600c": {
		"x": -7.5,
		"y": 9,
		"nodes": [
			["623k", .4]
		]
	},
	"HB": {
		"x": 0,
		"y": 0,
		"nodesa": [
			[2, -3.25, -1.8-2, .7, 1],
			[4, -3.25, -1.8-1, .7, 1],
			["6A", -1.85-1.4, -1.8, .7, .8],
			["6B", -1.85-1.4, -1, 1.4, .8],
			[8, -1.85, -1, .6, 1],
			[10, -1.25, -1, .5, 1],
			[12, -.75, -1, .5, 1],
			[14, -.25, -1, .5, 1],
			[16, .25, -1, .5, 1],
			[18, .75, -1, .5, 1],
			[20, 1.25, -1, .6, 1],
			["22A", 2.25, -1, .5, .8],
			["22B", 2.25+.5, -1.3, .5, 1.1],
			[24, 2.25+.3, -1.85, .7, .55],
			[26, 2.25+.3, -2.5, .7, .65],
			[28, 2.25+.3, -3.15, .7, .65],
			[30, 2.25+.3, -3.8, .7, .65],
			
			[11, 1.6, -4.3, .6, .9],
			[9, 1.6, -3.4, .6, .9],
			[7, .75, -2.5, .7, .6],

			[1, -2.2, -4.3, .6, .9],
			[3, -2.2, -3.4, .6, .9],
			[5, -1.45, -2.5, .7, .6],
		]
	},

	"700a": {
		"x": -7,
		"y": -5.5-2.5,
		"nodesa": [
			[710, 0, 0, .6, .6],
			[708, .6, 0, .6, .6],
			[706, 1.2, 0, .6, .6],
			[704, 1.8, 0, .4, .6],

			[711, 0, 1, .6, .6],
			[709, .6, 1, .6, .6],
			[707, 1.2, 1, .6, .6],
			[705, 1.8, 1, .6, .6],
			[703, 2.4, 1, .6, .6]
		]
	},

	"700b": {
		"x": -7,
		"y": -5.5,
		"nodesa": [
			[702, 1.8, .9, .5, .7],
			[701, 2.3, 1.1, .7, .5],
			[712, 0, 0, .7, .8]
		]
	},

	"Gule": {
		"x": -3,
		"y": -8,
		"nodesa": [
			["H1", 0, 0, .8, 1],
			["H2", .8, 0, .8, 1],
			["H3", 1.6, 0, .8, 1],
			["H4", 2.4, 0, .8, 1],
			["H5", 3.2, 0, .8, 1],
			["H6", 4, 0, .8, 1],
			["H7", 4.8, 0, 1, 1]
		]
	},

	"Porten": {
		"x": -9,
		"y": -1,
		"nodesa": [
			["P1+4", 1.6, 0, 1, 1],
			["P2", .8, 0, .8, 1],
			["P3", 0, 0, .8, 1],
			#["P4", 1, 1, 1, 1]
		]
	},

	"AX": {
		"x": -9,
		"y": -3,
		"nodesa": [
			["AX1", 0, 0, .8, .6],
			["AX2", .8, 0, .8, .6],
			["AX3", 1.6, 0, .8, .6]
		]
	},

	"Perm": {
		"x": 0,
		"y": 1.5,
		"nodesa": [
			["Perm", -.35, 0, .7, .5]
		]
	}
}

allerom = []

dobbeltrom = [
	"122",
	"222",
	"306",
	#"402",
	"421",
	#"502",
	"521",
	"605",
	"1",
	"2",
	"4",
	"11",
	"AX1",
	"AX2",
	"AX3",
	"H1",
	"H2",
	"H3",
	"H4",
	"H5",
	"H6",
]

parrom = [
	"712",
	"6B",
	"P1+4",
	"H7",
]

utlyst = []

fra = [
	# romnr
]

til = [
	# romnr
]

bytter = [
	# [fra, til, semesterantall]
]

farger = [
	'orangered',
	'orangered',   #1
	'darkgoldenrod3', #2
	'yellow', #3
	'yellowgreen', #4
	'green', #5
	'springgreen', #6
	'dodgerblue', #7
	'blue', #8
	'purple', #9
	'magenta', #10
	'red', #11
	'gray30', #12
	'black'  #13
]
farge_ukjent = 'orangered'

# hent utlyste rom fra fil
def load_utlyst(filnavn):
	lines = []
	with open(filnavn, "r") as content_file:
		lines = content_file.readlines()

	for line in lines:
		line = line.split("#")[0].strip()
		if len(line) > 0:
			if not str(line) in allerom:
				sys.stderr.write("OBS! Utlyst rom '%s' ikke funnet i romlisten\n" % str(line))
			utlyst.append(str(line))

# lag liste over alle rom
def gen_allerom():
	for groupid in table:
		group = table[groupid]

		if 'nodes' in group:
			for node in group['nodes']:
				allerom.append(str(node[0]))
		elif 'nodesa' in group:
			for node in group['nodesa']:
				allerom.append(str(node[0]))


# hent inn bytter fra fil
def load_bytter(filnavn):
	semesters = []
	lines = []
	with open(filnavn, "r") as content_file:
		lines = content_file.readlines()

	recheck = re.compile(r'^(.+) -> ([^ ]+)( \[(.*)\])?$', re.DOTALL)
	for line in lines:
		res = recheck.match(line.strip())
		if res:
			fra.append(str(res.group(1)))
			til.append(str(res.group(2)))
			semesters.append(int(res.group(4) if res.group(3) else -1))
			bytter.append([str(res.group(1)), str(res.group(2)), int(res.group(4)) if res.group(3) else -1])

	has_semesters = len(set(semesters)) > 1

# tegn labels for semesterantall
def draw_labels_semester():
	for i, farge in enumerate(farger):
		print "\tfarge%d [ label = \"%d semester\", fillcolor = %s, style = filled, pos = \"10, %.2f!\", shape = box, height = .25 ]" \
			% (i, i, farge, -1+i/2.5)

# tegn labels for bytter
def draw_labels_romstatus_resultat():
    print 'label0 [ label = "tildelt uten utlysning",       fillcolor = red,            style = filled, pos = "10, 9.0!", shape = box, height = .25 ]'
    print 'label1 [ label = "feil ved utlysning",      fillcolor = firebrick,      style = filled, pos = "10, 8.6!", shape = box, height = .25 ]'
    print 'label2 [ label = "utlyst og tildelt",            fillcolor = mediumblue,     style = filled, pos = "10, 8.2!", shape = box, height = .25 ]'
    print 'label3 [ label = "opprykksrom",                  fillcolor = royalblue,      style = filled, pos = "10, 7.8!", shape = box, height = .25 ]'
    print 'label4 [ label = "utlyst men ingen tildelt",     fillcolor = green,          style = filled, pos = "10, 7.4!", shape = box, height = .25 ]'
    print 'label5 [ label = "fraflyttet, ingen opprykk",    fillcolor = darkgreen,      style = filled, pos = "10, 7.0!", shape = box, height = .25 ]'
    print 'label6 [ label = "dobbeltrom",                   fillcolor = gray93,         style = filled, pos = "10, 6.6!", shape = box, height = .25 ]'
    print 'label7 [ label = "ingen endring",                fillcolor = gray40,         style = filled, pos = "10, 6.2!", shape = box, height = .25 ]'

# tegn labels for bytter
def draw_labels_romstatus_utlyst():
    print 'label4 [ label = "utlyst",                        fillcolor = green,          style = filled, pos = "10, 9.0!", shape = box, height = .25 ]'
    print 'label7 [ label = "ikke utlyst",                   fillcolor = gray40,         style = filled, pos = "10, 8.6!", shape = box, height = .25 ]'
    print 'label6 [ label = "dobbeltrom\n(fordeles av adm)", fillcolor = gray93,         style = filled, pos = "10, 8.1!", shape = box, height = .25 ]'

# finn stil for et rom
def get_extra(rom):
	rom = str(rom)
	extra = ""

	# utlyst rom
	if rom in utlyst:
		# feil: bytte fra
		if rom in fra and not rom in parrom and not rom in dobbeltrom:
			extra += ", style = filled, fillcolor=firebrick"

		# ingen tildelt
		elif not rom in til:
			extra += ", style = filled, fillcolor=green"

		# tildelt
		else:
			extra += ", style = filled, fillcolor=mediumblue"

	# ikke utlyst
	else:
		# tildelt
		if rom in til:
			# ikke opprykk
			if not rom in fra:
				extra += ", style = filled, fillcolor=red"

			# opprykksrom
			else:
				extra += ", style = filled, fillcolor=royalblue"

		# ikke tildelt, dobbeltrom
		elif rom in dobbeltrom:
			extra += ", style=filled, fillcolor=gray93"

		# fraflyttet
		elif rom in fra:
			extra += ", style=filled, fillcolor=darkgreen"

		# ikke tildelt, ikke dobbeltrom
		else:
			# antakelse: beboer forblir boende på rom
			extra += ", style = filled, fillcolor=gray40"

	if rom in dobbeltrom:
		extra += ", label = \"%s\\n(Dobbel)\"" % rom

	if rom in parrom:
		extra += ", label = \"%s\\n(Parrom)\"" % rom

	#if rom[:1] == "H" and len(rom) == 2:
	#	extra += ", style=filled, fillcolor=yellow"

	if rom == "Perm":
		extra += ", shape = circle, fillcolor=white"
	#
	#else:
	#	extra += ", style=filled, fillcolor=palegreen"
	return extra

# tegn rommene
def draw_nodes():
	for groupid in table:
		group = table[groupid]
		x = float(group['x'])
		y = float(group['y'])

		if 'nodes' in group:
			for node in group['nodes']:
				extra = get_extra(node[0])
				print "\t\"%s\" [ pos = \"%.4f,%.4f!\", shape = box, width = .8, height = %.4f, fixedsize = true%s ];" \
					% (node[0], x, y+(node[1]/2.0), float(node[1]), extra)
				y += node[1]
				if len(node) > 2: y += node[2]
		elif 'nodesa' in group:
			for node in group['nodesa']:
				ax = node[1] + x + node[3]/2.0
				ay = node[2] + y + node[4]/2.0
				
				extra = get_extra(node[0])
				print "\t\"%s\" [ pos = \"%.4f,%.4f!\", shape = box, width = %.4f, height = %.4f, fixedsize = true%s ];" \
					% (node[0], ax, ay, float(node[3]), float(node[4]), extra)

# tegn rombyttene
def draw_edges():
	for bytte in bytter:
		farge = farger[bytte[2]] if bytte[2] != -1 else farge_ukjent
		print "\t\"%s\" -> \"%s\" [color=%s, penwidth=1.5, arrowsize=1.4, constraint=false]" % (bytte[0], bytte[1], farge)


print """digraph {
	layout=fdp
	overlap = true
	
	edge[headclip=false, tailclip=false, constraint=false]
    splines=curved
    
    outputorder=nodesfirst"""

gen_allerom()

load_utlyst(file_utlysninger)

if file_bytter:
	draw_labels_romstatus_resultat()
	load_bytter(file_bytter)
	if has_semesters:
		draw_labels_semester()

else:
	draw_labels_romstatus_utlyst()

draw_nodes()
draw_edges()

print "}"
