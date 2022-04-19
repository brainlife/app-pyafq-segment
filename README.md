[![Abcdspec-compliant](https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg)](https://github.com/brain-life/abcd-spec)
[![Run on Brainlife.io](https://img.shields.io/badge/Brainlife-brainlife.app.295-blue.svg)](https://doi.org/10.25663/brainlife.app.295)

# AFQ Segmentation: pyAFQ

This app will segment a whole-brain tractogram into the 20 whole-brain tracks provided by Automatic Fiber Quantification (AFQ). This app takes a dwi, track/tck, and freesurfer inputs and outputs a white-matter classification (WMC) structure containing the names and streamlines indices of the AFQ tracks.

Specifically, this app will register the DWI and streamlines to MNI space and extract tracks using regions of interest derived from the Mori atlas. This app uses the recently developed Python port from the Yeatman lab (https://github.com/yeatmanlab/pyAFQ)

### Authors

- Brad Caron (bacaron@iu.edu)

### Contributors

- Soichi Hayashi (hayashis@iu.edu
- Franco Pestilli (franpest@iu.edu)

### Funding

[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-1636893](https://img.shields.io/badge/NSF_BCS-1636893-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-ACI-1916518](https://img.shields.io/badge/NSF_ACI-1916518-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1916518)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://grantome.com/grant/NIH/R01-EB029272-01)
[![NIH-NIMH-RF1MH121868](https://img.shields.io/static/v1?label=NIH%20NIMH&message=RF1MH121868&color=green)](https://grantome.com/grant/NIH/RF1-MH121868-01)



### Citations

Please cite the following articles when publishing papers that used data, code or other resources created by the brainlife.io community.

1. Jason D Yeatman, Robert F Dougherty, Nathaniel J Myall, Brian A Wandell, Heidi M Feldman, “Tract profiles of white matter properties: automating fiber-tract quantification”, PloS One, 7: e49790

2. Kruper, J., Yeatman, J. D., Richie-Halford, A., Bloom, D., Grotheer, M., Caffarra, S., Kiar, G., Karipidis, I. I., Roy, E., Chandio, B. Q., Garyfallidis, E., and Rokem, A (2021). Evaluating the reliability of human brain white matter tractometry. Aperture, 1:1-25


## Running the App

### On Brainlife.io

You can submit this App online at [https://doi.org/10.25663/brainlife.app.295](https://doi.org/10.25663/brainlife.app.295) via the 'Execute' tab.

### Running Locally (on your machine)

1. git clone this repo

2. Inside the cloned directory, create `config.json` with something like the following content with paths to your input files.

```json
{
    "track":    "testdata/track/track.tck",
    "freesurfer":    "test/data/freesurfer/output",
    "dwi":    "testdata/dwi/dwi.nii.gz",
    "bvals":    "testdata/dwi/dwi.bvals",
    "bvecs":    "testdata/dwi/dwi.bvecs"
}
```

### Sample Datasets

You can download sample datasets from Brainlife using [Brainlife CLI](https://github.com/brain-life/cli).

```
npm install -g brainlife
bl login
mkdir input
bl dataset download
```

3. Launch the App by executing 'main'

```bash
./main
```

## Output

The main output of this App is is a .mat structure of the white-matter classification. Within this matlab structure contains the 'classification' structure. This includes a 'names' field containg the name and index number of each track and a 'index' field which contains the streamline indices for each track. These indices refer to the streamlines found in the whole-brain tractogram input.

#### Product.json

The secondary output of this app is `product.json`. This file allows web interfaces, DB and API calls on the results of the processing.

### Dependencies

This App requires the following libraries when run locally.

- Python3: https://www.python.org/download/releases/3.0/
- matplotlib: https://matplotlib.org/users/installing.html
- numpy: https://numpy.org/install/
- dipy: https://dipy.org/documentation/1.2.0./installation/
- json: https://pypi.org/project/jsonlib-python3/
- pyAFQ: https://yeatmanlab.github.io/pyAFQ/installation_guide.html
- singularity: https://singularity.lbl.gov/quickstart
- scipy: https://www.scipy.org/install.html
