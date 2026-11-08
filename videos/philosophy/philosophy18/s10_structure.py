from __future__ import annotations

from videos.philosophy.philosophy18.common import *  # noqa: F403


class Structure(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"Structural realism", r"What survives a scientific revolution?", lit=(1823, 1989),
                            part=PART)
        with self.voiceover("Chapter nine. Structural realism."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.fresnel()
        self.worrall()
        self.ontic()

    def fresnel(self):
        d = load("fresnel")
        head = label(r"Fresnel's equations, \ before and after the aether", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        eqs = VGroup(
            MathTex(r"r_s = \frac{n_1\cos\theta_i - n_2\cos\theta_t}{n_1\cos\theta_i + n_2\cos\theta_t}", font_size=28,
                    color=THEORY),
            MathTex(r"r_p = \frac{n_2\cos\theta_i - n_1\cos\theta_t}{n_2\cos\theta_i + n_1\cos\theta_t}", font_size=28,
                    color=REAL)).arrange(DOWN, buff=0.3).move_to([-4.0, 1.1, 0])
        ax = Axes(x_range=[0, 90, 15], y_range=[0, 1, 0.25], x_length=6.2, y_length=3.6,
                  axis_config={"color": GREY_B, "font_size": 18, "include_numbers": True}).move_to([2.8, 0.4, 0])
        cs = series_plot(ax, [r[1] for r in d["curve"]], THEORY, xs=[r[0] for r in d["curve"]], width=4)
        cp = series_plot(ax, [r[2] for r in d["curve"]], REAL, xs=[r[0] for r in d["curve"]], width=4)
        xl = label(r"angle of incidence \ (degrees); \ air to glass, \ $n = " + f"{d['n2']:.1f}" + r"$", font_size=17,
                   color=GREY_A).next_to(ax, DOWN, buff=0.2)
        ls = label(r"$R_s$", font_size=20, color=THEORY).next_to(ax.c2p(70, d["curve"][70][1]), UP, buff=0.1)
        lp = label(r"$R_p$", font_size=20, color=REAL).next_to(ax.c2p(84, d["curve"][84][2]), RIGHT, buff=0.1)
        bdot = Dot(ax.c2p(d["brewster"], 0), color=GOAL)
        bl = label(r"Brewster: \ " + f"{d['brewster']:.1f}" + r"$^\circ$", font_size=18, color=GOAL).move_to(
            ax.c2p(32, 0.42))
        barr = Arrow(bl.get_bottom(), bdot.get_center(), buff=0.08, color=GOAL, stroke_width=2,
                     max_tip_length_to_length_ratio=0.12)
        rows = stack([(r"1823: \ derived from an elastic aether's vibrations", BAD),
                      (r"1865: \ Maxwell's fields obey the same boundary conditions", OK),
                      (r"the aether is gone; \ the equations, \ unchanged", GOAL)], font_size=20,
                     aligned_edge=LEFT, width=6.2).move_to([-3.6, -1.8, 0])
        with self.voiceover(
            "Augustin Fresnel's theory of light was one of Laudan's casualties: it described light as vibrations "
            "of an elastic aether, and there is no aether. <bookmark mark='a'/>Yet from that theory Fresnel derived "
            "these equations, giving the fraction of light reflected at a surface, for each polarization. "
            "<bookmark mark='b'/>The Reasoner computes them for light passing from air into glass. One "
            "polarization's reflectance falls to zero at a particular angle, which the equations fix at fifty-six "
            "point three degrees: Brewster's angle, where reflected light is perfectly polarized. "
            "<bookmark mark='c'/>Fresnel derived this from the aether in 1823. <bookmark mark='d'/>Maxwell's "
            "electromagnetic theory, forty years later, rederived exactly the same equations from fields with no "
            "aether at all. <bookmark mark='e'/>The ontology was discarded. The mathematical structure was kept."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eqs))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(xl))
            self.play(Create(cs), Create(cp), FadeIn(ls), FadeIn(lp), run_time=2)
            self.play(FadeIn(bdot), FadeIn(bl), GrowArrow(barr))
            for mk, r in zip("cde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def worrall(self):
        hc = history_card(1989, r"John Worrall", r"`Structural Realism: The Best of Both Worlds?'", width=6.6,
                          color=HIST).to_corner(UL, buff=0.35)
        rows = [
            (r"the thesis", r"believe what successful theories say about the \textit{structure} of the world, \ not "
                            r"about the nature of what has it", REAL),
            (r"both worlds", r"no miracles: \ the structure was right; \ meta-induction: \ the natures were wrong", OK),
            (r"Poincaré \ (1902)", r"`the true relations between real objects are the only reality we can attain'",
             THEORY),
            (r"Newman \ (1928)", r"if only structure is known, \ the claim is nearly empty: \ any set of the right size "
                                 r"can be given any structure", BAD),
            (r"the reply", r"the structure must be tied to observation, \ not merely to cardinality", GOAL),
        ]
        g = rows_table(rows, top=1.4, gap=0.45, width=8.6, x_text=-2.8)
        with self.voiceover(
            "John Worrall turned the example into a position. <bookmark mark='a'/>Structural realism says: believe "
            "what successful theories say about the structure of the world, the equations relating its parts, but "
            "not what they say about the nature of the things that have that structure. "
            "<bookmark mark='b'/>It promises the best of both worlds: success is no miracle, because the structure "
            "was right; and the meta-induction is disarmed, because only the natures were wrong. "
            "<bookmark mark='c'/>Henri Poincaré had said the same: the true relations between real objects are the "
            "only reality we can attain. <bookmark mark='d'/>But the mathematician Max Newman found a problem in "
            "1928: if we know only that the world has a certain abstract structure, we know almost nothing, since "
            "any collection of the right size can be given any structure. <bookmark mark='e'/>The structure "
            "structural realists believe in must be tied to observation, not merely to counting."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def ontic(self):
        head = label(r"Epistemic or ontic?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"epistemic \ (Worrall)", r"there are natures; \ we can know only their structure", REAL),
            (r"ontic \ (Ladyman, \ 1998)", r"there is nothing but structure: \ relations without intrinsic relata", ANTI),
            (r"the motivation", r"quantum particles lack individuality: \ swap two electrons and nothing changes "
                                r"(Part 26)", THEORY),
            (r"\textit{Every Thing Must Go}", r"Ladyman and Ross \ (2007): \ metaphysics should be naturalized, \ and "
                                              r"objects are a useful fiction", GOAL),
            (r"the objection", r"can there be relations with nothing to relate?", BAD),
        ]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.6, x_text=-2.4)
        with self.voiceover(
            "Structural realism comes in two strengths. <bookmark mark='a'/>Epistemic structural realism, "
            "Worrall's, says that the world has natures, but we can know only their structure. "
            "<bookmark mark='b'/>Ontic structural realism, proposed by James Ladyman in 1998, says that there is "
            "nothing but structure. <bookmark mark='c'/>Its motivation comes from physics: quantum particles of the "
            "same kind lack individuality, so swapping two electrons changes nothing, a theme of Part twenty-six. "
            "<bookmark mark='d'/>Ladyman and Don Ross's Every Thing Must Go argued that metaphysics should be "
            "naturalized, and that ordinary objects are a useful fiction. <bookmark mark='e'/>The standing "
            "objection: can there be relations with nothing to relate?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
