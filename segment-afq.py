#!/usr/bin/env python3

import os.path as op
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
import array as ar


def ismember(a_vec, b_vec):
    """ MATLAB equivalent ismember function """

    bool_ind = np.isin(a_vec,b_vec)
    common = a_vec[bool_ind]
    common_unique, common_inv  = np.unique(common, return_inverse=True)     # common = common_unique[common_inv]
    b_unique, b_ind = np.unique(b_vec, return_index=True)  # b_unique = b_vec[b_ind]
    common_ind = b_ind[np.isin(b_unique, common_unique, assume_unique=True)]
    
    return bool_ind, common_ind[common_inv



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
tg = load_tractogram(track,img)

# download and load waypoint ROIs and make bundle dictionary
bundles = api.make_bundle_dict(resample_to=MNI_T2_img)
bundle_names = list(bundles.keys())

# initialize segmentation and segment major fiber groups
segmentation = seg.Segmentation(return_idx=True)
segmentation.segment_afq(bundles,tg,fdata=dwi,fbval=bvals,fbvec=bvecs,mapping=mapping,reg_template=MNI_T2_img)

# save output
classification = {}
classification['names'] = []
classification['index'] = []

streamline_index = ar.array('i',np.range(tg.streamlines)) # generate indices integer array of N streamlines x 1

for names in range(np.size(bundle_names)):
	classification['names'] = np.append(classification['names'],bundle_names[names]).tolist()  	
	bool_ind = ismember(np.array(streamline_index),np.array(segmentation.fiber_groups['%s' % names]['idx']))
	classification['index'] = np.append(classification['index'],bool_ind[0])




