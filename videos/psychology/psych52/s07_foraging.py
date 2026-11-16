from __future__ import annotations

from videos.psychology.psych52.common import *  # noqa: F403


class Foraging(VoiceoverScene):
    def construct(self):
        card_section(self, 6, r"Information foraging", r"When should a reader leave a page?")
        self.mvt()
        self.scent()

    def mvt(self):
        d = load("foraging")
        head = heading(r"Charnov's rule, \ for readers")
        tr = 20.0
        k = int(np.where(d["travel"] == 20)[0][0])
        t_star, rate = float(d["leave"][k]), float(d["rate"][k])
        A = axes([-30, 120], [0, 11], x_length=6.0, y_length=3.2, xticks=[-20, 0, 40, 80, 120], yticks=[0, 5, 10],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"seconds (travel to the left of 0)",
                 ylabel=r"useful facts found", center=[-3.2, 0.3, 0], font_size=12)
        g = curve(A.ax, d["tt"], d["gain"], GOOD, stroke_width=4)
        tangent = Line(A.ax.c2p(-tr, 0), A.ax.c2p(120, rate * (120 + tr)), color=PERSON, stroke_width=3)
        dot = Dot(A.ax.c2p(t_star, rate * (t_star + tr)), radius=0.09, color=PERSON)
        rows = rows_of([
            (r"Pirolli and Card, \ 1999: \ people looking for information behave like animals foraging for food", WHITE),
            (r"a page is a patch: \ its useful facts come quickly at first, \ then more slowly", GOOD),
            (rf"the marginal value theorem: \ leave when the page's rate falls to the best overall rate; \ with 20 s "
             rf"of travel, \ after {t_star:.0f} s", PERSON),
            (rf"cheaper travel means shorter stays: \ {d['leave'][0]:.0f} s on a page when the next is 2 s away, \ "
             rf"{d['leave'][-1]:.0f} s when it is 80 s away", MODEL),
        ], 5.8, 19, 0.36).move_to([3.5, -0.1, 0])
        tag = psyche_tag(r"\texttt{work.mvt\_leave}, \ illustrative gain curve")
        with self.voiceover(
            "In 1999 Peter Pirolli and Stuart Card argued that people looking for information behave like animals "
            "foraging for food. <bookmark mark='a'/> It's an idea from behavioural ecology, applied to reading. "
            "<bookmark mark='b'/> A page is a patch. Its useful facts come quickly at first, then more slowly. "
            "<bookmark mark='c'/> Eric Charnov's marginal value theorem says: leave when the page's rate falls to the "
            "best overall rate. Draw the line from the start of the journey that just touches the curve. With twenty "
            "seconds of travel, leave after about half a minute. <bookmark mark='d'/> Cheaper travel means shorter "
            "stays: ten seconds on a page when the next is two seconds away, fifty when it's eighty seconds away. "
            "Fast search engines make readers skim."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(g))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(tangent), FadeIn(dot, scale=1.5))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def scent(self):
        chips_section(self, r"Information scent", [
            (r"scent", r"the cues a link gives about what lies behind it: \ its words, \ its picture, \ its place", GOOD),
            (r"following it", r"users choose the link whose words best match their goal, \ and leave a site when the "
                              r"scent fades", MODEL),
            (r"designing it", r"label links with the words users would use, \ not the organization's own names", PERSON),
            (r"testing it", r"first-click tests: \ if the first click is right, \ the task usually succeeds", SYMP),
        ], "Foragers follow scent. <bookmark mark='a'/> Information scent is what a link tells you about what lies "
           "behind it: its words, its picture, its place on the page. <bookmark mark='b'/> Users choose the link whose "
           "words best match their goal, and they leave a site when the scent fades. <bookmark mark='c'/> So label "
           "links with the words users would use, not the organization's own names for its departments. "
           "<bookmark mark='d'/> And test it with first-click tests. If the first click is right, the task usually "
           "succeeds.")
