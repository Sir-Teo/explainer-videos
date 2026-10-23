"""Scene order for the final cut: (module, Scene class, chapter title)."""

TITLE = "AI, Built: Part 21, Diffusion and Flow"

SCENES = [
    ("s01_hook", "Hook", "From noise"),
    ("s02_forward", "Forward", "1. Destroying data slowly"),
    ("s03_elbo", "ELBO", "2. The bound, and guessing the noise"),
    ("s04_tweedie", "Tweedie", "3. Tweedie's formula"),
    ("s05_dsm", "DSM", "4. Denoising score matching"),
    ("s06_sde", "SDE", "5. Running time backwards"),
    ("s07_samplers", "Samplers", "6. DDPM and DDIM"),
    ("s08_schedules", "Schedules", "7. Noise schedules"),
    ("s09_edm", "EDM", "8. EDM: preconditioning and Heun"),
    ("s10_dpmsolver", "DPMSolver", "9. DPM-Solver: an exact linear part"),
    ("s11_transport", "Transport", "10. Optimal transport and flow matching"),
    ("s12_reflow", "Reflow", "11. Rectified flow and reflow"),
    ("s13_distill", "Distill", "12. Distillation"),
    ("s14_onestep", "OneStep", "13. One step from scratch"),
    ("s15_guidance", "Guidance", "14. Guidance"),
    ("s16_pictures", "Pictures", "15. From points to pictures"),
    ("s17_discrete", "Discrete", "16. Diffusion for discrete data"),
    ("s18_textlm", "TextLM", "17. Diffusion language models"),
    ("s19_outro", "Outro", "Recap, problems, and what comes next"),
]
