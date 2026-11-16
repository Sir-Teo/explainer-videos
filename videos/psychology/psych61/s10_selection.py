from __future__ import annotations

from videos.psychology.psych61.common import *  # noqa: F403


class Selection(VoiceoverScene):
    def construct(self):
        card_section(self, 9, r"The natural selection of bad science", r"What do incentives do to methods?",
                     scale=("society",))
        self.model()
        self.run()

    def model(self):
        rows_section(self, r"Laboratories as organisms", [
            (r"Smaldino and McElreath, \ 2016: \ labs differ in effort: \ more care means fewer false positives "
             r"and fewer studies", WHITE),
            (r"only positive results are published; \ labs with more publications are copied, \ by students and "
             r"by hiring", MODEL),
            (r"no one cheats: \ every lab is honest; \ selection does the work", AUTH),
            (r"their review of power in the literature: \ no improvement over six decades", PERSON),
        ], "What do incentives do to methods? <bookmark mark='a'/> In 2016 Paul Smaldino and Richard McElreath "
           "modelled laboratories that differ in effort. More care means fewer false positives, and also fewer "
           "studies. <bookmark mark='b'/> Only positive results are published, and labs with more publications are "
           "copied, by their students and by hiring. <bookmark mark='c'/> No one cheats. Every lab is honest, and "
           "selection does the work. <bookmark mark='d'/> Their review of statistical power in the literature found "
           "no improvement over six decades.", tag=published_tag(r"Smaldino \& McElreath (2016)"))

    def run(self):
        d = load("science")
        head = heading(r"Two hundred generations, \ two rules")
        g = np.arange(1, len(d["pos_fdr"]) + 1)
        A1 = axes([0, 200], [0, 100], x_length=4.4, y_length=2.2, xticks=[0, 100, 200], yticks=[0, 50, 100],
                  xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", ylabel=r"mean effort",
                  center=[-4.0, 1.5, 0], font_size=11)
        A2 = axes([0, 200], [0, 1.0], x_length=4.4, y_length=2.2, xticks=[0, 100, 200], yticks=[0, 0.5, 1.0],
                  xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"generations",
                  ylabel=r"false share of positives", center=[-4.0, -1.5, 0], font_size=11)
        e1 = curve(A1.ax, g, d["pos_effort"], AUTH, stroke_width=3)
        e2 = curve(A1.ax, g, d["reg_effort"], GOOD, stroke_width=3)
        sm = lambda v: np.convolve(v, np.ones(9) / 9, mode="same")
        f1 = curve(A2.ax, g[4:-4], sm(d["pos_fdr"])[4:-4], AUTH, stroke_width=3)
        f2 = curve(A2.ax, g[4:-4], sm(d["reg_fdr"])[4:-4], GOOD, stroke_width=3)
        pos_end, reg_end = float(np.mean(d["pos_fdr"][-20:])), float(np.mean(d["reg_fdr"][-20:]))
        rows = rows_of([
            (r"Psyche's 100 labs; \ one true hypothesis in ten; \ power 0.8", WHITE),
            (rf"publish only positives, \ copy the most published: \ effort collapses, \ and {100 * pos_end:.0f}\% of "
             rf"published positives are false: \ your fourth number", AUTH),
            (rf"registered reports: \ methods reviewed before results, \ every result published: \ effort holds, \ "
             rf"and {100 * reg_end:.0f}\% are false (one hypothesis in ten is true, \ so some are)", GOOD),
            (r"change what is selected, \ and the methods follow; \ exhortation alone does not", YOU),
        ], 6.4, 18, 0.34).move_to([3.0, -0.1, 0])
        tag = psyche_tag(r"\texttt{community.bad\_science}")
        with self.voiceover(
            "Here's the model run. <bookmark mark='a'/> Psyche has a hundred labs. One hypothesis in ten is true, and "
            "power is zero point eight. <bookmark mark='b'/> Publish only positive results, and copy the most "
            "published labs. Effort collapses, and eighty-eight percent of the published positive results are false. "
            "That's your fourth number. <bookmark mark='c'/> Now registered reports: methods are reviewed before the "
            "results exist, and every result is published. Effort holds, and the false share is about two in five. "
            "Only one hypothesis in ten is true, so some false positives remain. <bookmark mark='d'/> Change what is "
            "selected, and the methods follow. Exhortation alone doesn't do it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A1), FadeIn(A2))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(e1), Create(f1), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(e2), Create(f2), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
