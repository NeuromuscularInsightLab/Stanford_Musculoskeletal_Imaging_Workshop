# Stanford Musculoskeletal Imaging Workshop
GitHub repository for the Stanford Musculoskeletal Imaging Workshop, taking place November 9–11, 2026.

| Session | Lead | Go to |
|---|---|---|
| MuscleMap Toolbox Hands-On Image Analysis | Dr. Eddo Wesselink | [Installation](#1-installation) · [Data](#2-data) |
| OpenMSK Hands-On Image Analysis | Dr. Anthony Gatti | [Installation](#1-installation-1) · [Data](#2-data-1) |

---

# MuscleMap Toolbox Hands-On Image Analysis
Led by Dr. Eddo Wesselink

[MuscleMap](https://github.com/MuscleMap/MuscleMap) is a free, open-source toolbox for whole-body muscle segmentation and analysis of MRI and CT images.

> **Please complete the installation below *before* the workshop.** It takes about 15 minutes and needs a stable internet connection (roughly 3 GB of downloads). Conference Wi-Fi will not be fast enough to do this on the day.

## 1. Installation

Every step below is a copy-paste block. Run the commands one after the other in a terminal:

* **Windows:** open **Anaconda Prompt** from the Start menu (installed with Miniconda in Step 1). Do not use the regular Command Prompt or PowerShell.
* **macOS:** open **Terminal**.
* **Linux:** open your terminal.

### Step 1 — Install Miniconda

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

### Step 2 — Create and activate the MuscleMap environment

```
conda create --name MuscleMap python=3.11.8 -y
conda activate MuscleMap
```

Your prompt should now start with `(MuscleMap)`.

> **Every time** you open a new terminal to use MuscleMap, run `conda activate MuscleMap` first.

### Step 3 — Download MuscleMap

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

### Step 4 — Install MuscleMap

Make sure your terminal is inside the MuscleMap folder (Step 3) and the environment is active (`(MuscleMap)` in your prompt), then run:

```
pip install -e .
```

This installs MuscleMap and all its dependencies, including a CPU version of PyTorch. This takes a few minutes.

### Step 5 — Enable your GPU (optional, but much faster)

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

### Step 6 — Check that MuscleMap works

```
mm_segment -h
```

If you see a help message listing the options of `mm_segment`, the installation was successful.

### Step 7 — Download the model weights before the workshop

MuscleMap downloads its segmentation model from Zenodo the **first time** you run `mm_segment`. Do this at home, not on conference Wi-Fi. Run `mm_segment` once on the example image provided in [Section 2](#2-data):

```
mm_segment -i image.nii.gz
```

After this, the model is cached on your computer and will not be downloaded again.

### Troubleshooting

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

### Useful links

* MuscleMap repository: https://github.com/MuscleMap/MuscleMap
* Installation and usage video tutorial: https://www.youtube.com/watch?v=utlUVdvy6WI
* Label definitions: https://musclemap.github.io/MuscleMap/muscle-anatomy/
* No programming? MuscleMap also exists as a [3D Slicer extension](https://www.youtube.com/watch?v=aAXxopcMeKI) and as a [NeuroDesk web app](https://musclemap.neurodesk.org/).

## 2. Data

*Example data and hands-on notebooks will be added here before the workshop.*

---

# OpenMSK Hands-On Image Analysis
Led by Dr. Anthony Gatti
## 1. Installation
## 2. Data
