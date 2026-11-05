from __future__ import annotations

from videos.stats.stats20.common import *  # noqa: F403


def step_box(title, sub, color, width=3.0):
    t = label(title, font_size=20, color=color)
    s = label(sub, font_size=15, color=GREY_A)
    for x in (t, s):
        if x.width > width - 0.3:
            x.width = width - 0.3
    body = VGroup(t, s).arrange(DOWN, buff=0.1)
    r = RoundedRectangle(width=width, height=body.height + 0.35, corner_radius=0.1, stroke_color=color, stroke_width=2,
                         fill_color="#11161d", fill_opacity=1)
    return VGroup(r, body.move_to(r))


class Reproducibility(VoiceoverScene):
    def construct(self):
        self.card()
        self.chain()
        self.provenance()
        self.privacy()
        self.ethics()
        self.checklist()

    def card(self):
        card = chapter_card(12, r"Reproducibility and ethics", r"Could someone else get the same answer?", part=PART)
        with self.voiceover("Chapter twelve. Reproducibility, and ethics."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def chain(self):
        d = load("repro")
        boxes = VGroup(
            step_box(r"CDC files", r"six .xpt files, \ public", NH),
            step_box(r"extract", r"\texttt{tools/nhanes\_extract.py}", DES),
            step_box(r"one CSV", rf"{d['rows']:,} rows, \ {d['cols']} columns", NH),
            step_box(r"the pipeline", r"\texttt{pipeline.py}: \ clean, \ fit", SALT),
            step_box(r"compute", r"\texttt{compute.py}: \ every number, \ seeded", SALT),
            step_box(r"cache", r"JSON, \ one file per result", GREY_A),
            step_box(r"scenes \& report", r"read the cache; \ compute nothing", HIT),
        )
        top = VGroup(*boxes[:4]).arrange(RIGHT, buff=0.45)
        bot = VGroup(boxes[6], boxes[5], boxes[4]).arrange(RIGHT, buff=0.45)  # the chain turns back, right to left
        VGroup(top, bot).arrange(DOWN, buff=1.0).move_to([0, 0.6, 0])
        bot.align_to(top, RIGHT)
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.05, stroke_width=3, color=GREY_B) for i in (0, 1, 2)],
                        Arrow(boxes[3].get_bottom(), boxes[4].get_top(), buff=0.05, stroke_width=3, color=GREY_B),
                        *[Arrow(boxes[i].get_left(), boxes[i + 1].get_right(), buff=0.05, stroke_width=3, color=GREY_B) for i in (4, 5)])
        foot = label(r"\texttt{python -m videos.stats.stats20.compute}: \ one command reruns everything", font_size=22,
                     color=OBS).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "<bookmark mark='a'/> Here is the chain from the CDC's files to every number in this part. Six public files, "
            "downloaded unchanged. <bookmark mark='b'/> A short extraction script that keeps the columns we use and renames "
            "them, nothing more. <bookmark mark='c'/> One CSV file. <bookmark mark='d'/> The pipeline, where every decision "
            "of chapters three to eight lives, as code. <bookmark mark='e'/> A compute script that produces every number, with "
            "fixed random seeds for the bootstrap and the World. <bookmark mark='f'/> Its results, cached. <bookmark mark='g'/> "
            "And the scenes and the report, which only read the cache. No number on screen was typed by hand, and one command "
            "reruns it all."
        ) as vo:
            for k, m_ in enumerate("abcdefg"):
                vo.wait_until(m_)
                anims = [FadeIn(boxes[k], shift=UP * 0.1)]
                if k > 0:
                    anims.append(GrowArrow(arrows[k - 1]))
                self.play(*anims)
            self.play(FadeIn(foot))
        self.wait(1.0)
        self.clear_scene()

    def provenance(self):
        d = load("repro")
        h = d["sha256"]
        rows = [
            cmath(r"\text{source}", r":", r"\text{NHANES 2017--2018, \ CDC / NCHS, \ public domain}", font_size=26),
            cmath(r"\text{fingerprint}", r":", rf"\texttt{{sha256 {h[:16]}\dots}}", font_size=26),
            cmath(r"\text{seeds}", r":", r"\text{the World 1662; \ bootstrap 1988; \ surveys 1--200}", font_size=26),
            cmath(r"\text{versions}", r":", r"\text{the code, \ in git; \ the packages, \ pinned}", font_size=26),
        ]
        rows[1][2].set_color(OBS)
        whys = [why(r"where the data came from"), why(r"any change to the file changes it"),
                why(r"random, \ but repeatable"), why(r"which code produced which number")]
        with self.voiceover(
            "Reproducibility needs four things recorded. <bookmark mark='a'/> Where the data came from. <bookmark mark='b'/> "
            "A fingerprint of the exact file: a SHA-256 hash, which changes if a single digit changes, so a reader can confirm "
            "they have the same data. <bookmark mark='c'/> The random seeds, so that even the bootstrap and the simulations "
            "come out identically. <bookmark mark='d'/> And the versions of the code and the packages. Without these, a "
            "result can't be checked, only believed."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def privacy(self):
        d = load("repro")
        rows = [
            cmath(r"\text{locations}", r":", rf"\text{{{d['psus_masked']} masked PSUs, \ no counties}}", font_size=28),
            cmath(r"\text{age}", r":", rf"\text{{top-coded at 80 \ ({d['age80']} adults)}}", font_size=28),
            cmath(r"\text{income ratio}", r":", rf"\text{{top-coded at 5 \ ({d['pir5']} people)}}", font_size=28),
            cmath(r"\text{finer data}", r":", r"\text{only in secure Research Data Centers}", font_size=28),
            cmath(r"\text{consent}", r":", r"\text{informed, \ reviewed by an ethics board}", font_size=28),
        ]
        whys = [why(r"chapter two"), why(r"a 97-year-old in a small town is findable"), why(r"so are the very rich"),
                why(r"by application, \ with oversight"), why(r"the people behind the rows")]
        with self.voiceover(
            "Public data must protect the people in it. NHANES does it in layers. <bookmark mark='a'/> No locations: only "
            "thirty masked PSUs. <bookmark mark='b'/> Age is top-coded at eighty, because a ninety-seven-year-old in a small "
            "county could be identified. <bookmark mark='c'/> The ratio of income to the poverty line is top-coded at five, for "
            "the same reason at the other end. <bookmark mark='d'/> Finer data exist, but only inside secure research centres, "
            "by application. <bookmark mark='e'/> And every participant gave informed consent to a protocol approved by an "
            "ethics review board. Part 63 will show how statistics itself can guarantee privacy."
        ) as vo:
            step = ladder(self, rows, whys, keep=5, top=2.8, x=-0.6, buff=0.62, edge=6.9)
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def ethics(self):
        rows = fit_rows(VGroup(
            label(r"race and ethnicity: \ social categories, \ reported with care, \ not biology", font_size=22, color=GREY_A),
            label(r"a null result deserves publication as much as a positive one", font_size=22, color=HIT),
            label(r"funding and interests: \ salt has an industry, \ and so does advice", font_size=22, color=OBS),
            label(r"consequences: \ a careless headline can change what millions eat", font_size=22, color=RES),
            label(r"the analyst's duty: \ say what the data show, \ and no more", font_size=24, color=SALT),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "And the ethics of the analysis itself. <bookmark mark='a'/> NHANES records race and ethnicity, and differences "
            "between groups are real, but they reflect social and environmental conditions; reporting them as biology causes "
            "harm. <bookmark mark='b'/> A null result like ours deserves to be published as much as a positive one, or the "
            "literature fills with flukes. <bookmark mark='c'/> Salt has an industry, and nutritional advice has its "
            "champions; who paid for a study should always be stated. <bookmark mark='d'/> A headline that says salt is "
            "harmless could change what millions of people eat. <bookmark mark='e'/> The analyst's duty is to say what the "
            "data show, as precisely as they show it, and no more."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def checklist(self):
        items = [r"question $\to$ estimand, \ in writing", r"design and weights understood", r"cleaning in code, \ logged",
                 r"exploration before modelling", r"a plan fixed before results", r"checks that could change the answer",
                 r"uncertainty from the design", r"sensitivity: \ every fork shown", r"measurement error faced",
                 r"causal claims only with a design for them", r"the pipeline checked where the truth is known",
                 r"one honest page", r"reproducible, \ private, \ fair"]
        rows = VGroup(*[label(rf"$\checkmark$ \ {t}", font_size=22, color=HIT if i % 2 == 0 else WHITE) for i, t in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.34),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.34)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        head = label(r"An analysis, \ in thirteen checks", font_size=34).to_edge(UP, buff=0.5)
        cols.next_to(head, DOWN, buff=0.5)
        if cols.width > 13:
            cols.width = 13
        with self.voiceover(
            "<bookmark mark='a'/> Here is the whole capstone as a checklist of thirteen items, one per chapter: from the "
            "estimand to the design, cleaning, exploration, the plan and its checks, uncertainty, sensitivity, measurement, "
            "causation, the World, the page, and reproducibility. Every analysis you do from now on can be held against it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.4), run_time=12.0)
        self.wait(2.0)
        self.clear_scene()
