#!/usr/bin/python3

import xmltodict
import subprocess
from docopt import docopt
import re

helper_path = 'waypoint_helper'

option_str = """kml2waypoint.

Usage:
  kml2waypoint.py --kml <kml_file> --bhv <bhv_template> --out <out_file>
  kml2waypoint.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --kml         kml file to use.
  --bhv         bhv template file to use
  --out         output file (defaults to stdout)

"""

def process_origin(point, output):
    if 'coordinates' in point.keys():
        coords = point['coordinates'].strip().split(',')
        print('LatOrigin = ' + coords[1].strip())
        print('LongOrigin = ' + coords[0].strip())
        output['origin'] = [coords[1].strip(), coords[0].strip()]
    else:
        print('No coordinates in origin!')

def get_point(coord, output):
    args = helper_path + ' ' + output['origin'][0] + ' '
    args += output['origin'][1] + ' ' + coord[1] + ' ' + coord[0]
    proc = subprocess.run(args, stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    if (proc.returncode == 0):
        return (proc.stdout.strip())
    else:
        print("Call to waypoint_helper failed with code " + str(proc.returncode))

def process_point(point, output):
    if 'origin' in output.keys() and 'coordinates' in point.keys():
        coord = point['coordinates'].strip().split(',')
        return ('point = ' + get_point(coord, output))
    else:
        print("Attempting to process point without defined origin and/or coordinates")
    return ""

def process_linestring(linestring, output):
    if 'origin' in output.keys() and 'coordinates' in linestring.keys():
        coords = linestring['coordinates'].strip().split('\n')
        retval = 'points = '
        for point in coords:
            retval += get_point(point.strip().split(','), output)
            retval += ' : '
        retval = retval.rstrip(':')
        return retval
    else:
        print("Attempting to process linestring without defined origin and/or coordinates")
    return ""

def process_placemark(placemark, output, leader):
    if 'name' in placemark.keys():
        if placemark['name'] == 'Origin' and 'Point' in placemark.keys():
            process_origin(placemark['Point'], output)
            return
        myname = leader + placemark['name']
        myname = myname.replace(' ', '_')
        print("Processing placemark " + placemark['name'] + ' with name ' + myname)
        if 'Point' in placemark.keys():
            output[myname] = process_point(placemark['Point'], output)
        elif 'LineString' in placemark.keys():
            output[myname] = process_linestring(placemark['LineString'], output)
        else:
            print('No point or linestring specified in ' + placemark['name'])
    else:
        print("Unnamed placemark!")

def process_layer(layer, output, multiple_layers):
    layer_name = ""
    if multiple_layers and 'name' in layer.keys():
        # Make a name we can
        layer_name = layer['name']
        layer_name = layer_name.replace(' ','_')
        layer_name += '_'
    if 'Placemark' in layer.keys():
        if isinstance(layer['Placemark'], list):
            for place in layer['Placemark']:
                process_placemark(place, output, layer_name)
        else:
            process_placemark(place, output, layer_name)
    else:
        print("No Placemark in layer!")

def process_kml(doc):
    output = {}
    if 'kml' in doc.keys() and 'Document' in doc['kml'].keys() and 'Folder' in doc['kml']['Document']:
        if isinstance(doc['kml']['Document']['Folder'], list):
            for layer in doc['kml']['Document']:
                process_layer(layer, output, True)
        else:
            process_layer(doc['kml']['Document']['Folder'], output, False)

    print(output)
    return output

def process_bhv(doc, bhv):
    out = ""
    pattern = re.compile(r'^.*###(\w+)###.*$')
    for line in bhv.splitlines():
        result = pattern.match(line);
        if result and result.group(1) in doc.keys():
            out += doc[result.group(1)]
        else:
            out += line
        out += '\n'
    return out

if __name__ == '__main__':
    args = docopt(option_str, version='kml2waypoint 0.1')
    kml_dict = {}
    bhv_template = ''
    if (args['--kml']):
        try:
            with open(args['<kml_file>']) as fd:
                kml_dict = xmltodict.parse(fd.read())
        except IOError:
            print('Failed to open file at ' + args['<kml_file>'] + ', exiting')
            exit()
    else:
        print("No KML file specified, exiting")
        exit()
    if (args['--bhv']):
        try:
            with open(args['<bhv_template>']) as fd:
                bhv_template = fd.read()
        except IOError:
            print('Failed to open file at ' + args['<bhv_template>'] + ', exiting')
            exit()
    else:
        print("No behavior template file specified, exiting")
        exit()

    output = process_bhv(process_kml(kml_dict), bhv_template)
    with open(args['<out_file>'], 'w') as fd:
        fd.write(output)

    print(args)
