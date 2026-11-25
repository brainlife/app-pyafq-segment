<h1 align="center">AFQ Segmentation with pyAFQ</h1>

<p align="center">
  The 20 major AFQ white matter tracts from a whole-brain tractogram, segmented with pyAFQ using Mori-atlas waypoint regions in MNI space.
</p>

<p align="center">
  <a href="https://github.com/brainlife/abcd-spec"><img src="https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg" alt="ABCD Spec v1.1"></a>
  <a href="https://doi.org/10.25663/brainlife.app.295"><img src="https://img.shields.io/badge/Brainlife-brainlife.app.295-blue.svg" alt="Run on brainlife.io"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-lightgrey.svg" alt="MIT license"></a>
</p>

> 📍 **This branch, `0.4.1`, is the brainlife.io App Segment white matter tracts using pyAFQ** ([doi:10.25663/brainlife.app.295](https://doi.org/10.25663/brainlife.app.295)).

## 🧠 At a glance

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Segments a whole-brain tractogram into the 20 AFQ major white matter tracts with pyAFQ 0.4.1, registering DWI to MNI and using Mori-atlas waypoint ROIs, and outputs a white matter classification.**

Registers the DWI b0 to the MNI152NLin2009cAsym T2w template (optionally affine first, then SyN), builds the AFQ bundle dictionary of waypoint ROIs, and runs pyAFQ segmentation on the tractogram. Outputs a classification structure with the names and streamline indices of the AFQ tracts, plus FreeSurfer surfaces for visualisation. DWI and tractogram must be in the same space.

| | |
|---|---|
| 📥 **Inputs** | `neuro/freesurfer` · `neuro/track/tck` · `neuro/dwi` |
| 📤 **Outputs** | `neuro/wmc` |
| 🐳 **Container** | `brainlife/freesurfer-mini:6.0.1` |
| ⚙️ **Resources** | 8 CPUs · 60 GB memory · 10 h walltime |
| 🔑 **Requires** | `FREESURFER_LICENSE` |
| 🔗 **Run it** | [doi.org/10.25663/brainlife.app.295](https://doi.org/10.25663/brainlife.app.295) |

#### 📥 Inputs

| Input | Datatype | Required | Description |
|---|---|---|---|
| `freesurfer` | `neuro/freesurfer` | yes | The path to the top directory of the Freesurfer datatype. This is used for the visualization. |
| `track` | `neuro/track/tck` | yes | The path to the whole-brain tractogram to be segmented. |
| `dwi` | `neuro/dwi` | yes | The path to the DWI datatype used to generate the whole-brain tractogram. |

#### 📤 Outputs

| Output | Datatype | Description |
|---|---|---|
| `wmc` | `neuro/wmc` | The AFQ classification structure including a classification.mat structure that contains the streamline indices in the whole-brain tractogram. |

<details>
<summary><b>⚙️ Parameters</b> (1)</summary>

| Parameter | Type | Default | Description |
|---|---|---|---|
| `affine` | boolean | `false` | If true, will first align the DWI to the MNI template using an affine registration before computing the non-linear warp. However, if this has already been done, the non-linear warp should work just fine and this can be set to false |

</details>

<!-- brainlife-app:end -->

## 🚀 Running the App

### ☁️ On brainlife.io

Open the App at [doi.org/10.25663/brainlife.app.295](https://doi.org/10.25663/brainlife.app.295), choose a whole-brain tractogram (`neuro/track/tck`), the DWI it was generated from and a FreeSurfer output of the same subject, and press **Execute**. The white matter classification (`neuro/wmc`, tagged `afq`) is archived to your project and can feed tract-profile and visualisation Apps.

The App registers the DWI to the MNI152NLin2009cAsym T2-weighted template (an optional affine step, then a non-linear SyN warp), builds the AFQ bundle dictionary of waypoint regions derived from the Mori atlas, and runs the [pyAFQ](https://github.com/yeatmanlab/pyAFQ) segmentation from the Yeatman lab. The DWI and the tractogram must be in the same space. The FreeSurfer input is used only to build brain surfaces for the brainlife.io viewer.

### 💻 Locally

You need [Singularity/Apptainer](https://apptainer.org/), [`jq`](https://jqlang.github.io/jq/) and a [FreeSurfer license](https://surfer.nmr.mgh.harvard.edu/registration.html). pyAFQ, DIPy, FreeSurfer and VTK come from the containers that `main` pulls.

1. Clone this repository and check out the branch used on brainlife.io: `git checkout 0.4.1` (the default branch uses a newer pyAFQ container).
2. Create `config.json` with the paths to your inputs:

   ```json
   {
       "track": "testdata/track/track.tck",
       "dwi": "testdata/dwi/dwi.nii.gz",
       "bvals": "testdata/dwi/dwi.bvals",
       "bvecs": "testdata/dwi/dwi.bvecs",
       "freesurfer": "testdata/freesurfer/output",
       "affine": false
   }
   ```

   Set `affine` to `true` to align the DWI to the MNI template with an affine registration before the non-linear warp; if the data are already roughly aligned, the non-linear warp alone works.

3. Export your license and run the App:

   ```bash
   export FREESURFER_LICENSE="$(cat ~/freesurfer/license.txt)"
   ./main
   ```

## 📦 Outputs

```text
wmc/
├── classification.mat   white matter classification structure
├── tracts/              one JSON file per tract (sub-sampled streamlines) and tracts.json, for the viewer
└── surfaces/            brain surfaces (VTK) built from the FreeSurfer aparc+aseg, for the viewer
```

`classification.mat` holds a `classification` structure with a `names` field (the name of each tract) and an `index` field (for every streamline in the input tractogram, the number of the tract it belongs to, or 0). The indices refer to the streamlines of the input whole-brain tractogram.

## 🩺 Troubleshooting

- **`Please set FREESURFER_LICENSE in .bashrc`**: export the `FREESURFER_LICENSE` environment variable before running `./main` (brainlife.io provides it automatically).
- **Tracts are missing or misplaced**: the DWI and the tractogram must be in the same space. If the DWI is far from MNI alignment, set `affine` to `true`.

## 📚 Citing

> [!TIP]
> If you use this App in your work, please cite the App, the software it builds on and brainlife.io (below). GitHub's **Cite this repository** button gives the App citation in APA and BibTeX.

- Yeatman JD, Dougherty RF, Myall NJ, Wandell BA, Feldman HM. Tract profiles of white matter properties: automating fiber-tract quantification. *PLoS One* 7:e49790 (2012).
- Kruper J, Yeatman JD, Richie-Halford A, Bloom D, Grotheer M, Caffarra S, Kiar G, Karipidis II, Roy E, Chandio BQ, Garyfallidis E, Rokem A. Evaluating the reliability of human brain white matter tractometry. *Aperture Neuro* 1:1–25 (2021). [doi:10.52294/e6198273-b8e3-4b63-babb-6e6b0da10669](https://doi.org/10.52294/e6198273-b8e3-4b63-babb-6e6b0da10669)
- Segment white matter tracts using pyAFQ. brainlife.io App. [doi:10.25663/brainlife.app.295](https://doi.org/10.25663/brainlife.app.295)
- Fischl. FreeSurfer. *NeuroImage* 62:774-781 (2012). [doi:10.1016/j.neuroimage.2012.01.021](https://doi.org/10.1016/j.neuroimage.2012.01.021)
- Hayashi S, Caron BA, Heinsfeld AS, et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. *Nature Methods* 21:809–813 (2024). [doi:10.1038/s41592-024-02237-2](https://doi.org/10.1038/s41592-024-02237-2)
- Avesani P, McPherson B, Hayashi S, et al. The open diffusion data derivatives, brain data upcycling via integrated publishing of derivatives and reproducible open cloud services. *Scientific Data* 6:69 (2019). [doi:10.1038/s41597-019-0073-y](https://doi.org/10.1038/s41597-019-0073-y)

## 👥 Authors

- Brad Caron

**Contributors:** Soichi Hayashi, Franco Pestilli, Giulia Bertò

## 💰 Funding

[![Wellcome-226486/Z/22/Z](https://img.shields.io/badge/Wellcome-226486%2FZ%2F22%2FZ-purple.svg)](https://wellcome.org/)
[![NIH-NINDS-U24NS140384](https://img.shields.io/badge/NIH_NINDS-U24NS140384-green.svg)](https://reporter.nih.gov/project-details/11261037)
[![NIH-NINDS-UM1NS132207](https://img.shields.io/badge/NIH_NINDS-UM1NS132207-green.svg)](https://reporter.nih.gov/project-details/11411328)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://reporter.nih.gov/project-details/10262925)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://reporter.nih.gov/project-details/10428625)
[![NIH-NIMH-R01MH126699](https://img.shields.io/badge/NIH_NIMH-R01MH126699-green.svg)](https://reporter.nih.gov/project-details/10460628)
[![NIH-NIDCD-R01DC020088](https://img.shields.io/badge/NIH_NIDCD-R01DC020088-green.svg)](https://reporter.nih.gov/project-details/11140284)
[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-2203524](https://img.shields.io/badge/NSF_BCS-2203524-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2203524)
[![NSF-IIS-1636893](https://img.shields.io/badge/NSF_IIS-1636893-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-OAC-2148729](https://img.shields.io/badge/NSF_OAC-2148729-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148729)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NSF-IIS-2148700](https://img.shields.io/badge/NSF_IIS-2148700-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148700)
[![NSF-OAC-1916518](https://img.shields.io/badge/NSF_OAC-1916518-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1916518)

<sub>brainlife.io is publicly funded, and acknowledging that support helps keep it running. This App was developed with support from Wellcome, the U.S. National Institutes of Health (including the BRAIN Initiative BRAIN CONNECTS program: The Axonal Projectome EXchange, U24NS140384, and the Center for Mesoscale Connectomics, UM1NS132207) and the U.S. National Science Foundation.</sub>

## ⚖️ License

[MIT](LICENSE). pyAFQ and FreeSurfer are distributed under their own licenses.
