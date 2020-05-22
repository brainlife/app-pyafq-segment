#!/bin/bash

freesurfer=`jq -r '.freesurfer' config.json`
dwi=`jq -r '.dwi' config.json`

export SUBJECTS_DIR=./

mri_convert $freesurfer/mri/aparc+aseg.mgz aparc+aseg.nii.gz
mri_vol2vol --mov aparc+aseg.nii.gz --targ ${dwi} --regheader --interp nearest --o aparc+aseg.nii.gz 
mri_convert $freesurfer/mri/aparc.a2009s+aseg.mgz aparc.a2009s+aseg.nii.gz
mri_vol2vol --mov aparc.a2009s+aseg.nii.gz --targ ${dwi} --regheader --interp nearest --o aparc.a2009s+aseg.nii.gz 

