# This file is part health_dentistry module for GNU Health HMIS component
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import io
import os
import json
from PIL import Image, ImageDraw
from trytond.report import Report
from trytond.pool import Pool


__all__ = ['Odontogram']


class Odontogram(Report):
    __name__ = 'health_dentistry.odontogram.report'

    radius = 37
    pieces = {
        '18': (37, 37), '17': (119, 37), '16': (201, 37), '15': (282, 37),
        '14': (362, 37), '13': (443, 37), '12': (524, 37), '11': (605, 37),
        '21': (744, 37), '22': (825, 37), '23': (906, 37), '24': (987, 37),
        '25': (1069, 37), '26': (1153, 37), '27': (1235, 37), '28': (1316, 37),
        '48': (37, 360), '47': (119, 360), '46': (201, 360), '45': (283, 360),
        '44': (365, 360), '43': (447, 360), '42': (529, 360), '41': (611, 360),
        '31': (744, 360), '32': (825, 360), '33': (907, 360), '34': (988, 360),
        '35': (1069, 360), '36': (1150, 360), '37': (1231, 360),
        '38': (1316, 360),
        '55': (283, 145), '54': (364, 145), '53': (445, 145), '52': (526, 145),
        '51': (607, 145),
        '61': (744, 145), '62': (825, 145), '63': (906, 145), '64': (987, 145),
        '65': (1068, 145),
        '85': (283, 253), '84': (364, 253), '83': (445, 253), '82': (526, 253),
        '81': (607, 253),
        '71': (744, 253), '72': (825, 253), '73': (906, 253), '74': (987, 253),
        '75': (1068, 253),
        }

    @classmethod
    def plot_extraction(cls, piece_center, status, im):
        missing_color = "#0000ff"  # blue
        for_extraction_color = "#ff0000"  # red
        if (status == 'M'):
            color = missing_color
        else:
            color = for_extraction_color

        xcenter, ycenter = piece_center
        llc = {'x': xcenter - 30, 'y': ycenter + 30}
        urc = {'x': xcenter + 30, 'y': ycenter - 30}
        ulc = {'x': xcenter - 30, 'y': ycenter - 30}
        lrc = {'x': xcenter + 30, 'y': ycenter + 30}
        draw = ImageDraw.Draw(im)
        draw.line((llc['x'], llc['y'], urc['x'], urc['y']),
                  fill=color, width=10)

        draw.line((ulc['x'], ulc['y'], lrc['x'], lrc['y']),
                  fill=color, width=10)

        return (im)

    @classmethod
    def plot_decayed(cls, tooth, piece_center, status, im):
        x, y = piece_center
        filling = (0, 0, 255)  # blue
        decayed = (255, 0, 0)  # red

        # Pick the color for decay of filling
        if status['ts'] == 'D':
            color = decayed
        else:
            color = filling

        position = (x, y)  # Center of the tooth
        draw = ImageDraw.Draw(im)

        tregions = status.copy()
        tregions.pop('ts')  # Delete ts element and focus on the tooth areas

        # Set the section of the filling / decay
        # Maxillar / upper region
        if (tooth in range(11, 28) or tooth in range(51, 65)):
            print(tooth, tregions)
            for key in tregions.keys():
                if (key in ['o', 'i']):  # Occlusal or Incisal
                    position = (x, y)  # Center of the tooth
                if (key == 'v'):  # Vestibular
                    position = (x, y - 25)
                if (key == 'p'):  # Palatine
                    position = (x, y + 25)
                if (key == 'd'):  # Distal
                    position = (x - 25, y)
                if (key == 'm'):  # Mesial
                    position = (x + 25, y)

                ImageDraw.floodfill(im, xy=position, value=color, thresh=200)

        # Mandibular / lower region
        if (tooth in range(31, 48) or tooth in range(71, 85)):
            for key in tregions.keys():
                if (key in ['o', 'i']):  # Occlusal or Incisal
                    position = (x, y)  # Center of the tooth
                if (key == 'l'):  # Lingual
                    position = (x, y - 25)
                if (key == 'v'):  # Vestibular
                    position = (x, y + 25)
                if (key == 'm'):  # Mesial
                    position = (x - 25, y)
                if (key == 'd'):  # Distal
                    position = (x + 25, y)

                ImageDraw.floodfill(im, xy=position, value=color, thresh=200)

        return (im)

    @classmethod
    def plot_odontogram(cls, dental_schema):

        # Get the template file from current module dir
        report_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(report_dir, 'odontogram_template.png')
        im = Image.open(filename)

        dschema = json.loads(dental_schema)

        for tooth, values in dschema.items():
            # Decayed or filled tooth
            # Plot it first to avoid wrong surface filling if overlapping with
            # other symbols
            if (values['ts'] in ('D', 'F')):
                status = dschema[tooth]  # Get all the keys (ts, o, m, d, ...)
                cls.plot_decayed(int(tooth), cls.pieces[tooth], status, im)

            # Missing or set for extraction tooth
            if (values['ts'] in ('M', 'E')):
                status = values['ts']
                cls.plot_extraction(cls.pieces[tooth], status, im)

        holder = io.BytesIO()
        im.save(holder, 'png')
        image_png = holder.getvalue()
        holder.close()
        return (image_png)

    @classmethod
    def get_context(cls, records, header, data):
        context = super(Odontogram, cls).get_context(
            records, header, data)

        dental_schema = \
            Pool().get('gnuhealth.patient')(data['id']).dental_schema

        context['patient_odontogram'] = cls.plot_odontogram(dental_schema)

        return context
