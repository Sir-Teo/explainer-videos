from __future__ import annotations

from videos.economics.econ62.common import *  # noqa: F403


class Experiment(VoiceoverScene):
    def construct(self):
        card(self, 4, r"The experiment, \ and why they had not done it", r"Does management cause productivity, \ and "
             r"why would an owner leave money on the floor?", "Chapter four. The experiment, and why they had not "
             "done it.", lit={2013: r"Bloom et al.", 2018: r"Bruhn, Karlan and Schoar"}, scale=("firm",),
             horizon=("a year", "a decade"))
        self.paths()
        self.why()

    def paths(self):
        X = load("experiment")
        tr, ct = np.array(X["paths"]["treated"]), np.array(X["paths"]["control"])
        w = np.arange(X["weeks"])
        tr = tr - tr[: X["start"]].mean()
        ct = ct - ct[: X["start"]].mean()
        ax = plane([0, X["weeks"]], [-0.15, 0.35], center=LEFT * 2.9 + DOWN * 0.4, x_length=6.6, y_length=4.4,
                   xticks=[0, 40, 70, 100, 140], yticks=[-0.1, 0, 0.1, 0.2, 0.3], xlabel=r"week",
                   ylabel=r"log productivity, \ against before", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:+.1f}".replace("-", "{-}") if v else "0", font_size=14)
        start = vline(ax, X["start"], -0.15, 0.35, WHITE, 1.4)
        ramp = shade(ax, [(X["start"], X["start"] + X["ramp"])], -0.15, 0.35, RECESS, 0.5)
        pt = path(ax, w, tr, TREAT, 2.6, smooth=False)
        pc = path(ax, w, ct, CTRL, 2.6, smooth=False)
        side = VGroup(
            label(rf"{X['plants']} plants in {X['firms']} firms; \ consulting for {X['treated_firms']} firms, \ chosen "
                  r"at random", font_size=19, color=WHITE),
            label(r"green: \ treated plants; \ grey: \ the others", font_size=19, color=TREAT),
            label(r"shaded: \ the practices phase in", font_size=19, color=GREY_A),
            label(rf"this run's estimate: \ +{100 * X['first_est']:.0f}\% \ ($\pm${200 * X['first_se']:.0f}, "
                  r"clustered by firm)", font_size=20, color=TREAT),
            label(rf"over 400 reruns: \ centred on +{100 * X['mean_est']:.0f}\%, \ spread "
                  rf"$\pm${100 * X['sd_est']:.0f} points", font_size=19, color=GREY_A),
            label(r"seventeen firms are few: \ the spread is the price", font_size=19, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        if side.width > 6.0:
            side.width = 6.0
            side.to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ agora.org.experiment; \ the practices' effect (17\%) planted", corner=DL,
                         font_size=12)
        with self.voiceover(
            "The Island runs its own version of the experiment. <bookmark mark='a'/> Twenty-eight plants in "
            "seventeen firms; eleven firms, chosen at random, get the consultants. Randomizing by firm matters: "
            "plants in the same firm share an owner, and would share the practices. <bookmark mark='b'/> Here is "
            "weekly productivity, treated plants in green and the others in grey, measured against each plant's "
            "own past. <bookmark mark='c'/> The practices phase in over thirty weeks. <bookmark mark='d'/> "
            f"Difference in differences over the following year: {100 * X['first_est']:.0f} percent higher, give "
            f"or take {200 * X['first_se']:.0f}, with the uncertainty computed firm by firm. <bookmark mark='e'/> "
            "Run the experiment many times on the Island and the estimates centre on the planted seventeen percent, "
            f"scattering by about {100 * X['sd_est']:.0f} points either way. <bookmark mark='f'/> That spread is the "
            "price of an experiment with seventeen firms, and it is why the real study's result, seventeen percent "
            "in the first year, was a surprise worth replicating."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(pc), Create(pt), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(ramp), Create(start), FadeIn(side[2]))
            for k, mk in enumerate("def"):
                vo.wait_until(mk)
                self.play(FadeIn(side[3 + k]))
        self.clear_scene()

    def why(self):
        cards = point_cards([
            (r"they did not know", r"many owners had not heard of the practices, \ or did not believe they would "
             r"help their plant: \ the study's main explanation", MGR),
            (r"they had no time", r"owners ran everything themselves and would not delegate beyond the family, \ so "
             r"firms could not grow past what one person could watch", OWN),
            (r"nothing forced them", r"protected, \ fragmented markets let badly run firms survive: \ chapter one's "
             r"weak competition", COST),
            (r"elsewhere too", r"Mexico, \ 432 small firms: \ a year of consulting raised productivity, \ and "
             r"employment about 50\% five years on \ (Bruhn, \ Karlan and Schoar)", PLANT),
        ], width=12.6, cols=2, font_size=20).move_to(DOWN * 0.2)
        head = label(r"why the money was left on the floor", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Bloom et al., \ QJE 128(1) (2013); \ Bruhn, \ Karlan and Schoar, \ JPE 126(2) (2018)",
                            corner=DL, font_size=12)
        with self.voiceover(
            "So why had the owners not done it? <bookmark mark='a'/> The study's main answer is information: many "
            "owners had not heard of the practices, or did not believe they would help their own plant, until they "
            "saw them work. <bookmark mark='b'/> Time is the second: the owners ran everything themselves and "
            "would not delegate beyond the family, so their firms could not grow beyond what one person could "
            "watch. <bookmark mark='c'/> And nothing forced them: in protected, fragmented markets, badly run firms "
            "survive, chapter one's weak competition again. <bookmark mark='d'/> The result has travelled. In "
            "Mexico, Miriam Bruhn, Dean Karlan and Antoinette Schoar gave a year of consulting to small firms "
            "chosen at random among four hundred and thirty-two; productivity rose, and five years later the "
            "treated firms employed about half as many people again."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()
