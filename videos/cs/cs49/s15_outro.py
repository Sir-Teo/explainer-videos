from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs49.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES


def tile(content, caption, color, TW=3.6, TH=2.3):
    frame = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                             stroke_width=1.5, fill_color=BG, fill_opacity=1)
    if content.width > TW:
        content.scale_to_fit_width(TW)
    if content.height > TH:
        content.scale_to_fit_height(TH)
    content.move_to(frame.get_center() + UP * 0.25)
    cap = label(caption, font_size=22, color=color).move_to(frame.get_bottom() + UP * 0.3)
    return Group(frame, content, cap)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.practice()
        self.problems()
        self.next_time()
        self.references()

    def recap(self):
        head = label(rf"Part {PART}: \ System Design II: \ Case Studies", font_size=34).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(MathTex(r"\lceil \log_{62} N \rceil", font_size=56, color=HEAD), r"short IDs", HEAD),
            tile(label(r"push, \ pull, \ or both", font_size=40, color=DATA), r"feed fan-out", DATA),
            tile(label(r"assign, \ not grab", font_size=44, color=KERN), r"dispatch", KERN),
            tile(label(r"buffer $\to$ bitrate", font_size=40, color=NO), r"adaptive streaming", NO),
            tile(MathTex(r"\textstyle\sum = 0", font_size=60, color=YES), r"the ledger", YES),
            tile(label(r"transform, \ or CRDT", font_size=40, color=LAM), r"collaborative editing", LAM),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. A shortener whose identifiers are sized by a logarithm and protected by the "
            "birthday bound. A feed whose fan-out is chosen on a power-law graph, pushing for most users and pulling "
            "for celebrities. A crawler that is fast only by being polite to many hosts at once. A dispatcher that "
            "assigns riders in batches rather than grabbing the nearest driver. Bitrate adaptation as a control loop "
            "that trades quality against stalls. A ledger whose entries always sum to zero, and whose payments are "
            "charged once. Editors that converge. And the Job, at a million books a day, for a hundredth of a cent a "
            "book. One idea runs through it: every design is a few hard ideas, and you have met them all before."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"running these systems: \ SLOs, \ incidents, \ capacity", [50]),
            (r"rendering video and graphics", [51]),
            (r"proving protocols and ledgers correct", [54]),
            (r"trusting the software these systems run", [55]),
            (r"the theory of distributed algorithms", [59]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 50 runs these systems, with service-level objectives, incident response and "
            "capacity planning. Part 51 opens the graphics and video pipelines behind the streaming service. Part 54 "
            "proves protocols and ledgers correct. Part 55 asks whether we can trust the software these systems run "
            "on. And Part 59 returns to the theory of distributed algorithms underneath them all."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"start", r"requirements and the napkin before boxes"),
            (r"choose", r"the one hard part, \ and spend the design budget there"),
            (r"name", r"every trade-off you made, \ and what you gave up"),
            (r"fail", r"design the error paths and the deploys, \ not only the happy path"),
            (r"test", r"simulate the design under load and failure before building it"),
        ])
        with self.voiceover(
            "In practice. Write requirements and do the napkin arithmetic before drawing any boxes. Find the one hard "
            "part of the problem and spend your design effort there. Name every trade-off you make, and what you "
            "gave up for it. Design the error paths and the way changes are deployed, not only the happy path. And "
            "simulate the design under load and failure before you build it."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"How many base62 characters does a shortener need for $10^{12}$ links, \ and how many collisions does a "
            r"7-character truncated hash give at $10^8$?",
            r"For followers drawn from a power law with exponent $\alpha$, \ derive the expected cost of fan-out on "
            r"write and on read, \ and the best celebrity threshold.",
            r"Show that a batched assignment never has a larger total pickup distance than greedy, \ and give an "
            r"example where it is much smaller.",
            r"Prove that double-entry posting preserves $\sum$ balances $= 0$, \ and that idempotency keys prevent "
            r"double charges under retries.",
            r"\textit{Build.} \ Add hinted handoff to a three-replica store, \ and measure availability and stale "
            r"reads when one node is partitioned.",
            r"$\bigstar$ \textit{Research.} \ The provably optimal fan-out policy for a power-law follower graph.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: add hinted handoff to a three-replica store and measure what it buys when one node is cut off. "
            "The last, marked with a star, is a research problem: the fan-out policy that provably minimizes a feed's "
            "work on a power-law graph."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 50, \ Keeping It Running", font_size=40).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"availability in series and in parallel", HEAD),
            (r"error budgets: \ reliability as a resource", YES),
            (r"alerts as hypothesis tests", DATA),
            (r"incidents, \ post-mortems and capacity", LAM))]).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "Next time, Part 50: keeping it running. A system is only as good as its worst hour, and reliability "
            "engineering turns that into mathematics: availability composed in series and in parallel, error budgets "
            "that make reliability a resource to spend, alerts as hypothesis tests, and incidents and the "
            "post-mortems that learn from them."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Kleppmann, \textit{Designing Data-Intensive Applications}; \ Xu, \textit{System Design Interview}, "
             r"\ vols. 1--2",
             r"Beyer et al., \textit{Site Reliability Engineering}"],
            [r"DeCandia et al. \ (2007, \ Dynamo); \ Ellis and Gibbs \ (1989, \ OT); \ Shapiro et al. \ (2011, \ "
             r"CRDTs)",
             r"Huang et al. \ (2014, \ BBA); \ Yin et al. \ (2015, \ MPC); \ Kuhn \ (1955, \ assignment)",
             r"Yuan et al. \ (2014); \ Gunawi et al. \ (2016); \ Bloom \ (1970)",
             r"Heydon and Najork \ (1999, \ Mercator); \ Perrin and Marlinspike \ (2016, \ double ratchet)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(2.0)


_ = (NO, YES, KERN, LAM, DATA)
