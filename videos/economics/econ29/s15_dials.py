from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ29.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dials: \ the Frisch elasticity", r"How much do people change their hours when the wage "
             r"changes for a while?", "Chapter thirteen. The Dials: the Frisch elasticity.",
             lit={1985: r"Hansen", 2011: r"Chetty and coauthors"}, scale=("person", "nation"),
             horizon=("a year",))
        self.frisch()
        self.why()

    def frisch(self):
        dial = dials.DIALS["frisch"]
        F = load("frisch")
        head = status_head(dial, r"the Frisch elasticity of labour supply \ (new)")
        frame, rows = dial_rows(dial, 0.0, 3.0, [0, 0.5, 1, 1.5, 2, 2.5, 3], r"\% change in hours per 1\% change "
                                r"in a temporary wage", top=2.0, step=0.62, fmt="{:.2f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 12.0, 17, GREY_A).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"Chetty, \ Guren, \ Manoli and Weber, \ \emph{AER} 101(3) (2011); \ this film",
                            corner=DR, font_size=12)
        with self.voiceover(
            "This part's new dial is the Frisch elasticity: how much people change their hours when the wage "
            "changes for a while. Raj Chetty, Adam Guren, Day Manoli and Andrea Weber gathered the evidence in "
            "2011. <bookmark mark='a'/> For people who already work, changing how many hours they work: about "
            "point five four. <bookmark mark='b'/> For the decision whether to work at all: about point two eight. "
            "<bookmark mark='c'/> The two margins together, for hours in the whole economy: about point eight two. "
            "<bookmark mark='d'/> Against that, the value typical in macroeconomic models, as the same review "
            "reports it: about two point eight four. <bookmark mark='e'/> And this film's number: to make the "
            "Island's hours even half as volatile as its output, the elasticity must be about "
            f"{F['half']:.1f}. <bookmark mark='f'/> The status: contested. Part of the gap closes by counting "
            "people who move in and out of work, and part remains. It decides whether a recession can be read as "
            "people choosing more leisure."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("f")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()

    def why(self):
        rows = VGroup(
            label(r"why the two numbers can differ", font_size=27, color=E.ACCENT),
            label(r"micro studies watch people whose wages change for a reason they can see, \ and for a while",
                  font_size=21, color=CONS),
            label(r"in an economy, \ most of the movement in hours is people starting and losing jobs",
                  font_size=21, color=HOURS),
            label(r"Rogerson and Hansen: \ jobs in shifts make the economy's elasticity far larger than anyone's",
                  font_size=21, color=OUTPUT),
            label(r"but people who lose jobs in a recession say they did not choose to: \ unemployment is not "
                  r"leisure", font_size=21, color=HOLD),
            label(r"which is why Parts 24 and 30 put frictions in the labour market", font_size=21,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Rogerson (1988); \ Hansen (1985); \ Chetty et al.\ (2011)", corner=DR, font_size=12)
        with self.voiceover(
            "Why can the two numbers differ so much? <bookmark mark='a'/> Studies of individuals watch people "
            "whose wages change for a reason they can see, for a while, and measure how their hours respond. "
            "<bookmark mark='b'/> But in a whole economy, most of the movement in hours is people starting and "
            "losing jobs. <bookmark mark='c'/> Rogerson and Hansen showed that when jobs come in shifts, the "
            "economy's elasticity can be far larger than any single person's. <bookmark mark='d'/> The trouble is "
            "that people who lose their jobs in a recession say they did not choose to: unemployment is not leisure "
            "taken because wages fell for a while. <bookmark mark='e'/> That is why the parts on search and on "
            "sticky prices put frictions into the labour market instead."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
