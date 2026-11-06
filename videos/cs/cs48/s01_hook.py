from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs48.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load


def si(x: float) -> str:
    for unit, k in (("P", 1e15), ("T", 1e12), ("G", 1e9), ("M", 1e6), ("k", 1e3)):
        if x >= k:
            return f"{x / k:.1f} {unit}"
    return f"{x:.0f}"


class Hook(VoiceoverScene):
    def construct(self):
        self.napkin()
        self.numbers()
        self.blocks()
        self.plan()

    def napkin(self):
        n = load("napkin")
        head = label(r"Design on a napkin", font_size=36).to_edge(UP, buff=0.3)
        paper = RoundedRectangle(width=11.6, height=5.6, corner_radius=0.3, stroke_color=GREY_C, stroke_width=1.5,
                                 fill_color="#151b27", fill_opacity=1).next_to(head, DOWN, buff=0.25)
        lines = [
            (rf"{n['dau'] / 1e6:.0f} million users a day $\times$ {n['requests_per_day'] / n['dau']:.0f} actions",
             rf"$=$ {n['requests_per_day'] / 1e6:.0f} million requests a day", WHITE),
            (r"$\div$ 86,400 seconds", rf"$\approx$ {n['avg_qps']:,.0f} per second on average", DATA),
            (r"$\times$ 3 at the evening peak", rf"$\approx$ {n['peak_qps']:,.0f} per second", HEAD),
            (r"one write in eleven", rf"$\approx$ {n['write_qps']:,.0f} writes per second", YES),
            (rf"2 kB each, \ {n['years']} years, \ {n['replicas']} copies",
             rf"$\approx$ {n['storage_bytes'] / 1e12:.0f} TB", LAM),
            (r"reads at the peak $\times$ 2 kB", rf"$\approx$ {n['read_bandwidth_Bps'] / 1e6:.0f} MB/s out", KERN),
        ]
        rows = VGroup()
        for a, b, c in lines:
            rows.add(VGroup(label(a, font_size=23, color=GREY_A), label(b, font_size=23, color=c)).arrange(RIGHT,
                                                                                                          buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(paper)
        for r in rows:
            r[1].align_to(rows[0][1], LEFT).shift(RIGHT * 0.0)
        note_ = note(r"an illustrative service; \ the arithmetic is the point", font_size=16).next_to(paper, DOWN,
                                                                                                   buff=0.1)
        with self.voiceover(
            "Every design begins on a napkin. <bookmark mark='a'/> Suppose ten million people use a service each "
            "day, twenty times each: two hundred million requests. <bookmark mark='b'/> A day has eighty-six "
            "thousand four hundred seconds, so that is about two thousand three hundred requests a second, on "
            "average. <bookmark mark='c'/> Traffic is not flat: the evening peak might be three times the mean, "
            "nearly seven thousand a second. <bookmark mark='d'/> If one request in eleven writes, about two hundred "
            "writes a second. <bookmark mark='e'/> At two kilobytes a write, kept for five years in three copies, "
            "about two hundred terabytes. <bookmark mark='f'/> And the reads at the peak move a dozen megabytes a "
            "second. Five minutes of arithmetic, and we know this needs a cluster, not a laptop, but not a "
            "datacentre either."
        ) as vo:
            self.play(FadeIn(head), FadeIn(paper), FadeIn(note_))
            for k, mk in enumerate("abcdef"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.15))
        self.wait(0.4)
        self.clear_scene()

    def numbers(self):
        head = label(r"Numbers to carry", font_size=36).to_edge(UP, buff=0.3)
        rows = [[r"main memory reference", r"$\sim$100 ns"], [r"read 1 MB sequentially from memory", r"$\sim$10 $\mu$s"],
                [r"random read from an SSD", r"$\sim$100 $\mu$s"], [r"round trip within a datacentre", r"$\sim$500 $\mu$s"],
                [r"read 1 MB sequentially from SSD", r"$\sim$1 ms"], [r"disk seek", r"$\sim$10 ms"],
                [r"round trip across a continent", r"$\sim$50--100 ms"]]
        tab = grid_table([r"operation", r"order of magnitude"], rows, widths=[6.4, 3.4], row_h=0.5, font_size=20,
                         mono_cols=())
        tab.next_to(head, DOWN, buff=0.4).shift(LEFT * 1.6)
        side = VGroup(label(r"$2^{10} \approx 10^3$", font_size=26, color=HEAD),
                      label(r"$2^{20} \approx 10^6$, \ $2^{30} \approx 10^9$", font_size=22, color=HEAD),
                      label(r"1 day $\approx 10^5$ s", font_size=22, color=DATA),
                      label(r"1 year $\approx \pi \times 10^7$ s", font_size=22, color=DATA)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3).next_to(tab, RIGHT, buff=0.7)
        foot = wrapped_label(r"after Jeff Dean's and Peter Norvig's ``latency numbers every programmer should know''; "
                             r"\ orders of magnitude for current hardware, \ not measurements \ (Part 39 measured "
                             r"some)", 12.4, font_size=18, color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Napkin arithmetic needs a few numbers in your head. <bookmark mark='a'/> A memory reference takes "
            "about a hundred nanoseconds. Reading a megabyte from memory, about ten microseconds; a random read from "
            "a solid-state disk, about a hundred. A round trip inside a datacentre, around half a millisecond. A "
            "spinning disk's seek, ten milliseconds, and a round trip across a continent, fifty to a hundred. "
            "<bookmark mark='b'/> And a few conversions: two to the tenth is about a thousand, a day is about a "
            "hundred thousand seconds, and a year is pi times ten to the seventh. These are orders of magnitude, "
            "after the lists Jeff Dean and Peter Norvig made famous; the point is to be right to within a factor "
            "of a few."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3), run_time=4)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s) for s in side], lag_ratio=0.3), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def blocks(self):
        head = label(r"A small set of blocks", font_size=36).to_edge(UP, buff=0.3)
        names = [(r"load balancer", HEAD), (r"cache", YES), (r"rate limiter", NO), (r"queue", LAM),
                 (r"shards", DATA), (r"replicas", DATA), (r"IDs", KERN), (r"blob store and CDN", GREY_A),
                 (r"geospatial index", KERN)]
        tiles = VGroup()
        for t, c in names:
            r = RoundedRectangle(width=3.6, height=0.85, corner_radius=0.12, stroke_color=c, stroke_width=2,
                                 fill_color=BG, fill_opacity=1)
            tiles.add(VGroup(r, label(t, font_size=21, color=c).move_to(r)))
        tiles.arrange_in_grid(rows=3, cols=3, buff=(0.35, 0.35)).next_to(head, DOWN, buff=0.5)
        maths = wrapped_label(r"and each block has mathematics of its own: \ hashing that rebalances gracefully, \ "
                              r"caches that survive stampedes, \ limiters that are token buckets, \ IDs that sort by "
                              r"time without coordination, \ curves that turn maps into keys", 12.4, font_size=21,
                              color=WHITE).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "A large system is assembled from a small set of blocks. <bookmark mark='a'/> Load balancers, caches, "
            "rate limiters and queues; shards and replicas; identifiers, blob stores and content delivery, and "
            "indexes for maps. <bookmark mark='b'/> Each block has mathematics of its own, much of it from earlier "
            "parts: hashing that rebalances gracefully, caches that survive a stampede, rate limiters that are token "
            "buckets in disguise, identifiers that sort by time without any coordination, and curves that turn a "
            "map into a list of keys."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in tiles], lag_ratio=0.2), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(maths))
        self.wait(0.4)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ System Design I: \ Building Blocks", font_size=36).to_edge(UP, buff=0.3)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"estimate before you design",
            r"Maglev hashing and the power of two choices",
            r"cache hit rates, \ Che's approximation, \ TinyLFU",
            r"stampedes, \ early expiration, \ token buckets",
            r"shards, \ replicas, \ time-ordered IDs",
            r"space-filling curves, \ and the Job as a service",
        ], font_size=25).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 48 of Computer Science, Built, the first of two parts on system design. "
            "<bookmark mark='a'/> We will estimate before we design; balance load with Maglev hashing and two random "
            "choices; predict a cache's hit rate with Che's approximation and beat LRU with an admission filter; "
            "survive a stampede; limit rates with token buckets; shard, replicate and name things; turn a map into "
            "keys with space-filling curves; and load-test the Job as a service."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()


_ = (KERN, LAM, NO, YES, si)
