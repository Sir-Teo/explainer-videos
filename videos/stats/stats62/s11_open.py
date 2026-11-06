from __future__ import annotations

from videos.stats.stats62.common import *  # noqa: F403


class OpenProblems(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter ten. Open problems at the frontiers of causal inference.", 10, r"Open problems",
                            r"Where identification stops")
        self.map_()
        self.op_unstructured()
        self.op_equilibrium()
        self.op_longterm()
        self.op_discovery()
        self.op_representation()
        self.problems()

    def map_(self):
        hdr = [r"when this fails", r"replace it with", r"and get"]
        body = [
            [r"a blocking set exists", r"the do-calculus, \ the front door", r"identification, \ or a hedge"],
            [r"no hidden confounding", r"a sensitivity model", r"bounds as $\Lambda$ grows"],
            [r"the confounder is measured", r"two proxies", r"proximal identification"],
            [r"no interference", r"an exposure mapping", r"direct and spillover effects"],
            [r"one treatment, \ one time", r"Q-learning, \ the g-formula", r"optimal regimes"],
            [r"a known graph", r"discovery, \ with assumptions", r"an equivalence class"],
            [r"the same population", r"selection diagrams", r"transported effects"],
            [r"a long wait", r"a surrogate index", r"early, \ if surrogacy holds"],
        ]
        cols = [GREY_B, IDC, HIDC, IDC, TRTC, TRTC, HIDC, IDC, GOLDC]
        tab = table_rows([hdr] + body, font_size=24, col_buff=0.7, row_buff=0.25, colors=cols).move_to([0, 0.1, 0])
        if tab.width > 13.4:
            tab.width = 13.4
        with self.voiceover(
            "<bookmark mark='a'/> The part in one table: each textbook assumption, what replaces it when it fails, and what "
            "that buys. <bookmark mark='b'/> The do-calculus and the front door where no blocking set exists. A sensitivity "
            "model where hidden confounding cannot be ruled out. Two proxies for an unmeasured confounder. An exposure "
            "mapping for interference. Q-learning and the g-formula for sequences of decisions. Discovery, up to "
            "equivalence, for an unknown graph. Selection diagrams for a new population. And a surrogate index for a long "
            "wait."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in tab[1:]], lag_ratio=0.6), run_time=20.0)
        self.wait(1.0)
        self.clear_scene()

    def op_unstructured(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Problem one: confounders in text, images and records. <bookmark mark='b'/> A doctor's notes "
            "or a patient's scans may hold the confounding information, but no one knows which features matter. <bookmark "
            "mark='c'/> Adjusting for learned representations, as Victor Veitch and co-authors proposed for text in 2020, "
            "works when the representation keeps every confounding signal, which cannot be checked from data alone. "
            "<bookmark mark='d'/> Valid inference when the adjustment set is learned by a deep model, with honest "
            "uncertainty about what it missed, is open.",
            [(r"\text{problem 1}", r":", r"\text{unstructured confounders}", 40),
             (r"\text{examples}", r":", r"\text{notes, \ scans, \ records}", 40),
             (r"\text{learned adjustment}", r":", r"\text{valid if nothing is lost}", 40),
             (r"\text{open}", r":", r"\text{inference with learned adjustment sets}", 40)],
            [r"high-dimensional and unknown", r"the data exist", r"Veitch, \ Sridhar \& Blei (2020)", r"Part 64"],
            colors=[(3, NAIVEC)])

    def op_equilibrium(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Problem two: interference at scale. <bookmark mark='b'/> A job-training programme that "
            "helps its participants may hurt non-participants competing for the same jobs; a price change ripples through a "
            "market. <bookmark mark='c'/> These general-equilibrium effects are interference with everyone, beyond any "
            "exposure mapping, and experiments at the level of whole markets are rare. <bookmark mark='d'/> Identifying "
            "equilibrium effects from partial experiments and observational networks, with guarantees, is open.",
            [(r"\text{problem 2}", r":", r"\text{general equilibrium}", 40),
             (r"\text{examples}", r":", r"\text{labour markets, \ prices}", 40),
             (r"\text{beyond}", r":", r"\text{any local exposure mapping}", 40),
             (r"\text{open}", r":", r"\text{identification from partial experiments}", 40)],
            [r"interference with everyone", r"displacement effects", r"chapter 4's limit", r"economics' frontier"],
            colors=[(3, NAIVEC)])

    def op_longterm(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Problem three: long-term effects without surrogacy. <bookmark mark='b'/> Chapter nine's "
            "index needs every path through the surrogates, which the surrogate paradox shows can fail silently. <bookmark "
            "mark='c'/> Combining many past experiments, each with both short and long outcomes, to learn which surrogates "
            "can be trusted for which treatments, is a promising route, a kind of meta-learning of surrogacy. <bookmark "
            "mark='d'/> Methods with guarantees that degrade gracefully when surrogacy is only approximate are open.",
            [(r"\text{problem 3}", r":", r"\text{long-term effects}", 40),
             (r"\text{surrogacy}", r":", r"\text{can fail silently}", 40),
             (r"\text{route}", r":", r"\text{learn surrogacy from past experiments}", 40),
             (r"\text{open}", r":", r"\text{graceful guarantees}", 40)],
            [r"beyond the index", r"CAST's lesson", r"meta-analysis of surrogates", r"robustness"],
            colors=[(3, NAIVEC)])

    def op_discovery(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Problem four: discovery with hidden variables, in finite samples. <bookmark mark='b'/> With "
            "latent confounders the output is a still larger class, from the FCI algorithm, and the tests multiply. "
            "<bookmark mark='c'/> Uniform consistency, valid confidence statements for an edge, is impossible under plain "
            "faithfulness, as James Robins and co-authors showed in 2003; strong faithfulness rescues it but is often false. "
            "<bookmark mark='d'/> Honest uncertainty quantification for learned causal graphs is open.",
            [(r"\text{problem 4}", r":", r"\text{discovery with latent variables}", 40),
             (r"\text{FCI}", r":", r"\text{a larger equivalence class}", 40),
             (r"\text{impossibility}", r":", r"\text{no uniform consistency under faithfulness}", 38),
             (r"\text{open}", r":", r"\text{confidence statements for graphs}", 40)],
            [r"Spirtes et al.", r"partial ancestral graphs", r"Robins et al. (2003)", r"chapter 7's caution"],
            colors=[(3, NAIVEC)])

    def op_representation(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Problem five: causal representation learning. <bookmark mark='b'/> Bernhard Schölkopf and "
            "co-authors asked in 2021 whether the causal variables themselves can be learned from raw data such as pixels. "
            "<bookmark mark='c'/> Identifiability results exist with interventions or multiple environments, Part sixty's "
            "invariance, but they need strong assumptions about how the data arose. <bookmark mark='d'/> When learned "
            "variables support valid causal conclusions, and how to test it, is open, and connects to Part sixty-four's "
            "questions about large models.",
            [(r"\text{problem 5}", r":", r"\text{causal representation learning}", 40),
             (r"\text{question}", r":", r"\text{learn the causal variables themselves}", 40),
             (r"\text{known}", r":", r"\text{identifiable with interventions}", 40),
             (r"\text{open}", r":", r"\text{when learned variables are causal}", 40)],
            [r"beyond given variables", r"Sch\"olkopf et al. (2021)", r"Part 60's environments", r"Part 64"],
            colors=[(3, NAIVEC)])

    def problems(self):
        self.list_voiceover(
            "<bookmark mark='a'/> Five open problems. <bookmark mark='b'/> Inference with learned adjustment sets for "
            "unstructured confounders. <bookmark mark='c'/> General-equilibrium effects. <bookmark mark='d'/> Long-term "
            "effects when surrogacy is only approximate. <bookmark mark='e'/> Honest uncertainty for learned graphs. "
            "<bookmark mark='f'/> And when learned representations are causal.",
            [(r"Open problems", S.ACCENT),
             (r"1. \ unstructured confounders and learned adjustment", WHITE),
             (r"2. \ general-equilibrium effects", WHITE),
             (r"3. \ long-term effects beyond surrogacy", WHITE),
             (r"4. \ uncertainty for learned causal graphs", WHITE),
             (r"5. \ causal representation learning", WHITE)],
            buff=0.42, font_size=25, head_size=40)
