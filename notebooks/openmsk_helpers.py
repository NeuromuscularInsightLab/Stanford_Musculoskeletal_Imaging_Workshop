"""Small helpers for the OpenMSK hands-on notebook.

Nothing here is clever. Read it, change it, or hand it to your LLM as context.
"""
import json            # read and write .json files
import os              # environment variables and paths
import urllib.request  # download files from the web
import zipfile         # unpack .zip files
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv

# Draw 3D scenes into memory instead of opening a window. Needed on Colab, which has no screen.
pv.OFF_SCREEN = True

# Where things live, relative to this file.
HERE = Path(__file__).resolve().parent              # notebooks/
DATA = HERE.parent / "data" / "OpenMSK"             # data/OpenMSK/ in this repository
OUT = Path(os.environ.get("TUTORIAL_OUT", DATA / "figures"))   # figures the notebook saves
OUT.mkdir(parents=True, exist_ok=True)
# Interactive 3D: "html" is drawn by your browser and needs no display. "static" draws a picture.
BACKEND_3D = os.environ.get("OPENMSK_3D", "html")


def _quiet_optional_imports():
    """pymskt and NSM announce optional packages they can't find, and NSM uses two names its libraries have
    since deprecated. Nothing here uses those packages, so import once, quietly. The filters match these
    exact messages only, so any other warning still shows."""
    import contextlib
    import importlib
    import io
    import warnings

    warnings.filterwarnings("ignore", message=".*n_faces_strict.*")              # NSM logs face counts with an old PyVista name
    warnings.filterwarnings("ignore", message="schedulefree not found")          # optional optimizer, only for training
    warnings.filterwarnings("ignore", message=".*torch.nn.utils.weight_norm.*")  # the saved model was built with it
    with contextlib.redirect_stdout(io.StringIO()):                              # pymskt prints "pyfocusr not found"
        for name in ("pymskt.mesh", "NSM.mesh"):
            try:
                importlib.import_module(name)
            except ImportError:  # not installed: fine, the parts that need them will say so later
                pass


_quiet_optional_imports()

# The public example knee on openmsk.com, used if the copy in this repository is missing.
EXAMPLE_URL = "https://openmsk.com/example/bundle"
# The B-score definitions live in the public OpenMSK repository.
BSCORE_URL = (
    "https://raw.githubusercontent.com/gattia/OpenMSK/main/BSCORE_MODELS/{}/model.json"
)
BSCORE_MODELS = {
    "bone_only": "NSM_Orig_BScore_Bone_Only_April_18_2025",
    "bone_cart": "NSM_Orig_BScore_Bone_Cartilage_April_17_2025",
}

# Colours. KL is ordered, so it gets one hue from light to dark.
KL_COLORS = ["#E39A92", "#D4736B", "#BC4A45", "#98201F", "#6A0D10"]
BLUE, RED = "#2F6DA8", "#B1040E"
BONE = "#E9E4D8"
INK, MUTED = "#222222", "#6B6B6B"   # dark text, and grey for axes and labels


def style():
    """One look for every plot: clean axes, readable text, and a font that exists on this machine."""
    import logging

    from matplotlib import font_manager

    # Without this, matplotlib warns once per text item when a font is missing.
    logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
    # Use the first of these fonts that's installed. Colab has DejaVu Sans; Macs and Windows have Arial.
    available = {f.name for f in font_manager.fontManager.ttflist}
    family = next((f for f in ("Arial", "Helvetica", "Liberation Sans", "DejaVu Sans") if f in available), "sans-serif")
    plt.rcParams.update(
        {
            "font.family": family,
            "font.size": 13,
            "axes.spines.top": False,     # no box around the plot, just the left and bottom axes
            "axes.spines.right": False,
            "axes.edgecolor": MUTED,
            "axes.labelcolor": INK,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "axes.grid": False,
            "figure.dpi": 110,            # size on screen
            "savefig.dpi": 220,           # sharper when saved
            "savefig.bbox": "tight",      # trim white space when saving
            "savefig.facecolor": "white",
        }
    )


def get_example_bundle(dest=DATA / "example"):
    """The public example knee: MRI plus every output. In this repository already; downloaded if missing."""
    dest = Path(dest)
    if (dest / "job_manifest.json").exists():   # already here: nothing to do
        return dest
    dest.mkdir(parents=True, exist_ok=True)
    archive = dest / "openmsk-example-bundle.zip"
    print("Downloading", EXAMPLE_URL)
    urllib.request.urlretrieve(EXAMPLE_URL, archive)   # download the zip
    with zipfile.ZipFile(archive) as z:
        z.extractall(dest)                             # unpack it
    archive.unlink()                                   # and delete the zip
    return dest


