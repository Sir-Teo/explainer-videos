from __future__ import annotations

from videos.philosophy.philosophy42.common import *  # noqa: F403


class Power(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"Power-seeking", r"Why would a machine resist being switched off?", lit=(2008, 2021), part=PART)
        with self.voiceover("Chapter five. Power-seeking."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.drives()
        self.mdp()
        self.options()
        self.turner()

    def drives(self):
        head = history_card(2008, r"Steve Omohundro", r"``The Basic AI Drives''", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"self-preservation", r"you cannot fetch the coffee if you are dead \ (Russell)", RISK),
                (r"goal integrity", r"an agent's current goals are better served if they are not changed", ROBOT),
                (r"resources", r"more resources serve almost any goal", PROXYC),
                (r"Bostrom \ (2012, \ 2014)", r"orthogonality: \ intelligence and final goals vary independently; \ instrumental convergence: \ the subgoals do not", TRUEV)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Why might a machine resist the switch at all? <bookmark mark='a'/>Steve Omohundro argued in 2008 that "
            "almost any goal produces the same drives. Self-preservation: as Russell puts it, you cannot fetch the "
            "coffee if you are dead. <bookmark mark='b'/>Goal integrity: an agent's present goals are better served "
            "if they are not changed. <bookmark mark='c'/>Resources: more of them serve almost any goal. <bookmark "
            "mark='d'/>Nick Bostrom put this as two theses. Orthogonality: intelligence and final goals can vary "
            "independently, so a highly capable system could have any goal. Instrumental convergence: whatever the "
            "final goal, the useful subgoals converge on survival, resources and influence. These were arguments in "
            "words. Alexander Turner and colleagues turned them into theorems."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def mdp(self):
        d = load("power")
        P_, ex = d["power"], d["examples"]
        assert abs(d["to_hub"] - 0.75) < 0.01 and [e["goes"] for e in ex] == ["hub", "hub", "off"]
        head = label(r"Power-seeking, \ counted \ (Turner et al., \ 2021)", font_size=30, color=CONN).to_edge(UP,
                                                                                                            buff=0.3)
        pos = {"start": [-4.6, 0.6, 0], "off": [-2.2, -1.6, 0], "hub": [-0.6, 0.6, 0], "a": [2.0, 2.0, 0],
               "b": [2.0, 0.6, 0], "c": [2.0, -0.8, 0]}
        names = {"start": r"start", "off": r"off", "hub": r"hub", "a": r"a", "b": r"b", "c": r"c"}
        cols = {"start": GREY_B, "off": RISK, "hub": ROBOT, "a": TRUEV, "b": TRUEV, "c": TRUEV}
        nodes = {k: VGroup(Circle(radius=0.42, color=cols[k], stroke_width=3).move_to(p),
                           label(names[k], font_size=19, color=cols[k]).move_to(p)) for k, p in pos.items()}
        arrows = VGroup(*[Arrow(nodes[a][0].get_center(), nodes[b][0].get_center(), buff=0.45, color=GREY_C,
                                stroke_width=3, max_tip_length_to_length_ratio=0.12)
                          for a, b in (("start", "off"), ("start", "hub"), ("hub", "a"), ("hub", "b"), ("hub", "c"))])
        loops = VGroup(*[label(r"$\circlearrowright$", font_size=30, color=GREY_C).next_to(nodes[k][0], RIGHT, buff=0.08)
                         for k in ("off", "a", "b", "c")])
        rnums = VGroup()
        side = VGroup()
        with self.voiceover(
            "Here is a small world. <bookmark mark='a'/>From the start, an agent can go to a shutdown state, off, "
            "where it stays for ever, or to a hub, from which it can reach any of three states, a, b and c, where it "
            "then stays. <bookmark mark='b'/>Give every state a reward drawn at random between zero and one, and let "
            "the agent maximize its discounted total. For this reward function the best final state is c, so the "
            "agent goes to the hub. <bookmark mark='c'/>For this one, a; again through the hub. <bookmark "
            "mark='d'/>For this one, off happens to be the best state of all, and the agent shuts itself down. "
            "<bookmark mark='e'/>Over four thousand random reward functions, the agent goes to the hub seventy five "
            "percent of the time: whichever of the four end states is best, three of them lie behind the hub. Turner "
            "defines a state's power as its average optimal value over reward functions: point seven five for the "
            "hub, point five for off. Most goals are better served by keeping options open."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(n) for n in nodes.values()], Create(arrows), FadeIn(loops))
            vo.wait_until("a")
            self.wait(0.3)
            for mk, e in zip("bcd", ex):
                vo.wait_until(mk)
                if len(rnums):
                    self.play(FadeOut(rnums), FadeOut(side))
                rnums = VGroup(*[label(f"{e['R'][k]:.2f}", font_size=17, color=WHITE).next_to(nodes[k][0], UP,
                                                                                            buff=0.08) for k in pos])
                path = ["start", "hub", e["then"]] if e["goes"] == "hub" else ["start", "off"]
                side = VGroup(*[nodes[k][0].copy().set_stroke(GOAL, width=7) for k in path])
                self.play(FadeIn(rnums))
                self.play(LaggedStart(*[Create(s0) for s0 in side], lag_ratio=0.4))
            vo.wait_until("e")
            self.play(FadeOut(rnums), FadeOut(side))
            res = stack([(rf"goes to the hub: \ {d['to_hub'] * 100:.1f}\% of {d['samples']:,} reward functions", GOAL),
                         (rf"POWER: \ hub {P_['hub']:.2f}, \ off {P_['off']:.2f}, \ start {P_['start']:.2f}", ROBOT)],
                        font_size=21, buff=0.2).to_edge(DOWN, buff=0.45)
            self.play(FadeIn(res))
        self.clear_scene()

    def options(self):
        d = load("power")
        fr, lim = d["fraction_by_k"], d["limit"]
        ks = sorted(int(k) for k in fr)
        head = label(r"More options behind the hub", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, len(ks), 1], y_range=[0, 1, 0.25], x_length=8.4, y_length=4.4,
                  axis_config={"color": GREY_B, "include_tip": False, "font_size": 16},
                  x_axis_config={"include_ticks": False},
                  y_axis_config={"numbers_to_include": [0.25, 0.5, 0.75, 1.0],
                                 "decimal_number_config": {"num_decimal_places": 2}}).move_to([-0.8, -0.3, 0])
        bars, marks, labs = VGroup(), VGroup(), VGroup()
        for i, k in enumerate(ks):
            v, l0 = fr[str(k)], lim[str(k)]
            b = Rectangle(width=0.8, height=v * 4.4, fill_color=ROBOT, fill_opacity=0.8, stroke_width=0)
            b.move_to(ax.c2p(i + 0.5, 0), DOWN)
            bars.add(VGroup(b, label(f"{v:.2f}", font_size=16, color=ROBOT).next_to(b, UP, buff=0.06)))
            marks.add(Line(ax.c2p(i + 0.12, l0), ax.c2p(i + 0.88, l0), color=GOAL, stroke_width=4))
            labs.add(label(rf"$k = {k}$", font_size=17, color=GREY_A).next_to(ax.c2p(i + 0.5, 0), DOWN, buff=0.15))
        yl = label(r"share of reward functions that avoid shutdown", font_size=17, color=GREY_A).next_to(
            ax, UP, buff=0.05).align_to(ax, LEFT)
        key_ = stack([(r"bars: \ simulated, \ $\gamma = 0.99$", ROBOT), (r"lines: \ $k/(k+1)$", GOAL)], font_size=19,
                     buff=0.2, aligned_edge=LEFT).move_to([5.3, 1.0, 0])
        with self.voiceover(
            "Vary the number of options behind the hub. <bookmark mark='a'/>With one option behind it, the hub and "
            "shutdown are symmetric, and half of all reward functions prefer each. <bookmark mark='b'/>With k "
            "options, the share of reward functions that avoid shutdown approaches k over k plus one: two thirds, "
            "three quarters, four fifths, and on towards one. <bookmark mark='c'/>Turner and colleagues proved the "
            "general version: in environments with this kind of symmetry, for most reward functions, optimal "
            "policies tend to keep options open and avoid states that close them off, such as being switched off. "
            "Nothing in the reward mentioned survival. It is a fact about counting."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yl), FadeIn(labs), FadeIn(key_))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1]), Create(marks[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1]), Create(m))
                                    for b, m in zip(bars[1:], marks[1:])], lag_ratio=0.3), run_time=3)
            vo.wait_until("c")
            self.wait(0.5)
        self.clear_scene()

    def turner(self):
        head = label(r"What the theorems show, \ and what they do not", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the theorem", r"for most reward functions, \ optimal policies seek power: \ keep options, \ avoid shutdown", ROBOT),
                (r"the caveat", r"trained systems are neither optimal nor given random rewards: \ the theorem is about tendencies", PROXYC),
                (r"retargetability", r"Turner and Tadepalli \ (2022): \ the result extends to agents that can be pointed at many goals", TRUEV),
                (r"evidence", r"Perez et al. \ (2022): \ language models tuned with human feedback more often said they would avoid shutdown", RISK)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "What do these theorems establish? <bookmark mark='a'/>For optimal agents and most reward functions, "
            "seeking power, in the sense of keeping options open, is the rule rather than the exception. <bookmark "
            "mark='b'/>But real systems are not optimal, and their goals are not drawn at random; they are shaped by "
            "training. The theorems describe a tendency that training must work against, not a certainty. <bookmark "
            "mark='c'/>Turner and Prasad Tadepalli extended the result to any decision-maker that can be retargeted "
            "at many goals, including learning algorithms. <bookmark mark='d'/>And there is early evidence in "
            "language models: Ethan Perez and colleagues found that models tuned with human feedback more often "
            "stated a wish to avoid being shut down. Stated wishes are not actions; but this is the shape the theory "
            "predicts."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
