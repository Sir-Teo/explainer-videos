from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant29.common import FORMULA, HURDLE, PART


class HighFlyer(VoiceoverScene):
    def construct(self):
        self.card()
        self.story()
        self.fireflyer()
        self.meaning()
        self.question()

    def card(self):
        c = chapter_card(11, r"From a quant fund to DeepSeek", r"What does an alpha factory have in common with a "
                         r"language-model lab?", part=PART)
        with self.voiceover('Chapter eleven. Technical papers connect High-Flyer Quant and DeepSeek through computing infrastructure. What does a quantitative-research pipeline have in common with a language-model lab, and where does the analogy stop?'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def story(self):
        steps = [(r"2021", r"Fire-Flyer's paper dates construction of its PCIe-A100 system to 2021"),
                 (r"Aug. 2024", r"Fire-Flyer AI-HPC version 1 describes hardware/software co-design and acknowledges DeepSeek-AI and High-Flyer Quant"),
                 (r"Dec. 2024", r"DeepSeek-V3 version 1 reports 2.788 million H800 GPU hours for official training"),
                 (r"\text{interpretation}", r"shared infrastructure and engineering experience are a connection, not proof of a causal fund-to-model efficiency advantage")]
        rows = VGroup(*[VGroup(label(a, font_size=20, color=HURDLE), wrapped_label(b, 9.2, 19, GREY_A)).arrange(RIGHT, buff=0.4, aligned_edge=UP) for a,b in steps]).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        rows.move_to(ORIGIN)
        with self.voiceover("Use the versioned technical record. <bookmark mark='a'/> Fire-Flyer's paper dates construction of its PCIe-A100 system to2021. <bookmark mark='b'/> Its August2024 version acknowledges contributors at both DeepSeek-AI and High-Flyer Quant and describes hardware-software co-design. <bookmark mark='c'/> DeepSeek-V3's December2024 version reports2.788million H800 GPU hours for official training. At an assumed two dollars per GPU hour, that is5.576million dollars. <bookmark mark='d'/> The report excludes prior research and ablation experiments on architecture, algorithms and data. This is not total project investment, an R1 cost estimate or a vendor-normalised comparison of identical models. The connection between the organisations does not itself establish a causal efficiency advantage.") as vo:
            for k,mk in enumerate(("a","b","c","d")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(rows[k], shift=RIGHT*0.2))
        self.wait(0.4)
        self.clear_scene()

    def fireflyer(self):
        card = firm_card(r"Fire-Flyer 2 (DeepSeek-AI, 2024)", "`Fire-Flyer AI-HPC: a cost-effective software-hardware co-design for deep learning', version 1 describes a deep-learning cluster architecture, with its own communication library and distributed file system",
                         numbers=((r"10{,}000", r"PCIe A100 graphics processors, as the authors report"),
                                  (r"\tfrac12", r"about half the cost of comparable DGX systems and 40\% less energy, for "
                                                 r"similar performance, as reported")),
                         source=r"arXiv 2408.14158v1, August 2024; author-reported systems comparison", kind=r"Paper file", width=10.6, font_size=22).move_to(ORIGIN)
        with self.voiceover(
            "The August2024 version1 report describes Fire-Flyer2. <bookmark mark='a'/> Its ten thousand PCIe-A100 processors use custom communication and storage engineering. These are the authors' system specifications. <bookmark mark='b'/> They report DGX-A100-like performance at about half the cost and forty percent less energy in their stated comparison. Hardware, workloads, accounting boundaries and measurement methods matter. This is a reported systems comparison, not our independent benchmark or proof that a trading strategy, language model or business has a universal cost advantage."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Indicate(card.submobjects[-1], color=QC.FIRM, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    def meaning(self):
        cards = VGroup(
            desk_question(r"the same machine", 'an alpha factory is a pipeline: data, compute, a search, specified, audited evaluation, and a library that grows. So is a model lab', width=12.4, font_size=19),
            desk_question(r"the same scarcity", 'data, compute, hypotheses and evaluation matter; their relative scarcity depends on the task', width=12.4, font_size=19),
            desk_question(r"a different market", 'adoption can affect signal rents and model applications differently; neither durable value nor decay is universal', width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "There is a useful engineering analogy. <bookmark mark='a'/> Both a quant research pipeline and a model lab organise data, compute, experiments and evaluation; neither evaluation is impossible to fool. <bookmark mark='b'/> Clean data, scientific judgement, infrastructure and well-specified objectives all matter. Their relative scarcity depends on the task. <bookmark mark='c'/> Sharing a model can improve access and applications while changing its commercial value; model quality can still become obsolete. Trading-signal adoption can reduce an edge in some models, but decay is not universal. These are different economic mechanisms, not a theorem that published models retain value forever while trading signals always disappear."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"why might a fund that trades on machine-learned signals give away its best language model, "
                       r"but never its best signal?")
        with self.voiceover(
            "Pause and predict. Why might a fund that trades on machine-learned signals give away its best language "
            "model, but never its best signal?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
