from __future__ import annotations

from videos.psychology.psych51.common import *  # noqa: F403


class Systems(VoiceoverScene):
    def construct(self):
        card_section(self, 11, r"Systems, \ checklists and crews", r"Can a system be safer than its people?",
                     scale=("society",))
        self.cheese()
        self.checklist()
        self.tenerife()
        self.crm()

    def cheese(self):
        d = load("cheese")
        head = heading(r"The Swiss cheese model")
        lp = np.log10(np.asarray(d["p"]))
        A = axes([0.3, 4.7], [-5, -1], x_length=5.4, y_length=3.0, xticks=None, yticks=[-5, -4, -3, -2, -1],
                 yfmt=lambda v: rf"10^{{{v:.0f}}}", ylabel=r"chance of an accident", center=[-3.3, 0.3, 0],
                 font_size=12)
        bs = VGroup(*[Rectangle(width=0.6, height=abs(A.ax.c2p(0, v)[1] - A.ax.c2p(0, -5)[1]), color=AUTH,
                                fill_opacity=0.8, stroke_width=0).move_to(A.ax.c2p(i + 1, (v - 5) / 2),)
                      for i, v in enumerate(lp)])
        for r_, v, i in zip(bs, lp, range(4)):
            r_.align_to(A.ax.c2p(i + 1, -5), DOWN)
        names = VGroup(*[label(rf"$\rho$ = {r:.1f}", font_size=14, color=GREY_A).next_to(A.ax.c2p(i + 1, -5), DOWN,
                                                                                         buff=0.12)
                         for i, r in enumerate(d["rho"])])
        nl = label(r"correlation between the layers' holes", font_size=13, color=GREY_A).next_to(names, DOWN, buff=0.1)
        rows = rows_of([
            (r"James Reason: \ defences in layers, \ each with holes; \ an accident needs a hole in every layer at "
             r"once", WHITE),
            (r"four layers, \ each failing one time in ten: \ independent, \ one accident in 10,000", MODEL),
            (rf"holes that share a cause (fatigue, \ a culture of shortcuts, \ one bad procedure): \ at $\rho$ = 0.6, "
             rf"\ about one in {1 / d['p'][-1]:.0f}", AUTH),
            (r"defence in depth works only if the layers fail independently; \ latent conditions make them fail "
             r"together", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{work.swiss\_cheese}, \ 400,000 simulated days")
        with self.voiceover(
            "Can a system be safer than its people? <bookmark mark='a'/> James Reason's answer is a picture: defences "
            "in layers, like slices of Swiss cheese, each with holes. An accident needs a hole in every layer at once. "
            "<bookmark mark='b'/> Take four layers, each failing one time in ten. If they fail independently, that's "
            "one accident in ten thousand. <bookmark mark='c'/> But holes can share a cause: fatigue, a culture of "
            "shortcuts, one bad procedure. With a correlation of zero point six between layers, it's about one in "
            "seventy. <bookmark mark='d'/> Defence in depth works only if the layers fail independently, and what "
            "Reason called latent conditions make them fail together."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(nl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(bs[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), LaggedStart(*[FadeIn(b_) for b_ in bs[1:]], lag_ratio=0.4))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def checklist(self):
        rows_section(self, r"The checklist", [
            (r"aviation's checklists began in 1935, \ after a new bomber crashed because a control lock was left on",
             WHITE),
            (r"2009: \ Alex Haynes and colleagues brought a 19-item surgical checklist to eight hospitals in eight "
             r"countries", MODEL),
            (r"before and after: \ deaths fell from about 1.5\% to 0.8\%, \ complications from about 11\% to 7\%", GOOD),
            (r"but it was a before-and-after study; \ in Ontario, \ where a mandate imposed it province-wide, \ deaths "
             r"and complications did not change", AUTH),
            (r"a checklist works through the team that owns it: \ the pause, \ the names, \ the permission to speak",
             YOU),
        ], "The checklist is the simplest defence. <bookmark mark='a'/> Aviation's checklists began in 1935, after a new "
           "bomber crashed on a test flight because a control lock had been left on. <bookmark mark='b'/> In 2009 Alex "
           "Haynes and colleagues brought a nineteen-item surgical checklist to eight hospitals in eight countries. "
           "<bookmark mark='c'/> Before and after, deaths fell from about one and a half percent to under one, and "
           "complications from about eleven percent to seven. <bookmark mark='d'/> But it was a before-and-after "
           "study. In Ontario, where a mandate imposed the checklist on every hospital, deaths and complications "
           "didn't change. <bookmark mark='e'/> A checklist works through the team that owns it: the pause, the "
           "names, and the permission to speak up.", tag=published_tag(r"Haynes et al.\ (2009)"))

    def tenerife(self):
        rows_section(self, r"Tenerife, \ 1977", [
            (r"two jumbo jets diverted to a small, \ fog-bound airport; \ one taxiing on the runway, \ one at its end",
             WHITE),
            (r"the other captain, \ a senior training pilot, \ began the takeoff without a takeoff clearance", AUTH),
            (r"the flight engineer asked whether the taxiing aircraft was clear of the runway; \ the captain said it "
             r"was", PERSON),
            (r"radio calls overlapped, \ and ``we are now at takeoff'' meant different things to the crew and to "
             r"the tower", MODEL),
            (r"583 people died: \ the deadliest accident in aviation's history", AUTH),
        ], "Here's the accident that changed crews. <bookmark mark='a'/> In 1977 two jumbo jets were diverted to a "
           "small, fog-bound airport on Tenerife. One was taxiing along the runway, and the other waited at its end. "
           "<bookmark mark='b'/> The waiting captain, a senior training pilot, began the takeoff without a takeoff "
           "clearance. <bookmark mark='c'/> His flight engineer asked whether the other aircraft was clear of the "
           "runway, and the captain said it was. <bookmark mark='d'/> Radio calls overlapped, and we are now at "
           "takeoff meant different things to the crew and to the tower. <bookmark mark='e'/> Five hundred and "
           "eighty-three people died. It's still the deadliest accident in aviation's history.")

    def crm(self):
        chips_section(self, r"Crew resource management", [
            (r"the finding", r"NASA's studies of the late 1970s: \ most accidents involved failures of communication, \ "
                             r"leadership and decision in the crew, \ not of flying skill", MODEL),
            (r"the training", r"speak up with a graded script, \ brief the plan, \ cross-check, \ and make the "
                              r"captain's authority open to challenge", GOOD),
            (r"the spread", r"operating theatres, \ emergency rooms, \ ships and control rooms", PERSON),
            (r"the evidence", r"attitudes and behaviour change reliably; \ effects on accidents are hard to measure, "
                              r"\ because accidents are rare", AUTH),
        ], "After Tenerife, and other crashes where someone saw the problem and didn't say so, came crew resource "
           "management. <bookmark mark='a'/> NASA's studies in the late nineteen seventies found that most accidents "
           "involved failures of communication, leadership and decision in the crew, not of flying skill. "
           "<bookmark mark='b'/> The training teaches speaking up with a graded script, briefing the plan, "
           "cross-checking, and making the captain's authority open to challenge. Part 34's obedience, designed "
           "against. <bookmark mark='c'/> It spread to operating theatres, emergency rooms, ships and control rooms. "
           "<bookmark mark='d'/> And the evidence: attitudes and behaviour change reliably. Effects on accidents are "
           "hard to measure, because accidents are rare. That's chapter seven's problem, at the level of a whole "
           "industry.", chip_w=3.2, text_w=9.0)
