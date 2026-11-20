from __future__ import annotations

from videos.economics.econ39.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ transparency and algorithms", r"What is still unsettled?",
             "Chapter fifteen. Frontier: transparency and algorithms.",
             lit={2018: r"Amazon's r\'esum\'e screen", 2023: r"Cullen and Pakzad-Hurson"}, scale=("firm",),
             horizon=("a year",))
        self.transparency()
        self.algorithms()
        self.questions()

    def transparency(self):
        F = tables.FRONTIER39.data
        steps = flow_chain([(r"a law: \ pay \\ must be disclosed", E.ACCENT), (r"workers see \\ each other's pay",
                                                                                  WORKER),
                            (r"a raise for one \\ invites demands \\ from all", LOSS),
                            (rf"average wages \\ {F['transparency']}\%", WAGE)],
                           notes=[r"US states, \\ various forms", r"gaps between \\ coworkers shrink",
                                  r"so the employer \\ refuses raises \\ more firmly", r"least where workers \\ had "
                                  r"little power anyway"], box_w=2.8, font_size=19, note_size=15).move_to(UP * 0.6)
        foot = label(r"equal pay, \ lower pay: \ transparency compresses wages \ partly by lowering the top",
                     font_size=20, color=E.ACCENT).to_edge(DOWN, buff=0.9)
        tag = published_tag(r"Cullen and Pakzad-Hurson, \ \emph{Econometrica} 91(3) (2023)", corner=DR, font_size=12)
        with self.voiceover(
            "The frontier begins with transparency. Many governments now require employers to disclose pay, to "
            "narrow unfair gaps. <bookmark mark='a'/> In 2023 Zoë Cullen and Bobak Pakzad-Hurson studied what "
            "happens. <bookmark mark='b'/> When workers can see each other's pay, <bookmark mark='c'/> a raise for "
            "one worker invites demands from the rest, so employers hold the line more firmly against everyone. "
            "<bookmark mark='d'/> In American states' transparency laws, average wages fell by about two percent, "
            "least where workers had little bargaining power to begin with. Transparency does narrow gaps between "
            "coworkers, partly by lowering the top."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(steps.boxes[0]), FadeIn(steps.notes[0]))
            vo.wait_until("a")
            self.play(Indicate(steps.boxes[0], color=WHITE, scale_factor=1.03))
            vo.wait_until("b")
            self.play(GrowArrow(steps.arrows[0]), FadeIn(steps.boxes[1]), FadeIn(steps.notes[1]))
            vo.wait_until("c")
            self.play(GrowArrow(steps.arrows[1]), FadeIn(steps.boxes[2]), FadeIn(steps.notes[2]))
            vo.wait_until("d")
            self.play(GrowArrow(steps.arrows[2]), FadeIn(steps.boxes[3]), FadeIn(steps.notes[3]), FadeIn(foot))
        self.clear_scene()

    def algorithms(self):
        hc = history_card(2018, r"Amazon's experimental r\'esum\'e screen", r"trained on ten years of r\'esum\'es, "
                          r"mostly from men, \ it learned to mark down applications containing the word `women's', "
                          r"\ and was dropped", color=LOSS, width=11.0, font_size=24).move_to(UP * 1.6)
        pts = point_cards([
            (r"a model learns \\ the past", r"if past hiring \\ discriminated, \\ so will the model", LOSS),
            (r"but it can \\ be audited", r"send it r\'esum\'es \\ that differ only \\ in the name", GAIN),
            (r"the same method", r"Bertrand and \\ Mullainathan's \\ design, run on \\ a machine", E.ACCENT),
        ], width=11.4, cols=3, font_size=19).move_to(DOWN * 1.3)
        tag = published_tag(r"Reuters, \ 10 October 2018", corner=DR, font_size=12)
        with self.voiceover(
            "Hiring is increasingly screened by software. <bookmark mark='a'/> In 2018 Reuters reported that Amazon "
            "had dropped an experimental résumé screen: trained on ten years of applications, mostly from men, it "
            "had learned to mark down résumés containing the word women's. <bookmark mark='b'/> A model trained on "
            "past decisions learns past discrimination. <bookmark mark='c'/> But unlike a recruiter, it can be "
            "audited at scale, by sending it pairs of applications that differ only in a name, <bookmark mark='d'/> "
            "which is exactly Bertrand and Mullainathan's design, now run on a machine."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.15))
            for mk, c in zip("bcd", pts.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def questions(self):
        rows = VGroup(
            label(r"open questions", font_size=27, color=E.ACCENT),
            label(r"artificial intelligence: \ will it substitute for experts, \ or raise the less skilled?",
                  font_size=21, color=MIDS),
            label(r"the stalled premium: \ is demand for skill slowing, \ or is college changing?", font_size=21,
                  color=COLLEGE),
            label(r"firms: \ how much of rising inequality is between employers?", font_size=21, color=FIRM),
            label(r"discrimination: \ why has the call-back gap not narrowed since 1989?", font_size=21,
                  color=BLACK_N),
            label(r"the child penalty: \ what policies, \ if any, \ shrink it?", font_size=21, color=WOMEN),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.2)
        with self.voiceover(
            "The open questions. <bookmark mark='a'/> Artificial intelligence can do some non-routine cognitive "
            "tasks: will it substitute for experts, or raise the productivity of the less skilled? "
            "<bookmark mark='b'/> Why has the college premium stalled: slower demand for skill, or a change in what "
            "college teaches and who attends? <bookmark mark='c'/> How much of rising inequality is inequality "
            "between employers? <bookmark mark='d'/> Why has the call-back gap not narrowed in a quarter of a "
            "century of experiments? <bookmark mark='e'/> And which policies, if any, shrink the child penalty? "
            "Studies of "
            "parental leave and childcare have found smaller effects than many hoped."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
