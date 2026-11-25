[![Abcdspec-compliant](https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg)](https://github.com/brain-life/abcd-spec)
[![Run on Brainlife.io](https://img.shields.io/badge/Brainlife-brainlife.app.295-blue.svg)](https://doi.org/10.25663/brainlife.app.295)

# AFQ Segmentation: pyAFQ

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

**Segments a whole-brain tractogram into the 20 AFQ major white matter tracts with pyAFQ 0.4.1, registering DWI to MNI and using Mori-atlas waypoint ROIs, and outputs a white matter classification.**

Registers the DWI b0 to the MNI152NLin2009cAsym T2w template (optionally affine first, then SyN), builds the AFQ bundle dictionary of waypoint ROIs, and runs pyAFQ segmentation on the tractogram. Outputs a classification structure with the names and streamline indices of the AFQ tracts, plus FreeSurfer surfaces for visualisation. DWI and tractogram must be in the same space.

Run it on brainlife.io: [https://doi.org/10.25663/brainlife.app.295](https://doi.org/10.25663/brainlife.app.295)

| Input | Datatype | Required | Description |
|---|---|---|---|
| `freesurfer` | `neuro/freesurfer` | yes | The path to the top directory of the Freesurfer datatype. This is used for the visualization. |
| `track` | `neuro/track/tck` | yes | The path to the whole-brain tractogram to be segmented. |
| `dwi` | `neuro/dwi` | yes | The path to the DWI datatype used to generate the whole-brain tractogram. |

| Output | Datatype | Description |
|---|---|---|
| `wmc` | `neuro/wmc` | The AFQ classification structure including a classification.mat structure that contains the streamline indices in the whole-brain tractogram. |

| Parameter | Type | Default | Description |
|---|---|---|---|
| `affine` | boolean | `false` | If true, will first align the DWI to the MNI template using an affine registration before computing the non-linear warp. However, if this has already been done, the non-linear warp should work just fine and this can be set to false |

Runtime: container `brainlife/freesurfer-mini:6.0.1`; 8 CPUs; 60 GB memory; 10 h walltime; needs `FREESURFER_LICENSE`.

<!-- brainlife-app:end -->

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