def load_bscore_model(kind="bone_only"):
    """The B-score is three things: a 512-long direction, a mean and an SD."""
    cache = DATA / "bscore_models" / f"{BSCORE_MODELS[kind]}.json"
    if not cache.exists():   # download once, then reuse the saved copy
        cache.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(BSCORE_URL.format(BSCORE_MODELS[kind]), cache)
    m = json.loads(cache.read_text())
    return {
        "vector": np.array(m["bscore_vector"], dtype=float),   # the OA direction in latent space
        "mean": float(m["mean_healthy"]),                      # where non-OA knees sit along it, on average
        "std": float(m["std_healthy"]),                        # and how spread out they are
    }


def bscore(latent, model):
    """B = (latent dot vector - non-OA mean) / non-OA SD."""
    # Project the latent onto the OA direction (a dot product), then express it in non-OA standard deviations.
    return (np.asarray(latent, dtype=float) @ model["vector"] - model["mean"]) / model["std"]


def move_to_bscore(latent, target, model):
    """Shortest move in latent space that lands a knee on a chosen B-score."""
    v = model["vector"]
    # How far the B-score has to change, converted back into latent units, applied along the B-score direction only.
    return np.asarray(latent, dtype=float) + (target - bscore(latent, model)) * model["std"] * v / (v @ v)


def load_decoder(model_dir=None, device=None):
    """Load the bone-only neural shape model (about 275 MB).

    Default: download from Hugging Face. The repo is gated, so accept the
    non-commercial terms at https://huggingface.co/aagatti/ShapeMedKnee and run
    `huggingface-cli login` first.
    Or set NSM_MODEL_DIR to a folder holding model_params_config.json + model/1150.pth.
    """
    import torch
    from NSM.models import TriplanarDecoder

    # Use the fastest hardware available: an NVIDIA GPU, then an Apple GPU, then the processor.
    device = device or ("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")
    model_dir = model_dir or os.environ.get("NSM_MODEL_DIR")
    if model_dir:   # a copy already on disk
        path_cfg = Path(model_dir) / "model_params_config.json"
        path_state = Path(model_dir) / "model" / "1150.pth"
    else:           # download from Hugging Face (cached after the first time)
        from huggingface_hub import hf_hub_download
        from huggingface_hub.utils import logging as hf_logging

        hf_logging.set_verbosity_error()   # no token is needed; skip the notice suggesting one

        repo, sub = "aagatti/ShapeMedKnee", "551_nsm_femur_bone_v0.0.1"
        path_cfg = hf_hub_download(repo, f"{sub}/model_params_config.json")
        path_state = hf_hub_download(repo, f"{sub}/model/1150.pth")
    # The config describes the network's shape. Build an empty network to match it.
    c = json.loads(Path(path_cfg).read_text())
    decoder = TriplanarDecoder(
        latent_dim=c["latent_size"],
        n_objects=c["objects_per_decoder"],
        conv_hidden_dims=c["conv_hidden_dims"],
        conv_deep_image_size=c["conv_deep_image_size"],
        conv_norm=c["conv_norm"],
        conv_norm_type=c["conv_norm_type"],
        conv_start_with_mlp=c["conv_start_with_mlp"],
        sdf_latent_size=c["sdf_latent_size"],
        sdf_hidden_dims=c["sdf_hidden_dims"],
        sdf_weight_norm=c["weight_norm"],
        sdf_final_activation=c["final_activation"],
        sdf_activation=c["activation"],
        sdf_dropout_prob=c["dropout_prob"],
        sum_sdf_features=c["sum_conv_output_features"],
        conv_pred_sdf=c["conv_pred_sdf"],
    )
    # Fill it with the trained weights, move it to the chosen hardware, and switch to inference mode.
    state = torch.load(path_state, map_location="cpu", weights_only=True)
    decoder.load_state_dict(state["model"])
    decoder.to(device).eval()
    decoder.device_name = device   # remembered so decode() uses the same hardware
    return decoder


def decode(decoder, latent, n=128, mm_per_unit=1.0, smooth=True):
    """Latent vector -> surface. Evaluates the SDF on an n^3 grid, then marching cubes."""
    import torch
    from NSM.mesh import create_mesh

    # The 512 numbers, as a tensor on the same hardware as the network.
    z = torch.tensor(np.asarray(latent, dtype=np.float32).ravel()).to(decoder.device_name)
    with torch.no_grad():   # inference only: no training bookkeeping, faster
        # Ask the network for the signed distance at every point of an n x n x n grid,
        # then find the surface where that distance is zero (marching cubes).
        m = create_mesh(
            decoder, z, n_pts_per_axis=n, scale_to_original_mesh=False,
            device=decoder.device_name, objects=1, batch_size=64**3,
        )
    # Plain PyVista mesh, scaled from model units to mm.
    surf = pv.PolyData(np.asarray(m.point_coords, dtype=float) * mm_per_unit, np.asarray(m.faces))
    if smooth:   # soften the small steps marching cubes leaves on the surface
        surf = surf.smooth_taubin(n_iter=30, pass_band=0.08)
    return surf


