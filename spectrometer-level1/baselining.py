import numpy as np


def baselined(freq, on_off, polyfit_deg=1):
    """
    Baseline for the final ON-OFF result
    :rtype: (numpy.array, numpy.array) - fitting curve and baselined ON-OFF
    result, respectively
    """
    # bdp curve fitting
    polyfit = np.poly1d(np.polyfit(freq, on_off, polyfit_deg))  # x, y, degree
    bsl_curv = polyfit(freq)
    return bsl_curv, (on_off - bsl_curv)
