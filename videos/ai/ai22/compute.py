"""Precompute everything numerical in Part 22 of the AI series ("Images, Video and 3D").

    python -m videos.ai.ai22.compute              # everything missing (about 2.5 CPU-hours on one core; resumable)
    python -m videos.ai.ai22.compute denoisers --force
    AI22_THREADS=2 python -m videos.ai.ai22.compute     # torch threads (default 1: on a busy machine 1 is fastest)
    AI22_QUICK=1 python -m videos.ai.ai22.compute       # a smoke test with tiny budgets, into .cache/ai22_quick

Results are cached in ``.cache/ai22/<name>.json`` (+ ``.npz``); the few trained weights other items reuse are kept
beside them (``*.pt``, a few MB).  Every random choice is seeded.  Items made of several trainings save each training
as it finishes (``CACHE.partial``), so an interrupted run resumes where it stopped; items that need another item's
model (the judge, the vision transformer) load or compute it first, so this module alone rebuilds the part.

The pictures are Part 21's 20 x 20 capital letters drawn from the system's fonts (``glyph_images``); the last four
fonts are held out.  Every model is trained here, on one CPU core.

Items (vision.py, latents.py, denoise.py, tokens.py, unified.py, video.py, scene3d.py):
    judge       a small convolutional classifier that reads letters: it scores every generated picture (the letter
                it reads, and a Frechet distance on its 128 features)
    vit         a small vision transformer, replayed: accuracy on unseen fonts, its position vectors becoming a grid,
                where its summary token looks, how far each head looks
    vitcnn      the vision transformer against a convolutional network with as many weights, at equal steps, on 3, 7
                and 20 training fonts, three seeds
    latents     convolutional autoencoders squeezing a letter into 16 to 100 numbers on grids of 1 x 1 to 10 x 10:
                rebuild error against the number of numbers, and flow matching in each latent space
    tsample     uniform against logit-normal training noise levels, three seeds, sampled with 1 to 40 steps
    shift       the resolution shift checked: letters drawn at 20, 40 and 80 pixels, the exact posterior over them
    denoisers   diffusion transformers (adaLN-Zero, adaLN, in-context), a U-Net, and REPA, at equal steps, three seeds
    guidance    classifier-free guidance swept on the adaLN-Zero transformer: right letters, distance, variety
    tokens      two tokenizers (one scale, five scales) and three token generators: raster order, MaskGIT, VAR
    unified     one transformer that names, draws and edits letters (Transfusion's two losses)
    video       the token arithmetic of video models
    vae3d       a causal video autoencoder on clips of a bouncing letter
    clips       video in a frame autoencoder's latents: one clip model against frame-by-frame models trained with
                teacher forcing or diffusion forcing; agreement between frames; rollouts 16 times past the given frames
    nerf        the volume-rendering integral checked; a small NeRF trained on a synthetic scene
    splat       3D Gaussian splatting: the covariance projection against Monte Carlo; splats fitted to the same scene
"""

from __future__ import annotations

from videos.ai.ai22.base import CACHE, compute_judge, compute_video, load  # noqa: F401
from videos.ai.ai22.denoise import compute_denoisers, compute_guidance  # noqa: E402
from videos.ai.ai22.latents import compute_latents, compute_shift, compute_tsample  # noqa: E402
from videos.ai.ai22.scene3d import compute_nerf, compute_splat  # noqa: E402
from videos.ai.ai22.tokens import compute_tokens  # noqa: E402
from videos.ai.ai22.unified import compute_unified  # noqa: E402
from videos.ai.ai22.video import compute_clips, compute_vae3d  # noqa: E402
from videos.ai.ai22.vision import compute_vit, compute_vitcnn  # noqa: E402

ITEMS = {
    "judge": compute_judge,
    "vit": compute_vit,
    "vitcnn": compute_vitcnn,
    "latents": compute_latents,
    "tsample": compute_tsample,
    "shift": compute_shift,
    "denoisers": compute_denoisers,
    "guidance": compute_guidance,
    "tokens": compute_tokens,
    "unified": compute_unified,
    "video": compute_video,
    "vae3d": compute_vae3d,
    "clips": compute_clips,
    "nerf": compute_nerf,
    "splat": compute_splat,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
