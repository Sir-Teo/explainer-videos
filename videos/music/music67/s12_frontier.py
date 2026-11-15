from __future__ import annotations

import numpy as np

from videos.music.music67.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 11, r"Frontier: \ the open problems of this series", r"What did sixty-six parts leave unanswered?")
        self.map_()
        self.samples()
        self.themes()
        self.wrong()
        self.finding()

    # ------------------------------------------------------------------
    def map_(self):
        d = load("stars")
        acts = [r"I", r"II", r"III", r"IV", r"V", r"VI", r"VII", r"VIII", r"IX", r"X", r"XI", r"XII"]
        counts = d["by_act"]
        top = max(counts)
        bars = VGroup()
        for i, (a, c) in enumerate(zip(acts, counts)):
            b = Rectangle(width=0.6, height=max(0.02, 3.0 * c / top), stroke_width=0, fill_color=TUNE, fill_opacity=0.85).move_to([-5.0 + 0.9 * i, -1.6 + 1.5 * c / top, 0])
            bars.add(VGroup(b, label(a, font_size=15, color=GREY_A).next_to(b, DOWN, buff=0.12).set_y(-1.85), label(str(c), font_size=14, color=WHITE).next_to(b, UP, buff=0.08)))
        note = label(rf"{d['count']} research questions, \ one per part where a part posed one as a question, \ read from the parts' notes", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.4)
        head = label(r"the series' open problems, \ by act", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Every part of this series ended with a research problem, marked with a star. Read them all from the parts' notes, "
            f"and {say(d['count'])} are open questions. <bookmark mark='a'/> Here they are by act. The later acts, where the "
            "series reaches the machines, the studio and the mind, pose the most; but every act has its open questions, "
            "including the oldest: sound itself, tuning, harmony."
        ) as vo:
            self.play(FadeIn(head), FadeIn(note))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.1), run_time=2.0)
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def samples(self):
        d = load("stars")
        rng = np.random.default_rng(67)
        pick = sorted(rng.choice(len(d["problems"]), 6, replace=False).tolist())
        rows_ = VGroup(*[label(rf"Part {d['problems'][i][0]}: \ " + d["problems"][i][1].replace("%", r"\%").replace("&", r"\&"), font_size=16, color=WHITE) for i in pick])
        rows_.arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to(DOWN * 0.2)
        for r in rows_:
            if r.width > 13:
                r.scale_to_fit_width(13)
        head = label(r"six of them, \ drawn at random", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Six of them, drawn at random so that none is chosen for being flattering. <bookmark mark='a'/> Each is phrased so "
            "that an answer could be computed, measured or heard, and each has a note in its part saying where to start. They "
            "are the most useful thing this series can leave: work that is not done."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows_], lag_ratio=0.25), run_time=2.4)
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def finding(self):
        items = [
            (r"a good problem is one you can make progress on this year, \ and that would matter if solved", WHITE),
            (r"look where two ways of knowing meet: \ a source question with a computation, \ a corpus with a listening test", WHITE),
            (r"look for a number nobody has measured, \ or a claim measured once \ (the audit of Chapter 8)", WHITE),
            (r"$\bigstar$ \ research problem: \ build a shared, \ open benchmark of verdicts in music research, \ re-run each year", EAR),
            (r"the series' own audit is its first entry", TUNE),
        ]
        rows_scene(self, r"finding a problem", items,
                   "How do you find a problem of your own? <bookmark mark='b'/> A good one is one you can make progress on this year, "
                   "and that would matter if solved. <bookmark mark='c'/> Look where two ways of knowing meet: a question about "
                   "sources with a computation, a corpus with a listening test. <bookmark mark='d'/> Look for a number nobody has "
                   "measured, or a claim measured only once. <bookmark mark='e'/> This part's own research problem: build a shared, "
                   "open benchmark of the verdicts of music research, re-run every year. <bookmark mark='f'/> The audit of Chapter 8 "
                   "is its first entry.", marks="bcdef")

    # ------------------------------------------------------------------
    def themes(self):
        items = [
            (r"perception: \ what listeners hear in tuning, \ timbre, \ rhythm and form, \ measured across cultures", WHITE),
            (r"history and analysis: \ claims about styles, \ tested on corpora that are not only canons", WHITE),
            (r"machines: \ transcription, \ separation and generation that are calibrated, \ and honest about their data", WHITE),
            (r"evaluation: \ metrics that track what listeners value, \ and benchmarks that are re-run", WHITE),
            (r"economics and rights: \ who is paid when music is streamed, \ sampled or learnt from", TUNE),
        ]
        rows_scene(self, r"the problems, \ grouped", items,
                   "Grouped, the open problems fall into five kinds. <bookmark mark='b'/> Perception: what listeners hear in tuning, "
                   "timbre, rhythm and form, measured across cultures. <bookmark mark='c'/> History and analysis: claims about "
                   "styles, tested on corpora that are not only canons. <bookmark mark='d'/> Machines: transcription, separation and "
                   "generation that are calibrated and honest about their data. <bookmark mark='e'/> Evaluation: metrics that track "
                   "what listeners value, and benchmarks that are re-run. <bookmark mark='f'/> And economics and rights: who is "
                   "paid when music is streamed, sampled or learnt from.", marks="bcdef")

    # ------------------------------------------------------------------
    def wrong(self):
        items = [
            (r"its instruments are models: \ a bowed string, \ a piano, \ a voice, \ built from physics and simplified", WHITE),
            (r"its listeners are often simulated, \ with tastes and errors chosen by the series", WHITE),
            (r"its corpora are small: \ Bach's chorales, \ a few dozen tunes, \ its own sixty-seven Variations", WHITE),
            (r"so its findings are about those models and corpora first; \ each says so in its notes, \ and the problems above are where to test them", TUNE),
        ]
        rows_scene(self, r"how this series could be wrong", items,
                   "And how could this series itself be wrong? <bookmark mark='b'/> Its instruments are models, a bowed string, a "
                   "piano, a voice, built from physics and simplified. <bookmark mark='c'/> Its listeners are often simulated, with "
                   "tastes and errors the series chose. <bookmark mark='d'/> Its corpora are small: Bach's chorales, a few dozen "
                   "tunes, its own sixty-seven Variations. <bookmark mark='e'/> So its findings are about those models and corpora "
                   "first. Each part says so in its notes, and the open problems are where to test them on the world.",
                   marks="bcde")
