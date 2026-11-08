# OpenMSK prompts

Prompts that work with the files in this folder. Paste one into a coding assistant that can read your files, or attach the files to a chat.

Three habits make these work:

1. **Give it the docs.** Attach `openmsk-outputs-guide.pdf` for outputs and `oai_teaching_cohort_data_dictionary.csv` for the sheet.
2. **State what the data can't do.** An assistant will not raise the sampling problem by itself, and it will write a confident paragraph about 12 events.
3. **Ask to see the plot first.** Look at the data before you ask for statistics.

Never paste identifiable data into a hosted LLM. Check your own institution's rules before using one on your own scans.

---

## Set up this notebook on your own computer

Colab needs none of this. These are for running `OpenMSK_hands_on.ipynb` on your own machine, following *Option 2* in the repository README.

**Walk me through it**

> I want to run notebooks/OpenMSK_hands_on.ipynb from the Stanford_Musculoskeletal_Imaging_Workshop GitHub repository on my own computer, not in Colab. Read the "Option 2: Jupyter on your own computer" section of the repository's README.md and notebooks/OpenMSK_requirements.txt. My computer is [a Mac with Apple silicon / a Mac with an Intel chip / Windows / Linux], [with / without] an NVIDIA GPU, and conda [is / is not] installed. Walk me through it one command at a time: get the repository, create the openmsk-workshop conda environment, install the requirements, register the Jupyter kernel and start JupyterLab in the repository folder. Say what each command does. If a command fails, ask me to paste the whole error before suggesting a fix.

**Fix an install error**

> I'm setting up the OpenMSK workshop notebook in a conda environment called openmsk-workshop, on [operating system]. This command failed: [command]. The full error is: [paste it]. Explain in plain words what went wrong, then give me the smallest fix. Don't recreate the environment unless nothing else will work, and tell me before changing anything outside it.

**Check that it works**

> In the openmsk-workshop environment, write a short Python script that imports pyvista, nrrd, torch, NSM and pymskt and prints each version; says whether torch can use a GPU (CUDA on NVIDIA, MPS on Apple silicon); and saves a PyVista sphere to sphere.png without opening a window. For anything that fails, tell me what it means and what to try.

**Let a coding agent do it**

> You're in a clone of the Stanford_Musculoskeletal_Imaging_Workshop repository. Read README.md, find the OpenMSK "Option 2" setup, and set up notebooks/OpenMSK_hands_on.ipynb to run on this machine. Tell me each command before you run it, and don't touch the MuscleMap environment. When it's done, run the whole notebook once with `jupyter nbconvert --to notebook --execute --output /tmp/check.ipynb notebooks/OpenMSK_hands_on.ipynb` and tell me which cells failed, if any.

---

## One knee

**Orient me**

> Here is an unzipped OpenMSK results folder and its openmsk-outputs-guide.pdf. Tell me what ran, what was skipped and why, which model and pipeline version produced it, and where the cartilage thickness and B-score are. Do not assume a file is missing because of its name: thickness is on the bone meshes and B-score is a key inside a JSON.

**Show me a thickness map**

> Using pyvista, read femur_mesh.vtk and colour it by the "thickness (mm)" array. Treat 0 as no cartilage and show those points in a bone colour. View from below, tilted forward, so the trochlea and both condyles are visible. Add a colour bar in mm. Save a PNG.

**Check the fit before trusting the score**

> Read NSM_bone_only_recon_params.json and NSM_recon_params.json. Report Bscore and assd_bone_mm from each. Then recompute the bone-only B-score by hand from latent, using bscore_vector, mean_healthy and std_healthy from BSCORE_MODELS/NSM_Orig_BScore_Bone_Only_April_18_2025/model.json in the OpenMSK repo. Tell me if it matches the file.

**Check the label scheme**

> Read the *_all-labels.nrrd file and report the voxel count of each label. The femur should be the largest structure. If the largest label is 7, this file uses the older native scheme (1 patellar cartilage, 2 femoral cartilage, 7 femur). If it is 1, it uses the canonical scheme (1 femur, 4 femoral cartilage, 7 patellar cartilage). Tell me which, and use the right names from here on.

## Many knees

**Build one sheet**

> I have a folder of OpenMSK results, one unzipped subfolder per scan. Write a script that makes one CSV with one row per scan: the folder name, every column from *_results.csv, Bscore and assd_bone_mm from both NSM params files if present, and each step's status from _step_log.json. Print how many scans are missing each output. Flag any scan with assd_bone_mm above the 95th percentile for me to look at.

**Join my demographics**

> Join that sheet to my_demographics.csv on subject ID. Show me every row that fails to match rather than dropping it silently. Show the distribution of each column before doing anything else.

## The OAI teaching sheet

Attach `oai_teaching_cohort.csv` and `oai_teaching_cohort_data_dictionary.csv`.

**Start here**

> Read the CSV and the data dictionary. Plot B-score and medial weight-bearing femur thickness by KL grade, one dot per knee with the median marked. The sheet is sampled equally by KL grade, so do not report any rates or prevalence as if they describe a population.

**Compare two measures**

> Does bscore_bone or thick_med_wb_fem_mm predict tkr_8y better, after adjusting for KL, sex, age and BMI? Use cross-validation and give confidence intervals. There are only 56 events, and the sampling is by KL. Tell me plainly what that can and cannot support.

**Survival**

> Make a Kaplan-Meier plot of knee replacement by B-score third, using followup_days and tkr_days. Censor at 8 years. Then do it again within KL 3 only and tell me how many events each curve rests on.

**Your own question**

> Are female and male knees on the same line? Plot B-score against KL grade by sex, then show me the plot before any statistics.

**Two B-scores**

> Compare bscore_bone and bscore_bone_cart. Show a Bland-Altman plot. Which knees disagree most, and are they different in any way the sheet can show?

## Latent vectors

Attach `oai_teaching_cohort_latents.csv` and `openmsk_helpers.py`.

**Group difference**

> Using openmsk_helpers.py, decode the average latent of KL 0 knees and of KL 4 knees. Colour the KL 4 surface by signed distance from the KL 0 surface, red where it sticks out and blue where it sits in. Show anterior, inferior and posterior views. Check the sign by confirming that a point far outside the reference gets a positive distance.

**Adjusted group difference**

> I want the shape difference between [group A] and [group B], adjusted for KL, sex, age and BMI. Regress the latents on the group and the covariates, take the group's coefficient as a direction, and decode the mean plus and minus half of it. Then shuffle the group labels 200 times, recompute, and tell me how the real map's 99th percentile compares with the null distribution.

**My own axis**

> Fit a new axis from [variable] the same way the B-score is built: direction between group means in latent space, unit length, then standardized against a reference group. Split the knees first and fit only on the training split. Report performance on the held-out knees only. These knees are from the OAI, where the shape model was trained, so tell me why even the held-out result may be optimistic.

## Running it yourself

**Set up and prove it works**

> Read README.MD and CLAUDE.md in this repo. Set up the environment on this machine. Run the pipeline on openmsk-example-knee.nrrd and check the results against the example bundle. Tell me before installing anything, and stop if a number differs by more than you can explain.

**Use my own segmentation**

> I have my own segmentation of a knee MRI, with this label table: [paste table]. Read the step documentation in CLAUDE.md. Work out the file names and remap table needed to run the steps from label_remap onward. Remember that a label missing from the remap table is deleted, not passed through, so check that every structure survives. Show me the plan first.
