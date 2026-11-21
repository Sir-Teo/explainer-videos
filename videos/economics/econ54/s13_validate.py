from __future__ import annotations

from videos.economics.econ54.common import *  # noqa: F403


class Validate(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Validation: \ predict the experiment", r"Would the model have known?",
             "Chapter eleven. Validation: predict the experiment.", lit={1997: r"PROGRESA", 2006: r"Todd and Wolpin"},
             scale=("household", "nation"), horizon=("a decade",))
        self.progresa()
        self.island()

    def progresa(self):
        steps = flow_chain(steps=[(r"control villages only: no subsidy", CONTROL),
                                  (r"children's wages differ from village to village", DATA),
                                  (r"a subsidy for school acts like a lower wage", MODEL),
                                  (r"predict the treated villages, then open the envelope", EST)],
                           box_w=3.0, box_h=1.25, font_size=19, buff=0.4).move_to(UP * 1.2)
        notes = VGroup(
            label(r"PROGRESA, \ Mexico, \ 1997: \ cash for mothers whose children attend school, \ villages chosen "
                  r"at random to start first", font_size=20, color=WHITE),
            label(r"Todd and Wolpin: \ the model's predictions were broadly close to the experiment's", font_size=20,
                  color=GAIN),
            label(r"then the model could answer what the experiment could not: \ other subsidy schedules",
                  font_size=20, color=E.ACCENT),
        ).arrange(DOWN, buff=0.3).next_to(steps, DOWN, buff=0.7)
        tag = published_tag(r"Todd and Wolpin, \ AER 96(5) (2006)", corner=DR, font_size=12)
        with self.voiceover(
            "How would we know if a structural model were wrong? The strongest test is to predict an experiment "
            "before looking at it. <bookmark mark='a'/> In 1997 Mexico began PROGRESA, which paid mothers when "
            "their children attended school, and started it first in villages chosen at random. Petra Todd and "
            "Kenneth Wolpin estimated a model of families' schooling choices using only the control villages, "
            "where there was no subsidy. <bookmark mark='b'/> How can data without a subsidy say what a subsidy "
            "does? Through wages. Children's wages differ from village to village, and a school subsidy works "
            "like a cut in the wage a child gives up by attending. <bookmark mark='c'/> If families treat a peso "
            "of subsidy like a peso of wages, the model can predict the subsidy's effect. <bookmark mark='d'/> They "
            "predicted the treated villages' schooling, then compared. <bookmark mark='e'/> The predictions were "
            "broadly close to what the experiment found. <bookmark mark='f'/> And once validated, the model could "
            "answer what the experiment could not, like how a different schedule of payments by age would have "
            "done."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(notes[0]))
            for mk, k in zip("abcd", range(4)):
                vo.wait_until(mk)
                an = [FadeIn(steps.boxes[k], shift=UP * 0.1)]
                if k > 0:
                    an.append(Create(steps.arrows[k - 1]))
                self.play(*an)
            vo.wait_until("e")
            self.play(FadeIn(notes[1]))
            vo.wait_until("f")
            self.play(FadeIn(notes[2]))
        self.clear_scene()

    def island(self):
        Sc = load("school")
        a, b = Sc["money"], Sc["label"]
        ax = plane([0.4, 2.6], [0, 0.38], center=LEFT * 1.6 + DOWN * 0.4, x_length=7.4, y_length=4.6, xticks=[],
                   yticks=[0, 0.1, 0.2, 0.3], ylabel=r"rise in attendance from the subsidy, \ points",
                   yfmt=lambda v: f"{100 * v:.0f}", font_size=14)

        def pair(x, w, col_exp):
            g = VGroup()
            for dx, val, se, col in ((-0.18, w["predicted_effect"], w["predicted_se"], MODEL),
                                     (0.18, w["experimental_effect"], w["experimental_se"], col_exp)):
                p = ax.ax.c2p(x + dx, val)
                lo, hi = ax.ax.c2p(x + dx, val - 1.96 * se), ax.ax.c2p(x + dx, val + 1.96 * se)
                g.add(VGroup(Line(lo, hi, color=col, stroke_width=3), Dot(p, radius=0.09, color=col)))
            return g

        pa = pair(1, a, GAIN)
        pb = pair(2, b, ERR)
        names = VGroup(label(r"a peso is a peso", font_size=19, color=GAIN).next_to(ax.ax.c2p(1, 0), DOWN, buff=0.25),
                       label(r"the label matters too", font_size=19, color=ERR).next_to(ax.ax.c2p(2, 0), DOWN,
                                                                                        buff=0.25))
        side = VGroup(
            label(rf"{Sc['villages']} villages, \ {Sc['per']} children each; \\ half get a subsidy worth "
                  rf"{Sc['subsidy']:.0f}", font_size=18, color=WHITE),
            label(r"purple: \ the model's prediction, \\ from the control villages", font_size=18, color=MODEL),
            label(r"the experiment: \ treated \\ minus control", font_size=18, color=GAIN),
            label(r"a second world: \ parents also \\ respond to what the money is for", font_size=18, color=ERR),
            label(r"the prediction fails, \\ and says which assumption did", font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = island_tag(r"simulated: \ the Island's villages", corner=DR, font_size=13)
        with self.voiceover(
            f"The Island runs the same test. <bookmark mark='a'/> {Sc['villages']} villages of {Sc['per']} "
            "children; half, chosen at random, get a subsidy for attendance. <bookmark mark='b'/> A schooling "
            "model estimated on the control villages alone, where children's wages vary, predicts that the "
            f"subsidy raises attendance by {100 * a['predicted_effect']:.1f} points. <bookmark mark='c'/> The "
            f"experiment finds {100 * a['experimental_effect']:.1f}. Validated. <bookmark mark='d'/> Now a second "
            "world, identical except that parents respond to the subsidy more than to the same money in wages, "
            "because it is labelled for school, or because it comes with a condition attached. The model, "
            "estimated as before, still predicts "
            f"{100 * b['predicted_effect']:.1f} points. The experiment finds {100 * b['experimental_effect']:.1f}. "
            "<bookmark mark='e'/> The prediction fails, and its failure is informative: the assumption that a "
            "peso is a peso, which let wages stand in for a subsidy, is what broke. A model that passes such a "
            "test has earned some trust; one that has never faced one has not."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(names[0]))
            vo.wait_until("b")
            self.play(FadeIn(pa[0], shift=UP * 0.1), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(pa[1], shift=UP * 0.1), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(names[1]), FadeIn(pb[0], shift=UP * 0.1), FadeIn(side[3]))
            self.play(FadeIn(pb[1], shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
