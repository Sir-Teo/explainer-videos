from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ49.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 14, r"The Dials: \ police, \ class size, \ teachers", r"What do the numbers say?",
             "Chapter fourteen. The Dials: police and crime, class size, and teachers.",
             lit={1997: r"Levitt", 1999: r"Krueger", 2014: r"Chetty et al."}, scale=("city", "person"),
             horizon=("a year",))
        self.police()
        self.classes()
        self.teachers()

    def _show(self, dial, title, lo, hi, ticks, unit, say, marks, fmt="{:.2f}"):
        head = status_head(dial, title)
        frame, rows = dial_rows(dial, lo, hi, ticks, unit, top=2.1, step=0.62, fmt=fmt)
        meaning = wrapped_label(tex_safe(dial.meaning), 11.2, 15, GREY_A).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"explainer.economics.dials, \ checked 2026-11-21", corner=DR, font_size=12)
        with self.voiceover(say) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip(marks, rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("z")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()

    def police(self):
        self._show(dials.DIALS["crime_police"], r"the elasticity of crime to police \ (new)", -7.5, 1.5,
                   [-7, -6, -5, -4, -3, -2, -1, 0, 1], r"percent change in crime per percent more police",
                   "The first dial, new to the course: the elasticity of crime with respect to police. Steven "
                   "Levitt's 1997 estimate for murder, using police hired before elections: minus three, with an "
                   "interval from minus seven to plus one, too wide to say much. <bookmark mark='a'/> William Evans "
                   "and Emily Owens, using federal hiring grants: minus 0.84 for murder, also with a wide interval. "
                   "<bookmark mark='b'/> Draca, Machin and Witt, after the London bombings: minus 0.3 to minus 0.4, "
                   "for crime as a whole. <bookmark mark='z'/> The status: contested. Every design that moves police "
                   "for reasons unrelated to crime finds that more police mean less crime; how much less for the "
                   "rarest and worst crimes is still uncertain.", "ab", fmt="{:.2f}")

    def classes(self):
        S = load("star")
        self._show(dials.DIALS["class_size"], r"the effect of a smaller class \ (new)", -1.0, 9.0,
                   [0, 2, 4, 6, 8], r"percentile points, \ a class of 13--17 against 22--25",
                   "The second: what a class a third smaller does to test scores, in percentile points. Alan "
                   "Krueger, from Tennessee's experiment: about four points in the first year. <bookmark mark='a'/> "
                   f"This film, from the same data, within schools: {S['small']:.1f}, from "
                   f"{S['small'] - 1.96 * S['small_se']:.1f} to {S['small'] + 1.96 * S['small_se']:.1f}. <bookmark "
                   "mark='b'/> Angrist, Lavy and colleagues, with Israel's later data: none. <bookmark mark='z'/> "
                   "The status: contested. The one large experiment found real gains; other designs, on other data, "
                   "range down to nothing.", "ab", fmt="{:.1f}")

    def teachers(self):
        self._show(dials.DIALS["teacher_va"], r"the spread of teachers' effects \ (new)", 0.0, 0.2,
                   [0, 0.05, 0.1, 0.15, 0.2], r"s.d. of scores from a teacher one s.d. better",
                   "The third: how much teachers differ. Chetty, Friedman and Rockoff: a teacher one standard "
                   "deviation better raises scores by 0.14 standard deviations in maths, <bookmark mark='a'/> and "
                   "0.10 in English. <bookmark mark='b'/> Eric Hanushek and Steven Rivkin's survey of the literature: "
                   "about 0.13 in reading. <bookmark mark='z'/> The status: settled within a range. Teachers differ, "
                   "by about a tenth of a standard deviation a year; what to do about it, in hiring, pay and "
                   "dismissal, is the argument.", "ab", fmt="{:.2f}")
