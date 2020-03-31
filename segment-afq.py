#!/usr/bin/env python3

import os.path as os
import matplotlib.pyplot as plt
import numpy as np
import nibabel as nib
import dipy.data as dpd
from dipy.data import fetcher
import dipy.tracking.utils as dtu
import dipy.tracking.streamline as dts
from dipy.io.streamline import save_tractogram, load_tractogram
from dipy.stats.analysis import afq_profile, gaussian_weights
from dipy.io.stateful_tractogram import StatefulTractogram
from dipy.io.stateful_tractogram import Space
import json
from AFQ import api
import AFQ.utils.streamlines as aus
import AFQ.data as afd
import AFQ.tractography as aft
import AFQ.registration as reg
import AFQ.dti as dti
import AFQ.segmentation as seg
from AFQ.utils.volume import patch_up_roi
import dipy.core.gradients as dpg
import scipy.io as sio
from matplotlib import cm

# make output directories
os.mkdir("wmc")
os.mkdir("wmc/tracts")
os.mkdir("wmc/surfaces")

# open configurable inputs
with open('config.json') as config_f:
    config = json.load(config_f)
    dwi = config["dwi"]
    bvals = config["bvals"]
    bvecs = config["bvecs"]
    track = config["track"]

# load dwi data and generate gradient table
dwi_img = nib.load(dwi)
gtab = dpg.gradient_table(bvals,bvecs)

# load MNI template and syn register dwi data to MNI
MNI_T2_img = dpd.read_mni_template()
warped_hardi, mapping = reg.syn_register_dwi(dwi, gtab)

# load tractogram
tg = load_tractogram(track,dwi_img)

# download and load waypoint ROIs and make bundle dictionary
bundles = api.make_bundle_dict(resample_to=MNI_T2_img)
bundle_names = list(bundles.keys())

# initialize segmentation and segment major fiber groups
segmentation = seg.Segmentation(return_idx=True)
segmentation.segment(bundles,tg,fdata=dwi,fbval=bvals,fbvec=bvecs,mapping=mapping,reg_template=MNI_T2_img)

# generate classification structure and tracts.json
names = np.array(bundle_names,dtype=object)
streamline_index = np.zeroes(len(tg.streamlines))
tractsfile = []

for bnames in range(np.size(bundle_names)):
    tract_ind = np.array(segmentation.fiber_groups['%s' % bundle_names[bnames]]['idx'])
    streamline_index[tract_ind] = bnames + 1
    streamlines = np.zeros([len(tg.streamlines[tract_ind])],dtype=object)
    for e in range(len(streamlines)):
        streamlines[e] = np.transpose(tg.streamlines[tract_ind][e]).round(2)

    color=list(cm.nipy_spectral(bnames))[0:3]
    count = len(streamlines)
    print("sub-sampling for json")
    if count < 1000:
        max = count
    else:
        max = 1000
    jsonfibers = np.reshape(streamlines[:max], [max,1]).tolist()
    for i in range(max):
        jsonfibers[i] = [jsonfibers[i][0].tolist()]

    with open ('wmc/tracts/'+str(bnames+1)+'.json', 'w') as outfile:
        jsonfile = {'name': names[bnames], 'color': color, 'coords': jsonfibers}
        json.dump(jsonfile, outfile)

    tractsfile.append({"name": names[bnames], "color": color, "filename": str(bnames+1)+'.json'})

with open ('wmc/tracts/tracts.json', 'w') as outfile:
    json.dump(tractsfile, outfile, separators=(',', ': '), indent=4)

# save classification structure
print("saving classification.mat")
sio.savemat('wmc/classification.mat', { "classification": {"names": names, "index": streamline_index }})

print("AFQ segmentation complete")
