#!/bin/bash

freesurfer=`jq -r '.freesurfer' config.json`

mri_convert $freesurfer/mri/aparc+aseg.mgz aparc+aseg.nii.gz
mri_convert $freesurfer/mri/aparc.a2009s+aseg.mgz aparc.a2009s+aseg.nii.gz
