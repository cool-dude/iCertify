import csv
import os

from datetime import datetime

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from lib import APP_DIR
from lib.config import config


def write_text_to_image(text):
    img = Image.open(config.get('user-settings', 'certificate'))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(config.get('app-settings', 'font-family'), eval(config.get('app-settings', 'font-size')))
    font_colour = eval(config.get('app-settings', 'font-colour'))
    xy_points = eval(config.get('user-settings', 'xy_cordinates'))
    draw.text(xy_points, text, font_colour, font=font)
    out_put_path = os.path.join(APP_DIR, config.get('app-settings', 'attachments'), "%s.pdf" % ("_".join(text.split())))
    create_dir_if_not_exists(out_put_path)
    img.save(out_put_path, "PDF", Quality=100)
    return out_put_path


def logit(parameters):
    header = ['name', 'email', 'datetime', 'attachment']
    parameters['datetime'] = str(datetime.now())
    file_path = os.path.join(APP_DIR, config.get('app-settings', 'attachments'), 'reports.csv')
    if not os.path.exists(file_path):
        create_dir_if_not_exists(file_path)
        with open(file_path, 'w') as wp:
            writer = csv.writer(wp)
            writer = csv.writer(wp, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(header)
    row_data = [parameters.get(key) for key in header]
    with open(file_path, 'a') as log:
        writer = csv.writer(log, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(row_data)

create_dir_if_not_exists = lambda path: os.makedirs(os.path.dirname(path)) if not os.path.exists(os.path.dirname(path)) else 1
