from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs45.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES


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
        head = label(rf"Part {PART}: \ The Cloud", font_size=34).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(MathTex(r"\text{desired} - \text{actual}", font_size=44, color=YES), r"reconciliation", YES),
            tile(MathTex(r"\tfrac{11}{9}\,\mathrm{OPT} + \tfrac{6}{9}", font_size=52, color=HEAD), r"first fit decreasing",
                 HEAD),
            tile(MathTex(r"u_{t} = K\,e_{t-d}", font_size=56, color=KERN), r"autoscaling", KERN),
            tile(MathTex(r"C(c, a)", font_size=60, color=DATA), r"Erlang C", DATA),
            tile(MathTex(r"\text{MTTDL}", font_size=56, color=LAM), r"durability", LAM),
            tile(label(r"\$ per request", font_size=40, color=NO), r"the bill", NO),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. Control loops that compare what should be with what is and close the gap, "
            "and stay correct when events are lost. Scheduling as bin packing, NP-hard, with heuristics that come "
            "within a few percent of optimal when they can sort the work first. Autoscalers as feedback "
            "controllers, which settle or oscillate depending on their gain and their delay, and Erlang's formula "
            "for how many servers a queue needs. Durability derived from a Markov chain, and the correlated failures "
            "that decide it in practice. And a bill for everything. One idea runs through it: the cloud is the "
            "series' ideas at the scale of buildings, with a price on every decision."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"logs, \ streams and warehouses in the cloud", [46]),
            (r"search engines on thousands of machines", [47]),
            (r"system design: \ load balancers, \ caches, \ queues", [48, 49]),
            (r"incidents, \ SLOs and capacity planning", [50]),
            (r"accelerators and the hardware of the datacentre", [60]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 46 builds logs, streams and warehouses on this infrastructure. Part 47 "
            "runs a search engine across thousands of machines. Parts 48 and 49 design whole systems from load "
            "balancers, caches and queues. Part 50 keeps them running, with service-level objectives and capacity "
            "plans. And Part 60 opens the accelerators that now fill the datacentre."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"declare", r"desired state in code; \ let controllers converge; \ never fix production by hand"),
            (r"size", r"requests and limits from measurements; \ pack by every resource, \ not just CPU"),
            (r"scale", r"modest gain, \ short delays, \ scale up fast and down slowly"),
            (r"store", r"spread replicas across zones and racks; \ test restores, \ not just backups"),
            (r"pay", r"tag every resource; \ spot for batch with checkpoints; \ watch egress"),
        ])
        with self.voiceover(
            "In practice. Declare the state you want in code, let controllers converge on it, and never fix "
            "production by hand. Size containers from measurements, and pack them by every resource, not just "
            "processor time. Scale with modest gain and short measurement delays, quickly up and slowly down. "
            "Spread replicas across zones and racks, and test restoring your data, not just backing it up. And tag "
            "every resource with its owner, run batch work on spot capacity with checkpoints, and watch the cost of "
            "moving data out."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Prove that next fit uses at most twice the optimal number of bins, \ and give inputs on which it uses "
            r"nearly twice.",
            r"Show that bin packing is NP-hard by reducing partition to deciding whether two bins suffice.",
            r"Derive Erlang C from the birth--death chain of an M/M/c queue, \ and the mean wait from it.",
            r"Derive the mean time to data loss for $n$ fragments of which any $k$ suffice, \ with failure rate "
            r"$\lambda$ per fragment and one repair at a time at rate $\mu$.",
            r"\textit{Build.} \ Add a reconciler for a second resource that depends on the first, \ and show it "
            r"converges in dependency order after random deletions.",
            r"$\bigstar$ \textit{Research.} \ Online vector bin packing of jobs with unknown lifetimes, \ with "
            r"predictions: \ near optimal when accurate, \ robust when not.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: give our reconciler a second kind of resource that depends on the first, and show that it "
            "converges in the right order after random deletions. The last, marked with a star, is a research "
            "problem: packing jobs whose lifetimes are unknown, helped by predictions that may be wrong."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 46, \ Logs, \ Streams and Warehouses", font_size=40).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"the log as the unifying abstraction", HEAD),
            (r"stream processing: \ windows, \ watermarks and late events", DATA),
            (r"column stores and why they compress", YES),
            (r"the Job as a live top twenty over a stream of novels", LAM))]).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "Next time, Part 46: logs, streams and warehouses. Every company's data ends up in an append-only log "
            "and a column-oriented warehouse, with stream processors in between computing answers continuously, and "
            "the hard part is time: events that arrive late, out of order and more than once. The Job becomes a live "
            "top twenty over a stream of novels."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Barroso, \ H\"olzle and Ranganathan, \textit{The Datacenter as a Computer}; \ Morris, "
             r"\textit{Infrastructure as Code}",
             r"Burns, \ Beda and Hightower, \textit{Kubernetes: Up and Running}"],
            [r"Verma et al. \ (2015, \ Borg); \ Burns et al. \ (2016); \ Agache et al. \ (2020, \ Firecracker)",
             r"Armbrust et al. \ (2010); \ Jonas et al. \ (2019); \ Coffman, \ Garey and Johnson; \ D\'osa \ (2007)",
             r"Young \ (1974); \ Lykouris and Vassilvitskii \ (2018); \ International Energy Agency \ (2024)",
             r"AWS list prices \ (us-east-1, \ 2024)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(2.0)


_ = (NO, YES, KERN, LAM, DATA)