DECODED = DATA / "decoded"   # surfaces decoded ahead of time, for anyone without the shape model


def decode_or_load(decoder, latent, name, n=128, mm_per_unit=1.0):
    """Decode a latent with the shape model or, if the model isn't loaded, read the copy saved in this repository."""
    path = DECODED / f"{name}.vtk"
    building = os.environ.get("OPENMSK_SAVE_DECODED")
    on_cpu_with_copy = decoder is not None and decoder.device_name == "cpu" and path.exists() and not building
    if decoder is None or on_cpu_with_copy:   # no model, or a slow CPU and a saved copy already here
        return pv.read(path)
    surf = decode(decoder, latent, n=n, mm_per_unit=mm_per_unit)
    if building:                               # only when building the repository's saved copies
        DECODED.mkdir(parents=True, exist_ok=True)
        surf.decimate(0.7).save(path)         # 30% of the triangles keeps the files small
    return surf


def signed_distance(surface, reference):
    """Per-vertex signed distance (mm) from `surface` to `reference`.

    Positive: `surface` sticks out beyond `reference`. Negative: it sits inside.
    The sign from VTK depends on which way the reference's faces wind, and marching
    cubes can wind them inward, so check against a point known to be outside.
    """
    # Distance from every point of `surface` to the nearest place on `reference`.
    d = np.asarray(surface.compute_implicit_distance(reference)["implicit_distance"])
    # A point far outside the reference must come out positive. If it doesn't, flip every sign.
    outside = np.array(reference.center) + [10 * reference.length, 0, 0]
    probe = pv.PolyData(outside.reshape(1, 3)).compute_implicit_distance(reference)["implicit_distance"][0]
    return d if probe > 0 else -d


def km_curve(days, event, horizon=2922):
    """Kaplan-Meier: returns times (years) and cumulative incidence."""
    days, event = np.asarray(days, float), np.asarray(event, bool)
    event = event & (days <= horizon)   # events after the horizon (8 years) don't count
    days = np.minimum(days, horizon)    # and everyone stops being followed at the horizon
    t = np.sort(np.unique(days[event]))   # each time at which someone had an event
    s, xs, ys = 1.0, [0.0], [0.0]         # s = fraction still event-free
    for ti in t:
        at_risk = (days >= ti).sum()                           # people still being followed at this time
        s *= 1 - ((days == ti) & event).sum() / at_risk        # the share of them who had the event now
        xs.append(ti / 365.25)                                 # days to years
        ys.append(1 - s)                                       # cumulative share with the event
    xs.append(horizon / 365.25)   # carry the curve flat to the end
    ys.append(1 - s)
    return np.array(xs), np.array(ys)


# ---- rendering ----
# Meshes are LPS: +x patient left, +y posterior, +z superior. All latents are right-knee frame.
# Each view is (direction from the knee to the camera, which way is up on screen).
VIEWS = {
    "trochlea": ((0, -0.55, -1.0), (0, -1, 0)),   # from below, tilted toward the front
    "anterior": ((0.0, -1.0, -0.15), (0, 0, 1)),
    "antlat": ((-0.6, -1.0, 0.0), (0, 0, 1)),
    "antmed": ((0.6, -1.0, 0.0), (0, 0, 1)),      # front and inner (medial) side
    "posterior": ((0.0, 1.0, -0.2), (0, 0, 1)),
    "superior": ((0, -0.15, 1.0), (0, -1, 0)),
}


def condyle_axis(femur):
    """Unit vector joining the lowest point of each condyle, so the view can be levelled."""
    p = np.asarray(femur.points)
    # Split the bottom of the femur into its two halves, left and right of the middle.
    mid = np.median(p[p[:, 2] < np.percentile(p[:, 2], 40), 0])
    tips = []
    for side in (p[:, 0] < mid, p[:, 0] >= mid):
        q = p[side]
        tips.append(q[q[:, 2] <= np.percentile(q[:, 2], 2)].mean(0))   # the lowest 2% of points: the condyle tip
    a = tips[1] - tips[0]
    return a / np.linalg.norm(a)


