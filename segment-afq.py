#!/usr/bin/env python3

"""Code adapted from pyAFQ tutorial (https://github.com/yeatmanlab/pyAFQ/blob/master/examples/plot_tract_profile.py).
   Author: Ariel Rokem (github.com/arokem)
   Adapted for brainlife.io by Brad Caron (github.com/bacaron)
"""

import os.path as os
import json
import numpy as np
import nibabel as nib
import dipy.data as dpd
from dipy.io.streamline import load_tractogram
from AFQ import api
import AFQ.registration as reg
import AFQ.segmentation as seg
import dipy.core.gradients as dpg
import scipy.io as sio
from matplotlib import cm

# open configurable inputs
with open('config.json') as config_f:
    config = json.load(config_f)
    dwi = config["dwi"]
    bvals = config["bvals"]
    bvecs = config["bvecs"]
    track = config["track"]
    affine = config["affine"]

# load dwi data and generate gradient table
dwi_img = nib.load(dwi)
gtab = dpg.gradient_table(bvals,bvecs,b0_threshold=50)

# load MNI template and syn register dwi data to MNI
MNI_T2_img = nib.load('/templateflow/tpl-MNI152NLin2009cAsym/tpl-MNI152NLin2009cAsym_res-01_T2w.nii.gz')

# run affine registration if requested
if affine == True:
    
    # create mean b0 image
    b0 = np.mean(dwi_img.get_fdata()[..., gtab.b0s_mask], -1)
    
    # register DWI to MNI using affine
    affine_hardi, prealign = reg.affine_registration(b0,MNI_T2_img.get_fdata(),dwi_img.affine,MNI_T2_img.affine)

# run nonlinear (SyN) registration
if affine == "":
    warped_hardi, mapping = reg.syn_register_dwi(dwi, gtab)
else:
    warped_hardi, mapping = reg.syn_register_dwi(dwi, gtab, prealign=prealign)

# load tractogram
tg = load_tractogram(track,dwi_img,bbox_valid_check=False)

# download and load waypoint ROIs and make bundle dictionary
bundles = api.make_bundle_dict(resample_to=MNI_T2_img)
bundle_names = list(bundles.keys())

print(f"Space before segmentation: {tg.space}")

# initialize segmentation and segment major fiber groups
print("running AFQ segmentation")
segmentation = seg.Segmentation(return_idx=True)
segmentation.segment(bundles,tg,fdata=dwi,fbval=bvals,fbvec=bvecs,mapping=mapping,reg_template=MNI_T2_img,reset_tg_space=True)

print(f"Space after segmentation: {tg.space}")

# re-load tractogram in RASMM space since it was warped to the VOX space during segmentation
#tg = load_tractogram(track,dwi_img,bbox_valid_check=False)

# generate classification structure and tracts.json
names = np.array(bundle_names,dtype=object)
streamline_index = np.zeros(len(tg.streamlines))
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

##########################################################################
# References:
# -------------------------
# .. [Yeatman2012] Jason D Yeatman, Robert F Dougherty, Nathaniel J Myall,
#                  Brian A Wandell, Heidi M Feldman, "Tract profiles of
#                  white matter properties: automating fiber-tract
#                  quantification", PloS One, 7: e49790
#
# .. [Yeatman2014] Jason D Yeatman, Brian A Wandell, Aviv Mezer Feldman,
#                  "Lifespan maturation and degeneration of human brain white
#                  matter", Nature Communications 5: 4932

