from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs43.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES


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
        head = label(rf"Part {PART}: \ APIs and Services", font_size=34).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(label(r"\texttt{96 01}", font_size=56, color=DATA), r"varints", DATA),
            tile(MathTex(r"\text{new} <: \text{old}", font_size=52, color=HEAD), r"schema evolution", HEAD),
            tile(MathTex(r"\text{exactly} = \text{at least} + \text{dedup}", font_size=36, color=YES),
                 r"delivery", YES),
            tile(label(r"backoff, \ jitter, \ budgets", font_size=34, color=KERN), r"retry storms", KERN),
            tile(label(r"do, \ undo", font_size=48, color=LAM), r"sagas and outboxes", LAM),
            tile(MathTex(r"1-(1-p)^k", font_size=56, color=NO), r"fan-out tails", NO),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. Protocol Buffers' wire format from first principles, byte for byte "
            "against the published examples, and schema evolution as a question about subtypes. Pagination with "
            "offsets that repeats rows and pagination with cursors that never does. Exactly-once delivery, checked "
            "in every execution of a model, as at-least-once delivery plus deduplication. Retry storms, and the "
            "backoff and budgets that end them. Outboxes that turn lost events into duplicates we can remove, and "
            "sagas that undo what they cannot finish. And tails that grow with fan-out. One idea runs through it: "
            "a remote call can fail in ways a local one cannot, so every message must be safe to lose, and safe to "
            "repeat."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"experiments that measure what an API change does to people", [44]),
            (r"services on rented machines, \ autoscaled", [45]),
            (r"logs, \ streams and change data capture", [46]),
            (r"system design from these building blocks", [48, 49]),
            (r"incidents, \ SLOs and error budgets", [50]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 44 measures what a change does to the people who use it, with controlled "
            "experiments. Part 45 runs services on rented machines that come and go. Part 46 turns the outbox into "
            "a stream, with logs and change data capture. Parts 48 and 49 design whole systems from these blocks. "
            "And Part 50 keeps them running, with service-level objectives and error budgets."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"design", r"additive changes only; \ never reuse a field number; \ cursors, \ not offsets"),
            (r"calls", r"a deadline on every call, \ passed down; \ retries with backoff, \ jitter and a budget"),
            (r"effects", r"idempotency keys on every write; \ the outbox, \ not two writes"),
            (r"workflows", r"sagas with idempotent compensations; \ dead-letter queues that someone reads"),
            (r"trust", r"mTLS between services; \ pin the token algorithm; \ store times in UTC"),
        ])
        with self.voiceover(
            "In practice. Change APIs only by adding, never reuse a field number, and page with cursors rather "
            "than offsets. Put a deadline on every call and pass it down, and retry with backoff, jitter and a "
            "budget. Give every write an idempotency key, and publish events through an outbox rather than two "
            "separate writes. Build workflows as sagas whose compensations are themselves idempotent, and make sure "
            "someone reads the dead-letter queue. Authenticate services to each other with mutual TLS, pin the "
            "algorithm your tokens are verified with, and store times in UTC."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Encode the message \texttt{\{a: 300, b: -3, c: [1, 2]\}} by hand \ (\texttt{a} an int32, \ "
            r"\texttt{b} an sint32, \ \texttt{c} packed), \ and decode it back.",
            r"Show that adding an optional field is backward and forward compatible, \ and that changing a field's "
            r"type is neither, \ by treating messages as records and compatibility as subtyping.",
            r"Prove that retrying until acknowledged, \ with a receiver that applies each id at most once, \ "
            r"delivers every message exactly once if the network eventually delivers some copy.",
            r"Show that offset pagination over a list receiving $k$ inserts per page repeats about $k$ rows per page, "
            r"\ and that cursor pagination repeats none.",
            r"\textit{Build.} \ Add a saga to our simulator in which the courier step can time out, \ and show that "
            r"an idempotent compensation keeps the invariant.",
            r"$\bigstar$ \textit{Research.} \ A compatibility checker proving that every existing client completes "
            r"every protocol run against a new version, \ under loss, \ duplication and reordering.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: add a courier timeout to our saga, and show that an idempotent compensation keeps every order "
            "consistent. The last, marked with a star, is a research problem: proving that a new version of a "
            "service keeps every existing client working, even on a network that loses, duplicates and reorders."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 44, \ People and Products", font_size=40).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"Fitts's law from Shannon's channel capacity", HEAD),
            (r"Hick's law as the entropy of a choice", DATA),
            (r"perception, \ colour and the formulas behind them", YES),
            (r"A/B tests, \ and the statistics of looking every morning", NO))]).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "Next time, Part 44: people and products. Software is used by people, and both can be measured. "
            "Fitts's law falls out of Shannon's channel capacity, Hick's law is the entropy of a choice, and where "
            "intuition runs out, industry runs controlled experiments, with statistics that are easy to get wrong."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Kleppmann, \textit{Designing Data-Intensive Applications}, \ ch. 4, 11--12; \ Newman, "
             r"\textit{Building Microservices}",
             r"Richardson, \textit{Microservices Patterns}; \ Hohpe and Woolf, \textit{Enterprise Integration "
             r"Patterns}"],
            [r"Birrell and Nelson \ (1984); \ Waldo et al. \ (1994); \ Saltzer, \ Reed and Clark \ (1984)",
             r"Fielding \ (2000); \ Garcia-Molina and Salem \ (1987); \ the Protocol Buffers encoding guide",
             r"RFC 6749 \ (OAuth 2.0); \ RFC 7519 and RFC 8725 \ (JWT); \ RFC 9110 \ (HTTP semantics)",
             r"Newcombe et al. \ (2015); \ Hawblitzel et al. \ (2015); \ Wilcox et al. \ (2015)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(2.0)


_ = (NO, YES, KERN, LAM)
