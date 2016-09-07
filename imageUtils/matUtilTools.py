# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 12:36:32 2016

@author: Johannes Hofmanninger, johannes.hofmanninger@meduniwien.ac.at
"""

import numpy as np
from PIL import Image
from matplotlib import cm


def norm01(x):
    r = (x - np.min(x)).astype(np.float)
    m = np.max(r)
    if m > 0:
        r /= np.max(r)

    return r


def norm0255(x):
    r = (x - np.min(x)).astype(np.float)
    m = np.max(r)
    if m > 0:
        r = np.round((r / np.max(r)) * 255)

    return r


def overlay(image, overlay_image, overlay_mask=1):
    if not Image.isImageType(image):
        image = Image.fromarray(norm0255(image)).convert("RGB")

    if not Image.isImageType(overlay_image):
        orig_ol_values = np.uint8(norm01(overlay_image) * 255)
        fg = np.zeros(orig_ol_values.shape)
        fg[orig_ol_values != 0] = 1
        jet_image = np.uint8(cm.jet(norm01(orig_ol_values)) * 255)
        jet_image[~fg.astype(bool), :] = 0
        overlay_image = Image.fromarray(jet_image)

    if ~isinstance(overlay_mask, (list, tuple, np.ndarray)) & isinstance(overlay_mask, (int, float)):
        if overlay_mask <= 1:
            ol_mask_value = overlay_mask * 255
        else:
            ol_mask_value = overlay_mask
        overlay_values = np.asanyarray(overlay_image)
        overlay_values = np.sum(overlay_values, axis=2)
        overlay_mask = np.zeros(overlay_values.shape)
        overlay_mask[overlay_values > 0] = ol_mask_value

    if (np.max(overlay_mask) > 255) | (np.max(overlay_mask) <= 1):
        overlay_mask = Image.fromarray(np.uint8(norm0255(overlay_mask)), 'L')
    else:
        overlay_mask = Image.fromarray(np.uint8(overlay_mask), 'L')

    overlay_image.putalpha(overlay_mask)
    image.paste(overlay_image, (0, 0), overlay_image)
    return image


def get_label_border(label_image):
    gx, gy = np.gradient(label_image)
    r = np.sqrt(np.power(gx, 2) + np.power(gy, 2));
    r[r > 0] = 1
    return r