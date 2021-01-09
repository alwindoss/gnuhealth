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
        '18': (37, 37), '17': (118, 37), '16': (199, 37), '15': (280, 37),
        '14': (229, 37), '13': (310, 37), '12': (391, 37), '11': (472, 37),
        '21': (744, 37), '22': (825, 37), '23': (906, 37), '24': (987, 37),
        '25': (1068, 37), '26': (1149, 37), '27': (1230, 37), '28': (1311, 37),
        '48': (37, 360), '47': (118, 360), '46': (199, 360), '45': (280, 360),
        '44': (361, 360), '43': (442, 360), '42': (523, 360), '41': (604, 360),
        '31': (744, 360), '32': (825, 360), '33': (906, 360), '34': (987, 360),
        '35': (1068, 360), '36': (1149, 360), '37': (1230, 360),
        '38': (1311, 360),
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
    def plot_extraction(cls, piece, status, im):
        missing_color = (5, 11, 50)  # deep blue
        for_extraction_color = (90, 0, 15)  # red
        if (status == 'M'):
            color = missing_color
        else:
            color = for_extraction_color

        xcenter, ycenter = piece
        llc = {'x': xcenter - 30, 'y': ycenter + 30}
        urc = {'x': xcenter + 30, 'y': ycenter - 30}
        ulc = {'x': xcenter - 30, 'y': ycenter - 30}
        lrc = {'x': xcenter + 30, 'y': ycenter + 30}

        # We'll use this for the tooth filling.
        # ImageDraw.floodfill(im, xy=piece, value=(255, 0, 255), thresh=200)

        draw = ImageDraw.Draw(im)
        draw.line((llc['x'], llc['y'], urc['x'], urc['y']),
                  fill=color, width=10)

        draw.line((ulc['x'], ulc['y'], lrc['x'], lrc['y']),
                  fill=color, width=10)

        return (im)

    @classmethod
    def plot_odontogram(cls, dental_schema):

        # Get the template file from current module dir
        report_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(report_dir, 'odontogram_template.png')
        im = Image.open(filename)

        dschema = json.loads(dental_schema)
        
        for tooth, values in dschema.items():
            if (values['ts'] in ('M', 'E')):
                status = values['ts']
                cls.plot_extraction(cls.pieces[tooth], status, im)

        holder = io.BytesIO()
        im.save(holder, 'png')
        image_png = holder.getvalue()
        holder.close()
        return (image_png)

    @classmethod
    def get_context(cls, records, data):
        context = super(Odontogram, cls).get_context(
            records, data)

        dental_schema = \
            Pool().get('gnuhealth.patient')(data['id']).dental_schema

        context['patient_odontogram'] = cls.plot_odontogram(dental_schema)

        return context
