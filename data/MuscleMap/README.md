# Example data

Axial T2-weighted lumbar spine MRI of one patient at the L4–L5 intervertebral disc level. This is the image used in the MuscleMap hands-on session.

| File | Level | Slices | Voxel size (mm) |
|---|---|---|---|
| `sub-01_T2w_L4-L5.nii.gz` | L4–L5 | 4 | 0.69 × 0.69 × 4.4 |

The file is one block of axial slices through the L4–L5 disc, angled parallel to the disc, as acquired in routine clinical practice.

## Source and license

These images are a subset of the **Lumbar Spine MRI Dataset** (version 2), published on Mendeley Data by Sud Sudirman, Ala Al Kafri, Friska Natalia, Hira Meidia, Nunik Afriliana, Wasfi Al-Rashdan, Mohammad Bashtawi and Mohammed Al-Jumaily, and distributed under the [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) license.

* Dataset: https://data.mendeley.com/datasets/k57fr854j2/2
* DOI: https://doi.org/10.17632/k57fr854j2.2

**Changes made:** the axial T2-weighted series of patient `0001` (series `T2_TSE_TRA_384`) was converted from DICOM to NIfTI with dcm2niix. Only the block of slices at the L4–L5 level was kept, and the file was renamed. No other processing was applied. The original dataset contains anonymised clinical data; no identifying information is included here.

The dataset authors ask that the following papers be cited when their data is used:

* Al-Kafri A, Sudirman S, Hussain A, Al-Jumeily D, Natalia F, Meidia H, Afriliana N, Al-Rashdan W, Bashtawi M, Al-Jumaily M. *Boundary Delineation of MRI Images for Lumbar Spinal Stenosis Detection Through Semantic Segmentation Using Deep Neural Networks.* IEEE Access. 2019;7:43487–43501. https://doi.org/10.1109/ACCESS.2019.2908002
* Natalia F, Meidia H, Afriliana N, Al-Kafri A, Sudirman S, Simpson A, Sophian A, Al-Jumaily M, Al-Rashdan W, Bashtawi M. *Development of Ground Truth Data for Automatic Lumbar Spine MRI Image Segmentation.* In: 2018 IEEE 20th International Conference on High Performance Computing and Communications (HPCC/SmartCity/DSS). 2018:1449–1454. https://doi.org/10.1109/HPCC/SmartCity/DSS.2018.00239
