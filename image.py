from skimage import io, filters, util
import matplotlib.pyplot as plt
import requests
import os

def blur(img, level=10):
  blurred = util.img_as_ubyte(filters.gaussian(img, sigma=level))
  return blurred

def fetch(resource):
  return io.imread(f'https://hashgram.s3-us-west-2.amazonaws.com/user-content/{resource}')

def apply_filter(img, *filters):
  _img = img
  for (filterfn, *args) in filters:
    try:
      # look for filter function in module context
      _img = globals()[f'{filterfn}'](_img, *args)
    except KeyError:
      pass
  return _img

def save_img(img, filename):
  io.imsave(f'./{filename}.jpg', img, format='jpg', quality=30)

def prune(filename):
  os.remove(f'./{filename}.jpg')

def process(resource_key, filters):
  img = apply_filter(fetch(resource_key), *filters)
  save_img(img, resource_key)