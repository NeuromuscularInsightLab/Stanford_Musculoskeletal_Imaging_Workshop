# Example data

Two images are used in the MuscleMap hands-on session: an axial T2-weighted lumbar spine MRI at the L4–L5 level (Example 1) and a Dixon fat-fraction image of both thighs from the workshop's hands-on imaging session (Example 2).

## Folder layout

| Folder | Contents |
|:--|:--|
| `source-data/lumbar/` | Example 1 input image. Do not modify. |
| `source-data/thigh/` | Example 2 input image. Do not modify. |
| `outputs/lumbar/` | Everything MuscleMap produces for Example 1: segmentation (`*_dseg.nii.gz`), JSON sidecar, fat maps and CSV results. Written by the notebook or by the terminal steps in the main README. |
| `outputs/thigh/` | Everything MuscleMap produces for Example 2: segmentation (`*_dseg.nii.gz`), JSON sidecar and the CSV with mean fat fraction and volume per structure. Included in the repository so the workshop does not wait for the segmentation. |

| File | Region | Matrix | Voxel size (mm) |
|:--|:--|:--|:--|
| `source-data/lumbar/sub-01_T2w_L4-L5.nii.gz` | L4–L5 disc level, 4 axial slices | 320 × 320 × 4 | 0.69 × 0.69 × 4.4 |
| `source-data/thigh/sub-workshop_thigh-example.nii.gz` | Both thighs, 26 axial slices | 624 × 512 × 26 | 0.8 × 0.8 × 8.0 |

## Example 1 · Lumbar spine

The file is one block of axial slices through the L4–L5 disc, angled parallel to the disc, as acquired in routine clinical practice.

### Source and license

The image is a subset of the **Lumbar Spine MRI Dataset** (version 2), published on Mendeley Data by Sud Sudirman, Ala Al Kafri, Friska Natalia, Hira Meidia, Nunik Afriliana, Wasfi Al-Rashdan, Mohammad Bashtawi and Mohammed Al-Jumaily, and distributed under the [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) license.

* Dataset: https://data.mendeley.com/datasets/k57fr854j2/2
* DOI: https://doi.org/10.17632/k57fr854j2.2

**Changes made:** the axial T2-weighted series of patient `0001` (series `T2_TSE_TRA_384`) was converted from DICOM to NIfTI with dcm2niix. Only the block of slices at the L4–L5 level was kept, and the file was renamed. No other processing was applied. The original dataset contains anonymised clinical data; no identifying information is included here.

The dataset authors ask that the following papers be cited when their data is used:

* Al-Kafri A, Sudirman S, Hussain A, Al-Jumeily D, Natalia F, Meidia H, Afriliana N, Al-Rashdan W, Bashtawi M, Al-Jumaily M. *Boundary Delineation of MRI Images for Lumbar Spinal Stenosis Detection Through Semantic Segmentation Using Deep Neural Networks.* IEEE Access. 2019;7:43487–43501. https://doi.org/10.1109/ACCESS.2019.2908002
* Natalia F, Meidia H, Afriliana N, Al-Kafri A, Sudirman S, Simpson A, Sophian A, Al-Jumaily M, Al-Rashdan W, Bashtawi M. *Development of Ground Truth Data for Automatic Lumbar Spine MRI Image Segmentation.* In: 2018 IEEE 20th International Conference on High Performance Computing and Communications (HPCC/SmartCity/DSS). 2018:1449–1454. https://doi.org/10.1109/HPCC/SmartCity/DSS.2018.00239

## Example 2 · Thigh Dixon MRI

A Dixon **proton-density fat-fraction** image of both thighs, acquired during the hands-on imaging session of the Stanford Musculoskeletal Imaging Workshop (November 2026). Voxel values are 0–1000 for a fat fraction of 0–100 %: muscle is dark, fat is bright. The acquisition is 0.8 mm isotropic; every tenth slice was kept and the stack was trimmed to the central 60 % of the thigh, giving 26 slices with an 8 mm spacing, so that the whole-body model segments it in a reasonable time on a CPU. No other processing was applied.

The segmentation (`outputs/thigh/sub-workshop_thigh-example_dseg.nii.gz`) and the metrics (`outputs/thigh/sub-workshop_thigh-example_average_results.csv`, from `mm_extract_metrics -m average`) are produced with MuscleMap exactly as shown in the notebook and are included so that the workshop does not wait for them.

### Source and license

Volunteer scan from the workshop's hands-on imaging session, anonymised. *To be completed: consent statement and terms of use.*
