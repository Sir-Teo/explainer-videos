from __future__ import annotations

from videos.economics.econ67.common import *  # noqa: F403


class Machine(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Economics with AI in the loop", r"What changes when machines read the literature, \ build "
             r"the data \ and propose the hypotheses?", "Chapter twelve. Economics with AI in the loop.",
             lit={2023: "Korinek", 2024: "Ludwig and Mullainathan"}, scale=("world",), horizon=("a decade",))
        self.uses()
        self.hypotheses()
        self.danger()

    def uses(self):
        ch = flow_chain([(r"read the literature", FIRST), (r"build the data", PUB), (r"write the code", TRUE),
                         (r"propose hypotheses", STATE), (r"check the work", ROW)], box_w=2.25, box_h=1.0,
                        font_size=17).move_to(UP * 1.3)
        rows = VGroup(
            label(r"Korinek (2023): \ language models already help with ideas, \ writing, \ background research, \ "
                  r"coding, \ data and mathematics", font_size=20, color=GREY_A),
            label(r"each step faster and cheaper; \ the errors are fluent, \ and need checking", font_size=20,
                  color=FAIL),
            label(r"the scarce skill moves from doing each step to judging the whole", font_size=20,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ch, DOWN, buff=0.7)
        tag = published_tag(r"Korinek, \ `Generative AI for Economic Research', \ \emph{JEL} 61(4) (2023)",
                            corner=DL, font_size=12)
        with self.voiceover(
            "Part sixty-five asked what AI does to the economy. This chapter asks what it does to economics. "
            "<bookmark mark='a'/> A research project is a chain: read the literature, build the data, write the "
            "code, propose a hypothesis, check the work. <bookmark mark='b'/> Anton Korinek catalogued how language "
            "models already help economists at each link, from brainstorming and writing to coding, data and "
            "mathematics. <bookmark mark='c'/> Each step gets faster and cheaper, and the errors get more fluent: a "
            "made-up reference reads like a real one. <bookmark mark='d'/> The scarce skill moves from doing each "
            "step to judging the whole chain."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in ch.boxes], lag_ratio=0.25),
                      LaggedStart(*[Create(a) for a in ch.arrows], lag_ratio=0.25), run_time=2.2)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def hypotheses(self):
        cards = point_cards([
            (r"the question", r"what do judges respond to, \ beyond what the law says they should?", FIRST),
            (r"the machine", r"a model trained on defendants' mug shots alone predicts judges' decisions to "
             r"detain", PUB),
            (r"the hypothesis", r"morphed faces show what the model sees; \ people name it: \ looking `well "
             r"groomed', \ looking `heavy-faced'", TRUE),
            (r"the test", r"the hypotheses must then be tested the old way, \ on data the search did not use",
             STATE),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"machines that propose hypotheses", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Ludwig and Mullainathan, \ \emph{QJE} 139(2) (2024)", corner=DL, font_size=12)
        with self.voiceover(
            "The most interesting use is the newest: machines that suggest what to test. <bookmark mark='a'/> Jens "
            "Ludwig and Sendhil Mullainathan asked what judges respond to when deciding whom to jail before trial. "
            "<bookmark mark='b'/> A deep-learning model shown only the defendants' mug shots predicted the judges' "
            "decisions far better than chance. <bookmark mark='c'/> To learn what it had found, they morphed faces "
            "along the model's predictions and asked people to describe the difference. Two features came out, "
            "looking well groomed and looking heavy-faced, neither in the standard lists of what sways judges. "
            "<bookmark mark='d'/> Hypotheses found this way must then be tested the old way, on data the search did "
            "not use. "
            "The machine proposes; the design disposes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def danger(self):
        Mc = load("machine")
        tries, fp = Mc["tries"], Mc["fp"]
        ax = plane([0, 3], [0, 1], center=LEFT * 2.2 + DOWN * 0.3, x_length=7.0, y_length=4.6,
                   xticks=[0, 1, 2, 3], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"specifications searched \ (no effect is real)", ylabel=r"chance of a significant result",
                   xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"), yfmt=lambda v: f"{100 * v:.0f}\\%",
                   font_size=14)
        lx = np.log10(np.array(tries, float))
        ln = path(ax, lx, fp, FAIL, 3.4, smooth=False)
        dots_ = VGroup(*[Dot(ax.ax.c2p(x, y), radius=0.08, color=FAIL) for x, y in zip(lx, fp)])
        nums = VGroup(*[label(rf"{100 * y:.0f}\%", font_size=16, color=FAIL).next_to(d, UL, buff=0.05)
                        for d, y in zip(dots_, fp)])
        side = VGroup(
            label(r"a person tries a few paths; \\ a machine can try them all", font_size=18, color=FAIL),
            label(r"the defences scale too:", font_size=18, color=GREY_A),
            label(r"hold out data the search never sees", font_size=18, color=TRUE),
            label(r"report the whole specification curve", font_size=18, color=TRUE),
            label(r"correct for the machine's errors \\ by prediction-powered inference \ (Part 64)",
                  font_size=18, color=TRUE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(ax.ax, RIGHT, buff=0.6)
        if side.get_right()[0] > 6.9:
            side.scale_to_fit_width(6.9 - side.get_left()[0])
        tag = island_tag(r"computed: \ agora.field.false\_positive, \ specifications moderately alike", corner=DL,
                         font_size=12)
        with self.voiceover(
            "The danger is chapter six at machine speed. <bookmark mark='a'/> With nothing real to find, one test "
            f"finds something {100 * fp[0]:.0f} percent of the time; ten specifications, {100 * fp[1]:.0f} percent; "
            f"a hundred, {100 * fp[2]:.0f}; a thousand, which a machine can run in a minute, "
            f"{100 * fp[3]:.0f} percent. <bookmark mark='b'/> A person tries a few forking paths; a machine can "
            "walk them all, and report the one that works. <bookmark mark='c'/> The defences scale too: keep data "
            "the search never sees and test there; report the whole specification curve of chapter nine rather "
            "than one point; and when a machine's labels stand in for data, correct for its errors with "
            "prediction-powered inference, from Part sixty-four."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(ln), LaggedStart(*[FadeIn(d) for d in dots_], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(n_) for n_ in nums], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in side[1:]], lag_ratio=0.3), run_time=2.0)
        self.clear_scene()
