#!/usr/bin/env python3

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
from matplotlib import cm

# make output directories
#os.mkdir("wmc")
#os.mkdir("wmc/tracts")
#os.mkdir("wmc/surfaces")

# open configurable inputs
with open('config.json') as config_f:
    config = json.load(config_f)
    dwi = config["dwi"]
    bvals = config["bvals"]
    bvecs = config["bvecs"]
    track = config["track"]

# load dwi data and generate gradient table
dwi_img = nib.load(dwi)
gtab = dpg.gradient_table(bvals,bvecs,b0_threshold=50)

# load MNI template and syn register dwi data to MNI
#MNI_T2_img = dpd.read_mni_template()
MNI_T2_img = nib.load('/templateflow/tpl-MNI152NLin2009cAsym/tpl-MNI152NLin2009cAsym_res-01_T2w.nii.gz')
warped_hardi, mapping = reg.syn_register_dwi(dwi, gtab)

# load tractogram
tg = load_tractogram(track,dwi_img,bbox_val_check=False)
#tg_acpc = transform_streamlines(tg.streamlines,dwi_img.get_affine())

# download and load waypoint ROIs and make bundle dictionary
bundles = api.make_bundle_dict(resample_to=MNI_T2_img)
bundle_names = list(bundles.keys())

print(f"Space before segmentation: {tg.space}")

# initialize segmentation and segment major fiber groups
print("running AFQ segmentation")
segmentation = seg.Segmentation(return_idx=True)
segmentation.segment(bundles,tg,fdata=dwi,fbval=bvals,fbvec=bvecs,mapping=mapping,reg_template=MNI_T2_img)

print(f"Space after segmentation: {tg.space}")

# re-load tractogram in RASMM space since it was warped to the VOX space during segmentation
tg = load_tractogram(track,dwi_img)

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
