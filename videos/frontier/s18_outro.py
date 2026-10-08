from __future__ import annotations

import json

import numpy as np

from explainer import *  # noqa: F403
from videos.frontier.common import label, load, note, pipeline_map, pocket_total_flops, sci, source


class Outro(VoiceoverScene):
    def construct(self):
        self.evals()
        self.whole_pipeline()
        self.ledger()
        self.closing()

    # ------------------------------------------------------------------
    def evals(self):
        cols = VGroup(
            VGroup(label(r"\textbf{capabilities}", font_size=30, color=C.REWARD),
                   label(r"GPQA Diamond (science)", font_size=24), label(r"Humanity's Last Exam", font_size=24),
                   label(r"HMMT 2026 (math)", font_size=24), label(r"SWE-bench Pro, Terminal-Bench (agents)", font_size=24)),
            VGroup(label(r"\textbf{safety}", font_size=30, color=C.PENALTY),
                   label(r"red-teaming", font_size=24), label(r"dangerous-capability tests", font_size=24),
                   label(r"refusals and over-refusals", font_size=24), label(r"$\rightarrow$ a published system card", font_size=24)),
        )
        for c in cols:
            c.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        cols.arrange(RIGHT, buff=1.5, aligned_edge=UP).move_to(UP * 0.4)
        head = label(r"Before release: evaluation", font_size=38).to_edge(UP, buff=0.5)
        warn = label(r"Benchmarks saturate and leak: in Feb 2026 OpenAI stopped reporting SWE-bench Verified (contamination)",
                     font_size=24, color=GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Before release, the model is evaluated: on hard benchmarks in science, math and coding, on long agentic "
            "tasks, <bookmark mark='s'/> and on safety tests, all written up in a system card. <bookmark mark='w'/> "
            "Benchmarks are a moving target: they saturate, and they leak into training data. In February 2026, "
            "OpenAI stopped reporting the popular SWE-bench Verified because of contamination."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cols[0], lag_ratio=0.15))
            vo.wait_until("s")
            self.play(FadeIn(cols[1], lag_ratio=0.15))
            vo.wait_until("w")
            self.play(FadeIn(warn))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def whole_pipeline(self):
        m = pipeline_map(width=13.4).move_to(UP * 1.6)
        notes = [
            r"$\sim$2 billion pages\\per monthly crawl",
            r"13\% of pages survive;\\15--36T tokens",
            r"$10^{25}$--$10^{27}$ FLOPs;\\sparse MoE, Muon,\\FP8 / FP4",
            r"$10^4$--$10^5$ GPUs;\\4 kinds of parallelism;\\failures every few hours",
            r"SFT, preferences,\\RL with verifiers\\and tools",
            r"evaluated,\\then released",
        ]
        subs = VGroup(*[note(t, font_size=21, color=GREY_A).next_to(g.text, DOWN, buff=0.25) for t, g in zip(notes, m.stages)])
        keys = ["w", "d", "p", "g", "r", "a"]
        with self.voiceover(
            "So here is the whole pipeline. <bookmark mark='w'/> Billions of crawled pages, <bookmark mark='d'/> "
            "filtered and deduplicated down to tens of trillions of tokens. <bookmark mark='p'/> A recipe chosen with "
            "scaling laws, today usually a sparse mixture of experts, trained with Muon or AdamW in eight- or even "
            "four-bit arithmetic. <bookmark mark='g'/> Tens of thousands of GPUs, coordinated by four kinds of "
            "parallelism, and kept alive through failures every few hours. <bookmark mark='r'/> Then fine-tuning, "
            "preferences and reinforcement learning, which now takes a substantial share of the compute. "
            "<bookmark mark='a'/> And finally, the assistant."
        ) as vo:
            for i, k in enumerate(keys):
                vo.wait_until(k)
                anims = [FadeIn(m.stages[i], shift=UP * 0.15), FadeIn(subs[i])]
                if i:
                    anims.append(GrowArrow(m.arrows[i - 1]))
                self.play(*anims, run_time=0.8)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger(self):
        from videos.frontier.compute import RUN_DIR

        pocket = pocket_total_flops()
        biggest = max(json.loads(f.read_text())["counts"]["total"] for f in RUN_DIR.glob("*.json"))
        most_tokens = max(json.loads(f.read_text())["run"]["tokens"] for f in RUN_DIR.glob("*.json"))
        assert 1e14 < pocket < 1e15 and 2.5e6 < biggest < 3.5e6
        rows = [
            (r"largest model", rf"{biggest / 1e6:.1f} million parameters", r"up to 2.8 trillion (Kimi K3)"),
            (r"tokens in one run", rf"{most_tokens / 1e6:.0f} million", r"33 trillion (DeepSeek-V4)"),
            (r"all training compute", rf"${sci(pocket)}$ FLOPs", r"$\sim 10^{27}$ FLOPs (largest estimate)"),
            (r"hardware", r"4 CPU cores", r"100{,}000+ GPUs"),
        ]
        hdr = VGroup(label(r"", font_size=28), label(r"this video", font_size=30, color=C.KEPT),
                     label(r"the frontier, 2026", font_size=30, color=C.COMPUTE))
        table = VGroup(hdr)
        for a, b, c in rows:
            table.add(VGroup(label(a, font_size=26, color=GREY_A), label(b, font_size=26), label(c, font_size=26)))
        xs = [-4.4, -0.4, 4.0]
        for i, r in enumerate(table):
            for j, cell in enumerate(r):
                cell.move_to([xs[j], 2.0 - i * 0.85, 0])
        line = Line([-6.3, 1.6, 0], [6.3, 1.6, 0], color=GREY_D)
        head = label(r"Pocket scale vs.\ frontier scale", font_size=36).to_edge(UP, buff=0.4)
        src = source(r"Kimi K3 (Moonshot AI, Jul 2026); DeepSeek-V4 (Apr 2026); Epoch AI; OpenAI (GPT-6 Astra, Sep 2026)")
        with self.voiceover(
            "And our pocket versions? The largest model we trained had about three million parameters, against up "
            "to 2.8 trillion at the frontier. All of our training runs together took less than ten to the fifteen "
            "operations; the largest frontier run is estimated at around ten to the twenty-seven. Four CPU cores, "
            "against a hundred thousand GPUs. Yet the curves have the same shapes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(hdr), Create(line))
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in table[1:]], lag_ratio=0.3), run_time=2.5)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def closing(self):
        lines = VGroup(
            label(r"Most of what is known comes from open-weight labs' reports:", font_size=30),
            label(r"the leading closed labs publish very little about how they train.", font_size=30, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.8)
        opens = VGroup(
            label(r"\textbf{OLMo 3} (Ai2): every dataset, checkpoint and line of training code", font_size=28),
            label(r"\textbf{nanochat} (Karpathy): a GPT-2-grade chat model for under \$100", font_size=28),
            label(r"\textbf{The Smol Training Playbook}, \textbf{The Ultra-Scale Playbook} (Hugging Face)", font_size=28),
            label(r"\textbf{datatrove}, \textbf{torchtitan}, \textbf{Megatron}, \textbf{verl}, \textbf{TRL}: the tools themselves", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 0.5)
        with self.voiceover(
            "Almost everything in this video comes from open-weight labs and open-source projects; the leading "
            "closed labs publish very little about how their models are trained. But the shape of the pipeline has "
            "been stable for years: get the data right, choose the size with scaling laws, keep the run stable across "
            "thousands of machines, and then teach the model with feedback. <bookmark mark='o'/> And more of it is "
            "open than ever. AI2's OLMo 3 releases every dataset and checkpoint; nanochat trains a GPT-2-grade chat "
            "model for under a hundred dollars; Hugging Face's playbooks write down the hard-won lessons. If you want "
            "to know how these models are made, you can run the whole thing yourself, at whatever scale you have."
        ) as vo:
            self.play(FadeIn(lines))
            vo.wait_until("o")
            self.play(LaggedStart(*[FadeIn(o, shift=RIGHT * 0.2) for o in opens], lag_ratio=0.3), run_time=2.5)
        self.wait(1.0)
        self.clear_scene()
        card = VGroup(
            label(r"How Frontier AI Models Are Trained", font_size=56),
            label(r"every chart: a real run, on a 4-core CPU", font_size=30, color=GREY_A),
            label(r"sources and code: \texttt{videos/frontier}", font_size=26, color=GREY_B),
        ).arrange(DOWN, buff=0.35)
        self.play(FadeIn(card, scale=1.05), run_time=1.2)
        self.wait(3.0)
        self.play(FadeOut(card))
