FROM python:3.6

ENV DEBIAN_FRONTEND=noninteractive 

RUN apt-get update && apt-get -y install sudo python3.6 python3-pip jq time git curl unzip

#RUN pip3 install git+git://github.com/yeatmanlab/pyAFQ.git@master#egg=pyAFQ
RUN pip3 install pyAFQ

#make it work under singularity
RUN ldconfig && mkdir -p /N/u /N/home /N/dc2 /N/soft /mnt/scratch /share1

# Precaching atlases
# borrowed from https://github.com/poldracklab/fmriprep/blob/master/Dockerfile
ENV TEMPLATEFLOW_HOME=/templateflow
RUN python3 -c "from templateflow import api as tfapi; \
               tfapi.get('MNI152NLin6Asym', atlas=None, resolution=[1, 2], \
                         desc=None, extension=['.nii', '.nii.gz']); \
               tfapi.get('MNI152NLin6Asym', atlas=None, resolution=[1, 2], \
                         desc='brain', extension=['.nii', '.nii.gz']); \
               tfapi.get('MNI152NLin2009cAsym', atlas=None, extension=['.nii', '.nii.gz']); \
               tfapi.get('OASIS30ANTs', extension=['.nii', '.nii.gz']); \
               tfapi.get('fsaverage', density='164k', desc='std', suffix='sphere'); \
               tfapi.get('fsaverage', density='164k', desc='vaavg', suffix='midthickness'); \
               tfapi.get('fsLR', density='32k'); \
               tfapi.get('MNI152NLin6Asym', resolution=2, atlas='HCP', suffix='dseg')"
RUN chmod -R go=u /templateflow

#preven ~/.local stuff to be loaded (singularity)
ENV PYTHONNOUSERSITE=true

RUN apt-get install -y locales
RUN echo "LC_ALL=en_US.UTF-8" >> /etc/environment && echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && echo "LANG=en_US.UTF-8" > /etc/locale.conf && locale-gen en_US.UTF-8
ENV LC_CTYPE="en_US.UTF-8"
