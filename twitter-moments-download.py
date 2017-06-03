"""
Download set of images contained in a twitter "moment"
"""
# coding: utf-8

import argparse
import requests as r
from bs4 import BeautifulSoup as bs

filename = 'https://twitter.com/i/moments/792234795015114753'

parser = argparse.ArgumentParser()
parser.add_argument('-u','--url')
args = parser.parse_args()

url = args.url

moment_url = r.get(url)
parsed_content = bs(moment_url.content, 'html.parser')
moment_images = parsed_content.find_all(
    'img', {'class': "MomentMediaItem-entity MomentMediaItem-entity--image"})
moment_image_urls = [
    x.attrs['data-resolved-url-large'] for x in moment_images
    if 'data-resolved-url-large' in x.attrs
]
for x in moment_image_urls:
    with open(x.split('/')[-1], 'wb') as f:
        f.write(r.get(x).content)
