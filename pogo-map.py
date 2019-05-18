# KMZ file for upload to Google My Maps

from __future__ import annotations

import json
from pathlib import Path
import re
import shutil
from typing import List
from zipfile import ZipFile, ZIP_DEFLATED


class KML():

    def __init__(self, title: str, filename: str):
        self.file = Path(f'{filename}.kml')
        self.data = [
            f'<?xml version="1.0" encoding="UTF-8"?>',
            f'<kml xmlns="http://www.opengis.net/kml/2.2">',
            f'  <Document>',
            f'    <name>{title}</name>',
            f'    <description>Map of Pokmon Go stops and gyms.</description>',
            f'  </Document>',
            f'</kml>'
        ]

    def add_icon(self, p):
        kml = []
        for selection in ['normal', 'highlight']:
            kml += [
                f'    <Style id="{p.stem}-{selection}">',
                f'      <IconStyle>',
                f'        <scale>1.1</scale>',
                f'        <Icon>',
                f'          <href>{p.as_posix()}</href>',
                f'        </Icon>',
                f'      </IconStyle>',
                f'      <LabelStyle>',
                f'        <scale>0</scale>',
                f'      </LabelStyle>',
                f'      <BalloonStyle>',
                f'        <text><![CDATA[<h3>$[name]</h3>]]></text>',
                f'      </BalloonStyle>',
                f'    </Style>',
            ]

        kml.append(f'    <StyleMap id="{p.stem}">')
        for selection in ['normal', 'highlight']:
            kml += [
                f'      <Pair>',
                f'        <key>{selection}</key>',
                f'        <styleUrl>#{p.stem}-{selection}</styleUrl>',
                f'      </Pair>',
            ]
        kml.append('    </StyleMap>')
        self.data[-3:-3] = kml
        return self

    def add_pogo_intel(self, *args: List[str]):
        for type_of_place in ['gyms', 'pokestops']:
            kml = [
                f'    <Folder>',
                f'      <name>{type_of_place.capitalize()}</name>',
            ]

            for p in args:
                with open(p, 'r') as f:
                    data = json.loads(f.read())[type_of_place]

                for _, poi in data.items():
                    styleUrl = type_of_place
                    if type_of_place == 'gyms' and poi.get('isEx', False):
                        styleUrl += '_ex'

                    kml += [
                        f'      <Placemark>',
                        f'        <name>{poi["name"]}</name>',
                        f'        <description></description>',
                        f'        <styleUrl>#{styleUrl}</styleUrl>',
                        f'        <Point>',
                        f'          <coordinates>',
                        f'            {poi["lng"]},{poi["lat"]},0',
                        f'          </coordinates>',
                        f'        </Point>',
                        f'      </Placemark>',
                    ]
            kml.append('    </Folder>')
            self.data[-3:-3] = kml
        return self

    def write(self, kmz: bool=False):

        if kmz:
            self.file = Path(str.replace(str(self.file), 'kml', 'kmz'))

        if self.file.exists():
            self.file.unlink()

        if kmz:
            with ZipFile(self.file, mode='w', compression=ZIP_DEFLATED) as z:
                # Write KML file to archive
                self.file = self.file.parent.joinpath('doc.kml')
                self.write(kmz=False)
                z.write(self.file)
                self.file.unlink()

                # Copy images to archive
                pattern = re.compile(r'\s*<href>(.*)</href>\n?')
                images = [pattern.search(line).groups()[0] for line in self.data if pattern.match(line) is not None]
                for image in set(images):
                    z.write(image)
        else:
            with self.file.open('w') as f:
                f.write('\n'.join(self.data))


if __name__ == '__main__':
    # Get input arguments
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('title')

    args = parser.parse_args()

    # Create KML file
    kml = KML(
        title = args.title,
        filename = 'IITC-pogo',
    )

    # Create style maps for icons
    for p in Path('images').glob('*.png'):
        kml.add_icon(p)

    # Add pokestop and gym information
    possible_files = [
        'IITC-pogo.json',
        'sponsored.json',
    ]
    kml.add_pogo_intel(*[_ for _ in possible_files if Path(_).exists()])

    kml.write(kmz=True)
