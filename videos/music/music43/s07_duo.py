from __future__ import annotations

import numpy as np

from videos.music.music43.common import *  # noqa: F403

CASE_C = {"both listen": TUNE, "nobody listens": EAR, "one over-corrects": BLUE}


class Duo(SoundScene):
    def construct(self):
        chapter(self, 6, r"Playing together", r"How do two players stay together?")
        self.model()
        self.quiz()
        self.curve()
        self.nma()
        self.meaning()

    # ------------------------------------------------------------------
    def model(self):
        rows_ = text_rows([
            (r"each player has an inner timekeeper: \ the next beat is due one period after the last, \ give or take", WHITE),
            (r"each hears the asynchrony: \ how far the partner's last note was from their own", WHITE),
            (r"and corrects by a fraction $\alpha$ of it: \ $t_{k+1} = t_k + T - \alpha\,(t_k - u_k) + \text{noise}$", TUNE),
            (r"for a duo, \ the asynchrony obeys \ $A_{k+1} = (1 - \alpha_1 - \alpha_2)\,A_k + \text{noise}$", WHITE),
            (r"Vorberg and Wing \ (1996): \ linear phase correction, \ the standard model of synchronization", GREY_A),
        ])
        head = label(r"linear phase correction", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "How do two players stay together? The standard model is simple. <bookmark mark='a'/> Each player has an inner "
            "timekeeper: the next note is due one period after the last, give or take some noise. <bookmark mark='b'/> Each "
            "hears the asynchrony, how far the partner's last note was from their own, <bookmark mark='c'/> and corrects the "
            "next note by a fraction alpha of it. <bookmark mark='d'/> For a duo, the asynchrony then shrinks each beat by "
            "the factor one minus the two players' alphas, plus fresh noise. <bookmark mark='e'/> This is Dirk Vorberg and "
            "Alan Wing's linear phase correction model, from 1996."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_.copy().set_opacity(0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plot(self, ms, col, title, w=3.6, h=1.6, lim=280):
        n = len(ms)
        ax = VGroup(Line([0, 0, 0], [w, 0, 0], color=GREY_D), Line([0, -h / 2, 0], [0, h / 2, 0], color=GREY_D))
        pts = [[w * i / (n - 1), max(min(v / lim, 1), -1) * h / 2, 0] for i, v in enumerate(ms)]
        line = VMobject(color=col, stroke_width=3).set_points_as_corners(pts)
        dots = VGroup(*[Dot(p, radius=0.04, color=col) for p in pts])
        return VGroup(label(title, font_size=18, color=col), VGroup(ax, line, dots)).arrange(DOWN, buff=0.2)

    def quiz(self):
        d = load("duo")
        c = clip("duo.three")
        card = listen_card(r"Three duos, \ each playing 24 beats, \ one on a high note and one on a low. \ "
                           r"In one of them nobody listens to the other. \ Which?", width=10.4)
        with self.voiceover(
            "A question for your ears. Three model duos, each playing twenty-four beats, one player on a high note and one "
            "on a low note. Their inner tempos differ by a little over two per cent. In one duo, nobody listens to the "
            "other. Which one?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        order = d["order"]
        boxes = VGroup(*[VGroup(RoundedRectangle(width=3.0, height=1.2, corner_radius=0.15, stroke_color=GREY_B), label(t, font_size=24, color=WHITE)).arrange(DOWN, buff=-0.8)
                         for t in (r"first", r"second", r"third")]).arrange(RIGHT, buff=1.0).move_to(UP * 1.2)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"three duos", detail=r"Part 7's piano, \ model players", corner=DL, tag_corner=DR)
            for i, k in enumerate(order):
                end = st[order[i + 1]] - 0.4 if i + 1 < len(order) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.08)
        plots = VGroup(*[self.plot(d["cases"][k]["asynchrony_ms"], CASE_C[k], k) for k in order]).arrange(RIGHT, buff=0.7).move_to(DOWN * 1.3)
        for p_, b in zip(plots, boxes):
            p_.set_x(b.get_x())
        cap = label(r"asynchrony, \ beat by beat \ (the scale runs to $\pm$280 ms)", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.25)
        cs = d["cases"]
        with self.voiceover(
            "The second. With nobody correcting, the small difference in tempo accumulates, and the low player falls "
            f"{say(cs['nobody listens']['final_ms'])} milliseconds behind by the last beat. In the first duo both correct by "
            "a quarter of each asynchrony, and they stay within a few tens of milliseconds. The third is the strange one: one "
            "player corrects by more than the whole asynchrony, so every correction overshoots, and the duo shakes itself "
            "apart, alternating sides by more and more."
        ):
            self.play(FadeIn(plots), FadeIn(cap), boxes[1][0].animate.set_stroke(EAR, 4))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curve(self):
        d = load("duo_curve")
        al, ex, sm = np.array(d["alpha"]), np.array(d["exact_ms"]), np.array(d["sim_ms"])
        x0, y0, W, H = -5.0, -2.0, 7.4, 3.6
        top = 60.0
        def P_(a, v):
            return [x0 + W * a / 2.0, y0 + H * min(v, top) / top, 0]
        ax = VGroup(Line([x0, y0, 0], [x0 + W, y0, 0], color=GREY_B), Line([x0, y0, 0], [x0, y0 + H, 0], color=GREY_B))
        line = VMobject(color=TUNE, stroke_width=4).set_points_as_corners([P_(a, v) for a, v in zip(al, ex)])
        dots = VGroup(*[Dot(P_(a, v), radius=0.05, color=BLUE) for a, v in zip(al, sm)])
        walls = VGroup(DashedLine([x0, y0, 0], [x0, y0 + H, 0], color=EAR), DashedLine([x0 + W, y0, 0], [x0 + W, y0 + H, 0], color=EAR))
        best = Dot(P_(d["best_alpha"], d["best_ms"]), radius=0.1, color=WHITE)
        labs = VGroup(label(r"total correction $\alpha_1 + \alpha_2$", font_size=16, color=GREY_A).move_to([x0 + W / 2, y0 - 0.45, 0]),
                      label(r"0", font_size=14, color=GREY_A).move_to([x0, y0 - 0.2, 0]), label(r"1", font_size=14, color=GREY_A).move_to([x0 + W / 2, y0 - 0.2, 0]),
                      label(r"2", font_size=14, color=GREY_A).move_to([x0 + W, y0 - 0.2, 0]),
                      label(r"spread of the asynchrony \ (ms)", font_size=16, color=GREY_A).move_to([x0 + 1.4, y0 + H + 0.3, 0]),
                      label(rf"best: \ {d['best_alpha']:.2f}, \ {d['best_ms']:.0f} ms", font_size=16, color=WHITE).next_to(best, DOWN, buff=0.2))
        side = VGroup(label(r"gold: \ the exact formula", font_size=18, color=TUNE), label(r"blue: \ 3,000 simulated beats each", font_size=18, color=BLUE),
                      label(r"stable only between 0 and 2", font_size=18, color=EAR), label(rf"timekeeper noise {d['timer_ms']:.0f} ms, \ motor noise {d['motor_ms']:.0f} ms", font_size=16, color=GREY_A)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * 4.9 + UP * 0.3)
        head = label(r"how much should a player correct?", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "How much should players correct? <bookmark mark='a'/> The asynchrony's spread can be written in closed form: it "
            "is finite only when the total correction lies between zero and two, the walls of stability. "
            "<bookmark mark='b'/> Simulations, three thousand beats for each point, sit on the formula. "
            f"<bookmark mark='c'/> The best total, for these noise levels, is about {say(d['best_alpha'], 2)}: a little less "
            "than correcting the whole asynchrony at once, because some of what is heard is motor noise that will not repeat."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(labs[:5]), FadeIn(walls))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(side[0]), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(FadeIn(dots), FadeIn(side[1]), FadeIn(side[3]))
            vo.wait_until("c")
            self.play(FadeIn(best), FadeIn(labs[5]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def meaning(self):
        items = [
            (r"tapping experiments \ (Repp's reviews, \ 2005 and 2013) \ find people correct by roughly a quarter to a half", WHITE),
            (r"a leader who corrects little and a follower who corrects a lot stay together just as well", WHITE),
            (r"so `who leads' is a question about the alphas: \ it can be measured from recordings", WHITE),
            (r"over-correcting is real: \ ensembles that chase each other's errors rush and drag in turn", TUNE),
            (r"chapter 7: \ four players, \ and a conductor", GREY_A),
        ]
        rows_scene(self, r"what the model says", items,
                   "What does this say about real players? <bookmark mark='b'/> Tapping experiments, reviewed by Bruno Repp in "
                   "2005 and 2013, find people correct by roughly a quarter to a half of each asynchrony. "
                   "<bookmark mark='c'/> A leader who corrects little and a follower who corrects a lot stay together just as "
                   "well as two equals, <bookmark mark='d'/> so who leads is a question about the alphas, and it can be measured "
                   "from recordings. <bookmark mark='e'/> Over-correcting is real too: ensembles that chase each other's errors "
                   "rush and drag in turn. <bookmark mark='f'/> Chapter seven adds two more players, and a conductor.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def nma(self):
        items = [
            (r"tap along with a metronome and you will tap early: \ typically 20 to 50 ms before the click", WHITE),
            (r"the `negative mean asynchrony': \ found in almost every tapping study, \ smaller in musicians", WHITE),
            (r"one explanation: \ the brain times the feel of the tap, \ which reaches it later than the sound of the click", WHITE),
            (r"ensembles have their own offsets: \ the lead player's onset is not the only `true' beat", TUNE),
            (r"synchronization is prediction, \ not reaction: \ a reaction would take 150 ms or more", GREY_A),
        ]
        rows_scene(self, r"early, \ on purpose", items,
                   "One more finding from tapping. <bookmark mark='b'/> Tap along with a metronome and you will tap early, "
                   "typically twenty to fifty milliseconds before the click: the negative mean asynchrony, found in almost every "
                   "tapping study and smaller in musicians. <bookmark mark='c'/> One explanation is that the brain times the "
                   "feel of the tap, which reaches it later than the sound of the click. <bookmark mark='d'/> Ensembles have "
                   "offsets of their own, so the lead player's onset is not the only true beat. <bookmark mark='e'/> And all of "
                   "this is prediction, not reaction: a reaction to a sound takes a hundred and fifty milliseconds or more, far "
                   "too slow to play together.", marks="bcde")
