#!/usr/bin/env python
# vim:set ft=python fileencoding=utf-8 sr et ts=4 sw=4 : See help 'modeline'
# From http://www.noah.org/wiki/Wavelength_to_RGB_in_Python

"""
    == A few notes about color ==

    Color   Wavelength(nm) Frequency(THz)
    Red     620-750        484-400
    Orange  590-620        508-484
    Yellow  570-590        526-508
    Green   495-570        606-526
    Blue    450-495        668-606
    Violet  380-450        789-668

    f is frequency (cycles per second)
    l (lambda) is wavelength (meters per cycle)
    e is energy (Joules)
    h (Plank's constant) = 6.6260695729 x 10^-34 Joule*seconds
                         = 6.6260695729 x 10^-34 m^2*kg/seconds
    c = 299792458 meters per second
    f = c/l
    l = c/f
    e = h*f
    e = c*h/l

    List of peak frequency responses for each type of 
    photoreceptor cell in the human eye:
        S cone: 437 nm
        M cone: 533 nm
        L cone: 564 nm
        rod:    550 nm in bright daylight, 498 nm when dark adapted. 
                Rods adapt to low light conditions by becoming more sensitive.
                Peak frequency response shifts to 498 nm.

"""
import numpy as np


def wavelength_to_rgb(wavelength, gamma=0.8):
    """This converts a given wavelength of light to an
    approximate RGB color value. The wavelength must be given
    in nanometers in the range from 380 nm through 750 nm
    (789 THz through 400 THz).

    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html
    """

    wavelength = float(wavelength)
    if wavelength >= 380 and wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif wavelength >= 440 and wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif wavelength >= 490 and wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif wavelength >= 510 and wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif wavelength >= 580 and wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif wavelength >= 645 and wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    R *= 255
    G *= 255
    B *= 255
    return (int(R), int(G), int(B))


def wavelength_to_rgb_np(wavelength, gamma=0.8):
    """This converts a given wavelength of light to an
    approximate RGB color value. The wavelength must be given
    in nanometers in the range from 380 nm through 750 nm
    (789 THz through 400 THz).

    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html
    """

    shape_rgb = np.shape(wavelength) + (3,)
    rgb_blank = np.ones(shape_rgb, dtype=np.float64)

    rgb_380_440 = rgb_blank.copy()
    rgb_380_440_attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
    rgb_380_440[..., 0] = (
        (-(wavelength - 440) / (440 - 380)) * rgb_380_440_attenuation
    ) ** gamma
    rgb_380_440[..., 1] = 0.0
    rgb_380_440[..., 2] = (1.0 * rgb_380_440_attenuation) ** gamma
    rgb_380_440[np.isnan(rgb_380_440)] = 0

    rgb_440_490 = rgb_blank.copy()
    rgb_440_490[..., 0] = 0.0
    rgb_440_490[..., 1] = ((wavelength - 440) / (490 - 440)) ** gamma
    rgb_440_490[..., 2] = 1.0
    rgb_440_490[np.isnan(rgb_440_490)] = 0

    rgb_490_510 = rgb_blank.copy()
    rgb_490_510[..., 0] = 0.0
    rgb_490_510[..., 1] = 1.0
    rgb_490_510[..., 2] = (-(wavelength - 510) / (510 - 490)) ** gamma
    rgb_490_510[np.isnan(rgb_490_510)] = 0

    rgb_510_580 = rgb_blank.copy()
    rgb_510_580[..., 0] = ((wavelength - 510) / (580 - 510)) ** gamma
    rgb_510_580[..., 1] = 1.0
    rgb_510_580[..., 2] = 0.0
    rgb_510_580[np.isnan(rgb_510_580)] = 0

    rgb_580_645 = rgb_blank.copy()
    rgb_580_645[..., 0] = 1.0
    rgb_580_645[..., 1] = (-(wavelength - 645) / (645 - 580)) ** gamma
    rgb_580_645[..., 2] = 0.0
    rgb_580_645[np.isnan(rgb_580_645)] = 0

    rgb_645_750 = rgb_blank.copy()
    rgb_645_750_attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
    rgb_645_750[..., 0] = (1.0 * rgb_645_750_attenuation) ** gamma
    rgb_645_750[..., 1] = 0.0
    rgb_645_750[..., 2] = 0.0
    rgb_645_750[np.isnan(rgb_645_750)] = 0

    rgb = (
        rgb_380_440 * ((wavelength >= 380) & (wavelength <= 440))[..., np.newaxis]
        + rgb_440_490 * ((wavelength > 440) & (wavelength <= 490))[..., np.newaxis]
        + rgb_490_510 * ((wavelength > 490) & (wavelength <= 510))[..., np.newaxis]
        + rgb_510_580 * ((wavelength > 510) & (wavelength <= 580))[..., np.newaxis]
        + rgb_580_645 * ((wavelength > 580) & (wavelength <= 645))[..., np.newaxis]
        + rgb_645_750 * ((wavelength > 645) & (wavelength <= 750))[..., np.newaxis]
    )
    # rgb[np.isnan(rgb)] = 0
    return rgb
    # return (rgb * 255).astype(np.uint8)
