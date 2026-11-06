from __future__ import annotations

import math
import random

from explainer.cs import *  # noqa: F403
from videos.cs.cs49.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, bar_chart, load


def num(x, digits=0):
    """A number with thousands separators, for Tex."""
    return f"{x:,.{digits}f}".replace(",", "{,}")


def mega(x):
    return rf"{x / 1e6:.1f}\,M"


def stat(value, text, color, w=2.9, h=1.05):
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=color, stroke_width=2,
                             fill_color=BG, fill_opacity=1)
    g = VGroup(label(value, font_size=28, color=color), label(text, font_size=16, color=GREY_A)).arrange(
        DOWN, buff=0.1).move_to(frame)
    return VGroup(frame, g)


class Feed(VoiceoverScene):
    def construct(self):
        self.card()
        self.graph()
        self.two()
        self.celebrity()
        self.hybrid()

    def card(self):
        card = chapter_card(2, r"A news feed: \ fan-out", r"Should a post travel to its readers, \ or readers to it?",
                            lit=(2006, 2010), extra=((2006, r"Facebook's News Feed"),
                                                     (2010, r"Silberstein et al.: \ feeds")), part=PART)
        with self.voiceover("Chapter two. A news feed, and the question of fan-out."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def graph(self):
        f = load("feed")
        head = label(r"The follower graph", font_size=36).to_edge(UP, buff=0.3)
        rng = random.Random(4)
        # a schematic power-law graph: three giants, a few mid-sized accounts, many small ones
        centre = [-3.4, -0.2]
        small = [[centre[0] + 2.9 * math.cos(a) * rng.uniform(0.75, 1.0),
                  centre[1] + 2.6 * math.sin(a) * rng.uniform(0.75, 1.0), 0]
                 for a in [2 * math.pi * k / 48 + rng.uniform(-0.05, 0.05) for k in range(48)]]
        giants = [[-4.3, 0.5, 0], [-2.4, -0.9, 0], [-3.6, -1.3, 0]]
        sizes = [0.42, 0.3, 0.22]
        mids = [[-2.3, 0.9, 0], [-4.7, -0.7, 0], [-3.0, 0.2, 0], [-4.0, 1.4, 0]]
        edges = VGroup()
        for p in small:
            for g, sz in zip(giants, sizes):
                if rng.random() < sz * 2.0:
                    edges.add(Line(p, g, stroke_width=0.8, color=GREY_D, stroke_opacity=0.7))
            if rng.random() < 0.3:
                edges.add(Line(p, mids[rng.randrange(len(mids))], stroke_width=0.8, color=GREY_D, stroke_opacity=0.7))
        dots = VGroup(*[Dot(p, radius=0.05, color=DATA) for p in small])
        mdots = VGroup(*[Dot(p, radius=0.1, color=LAM) for p in mids])
        gdots = VGroup(*[Dot(p, radius=r, color=HEAD) for p, r in zip(giants, sizes)])
        gnote = note(r"schematic: \ dot size is follower count", font_size=16).next_to(
            VGroup(dots, gdots), DOWN, buff=0.15)
        tiles = VGroup(
            stat(num(f["users"]), r"users \ (synthetic)", WHITE),
            stat(num(f["median_followers"]), r"median followers", DATA),
            stat(num(f["mean_followers"]), r"mean followers", LAM),
            stat(num(f["max_followers"]), r"the largest account", HEAD),
            stat(num(f["posts"]), r"posts a day \ (half each)", YES),
            stat(mega(f["reads"]), r"timeline reads a day \ (20 each)", KERN),
        ).arrange_in_grid(rows=3, cols=2, buff=(0.25, 0.25)).move_to([3.5, -0.1, 0])
        with self.voiceover(
            "A news feed shows each user the recent posts of everyone they follow. <bookmark mark='a'/> The data is "
            "a follower graph, and real follower graphs follow a power law: most accounts have a few dozen "
            "followers, and a handful have millions. <bookmark mark='b'/> Our instrument draws a synthetic graph of "
            f"{num(f['users'])} users from such a law. The median account has {f['median_followers']:.0f} followers, "
            f"but the mean is {f['mean_followers']:.0f}, pulled up by the giants, and the largest is followed by "
            "everyone. <bookmark mark='c'/> Each user posts half a time a day and opens the timeline twenty times: "
            "fifty thousand posts against two million reads. The question is when to do the work of putting "
            "those posts together."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(dots), Create(edges), run_time=2)
            self.play(GrowFromCenter(gdots), GrowFromCenter(mdots), FadeIn(gnote))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t) for t in tiles[:4]], lag_ratio=0.4), run_time=2.5)
            self.play(Indicate(gdots, color=HEAD))
            vo.wait_until("c")
            self.play(FadeIn(tiles[4]), FadeIn(tiles[5]))
        self.wait(0.4)
        self.clear_scene()

    def two(self):
        f = load("feed")
        head = label(r"Fan-out on write, \ or on read", font_size=36).to_edge(UP, buff=0.3)
        ys = [2.0, 1.35, 0.7, 0.05, -0.6]

        def timelines(x, color, text):
            return VGroup(*[RoundedRectangle(width=1.5, height=0.42, corner_radius=0.06, stroke_color=color,
                                             stroke_width=1.6, fill_color=BG, fill_opacity=1).move_to([x, y, 0])
                            for y in ys]), label(text, font_size=16, color=color)
        author = VGroup(Circle(radius=0.38, color=HEAD, fill_color=BG, fill_opacity=1).move_to([-5.7, 0.7, 0]))
        author.add(label(r"author", font_size=16, color=HEAD).next_to(author[0], DOWN, buff=0.12))
        tl, tlt = timelines(-2.6, DATA, r"followers' timelines")
        tlt.next_to(tl, UP, buff=0.12)
        pw = label(r"\textbf{push}: \ write each post into every follower's timeline", font_size=19,
                   color=HEAD)
        reader = VGroup(Circle(radius=0.38, color=YES, fill_color=BG, fill_opacity=1).move_to([5.7, 0.7, 0]))
        reader.add(label(r"reader", font_size=16, color=YES).next_to(reader[0], DOWN, buff=0.12))
        al, alt = timelines(2.6, LAM, r"followees' own posts")
        alt.next_to(al, UP, buff=0.12)
        pl = label(r"\textbf{pull}: \ gather from every followee at each read", font_size=19, color=YES)
        pw.move_to([-3.6, -1.35, 0])
        pl.move_to([3.6, -1.35, 0])
        e1 = label(rf"{num(f['posts'])} posts $\times$ {num(f['mean_followers'])} followers $=$ "
                   rf"\textbf{{{mega(f['push_writes'])}}} writes a day", font_size=20, color=HEAD)
        e2 = label(rf"{mega(f['reads'])} reads $\times$ {num(f['mean_followers'])} followees $=$ "
                   rf"\textbf{{{mega(f['pull_reads'])}}} fetches a day", font_size=20, color=YES)
        e1.move_to([-3.5, -2.1, 0])
        e2.move_to([3.5, -2.1, 0])
        ratio = f["pull_reads"] / f["push_writes"]
        foot = wrapped_label(rf"every edge is one follower and one followee, \ so the two means are equal and the "
                             rf"ratio is reads over posts: \ {ratio:.0f}$\times$", 12.4, font_size=19,
                             color=WHITE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "There are two ways. <bookmark mark='a'/> Fan-out on write, or push: when someone posts, write the post "
            "into the timeline of every follower, so that reading a timeline is a single fetch. "
            "<bookmark mark='b'/> Fan-out on read, or pull: store each post once, with its author, and at every "
            "read gather the recent posts of everyone the reader follows. <bookmark mark='c'/> On our graph, push "
            f"costs fifty thousand posts times {f['mean_followers']:.0f} followers, about "
            f"{f['push_writes'] / 1e6:.1f} million timeline writes a day. Pull costs two million reads times "
            f"{f['mean_followers']:.0f} followees, about {f['pull_reads'] / 1e6:.0f} million fetches. "
            "<bookmark mark='d'/> Every follow is one follower and one followee, so the two averages are equal, and "
            f"the ratio is just reads over posts: {ratio:.0f} times. Read-heavy, so push wins on total work."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(author), FadeIn(tl), FadeIn(tlt), FadeIn(pw))
            pk = VGroup(*[Dot(author[0].get_center(), radius=0.08, color=HEAD) for _ in ys])
            self.add(pk)
            self.play(*[d.animate.move_to(b.get_center()) for d, b in zip(pk, tl)], run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(reader), FadeIn(al), FadeIn(alt), FadeIn(pl))
            qk = VGroup(*[Dot(b.get_center(), radius=0.08, color=YES) for b in al])
            self.add(qk)
            self.play(*[d.animate.move_to(reader[0].get_center()) for d in qk], run_time=1.5)
            self.play(FadeOut(qk))
            vo.wait_until("c")
            self.play(FadeIn(e1))
            self.play(FadeIn(e2))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def celebrity(self):
        f = load("feed")
        top = f["hybrid"][2]                           # accounts with at least 10,000 followers
        share = top["pull_reads"] / f["pull_reads"]    # their share of all follow edges
        head = label(r"The celebrity problem", font_size=36).to_edge(UP, buff=0.3)
        c = [-3.6, -0.1, 0]
        star = Dot(c, radius=0.38, color=HEAD)
        ring = VGroup(*[Dot([c[0] + 2.6 * math.cos(2 * math.pi * k / 64), c[1] + 2.4 * math.sin(2 * math.pi * k / 64),
                             0], radius=0.045, color=DATA) for k in range(64)])
        spokes = VGroup(*[Line(c, d.get_center(), stroke_width=0.8, color=GREY_D) for d in ring])
        counter = DecimalNumber(0, num_decimal_places=0, group_with_commas=True, font_size=30, color=HEAD)
        ctext = label(r"timeline writes for one post", font_size=17, color=GREY_A)
        cg = VGroup(counter, ctext).arrange(DOWN, buff=0.08).move_to(c)
        cg.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)
        vals = [f["median_followers"], f["mean_followers"], f["max_followers"]]
        chart = bar_chart(vals, [r"median", r"mean", r"largest"], [DATA, LAM, HEAD], height=2.6, bar_w=0.7,
                          gap=0.6, log=True, vmax=1e5, fmt_=lambda v: num(v), font_size=18)
        ttl = label(r"fan-out of one post \ (log scale)", font_size=18, color=GREY_A)
        side = VGroup(ttl, chart).arrange(DOWN, buff=0.3).move_to([3.4, 1.0, 0])
        facts = VGroup(
            wrapped_label(rf"one post by the largest account costs as much as "
                          rf"{num(f['max_followers'] / f['median_followers'])} posts by a median one", 5.8,
                          font_size=19, color=WHITE),
            wrapped_label(rf"the {top['celebrities']} accounts with at least {num(top['threshold'])} followers, \ "
                          rf"{100 * top['celebrities'] / f['users']:.2f}\% of users, \ receive "
                          rf"{100 * share:.0f}\% of all follows", 5.8, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(side, DOWN, buff=0.45)
        with self.voiceover(
            "Push has a flaw, and it lives at the top of the power law. <bookmark mark='a'/> When the largest "
            f"account posts, the system must write {num(f['max_followers'])} timelines, a burst of work on the "
            "timeline store, and the last follower sees the post only when the last write lands. "
            "<bookmark mark='b'/> On a log scale the gap is plain: the median post fans out to "
            f"{f['median_followers']:.0f} timelines, the mean to {f['mean_followers']:.0f}, and the largest to all "
            f"of them. One such post costs as much as {f['max_followers'] / f['median_followers']:,.0f} ordinary "
            f"ones. <bookmark mark='c'/> And the giants are few but heavy: the {top['celebrities']} accounts with at "
            f"least ten thousand followers, about a tenth of a percent of users, receive {100 * share:.0f} percent "
            "of all follows. Real networks have accounts with tens of millions of followers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ring), Create(spokes), FadeIn(star))
            vo.wait_until("a")
            self.play(FadeIn(cg))
            self.play(ChangeDecimalToValue(counter, f["max_followers"]),
                      LaggedStart(*[Indicate(d, color=HEAD, scale_factor=1.6) for d in ring], lag_ratio=0.05),
                      run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(ttl), FadeIn(chart[0]), FadeIn(chart.names))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in chart.bars], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(v) for v in chart.vals], lag_ratio=0.3), run_time=2)
            self.play(FadeIn(facts[0]))
            vo.wait_until("c")
            self.play(FadeIn(facts[1]))
        self.wait(0.4)
        self.clear_scene()

    def hybrid(self):
        f = load("feed")
        rows = sorted(f["hybrid"], key=lambda r: -r["threshold"])     # push everything first
        head = label(r"The hybrid: \ push most, \ pull the giants", font_size=36).to_edge(UP, buff=0.3)
        names = [r"push all"] + [rf"pull\\$\geq${num(r['threshold'])}" for r in rows[1:]] + [r"pull all"]
        ops = [r["total"] for r in rows] + [f["pull_reads"]]
        cols = [HEAD, KERN, KERN, KERN, YES]
        c1 = bar_chart(ops, names, cols, height=2.5, bar_w=0.6, gap=0.5, log=True, vmax=1e9,
                       fmt_=lambda v: mega(v), font_size=17)
        t1 = label(r"operations a day \ (log scale)", font_size=18, color=GREY_A)
        g1 = VGroup(t1, c1).arrange(DOWN, buff=0.3)
        fan = [r["max_fanout_per_post"] for r in rows]
        c2 = bar_chart(fan, names[:4], cols[:4], height=2.5, bar_w=0.6, gap=0.5, log=True, vmax=1e5,
                       fmt_=lambda v: num(v), font_size=17)
        t2 = label(r"the worst fan-out of one post \ (log scale)", font_size=18, color=GREY_A)
        g2 = VGroup(t2, c2).arrange(DOWN, buff=0.3)
        VGroup(g1, g2).arrange(RIGHT, buff=1.0, aligned_edge=DOWN).next_to(head, DOWN, buff=0.45)
        h = rows[1]
        foot = VGroup(
            wrapped_label(rf"pulling the {h['celebrities']} giants costs {ops[1] / ops[0]:.0f}$\times$ the operations "
                          rf"of pure push, \ but caps a post's fan-out at {num(h['max_fanout_per_post'])}; \ and the "
                          r"pulled posts are the same few hot items for everyone, \ ideal for a cache \ (Part 48)",
                          12.6, font_size=19, color=WHITE),
            wrapped_label(r"Silberstein et al. \ (2010) \ choose per pair of author and reader, \ comparing how "
                          r"often one posts with how often the other reads: \ frequent readers of rare posters get "
                          r"pushes", 12.6, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The cure is a hybrid. <bookmark mark='a'/> Push the posts of ordinary accounts, and pull the posts of "
            "accounts above a threshold at read time, merging them in. Our instrument counts both kinds of work "
            "for each threshold. <bookmark mark='b'/> Counted in operations, pure push is still cheapest: pulling "
            f"the {h['celebrities']} giants multiplies the total about {ops[1] / ops[0]:.0f} fold, because pulls "
            "happen at every read. <bookmark mark='c'/> What the hybrid buys is the worst case. No post now fans out "
            f"to more than {num(h['max_fanout_per_post'])} timelines, and the pulled posts are the same few hot "
            "items read by everyone, which a cache serves almost for free. <bookmark mark='d'/> Silberstein and "
            "colleagues made the choice per pair in 2010, comparing how often the author posts with how often the "
            "reader reads. The trade-off is total work against the tail."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(t1), FadeIn(c1[0]), FadeIn(c1.names))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in c1.bars], lag_ratio=0.25),
                      LaggedStart(*[FadeIn(v) for v in c1.vals], lag_ratio=0.25), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(t2), FadeIn(c2[0]), FadeIn(c2.names))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in c2.bars], lag_ratio=0.25),
                      LaggedStart(*[FadeIn(v) for v in c2.vals], lag_ratio=0.25), run_time=2.5)
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (NO,)
