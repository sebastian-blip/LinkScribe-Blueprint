import urllib.parse
import random
import datetime
import string

import requests
from bs4 import BeautifulSoup
import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

from metadata.path import Path


def web_scraping(url) -> dict:

    response = requests.get(url)
    nombre_aleatorio = 'morfeo'

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.title.string

        description = soup.find('meta', attrs={'name': 'description'})

        if description is None:
            description = soup.find('meta', attrs={'property': 'og:description'})

        if description:
            description = description.get('content')
        else:
            description = 'No se encontró una descripción.'

        img_tag = soup.find('img')

        if img_tag:
            main_image = img_tag["src"]

            main_image = urllib.parse.urljoin(url, main_image)

            image_response = requests.get(main_image)
            if image_response.status_code == 200:
                image_data = image_response.content

                fecha_actual = datetime.datetime.now()
                numero_aleatorio = random.randint(1, 10)
                letra_aleatoria = random.choice(string.ascii_lowercase)
                nombre_aleatorio = fecha_actual.strftime("%Y%m%d") + str(
                    numero_aleatorio) + letra_aleatoria

                if 'svg' in main_image:
                    temp_image_path = os.path.join(Path.out_, f'{nombre_aleatorio}.SVG')
                    tem_img = os.path.join(Path.out_, f'{nombre_aleatorio}.jpg')

                    with open(temp_image_path, 'wb') as temp_file:
                        temp_file.write(image_data)

                    drawing = svg2rlg(temp_image_path)

                    renderPM.drawToFile(drawing, tem_img, fmt="JPG")

                    os.remove(temp_image_path)

                else:
                    tem_img = os.path.join(Path.out_, f'{nombre_aleatorio}.jpg')
                    with open(tem_img, 'wb') as temp_file:
                        temp_file.write(image_data)

        data = {
            'title': title,
            'description': description,
            'main_image': f'{nombre_aleatorio}.jpg'
        }
    else:
        data = None

    return data

