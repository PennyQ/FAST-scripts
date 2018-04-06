import numpy as np


def bdp_correction(data, freq):
    data_after_bdp = None

    # iterate data with each spectra
    for spectra in np.nditer(data, flags=['external_loop'], order='F'):
        good_data_index = range(spectra.shape[0])

        # calculate 3 times for bandpass fitting and data filterring
        for k in range(3):
            #  select good data only with good_data_index indexing
            freq_sel = freq[good_data_index]
            data_sel = spectra[good_data_index]

            # bdp curve fitting
            polyfit = np.poly1d(np.polyfit(freq_sel, data_sel, 1))  # x, y, degree
            bdp_curv = polyfit(freq)

            # calculate residual and corresponding rms
            res_signal = abs(spectra) - polyfit(freq)
            rms = np.std(res_signal)

            # get index for good data
            good_data_index = np.where(res_signal <= 3.*rms)

        try:
            bdp_curv = bdp_curv/np.median(bdp_curv)  # normalization
        except ZeroDivisionError:
            bdp_curv = bdp_curv
        nor_bdp = spectra/bdp_curv
        nor_bdp = nor_bdp.reshape(nor_bdp.shape[0], 1)  # reshape for appending

        if data_after_bdp is None:
            data_after_bdp = nor_bdp
        else:
            data_after_bdp = np.append(data_after_bdp, nor_bdp, axis=1)  # bdp correction
    return data_after_bdp


def baselined(freq, on_off):
    # bdp curve fitting
    polyfit = np.poly1d(np.polyfit(freq, on_off, 1))  # x, y, degree
    bsl_curv = polyfit(freq)
    return (on_off - bsl_curv)
