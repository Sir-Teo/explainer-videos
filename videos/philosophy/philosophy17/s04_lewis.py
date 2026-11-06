from __future__ import annotations

from videos.philosophy.philosophy17.common import *  # noqa: F403


def bottle(color=EFFECT):
    body = RoundedRectangle(width=0.36, height=0.8, corner_radius=0.08, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.25)
    neck = Rectangle(width=0.14, height=0.3, stroke_color=color, stroke_width=3).next_to(body, UP, buff=0)
    return VGroup(body, neck)


class Lewis(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"Counterfactual dependence", r"Would it have happened anyway?", lit=(1973, 2000),
                            part=PART)
        with self.voiceover("Chapter three. Counterfactual dependence."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.analysis()
        self.preemption()
        self.more()
        self.transitivity()

    def analysis(self):
        hc = history_card(1973, r"David Lewis", r"`Causation'", width=4.6, color=HIST).to_corner(UL, buff=0.35)
        rows = stack([
            (r"$e$ depends on $c$: \ \ if $c$ had not occurred, \ $e$ would not have occurred", CAUSE),
            (r"the counterfactual is read on Part 14's spheres: \ the closest worlds without $c$", GREY_A),
            (r"$c$ causes $e$: \ \ a chain of dependences runs from $c$ to $e$", EFFECT),
            (r"the chain makes causation transitive, \ and handles some redundancy", GREY_A),
        ], font_size=23, aligned_edge=LEFT, buff=0.35).next_to(hc, DOWN, buff=0.5).set_x(0)
        chain = VGroup(*[label(t, font_size=22, color=c) for t, c in ((r"$c$", CAUSE), (r"$d_1$", WHITE),
                                                                      (r"$d_2$", WHITE), (r"$e$", EFFECT))]).arrange(
            RIGHT, buff=1.2).next_to(rows, DOWN, buff=0.6)
        arrows = VGroup(*[Arrow(chain[i].get_right(), chain[i + 1].get_left(), buff=0.15, color=GREY_B,
                                stroke_width=3) for i in range(3)])
        with self.voiceover(
            "David Lewis took up Hume's second definition. <bookmark mark='a'/>An event e depends on an event c if, "
            "had c not occurred, e would not have occurred. <bookmark mark='b'/>The counterfactual is read with the "
            "similarity semantics of Part 14: in the closest worlds without c, is there no e? "
            "<bookmark mark='c'/>Then c causes e if there is a chain of such dependences leading from c to e. "
            "<bookmark mark='d'/>The chain makes causation transitive, and, as we will see, handles some cases where "
            "the effect would have happened anyway."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
                if mk == "c":
                    self.play(FadeIn(chain), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.3))
        self.clear_scene()

    def preemption(self):
        d = {(c["case"], c["candidate"]): c for c in load("preempt")["cases"]}
        head = label(r"Suzy and Billy", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        suzy = Dot([-5.6, 1.0, 0], radius=0.16, color=SUZY)
        billy = Dot([-5.6, -0.4, 0], radius=0.16, color=BILLY)
        sl = label(r"Suzy", font_size=20, color=SUZY).next_to(suzy, LEFT, buff=0.15)
        bl = label(r"Billy", font_size=20, color=BILLY).next_to(billy, LEFT, buff=0.15)
        b = bottle().move_to([2.4, 0.3, 0])
        rs = Dot(suzy.get_center(), radius=0.09, color=SUZY)
        rb = Dot(billy.get_center(), radius=0.09, color=BILLY)
        shards = VGroup(*[Line(ORIGIN, 0.35 * np.array([np.cos(a), np.sin(a), 0]), color=EFFECT, stroke_width=3)
                          .shift(b.get_center()) for a in np.linspace(0, TAU, 9, endpoint=False)])
        rows = stack([
            (r"both throw; \ Suzy's rock arrives first; \ the bottle shatters", WHITE),
            (r"had Suzy not thrown, \ Billy's rock would have shattered it: \ no dependence", BAD),
            (r"but-for test, \ computed: \ Suzy " + (r"$\checkmark$" if d[("rock throwing", "ST")]["but_for"] else
                                                    r"$\times$") + r", \ Billy " +
             (r"$\checkmark$" if d[("rock throwing", "BT")]["but_for"] else r"$\times$"), BAD),
            (r"Lewis's chain rescues early preemption; \ late preemption \ (Hall, \ 2004) \ defeats it", GOAL),
        ], font_size=21, aligned_edge=LEFT, width=7.0).move_to([3.2, -2.2, 0])
        with self.voiceover(
            "Ned Hall's example has become the standard test. <bookmark mark='a'/>Suzy and Billy both throw rocks at "
            "a bottle. Suzy's arrives first, and the bottle shatters; Billy's flies through the empty space where "
            "the bottle was. <bookmark mark='b'/>Suzy caused the shattering. But had she not thrown, Billy's rock "
            "would have shattered the bottle anyway, so the shattering does not depend on her throw. "
            "<bookmark mark='c'/>The Reasoner runs the simple but-for test on a model of the case: neither Suzy nor "
            "Billy passes it. <bookmark mark='d'/>Lewis's chains rescue some such cases, when the backup is cut off "
            "early. But here Billy's rock is cut off only by the bottle's having already shattered: late preemption. "
            "There is no chain of dependence, and the counterfactual analysis says Suzy was not a cause."
        ) as vo:
            self.play(FadeIn(head), FadeIn(suzy), FadeIn(billy), FadeIn(sl), FadeIn(bl), FadeIn(b))
            vo.wait_until("a")
            self.play(rs.animate.move_to(b.get_center()), rb.animate.move_to([-0.6, -0.1, 0]), run_time=1.4,
                      rate_func=linear)
            self.play(FadeOut(b), FadeIn(shards, scale=0.3), rb.animate.move_to([4.6, 0.6, 0]), FadeIn(rows[0]),
                      run_time=1.2)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def more(self):
        head = label(r"Trumping and overdetermination", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"trumping \ (Schaffer, \ 2000)", r"a major and a sergeant both shout `Advance!'; \ soldiers obey the "
                                                r"higher rank: \ the major's order is the cause, \ though the advance "
                                                r"depends on neither", CAUSE),
            (r"overdetermination", r"two rocks strike at the same instant: \ each a cause? \ the effect depends on "
                                   r"neither", BILLY),
            (r"Lewis \ (2000)", r"`causation as influence': \ altering $c$ alters whether, \ when and how $e$ "
                                r"occurs", OK),
            (r"the lesson", r"dependence is evidence of causation, \ not its definition", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.4, x_text=-2.4)
        with self.voiceover(
            "Two more cases. <bookmark mark='a'/>Jonathan Schaffer's trumping: a major and a sergeant both shout "
            "advance, and the soldiers, who obey the higher rank, advance. The major's order is the cause, though "
            "the advance depends on neither order. <bookmark mark='b'/>Overdetermination: two rocks strike the "
            "bottle at exactly the same instant. Intuition calls each a cause, but the shattering depends on "
            "neither. <bookmark mark='c'/>Lewis's last theory, causation as influence, said that c causes e when "
            "small alterations of c would alter whether, when or how e occurs. <bookmark mark='d'/>The lesson most "
            "have drawn: dependence is evidence of causation, not its definition."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def transitivity(self):
        head = label(r"Is causation transitive? \ The boulder", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        g = CausalGraph({"boulder": [-4.4, 0.2, 0], "duck": [-1.2, 1.6, 0], "survive": [2.0, 0.2, 0]},
                        [("boulder", "duck"), ("duck", "survive"), ("boulder", "survive")], radius=0.62, font_size=18,
                        colors={"boulder": BAD, "duck": CAUSE, "survive": OK})
        notes = stack([(r"a boulder falls toward a hiker; \ she sees it and ducks; \ she survives", WHITE),
                       (r"the boulder caused the duck; \ the duck caused survival", CAUSE),
                       (r"did the boulder cause her survival? \ Surely not \ (Hall, \ 2000)", BAD),
                       (r"its threat and its warning cancel: \ a structure Chapter 6 can represent", GOAL)],
                      font_size=21).next_to(g, DOWN, buff=0.55)
        with self.voiceover(
            "Lewis's chains also make causation transitive, and transitivity has its own counterexamples. "
            "<bookmark mark='a'/>A boulder falls toward a hiker. She sees it and ducks, and survives. "
            "<bookmark mark='b'/>The boulder caused her ducking, and her ducking caused her survival. "
            "<bookmark mark='c'/>Did the boulder cause her survival? Surely not: without the boulder she would have "
            "survived anyway. <bookmark mark='d'/>The boulder both threatens and warns, and the two paths cancel. "
            "Saying this properly needs more structure than a chain of events: the structural models of chapter six."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g.node["boulder"]), FadeIn(g.node["duck"]), FadeIn(g.node["survive"]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(GrowArrow(g.edge[("boulder", "duck")]), GrowArrow(g.edge[("duck", "survive")]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(GrowArrow(g.edge[("boulder", "survive")]), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.clear_scene()
