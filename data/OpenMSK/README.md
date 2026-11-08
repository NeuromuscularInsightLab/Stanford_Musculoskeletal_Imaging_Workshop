# OpenMSK example data

| Folder | Contents |
|:--|:--|
| `example/` | One knee MRI and every output OpenMSK produced for it. The same files as **MRI + all results** on [openmsk.com](https://openmsk.com) |
| `oai_teaching_cohort/` | A small teaching sheet from the Osteoarthritis Initiative, plus each knee's shape-model latent vector |
| `decoded/` | Knees decoded ahead of time from the shape model: the average KL 0 and KL 4 knees, the B-score walk, and the sex and pain axes. The notebook uses them only if it can't download the model |
| `figures/` | Made by the notebook. Not tracked |

## `example/`

`openmsk-example-knee.nrrd` is a sagittal knee MRI, 512 x 512 x 96 voxels at 0.312 x 0.313 x 1 mm. It's one of the OpenMSK maintainers' own knees, published deliberately, with no patient identifiers. Free to use for research and teaching. `openmsk-outputs-guide.pdf` and `README.txt` inside the folder explain every file.

## `oai_teaching_cohort/`

500 baseline knees: 100 per KL grade, one knee per person. OAI participant IDs are replaced with `K0001`-style labels. `oai_teaching_cohort_data_dictionary.csv` describes each column.

- Equal numbers per KL grade is a teaching choice, so rates in this sheet are not OAI rates.
- `bscore_bone` uses the same model as `NSM_bone_only_recon_params.json` from the website.
- The thickness columns use a different regional definition from the website's `*_results.csv`. Don't pool the two.

Data used here were obtained from the Osteoarthritis Initiative (OAI) database, https://nda.nih.gov/oai.