def camera(mesh, view="trochlea", axis=None, zoom=3.5, focus=None):
    """Camera (position, focus, up). With `axis`, the condyles sit level on screen."""
    d0, up0 = (np.array(v, float) for v in VIEWS[view])
    d0 /= np.linalg.norm(d0)
    if axis is not None and view in ("trochlea", "anterior", "posterior", "superior"):
        # Turn the view slightly so the condyle line runs exactly left-right on screen.
        d = d0 - (d0 @ axis) * axis
        d /= np.linalg.norm(d)
        up = np.cross(d, axis)
        if up @ up0 < 0:   # keep "up" pointing the way the view intends
            up = -up
    else:
        d, up = d0, up0
    c = np.array(mesh.center if focus is None else focus, float)   # what the camera looks at
    # Stand back far enough to fit the mesh; bigger zoom means further away.
    return [tuple(c + d * mesh.length * zoom / 2.0), tuple(c), tuple(up)]


def show3d(items, cam, size=(700, 600)):
    """Interactive 3D in the notebook: drag to rotate, scroll to zoom. Same items as render().

    The scene is drawn by your browser, so it works in Colab, Jupyter and VS Code without a display.
    Set OPENMSK_3D=static for a plain picture instead.
    """
    from IPython.display import HTML
    from PIL import Image as PILImage

    pl = pv.Plotter(off_screen=True, window_size=list(size), border=False)
    pl.set_background("white")
    for mesh, kw in items:   # each item is (mesh, drawing options)
        # Matte bone-like lighting, unless the caller asks for something else.
        k = dict(smooth_shading=True, specular=0.15, specular_power=20, ambient=0.28, diffuse=0.72, show_scalar_bar=False)
        k.update(kw)
        if "scalars" not in k and "color" not in k:   # no colouring asked for: draw it bone-coloured
            k["color"] = BONE
        pl.add_mesh(mesh, **k)
    pl.camera_position = cam
    if BACKEND_3D == "static":   # asked for a picture instead
        img = pl.screenshot(return_img=True)
        pl.close()
        return PILImage.fromarray(img)
    try:
        # Write the whole scene into a small web page (vtk.js) that your browser can draw and rotate.
        page = pl.trame.export_html(None).getvalue()
    except Exception as err:  # no browser viewer available: fall back to a picture
        print(f"Interactive view unavailable ({type(err).__name__}), showing a picture instead.")
        img = pl.screenshot(return_img=True)
        pl.close()
        return PILImage.fromarray(img)
    pl.close()
    # Put that page inside the notebook. Quotes must be escaped to sit inside the srcdoc attribute.
    srcdoc = page.replace("&", "&amp;").replace('"', "&quot;")
    return HTML(f'<div><iframe srcdoc="{srcdoc}" width="{size[0]}" height="{size[1]}" style="border:0"></iframe></div>')


def render(items, cam, path=None, size=(1000, 1000), background="white"):
    """items: list of (mesh, kwargs) passed to add_mesh. Returns an RGB array."""
    pl = pv.Plotter(off_screen=True, window_size=list(size), border=False)
    pl.set_background(background)
    pl.enable_anti_aliasing("ssaa")   # smoother edges
    for mesh, kw in items:
        # Same matte lighting as show3d, so pictures and 3D views match.
        k = dict(smooth_shading=True, specular=0.15, specular_power=20, ambient=0.28, diffuse=0.72, show_scalar_bar=False)
        k.update(kw)
        if "scalars" not in k and "color" not in k:
            k["color"] = BONE
        pl.add_mesh(mesh, **k)
    pl.camera_position = cam
    img = pl.screenshot(str(path) if path else None, return_img=True)   # save to `path` if given, and return the picture
    pl.close()
    return img


def diverging_cmap():
    """Blue (sits in) - bone (no difference) - red (sticks out)."""
    from matplotlib.colors import LinearSegmentedColormap

    return LinearSegmentedColormap.from_list("bonediv", ["#2B5C8A", "#8FB3D1", BONE, "#E0937F", "#8C1515"])


def error_cmap():
    """Bone (no error) to red (large error)."""
    from matplotlib.colors import LinearSegmentedColormap

    return LinearSegmentedColormap.from_list("boneerr", [BONE, "#E0937F", "#8C1515"])


