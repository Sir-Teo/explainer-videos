from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs48.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES


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
        head = label(rf"Part {PART}: \ System Design I: \ Building Blocks", font_size=34).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(label(r"users $\to$ QPS $\to$ TB", font_size=40, color=HEAD), r"the napkin", HEAD),
            tile(label(r"two choices", font_size=44, color=DATA), r"load balancing", DATA),
            tile(MathTex(r"\textstyle\sum_i p_i(1-e^{-p_i T})", font_size=40, color=YES), r"Che's approximation", YES),
            tile(MathTex(r"\Delta \beta \ln U", font_size=56, color=NO), r"early expiration", NO),
            tile(MathTex(r"\sigma + \rho t", font_size=60, color=LAM), r"token buckets", LAM),
            tile(label(r"Hilbert $>$ Z-order", font_size=40, color=KERN), r"maps as keys", KERN),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. A napkin that turns daily users into queries per second, terabytes and "
            "bandwidth. Load balancing by two random choices and Maglev's table, which barely moves anything when a "
            "server leaves. Caches whose hit rates Che's formula predicts, and an admission filter that beats LRU. "
            "Stampedes, and the probabilistic early refresh that removes them. Token buckets, and why a fixed window "
            "lets through twice its limit. Identifiers that sort by time, and why random keys scatter a B-tree. "
            "Curves that turn a map into keys. And the Job as a service, whose tail more than doubled its capacity "
            "with a small cache. One idea runs through it: estimate first, and let the numbers choose the blocks."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"eight whole systems designed from these blocks", [49]),
            (r"SLOs, \ capacity planning and incidents", [50]),
            (r"spectral views of load and expansion", [56]),
            (r"the theory of distributed algorithms behind the blocks", [59]),
            (r"hardware that changes the napkin's numbers", [60]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 49 designs eight whole systems, from a URL shortener to a ride-hailing "
            "service, with these blocks. Part 50 keeps them running, with service-level objectives and capacity "
            "plans. Part 56 looks at load and expansion through the spectrum of a graph, Part 59 at the theory of "
            "the distributed algorithms underneath, and Part 60 at hardware that keeps changing the napkin's "
            "numbers."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"estimate", r"QPS at the peak, \ storage over years, \ bandwidth out; \ to within a factor of a few"),
            (r"balance", r"least-loaded of two random choices; \ Maglev or rendezvous hashing for affinity"),
            (r"cache", r"measure the hit rate; \ jittered TTLs, \ request coalescing, \ early refresh"),
            (r"limit", r"token buckets at the edge; \ sliding windows, \ not fixed ones"),
            (r"keys", r"time-ordered IDs for B-trees; \ shard keys that spread hot data"),
        ])
        with self.voiceover(
            "In practice. Estimate the peak queries per second, the storage over years and the bandwidth, to within "
            "a factor of a few, before drawing a box. Balance with the less loaded of two random choices, and hash "
            "consistently where affinity matters. Measure your cache's hit rate, jitter its expiry times, coalesce "
            "identical requests and refresh popular entries early. Put token buckets at the edge, and use sliding "
            "windows rather than fixed ones. And choose time-ordered identifiers for B-trees, and shard keys that "
            "spread the hot data."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Show that removing one of $n$ backends from a consistent-hash ring moves only the keys it owned, \ and "
            r"compute the load imbalance with $v$ virtual nodes.",
            r"Derive Che's approximation for LRU under independent references, \ and check it against a simulation.",
            r"Show that XFetch's early-refresh rule makes the expected number of concurrent rebuilds at expiry "
            r"$O(1)$.",
            r"Prove that a token bucket with rate $\rho$ and depth $\sigma$ admits at most $\sigma + \rho t$ requests "
            r"in any interval of length $t$.",
            r"\textit{Build.} \ Add request coalescing to the Job service \ (one rebuild per missing key) \ and "
            r"measure p99 during a cache flush.",
            r"$\bigstar$ \textit{Research.} \ A cache admission policy with a provable competitive ratio on drifting "
            r"Zipf traffic.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: add request coalescing to the Job service, so that each missing key is rebuilt once, and "
            "measure the tail while the cache is flushed. The last, marked with a star, is a research problem: an "
            "admission policy with a proof of how close it stays to the best cache when popularity drifts."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 49, \ System Design II: \ Case Studies", font_size=40).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"a URL shortener, \ a news feed, \ a chat service", HEAD),
            (r"a video platform, \ a ride-hailing dispatcher", DATA),
            (r"each from the napkin up, \ stress-tested in simulation", YES))]).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "Next time, Part 49: system design case studies. Eight systems everyone uses, a URL shortener, a news "
            "feed, a chat service, a video platform, a ride-hailing dispatcher and more, each designed from the "
            "napkin up with this part's blocks, and stress-tested in simulation."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Kleppmann, \textit{Designing Data-Intensive Applications}; \ Xu, \textit{System Design Interview}",
             r"Barroso, \ H\"olzle and Ranganathan, \textit{The Datacenter as a Computer}"],
            [r"Eisenbud et al. \ (2016, \ Maglev); \ Mitzenmacher \ (2001, \ two choices); \ Che et al. \ (2002)",
             r"Einziger, \ Friedman and Manes \ (2017, \ TinyLFU); \ Vattani et al. \ (2015); \ Nishtala et al. \ "
             r"(2013)",
             r"Kraska et al. \ (2018); \ Ferragina and Vinciguerra \ (2020); \ Bronson et al. \ (2021)",
             r"RFC 9562 \ (UUIDs, \ 2024); \ Google's S2 geometry library; \ Uber's H3"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(2.0)


_ = (NO, YES, KERN, LAM, DATA)
