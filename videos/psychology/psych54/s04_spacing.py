from __future__ import annotations

from videos.psychology.psych54.common import *  # noqa: F403


class Spacing(VoiceoverScene):
    def construct(self):
        card_section(self, 3, r"Spacing and interleaving", r"Why does mixed practice feel worse and work better?")
        self.ridge()
        self.interleave()

    def ridge(self):
        d = load("ridge")
        head = heading(r"The best gap depends on when you need it")
        A = axes([-2.2, 2.1], [0.2, 1.0], x_length=5.6, y_length=3.0, xticks=[-1, 0, 1, 2], yticks=[0.4, 0.6, 0.8, 1.0],
                 xfmt=lambda v: f"{10 ** v:g}", yfmt=lambda v: f"{100 * v:.0f}\\%", xlabel=r"gap between study sessions "
                 r"(days)", ylabel=r"recall at the test", center=[-3.3, 0.3, 0], font_size=12)
        cols = [SYMP, MODEL, PERSON, AUTH]
        lg = np.log10(d["gaps"])
        cs = VGroup(*[curve(A.ax, lg, d["recall"][i], cols[i], stroke_width=3) for i in range(4)])
        dots = VGroup(*[Dot(A.ax.c2p(float(np.log10(d["best_gap"][i])), float(d["recall"][i].max())), radius=0.07,
                            color=cols[i]) for i in range(4)])
        key = VGroup(*[label(rf"test {int(r)} days later", font_size=12, color=c) for r, c in zip(d["retention"], cols)])
        key.arrange(RIGHT, buff=0.25).next_to(A, UP, buff=0.2)
        rows = rows_of([
            (r"Part 21's ridgeline (Cepeda and colleagues, \ 2008), \ on Psyche's memory: \ study, \ restudy after a "
             r"gap, \ test later", WHITE),
            (rf"for a test a week away, \ the best gap is about {d['best_gap'][0]:g} days; \ a year away, \ "
             rf"{d['best_gap'][-1]:g} days or more", MODEL),
            (r"the cost of too long a gap is small; \ the cost of too short a gap is large", GOOD),
            (r"so plan reviews against the date you need the knowledge, \ not the next quiz", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{memory.spacing\_ridge} (Part 21)")
        with self.voiceover(
            "Part 21 found spacing's ridgeline. Here it is again, as a design rule. <bookmark mark='a'/> Psyche "
            "studies, restudies after a gap, and is tested later. <bookmark mark='b'/> For a test a week away, the "
            "best gap is a couple of days. For a test a year away, it's three months or more. <bookmark mark='c'/> "
            "The cost of too long a gap is small, and the cost of too short a gap is large. <bookmark mark='d'/> So "
            "plan reviews against the date you'll need the knowledge, not the next quiz."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[Create(c) for c in cs], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(dots))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def interleave(self):
        rows_section(self, r"Interleaving", [
            (r"blocked practice: \ ten problems of type A, \ then ten of B; \ interleaved: \ A, \ C, \ B, \ A, \ in a "
             r"mixed order", WHITE),
            (r"Rohrer and Taylor, \ 2007: \ students practising volumes of solids did better during blocked practice, "
             r"\ and much worse a week later than those who interleaved", AUTH),
            (r"interleaving makes the learner choose the method, \ which is what the test (and life) will ask; \ "
             r"blocking tells them", MODEL),
            (r"a classroom trial in mathematics found the benefit at a month's delay (Rohrer and colleagues, \ 2020)",
             GOOD),
            (r"it helps most when the categories are confusable; \ for very different topics the gain is small", YOU),
        ], "Interleaving is spacing's cousin. <bookmark mark='a'/> Blocked practice is ten problems of one type, then "
           "ten of the next. Interleaved practice mixes them. <bookmark mark='b'/> In 2007 Doug Rohrer and Kelli "
           "Taylor found that students practising volumes of solids did better during blocked practice, and much "
           "worse a week later than those who interleaved. <bookmark mark='c'/> Interleaving makes the learner "
           "choose the method, which is what the test, and life, will ask. Blocking tells them. "
           "<bookmark mark='d'/> A classroom trial in mathematics found the benefit a month later. "
           "<bookmark mark='e'/> It helps most when the categories are confusable. For very different topics the "
           "gain is small.", tag=published_tag(r"Rohrer \& Taylor (2007)"))