def colorbar(path, label, vmin, vmax, cmap, ticks=None, height=3.2):
    """A standalone vertical colour bar, saved as an image."""
    from matplotlib.cm import ScalarMappable
    from matplotlib.colors import Normalize

    fig, ax = plt.subplots(figsize=(1.05, height))
    fig.subplots_adjust(left=0.08, right=0.35, top=0.97, bottom=0.03)
    cb = fig.colorbar(ScalarMappable(Normalize(vmin, vmax), cmap), cax=ax, ticks=ticks)
    cb.set_label(label, color=INK, fontsize=12)
    cb.ax.tick_params(labelsize=11, colors=MUTED, length=0)
    cb.outline.set_visible(False)
    fig.savefig(path, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ---- shape-model intuition ----

def sdf_slice(decoder, latent, plane="sagittal", offset=0.0, n=200, extent=1.0):
    """The signed distance the network predicts on a flat slice through the knee, in model units.

    plane: "sagittal" (side view, fixed x) or "coronal" (front view, fixed y). offset: where the slice sits.
    Returns the two in-plane coordinates and an n x n grid of distances: negative inside the bone, positive outside.
    """
    import torch
    from NSM.mesh.main import get_sdfs

    a = np.linspace(-extent, extent, n)
    u, v = np.meshgrid(a, a)                       # a square grid of points on the slice
    fixed = np.full(u.size, offset)
    if plane == "sagittal":                        # x fixed; y runs front to back, z bottom to top
        pts = np.column_stack([fixed, u.ravel(), v.ravel()])
    else:                                          # y fixed; x runs side to side, z bottom to top
        pts = np.column_stack([u.ravel(), fixed, v.ravel()])
    z = torch.tensor(np.asarray(latent, dtype=np.float32).ravel()).to(decoder.device_name)
    with torch.no_grad():
        # One question to the network per point: "how far is this point from the bone surface?"
        sdf = get_sdfs(decoder, torch.tensor(pts, dtype=torch.float32), z, batch_size=64**3,
                       objects=1, device=decoder.device_name)
    return u, v, sdf.numpy()[:, 0].reshape(n, n)


def morph_viewer(surfaces, reference, clim, label, prefix="", start=None, view="trochlea", axis=None,
                 max_points=12000, height=560):
    """A 3D view with a slider: drag the slider to step through surfaces, drag the bone to rotate it.

    surfaces: {slider label: surface}. Each surface is coloured by its distance (mm) from `reference`.
    Drawn by your browser with plotly, so it works in Colab without a display.
    """
    import plotly.graph_objects as go

    # The same blue - bone - red colours as the other maps, in plotly's format.
    colorscale = [[0, "#2B5C8A"], [0.25, "#8FB3D1"], [0.5, BONE], [0.75, "#E0937F"], [1, "#8C1515"]]

    def trace(surface):
        s = surface.triangulate()
        if s.n_points > max_points:                        # fewer triangles, so the page stays light
            s = s.decimate(1 - max_points / s.n_points)
        d = signed_distance(s, reference)                  # colour: mm in or out from the reference
        tri = s.faces.reshape(-1, 4)[:, 1:]                # each triangle's three corner indices
        p = s.points
        return go.Mesh3d(x=p[:, 0], y=p[:, 1], z=p[:, 2], i=tri[:, 0], j=tri[:, 1], k=tri[:, 2],
                         intensity=d, colorscale=colorscale, cmin=clim[0], cmax=clim[1],
                         colorbar=dict(title=label, len=0.6), hoverinfo="skip", flatshading=False,
                         lighting=dict(ambient=0.45, diffuse=0.75, specular=0.12, roughness=0.8),
                         lightposition=dict(x=100, y=-200, z=-150))

    names = [str(k) for k in surfaces]
    first = names.index(str(start)) if start is not None else len(names) // 2
    # Every surface is its own layer; only one is visible at a time. The slider switches which.
    traces = [trace(s) for s in surfaces.values()]
    for i, t in enumerate(traces):
        t.visible = i == first
    fig = go.Figure(data=traces)
    # Start from the same view as the pictures: camera direction from the knee, and which way is up.
    pos, focus, up = camera(reference, view, axis=axis)
    eye = np.array(pos) - np.array(focus)
    eye = 1.7 * eye / np.linalg.norm(eye)
    fig.update_layout(
        height=height, margin=dict(l=0, r=0, t=10, b=0), paper_bgcolor="white", uirevision="keep",
        scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False, aspectmode="data", uirevision="keep",
                   camera=dict(eye=dict(x=eye[0], y=eye[1], z=eye[2]), up=dict(x=up[0], y=up[1], z=up[2]))),
        # The slider: each step makes one layer visible and hides the rest. Your rotation stays put.
        sliders=[dict(active=first, currentvalue=dict(prefix=prefix), pad=dict(t=10),
                      steps=[dict(label=n, method="restyle", args=[{"visible": [j == i for j in range(len(names))]}])
                             for i, n in enumerate(names)])],
    )
    return fig
