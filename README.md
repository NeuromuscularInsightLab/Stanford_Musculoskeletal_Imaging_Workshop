# Stanford Musculoskeletal Imaging Workshop
GitHub repository for the Stanford Musculoskeletal Imaging Workshop, taking place November 9–11, 2026.

| Session | Lead | Go to |
|---|---|---|
| MuscleMap Toolbox Hands-On Image Analysis | Dr. Eddo Wesselink | [Three ways to run MuscleMap](#musclemap-toolbox-hands-on-image-analysis) · [Example data](#example-data) |
| OpenMSK Hands-On Image Analysis | Dr. Anthony Gatti | [Installation](#1-installation) · [Data](#2-data) |

---

# MuscleMap Toolbox Hands-On Image Analysis
Led by Dr. Eddo Wesselink

[MuscleMap](https://github.com/MuscleMap/MuscleMap) is a free, open-source toolbox for whole-body muscle segmentation and analysis of MRI and CT images.

There are **three ways** to run MuscleMap. Pick the one that suits you and click it to expand the instructions. You only need one.

| | Option | Best for | Installation |
|---|---|---|---|
| 1 | **Terminal** (Python command line) | Batch processing, scripting, extracting metrics | ~15 min, before the workshop |
| 2 | **3D Slicer** (desktop app, point-and-click) | Running and visually inspecting single cases | ~15 min, before the workshop |
| 3 | **NeuroDesk web app** (browser) | Trying MuscleMap without installing anything | None |

> **Do the installation at home, before the workshop.** Options 1 and 2 download roughly 3 GB. Conference Wi-Fi will not be fast enough to do this on the day. Option 3 is the fallback if your installation fails.

<details>
<summary><b>Option 1 — Terminal (Python command line)</b></summary>

<br>

Every step below is a copy-paste block. Do all of this **before the workshop**: it takes about 15 minutes and downloads roughly 3 GB. Run the commands one after the other in a terminal:

* **Windows:** open **Anaconda Prompt** from the Start menu (installed with Miniconda in Step 1). Do not use the regular Command Prompt or PowerShell.
* **macOS:** open **Terminal**.
* **Linux:** open your terminal.

#### Step 1 — Install Miniconda

If you already have Anaconda or Miniconda installed, skip this step.

Download the installer for your computer, run it, and accept all default settings:

| Operating system | Download |
|---|---|
| **Windows** | [Miniconda3-latest-Windows-x86_64.exe](https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe) |
| **Mac with Apple Silicon** (M1, M2, M3, M4) | [Miniconda3-latest-MacOSX-arm64.pkg](https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.pkg) |
| **Mac with Intel chip** | [Miniconda3-latest-MacOSX-x86_64.pkg](https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.pkg) |
| **Linux** | [Miniconda3-latest-Linux-x86_64.sh](https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh) |

Not sure which Mac you have? Click the Apple menu → **About This Mac**. If it says "Chip: Apple M…", pick Apple Silicon; if it says "Processor: Intel…", pick Intel.

**Linux only** — run the installer from a terminal and answer `yes` to the questions:

```
bash ~/Downloads/Miniconda3-latest-Linux-x86_64.sh
```

After installing, **close and reopen your terminal** (Windows: open **Anaconda Prompt** from the Start menu). All installers and options are also listed on the [Miniconda installation page](https://www.anaconda.com/docs/getting-started/miniconda/install).

#### Step 2 — Create and activate the MuscleMap environment

```
conda create --name MuscleMap python=3.11.8 -y
conda activate MuscleMap
```

Your prompt should now start with `(MuscleMap)`.

> **Every time** you open a new terminal to use MuscleMap, run `conda activate MuscleMap` first.

#### Step 3 — Download MuscleMap

**Option A — with git** (if `git` is installed):

```
git clone --depth 1 https://github.com/MuscleMap/MuscleMap
cd MuscleMap
```

**Option B — without git** (download a ZIP from your browser):

1. Open https://github.com/MuscleMap/MuscleMap
2. Click the green **<> Code ▼** button
3. Click **Download ZIP**
4. Unzip the file. This creates a folder called `MuscleMap-main`
5. In your terminal, go into that folder (adjust the path to where you unzipped it):

```
cd Downloads/MuscleMap-main
```

#### Step 4 — Install MuscleMap

Make sure your terminal is inside the MuscleMap folder (Step 3) and the environment is active (`(MuscleMap)` in your prompt), then run:

```
pip install -e .
```

This installs MuscleMap and all its dependencies, including a CPU version of PyTorch. This takes a few minutes.

#### Step 5 — Enable your GPU (optional, but much faster)

MuscleMap works on CPU, but a GPU makes segmentation many times faster. Find your situation in the table:

| Your computer | What to do |
|---|---|
| **Mac** (Intel or Apple Silicon) | Nothing. MuscleMap runs on CPU on Mac. Skip to Step 6. |
| **Windows / Linux without an NVIDIA GPU** | Nothing. Skip to Step 6. |
| **Windows / Linux with an NVIDIA GPU** | Follow **5a** below. |
| **Linux with an AMD GPU** (ROCm) | Follow **5b** below. |

Not sure whether you have an NVIDIA GPU? Run `nvidia-smi` in your terminal. If you get a table with your GPU name, you have one. If you get "command not found", you do not (or the driver is not installed) and you can skip to Step 6.

#### 5a — NVIDIA GPU (Windows or Linux)

1. Run:

   ```
   nvidia-smi
   ```

2. Look at the **top-right corner** of the output for `CUDA Version: XX.X`.

3. Pick the **one** command that matches and run it:

   **CUDA Version 12.1 or higher** (most computers):

   ```
   pip uninstall -y torch
   pip install torch==2.4.1 --index-url https://download.pytorch.org/whl/cu121
   ```

   **CUDA Version 11.8, 11.9 or 12.0:**

   ```
   pip uninstall -y torch
   pip install torch==2.4.1 --index-url https://download.pytorch.org/whl/cu118
   ```

   **CUDA Version lower than 11.8:** update your NVIDIA driver from https://www.nvidia.com/drivers, restart, and then use the "12.1 or higher" command.

4. Check that the GPU is detected:

   ```
   python -c "import torch; print('PyTorch', torch.__version__); print('GPU available:', torch.cuda.is_available())"
   ```

   You should see `GPU available: True`. If it says `False`, update your NVIDIA driver, restart your computer, and run the check again.

#### 5b — AMD GPU with ROCm (Linux only)

```
pip uninstall -y torch
pip install torch==2.4.1 --index-url https://download.pytorch.org/whl/rocm6.1
python -c "import torch; print('GPU available:', torch.cuda.is_available())"
```

#### Step 6 — Check that MuscleMap works

```
mm_segment -h
```

If you see a help message listing the options of `mm_segment`, the installation was successful.

#### Step 7 — Download the model weights before the workshop

MuscleMap downloads its segmentation model from Zenodo the **first time** you run `mm_segment`. Do this at home, not on conference Wi-Fi. Run `mm_segment` once on the example image that comes with this repository (see [the example data section](#example-data)). First download this repository (green **<> Code ▼** button → **Download ZIP**, or `git clone`), then in your terminal go into its `data/MuscleMap` folder and run:

```
mm_segment -i sub-01_T2w_L4-L5.nii.gz
```

This takes a few minutes on CPU. When it finishes you will find `sub-01_T2w_L4-L5_dseg.nii.gz` next to the input image. After this, the model is cached on your computer and will not be downloaded again.

#### Troubleshooting

| Problem | Fix |
|---|---|
| `conda: command not found` (Windows) | Open **Anaconda Prompt** instead of Command Prompt / PowerShell. |
| `conda: command not found` (Mac/Linux) | Close and reopen your terminal after installing Miniconda. If it persists, run `~/miniconda3/bin/conda init` and reopen the terminal. |
| `CondaError: Run 'conda init' before 'conda activate'` | Run `conda init`, close the terminal, open it again and retry Step 2. |
| `mm_segment: command not found` | The environment is not active. Run `conda activate MuscleMap`. |
| `pip install -e .` fails with "no such file setup.py" | You are not inside the MuscleMap folder. Run `cd MuscleMap` (or `cd MuscleMap-main`) first. |
| `GPU available: False` after Step 5 | Your NVIDIA driver is too old. Update it from https://www.nvidia.com/drivers, restart, and run the check again. |
| Segmentation is slow or runs out of memory | Run `mm_segment -i image.nii.gz -s 75 -c auto` (lower overlap, automatic chunk size). |

Still stuck? Email the workshop team before the workshop, or bring your laptop 30 minutes early.

#### Useful links

* MuscleMap repository: https://github.com/MuscleMap/MuscleMap
* Installation and usage video tutorial: https://www.youtube.com/watch?v=utlUVdvy6WI
* Label definitions: https://musclemap.github.io/MuscleMap/muscle-anatomy/
* Prefer not to use the command line? See Option 2 (3D Slicer) and Option 3 (NeuroDesk) above.

</details>

<details>
<summary><b>Option 2 — 3D Slicer (desktop app, point-and-click)</b></summary>

<br>

[3D Slicer](https://www.slicer.org/) is a free, open-source desktop application for medical image visualisation. MuscleMap is available as a Slicer extension, so you can segment and inspect images without typing any commands.

**Video tutorial:** https://www.youtube.com/watch?v=aAXxopcMeKI&t=14s walks through the whole installation below. One thing has changed since the video was recorded: it says to install the *Preview Release* of Slicer, but MuscleMap is now available in the **Stable Release**. Use the Stable Release.

#### Step 1 — Install 3D Slicer

1. Go to https://download.slicer.org/
2. Under **Stable Release**, click the download for your operating system (Windows, macOS or Linux). You need version **5.12 or newer**.
3. Run the installer and accept the default settings. On macOS, drag Slicer into your Applications folder.
4. Start 3D Slicer.

#### Step 2 — Install the MuscleMap extension

1. In Slicer, open the menu **View → Extensions Manager**.
2. In the search box, type **MuscleMap**.
3. Click **Install**. The **PyTorch** extension that MuscleMap needs is installed automatically with it.
4. When asked, **restart Slicer**.

#### Step 3 — Install PyTorch inside Slicer

1. Open the menu **View → Modules → Utilities → PyTorch Utils**.
2. Click **Install PyTorch**. Leave the settings on automatic: the module detects whether you have a compatible NVIDIA GPU and installs the matching GPU build, or a CPU build otherwise.
3. Wait until the module reports that PyTorch was installed successfully. This can take several minutes.

#### Step 4 — Install the MuscleMap dependencies

1. Open the menu **View → Modules → MuscleMap → MuscleMap Whole-body Segmentation**.
2. Click **Install MuscleMap dependencies**. This is a one-time step and takes several minutes.
3. Wait for the message *MuscleMap dependencies are installed and ready*.

#### Step 5 — Test it and download the model weights before the workshop

1. In the MuscleMap module, click **Load volume from file…** and open `data/MuscleMap/sub-01_T2w_L4-L5.nii.gz` from this repository (download the repository first via the green **<> Code ▼** button → **Download ZIP**).
2. Make sure it is selected under **Input volume**.
3. Click **Run MuscleMap segmentation**. The first run downloads the segmentation model from Zenodo, so do this at home, not on conference Wi-Fi.
4. When it finishes, the segmentation appears over the image. Click **Show 3D** to see it in 3D.

#### Troubleshooting

| Problem | Fix |
|---|---|
| MuscleMap does not appear in the Extensions Manager | Check that you installed the **Stable Release** of version 5.12 or newer, and that you have an internet connection. |
| PyTorch installation fails (Windows) | Close Slicer, right-click the Slicer icon and choose **Run as administrator**, then repeat Step 3. |
| Segmentation is very slow | Without a GPU, segmentation takes 1 to 20 minutes depending on image size. Under **Advanced**, tick **Force lower overlap**. |
| Segmentation fails with an out-of-memory error | Under **Advanced**, tick **Force CPU (ignore GPU)** and run again. |

</details>

<details>
<summary><b>Option 3 — NeuroDesk web app (no installation)</b></summary>

<br>

MuscleMap runs in your browser inside the [NeuroDesk](https://www.neurodesk.org/) environment. Nothing to install. Use this if you cannot get Option 1 or 2 to work.

1. Go to https://webapps.neurodesk.org/musclemap/
2. Drag and drop your image into the page. NIfTI files (`.nii` or `.nii.gz`) and DICOM folders are both accepted. For the workshop, use `data/MuscleMap/sub-01_T2w_L4-L5.nii.gz` from this repository.
3. Select the uploaded image and click **Run segmentation**.
4. The labelled result appears in the viewer. The segmentation can be exported for further analysis.

Processing runs without a GPU, so expect a few minutes per image.

</details>

## Example data

The [`data/MuscleMap/`](data/MuscleMap/) folder contains the example image used in the hands-on session: an axial T2-weighted lumbar spine MRI of one patient at the L4–L5 disc level.

| File | Level | Slices |
|---|---|---|
| `data/MuscleMap/sub-01_T2w_L4-L5.nii.gz` | L4–L5 | 4 |

The file is a small stack of axial slices through the L4–L5 intervertebral disc, as acquired in routine clinical practice. Nothing needs to be downloaded separately: the image comes with this repository.

The images are taken from the open *Lumbar Spine MRI Dataset* (Sudirman et al., Mendeley Data, CC BY 4.0) and were converted from DICOM to NIfTI. See [`data/MuscleMap/README.md`](data/MuscleMap/README.md) for the full attribution.

*Hands-on notebooks will be added here before the workshop.*

---

# OpenMSK Hands-On Image Analysis
Led by Dr. Anthony Gatti
## 1. Installation
## 2. Data
