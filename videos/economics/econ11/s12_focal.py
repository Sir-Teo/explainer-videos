from __future__ import annotations

from videos.economics.econ11.common import *  # noqa: F403

RED_L = "#F25F5C"
AMBER = "#F2C14E"
GREEN_L = "#7BD88F"


def traffic_light(height=1.6):
    box = RoundedRectangle(width=height * 0.42, height=height, corner_radius=0.08, stroke_color=GREY_B,
                           stroke_width=2, fill_color="#1F2430", fill_opacity=1)
    lamps = VGroup(*[Circle(radius=height * 0.12, stroke_width=0, fill_color=c, fill_opacity=0.9)
                     for c in (RED_L, AMBER, GREEN_L)]).arrange(DOWN, buff=height * 0.07).move_to(box)
    return VGroup(box, lamps)


class Focal(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Focal points and correlated equilibrium", r"When a game has many equilibria, how do people "
             r"pick one?", "Chapter ten. Focal points and correlated equilibrium.",
             lit={1974: r"Aumann's correlated equilibrium"}, scale=("person", "city"))
        self.focal()
        self.light()

    def focal(self):
        hc = history_card(1960, r"Thomas Schelling, \ \emph{The Strategy of Conflict}", r"questions with many "
                          r"right answers, \ as long as two people give the same one", color=COOP, width=11.4,
                          font_size=24).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"you must meet a stranger in New York tomorrow, \ with no way to arrange it: \ where, \ and when?",
                  font_size=24),
            label(r"the commonest answer among his students: \ noon, \ at the information booth in Grand Central",
                  font_size=24, color=COOP),
            label(r"heads or tails? \ heads. \ \ a number? \ one. \ \ divide \$100? \ in half", font_size=24,
                  color=GREY_A),
            label(r"a focal point: \ an equilibrium that stands out, \ because of what the players share", font_size=25,
                  color=EQ),
            label(r"theory says which outcomes are stable; \ culture, \ history and salience pick among them",
                  font_size=24, color=LEVEL),
        ).arrange(DOWN, buff=0.36).next_to(hc, DOWN, buff=0.5)
        tag = published_tag(r"Schelling, \emph{The Strategy of Conflict} (1960), ch.\ 3", corner=DR, font_size=13)
        with self.voiceover(
            "Thomas Schelling studied how people choose among equilibria, with questions that have many right "
            "answers, as long as two people give the same one. <bookmark mark='a'/> You must meet a stranger in New "
            "York tomorrow, and neither of you can contact the other. Where do you go, and when? "
            "<bookmark mark='b'/> The commonest answer among his students was noon, at the information booth in Grand "
            "Central Station. <bookmark mark='c'/> Heads or tails? Most say heads. Name a positive number: one. "
            "Divide a hundred dollars: in half. <bookmark mark='d'/> Schelling called such an outcome a focal point: "
            "an equilibrium that stands out because of what the players have in common. "
            "<bookmark mark='e'/> Theory says which outcomes are stable; culture, history and salience pick among "
            "them."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def light(self):
        c = load("correlated")
        A, B, P = np.array(c["A"]), np.array(c["B"]), np.array(c["P"])
        mat = matrix(A, B, [r"go", r"stop"], [r"go", r"stop"], row_name=r"Ana", col_name=r"Bo", cell_w=2.0,
                     cell_h=0.95, font_size=26).shift(LEFT * 3.3 + UP * 1.4)
        probs = VGroup()
        for i in range(2):
            for j in range(2):
                v = P[i, j]
                probs.add(label(rf"{v:.2f}" if v > 1e-9 else r"0", font_size=22, color=AMBER).next_to(
                    mat.cells[i][j], DOWN, buff=-0.28).shift(RIGHT * 0.55))
        light = traffic_light(1.6).next_to(mat, DOWN, buff=0.55).align_to(mat, LEFT)
        sig = VGroup(
            label(r"the light tells each driver \\ privately: \ go or stop", font_size=17, color=GREY_A),
            label(rf"Ana go, \ Bo stop: \ {P[0, 1]:.2f}", font_size=17, color=AMBER),
            label(rf"Ana stop, \ Bo go: \ {P[1, 0]:.2f}", font_size=17, color=AMBER),
            label(rf"both stop: \ {P[1, 1]:.2f}; \ both go: \ never", font_size=17, color=AMBER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(light, RIGHT, buff=0.3)
        side = VGroup(
            label(r"two drivers at a crossing: \ chicken again", font_size=21),
            label(r"pure equilibria: \ one goes, \ one stops: \ unfair, \ 7 and 2", font_size=21, color=GREY_A),
            label(rf"the mixed one: \ each goes with chance {c['p_dare']:.2f}; \\ crashes happen, \ each expects "
                  rf"{c['mixed']:.2f}", font_size=21, color=DEFECT),
            label(r"a light that randomizes, \ and tells each only their own colour", font_size=21, color=AMBER),
            label(r"told stop, \ the other goes a third of the time: \\ stopping is as good as going; \ told go, \ "
                  r"the other stops", font_size=19, color=GREY_A),
            label(rf"obeying is an equilibrium, \ and each expects {c['ce']:.2f}", font_size=22, color=EQ),
            label(r"Aumann (1974): \ a correlated equilibrium", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Aumann, Journal of Mathematical Economics 1(1) (1974)", corner=DR, font_size=13)
        with self.voiceover(
            "Sometimes something outside the game can coordinate the players better than they can alone. "
            "<bookmark mark='a'/> Two drivers reach a crossing at once. It is chicken again: each would like to go "
            "while the other stops, and if both go they crash. <bookmark mark='b'/> The pure equilibria have one "
            "driver always giving way: seven for one, two for the other. <bookmark mark='c'/> The mixed equilibrium "
            "is fair, but each goes a third of the time, crashes happen, and each expects four and two thirds. "
            "<bookmark mark='d'/> Now add a traffic light that picks one of three signals at random and tells each "
            "driver only their own colour: Ana go and Bo stop a quarter of the time, the reverse a quarter of the "
            "time, both stop half the time, and never both go. <bookmark mark='e'/> A driver told to stop knows "
            "the other is going one time in three, which makes stopping as good as going; a driver told to go knows "
            "the other has been told to stop. <bookmark mark='f'/> Obeying the light is an equilibrium, and each driver expects five and a "
            "quarter, better than the mixed equilibrium, and fair. <bookmark mark='g'/> Robert Aumann called it a "
            "correlated equilibrium in 1974. Traffic lights, conventions and even prices can play the role of the "
            "light."
        ) as vo:
            self.play(FadeIn(mat), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(frame_cell(mat, 0, 1)), Create(frame_cell(mat, 1, 0)), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(light), FadeIn(probs), FadeIn(sig), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
            vo.wait_until("g")
            self.play(FadeIn(side[6]))
        self.clear_scene()
