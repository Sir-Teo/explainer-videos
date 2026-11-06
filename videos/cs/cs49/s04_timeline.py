from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs49.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load, mono


def block(name, sub, color, w=2.3, h=0.95):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=color, stroke_width=2,
                         fill_color=BG, fill_opacity=1)
    t = label(name, font_size=19, color=WHITE)
    s = label(sub, font_size=15, color=color)
    for m in (t, s):
        if m.width > w - 0.15:
            m.width = w - 0.15
    VGroup(t, s).arrange(DOWN, buff=0.08).move_to(r)
    return VGroup(r, t, s)


def link(a, b, color=GREY_C):
    return Arrow(a, b, buff=0.08, stroke_width=2, color=color, max_tip_length_to_length_ratio=0.12)


def post_chip(text, color, w=1.3, h=0.4, size=17):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.06, stroke_color=color, stroke_width=1.6,
                         fill_color=BG, fill_opacity=1)
    return VGroup(r, mono(text, size=size, color=color).move_to(r))


class Timeline(VoiceoverScene):
    def construct(self):
        self.card()
        self.readpath()
        self.ranking()
        self.paging()
        self.ryw()

    def card(self):
        card = chapter_card(3, r"A news feed: \ ranking and reading",
                            r"Which posts come first, \ and how do you page through a moving list?",
                            lit=(2010, 2016), extra=((2010, r"EdgeRank described"),
                                                     (2016, r"Twitter's ranked timeline")), part=PART)
        with self.voiceover("Chapter three. A news feed, continued: ranking, and reading."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def readpath(self):
        f = load("feed")
        head = label(r"The read path", font_size=36).to_edge(UP, buff=0.3)
        y = 1.3
        reader = block(r"reader", r"opens the app", WHITE, w=1.7).move_to([-5.75, y, 0])
        svc = block(r"timeline service", r"stateless", DATA).move_to([-3.25, y, 0])
        tcache = block(r"timeline cache", r"post IDs, \ pushed", HEAD).move_to([-0.45, y + 0.95, 0])
        giants = block(r"giants' posts", r"pulled, \ chapter 2", KERN).move_to([-0.45, y - 0.95, 0])
        hyd = block(r"post store", r"ID $\to$ text, \ author", LAM).move_to([2.25, y, 0])
        rank = block(r"ranker", r"Part 47", YES, w=1.9).move_to([4.95, y, 0])
        boxes = VGroup(reader, svc, tcache, giants, hyd, rank)
        arrows = VGroup(link(reader.get_right(), svc.get_left()), link(svc.get_right(), tcache.get_left()),
                        link(svc.get_right(), giants.get_left()), link(tcache.get_right(), hyd.get_left()),
                        link(giants.get_right(), hyd.get_left()), link(hyd.get_right(), rank.get_left()))
        keep = 800
        mem = f["users"] * keep * 8
        lines = VGroup(
            wrapped_label(r"\textbf{merge}: \ the pushed IDs and the giants' latest, \ newest first; \ "
                          r"\textbf{hydrate}: \ look each ID up; \ \textbf{rank}; \ return a page of twenty", 12.4,
                          font_size=19, color=WHITE),
            wrapped_label(rf"timelines hold IDs, \ not copies: \ {num(f['users'])} users $\times$ {keep} IDs "
                          rf"$\times$ 8 bytes $=$ {mem / 1e6:.0f} MB of cache, \ and a deleted post is one write, \ "
                          r"not one per follower", 12.4, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.45)
        src = note(r"800 entries a timeline: \ Twitter's figure \ (Krikorian, \ 2013)", font_size=16).next_to(
            lines, UP, buff=0.2).align_to(lines, LEFT)
        with self.voiceover(
            "Chapter two decided how posts reach a timeline. Now read one. <bookmark mark='a'/> The reader's "
            "request reaches a stateless timeline service. <bookmark mark='b'/> It fetches the reader's timeline "
            "from a cache, a list of post identifiers that pushes have filled, and the latest posts of the few "
            "giants the reader follows, which are pulled. <bookmark mark='c'/> It merges the two lists, newest "
            "first, then hydrates them: looks each identifier up in the post store to get its text and author. A "
            "ranker orders them, and a page of twenty goes back. <bookmark mark='d'/> Timelines hold identifiers, "
            "not copies. Twitter described keeping about eight hundred per timeline in 2013; for our hundred "
            f"thousand users, at eight bytes each, that is about {mem / 1e6:.0f} megabytes. And deleting a post is "
            "one write, not one per follower."
        ) as vo:
            self.play(FadeIn(head), FadeIn(boxes), Create(arrows))
            pk = Dot(reader.get_center(), radius=0.11, color=DATA)
            vo.wait_until("a")
            self.play(FadeIn(pk))
            self.play(pk.animate.move_to(svc.get_center()), run_time=0.8)
            vo.wait_until("b")
            p1, p2 = pk.copy().set_color(HEAD), pk.copy().set_color(KERN)
            self.play(p1.animate.move_to(tcache.get_center()), p2.animate.move_to(giants.get_center()), run_time=0.8)
            vo.wait_until("c")
            self.play(p1.animate.move_to(hyd.get_center()), p2.animate.move_to(hyd.get_center()), run_time=0.8)
            self.play(FadeOut(p2), p1.animate.move_to(rank.get_center()).set_color(YES), FadeIn(lines[0]),
                      run_time=0.8)
            self.play(p1.animate.move_to(reader.get_center()), FadeOut(pk), run_time=1.2)
            self.play(FadeOut(p1))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]), FadeIn(src))
        self.wait(0.4)
        self.clear_scene()

    def ranking(self):
        head = label(r"Ranking: \ newest first is not best first", font_size=36).to_edge(UP, buff=0.3)
        # illustrative candidates: (name, affinity with the reader, weight of the kind of post, age in hours)
        cands = [(r"a photo", 0.2, 1.0, 1), (r"a link", 0.9, 0.6, 2), (r"a status", 0.1, 0.5, 3),
                 (r"a video", 0.8, 1.0, 5), (r"a status", 0.6, 0.5, 8), (r"a photo", 0.95, 1.0, 16)]

        def score(a, w, age):
            return a * w * math.exp(-age / 12)
        sc = [score(a, w, t) for _, a, w, t in cands]
        order = sorted(range(len(cands)), key=lambda i: -sc[i])
        rows = VGroup()
        for i, (nm, a, w, t) in enumerate(cands):
            txt = label(rf"{nm}, \ {t} h old", font_size=18, color=WHITE)
            feat = label(rf"${a:.2f} \times {w:.1f} \times e^{{-{t}/12}}$", font_size=18, color=GREY_A)
            bar = Rectangle(width=max(0.05, 2.6 * sc[i] / max(sc)), height=0.24, stroke_width=0, fill_color=YES,
                            fill_opacity=0.85)
            val = label(f"{sc[i]:.2f}", font_size=17, color=YES)
            txt.move_to([-4.9, 0, 0])
            feat.move_to([-1.6, 0, 0])
            bar.move_to([0.6, 0, 0], aligned_edge=LEFT)
            val.next_to(bar, RIGHT, buff=0.12)
            rows.add(VGroup(txt, feat, bar, val))
        top = 1.9
        for i, r in enumerate(rows):
            r.shift(UP * (top - 0.62 * i))
        hdr = VGroup(label(r"candidates, \ newest first", font_size=17, color=GREY_B).move_to([-4.9, 2.55, 0]),
                     label(r"affinity $\times$ weight $\times$ decay", font_size=17, color=GREY_B).move_to(
                         [-1.6, 2.55, 0]),
                     label(r"score", font_size=17, color=GREY_B).move_to([1.2, 2.55, 0]))
        ill = note(r"illustrative posts and weights", font_size=16).next_to(hdr, UP, buff=0.1).to_edge(RIGHT,
                                                                                                    buff=0.5)
        side = wrapped_label(r"EdgeRank \ (Facebook, \ 2010): \ affinity $\times$ weight $\times$ time decay, \ "
                             r"summed over a post's interactions", 3.0, font_size=18, color=HEAD).move_to([5.1, 1.2, 0])
        foot = wrapped_label(r"today: \ learned models predict each action \ (a like, \ a reply, \ a hide) \ "
                             r"from many features, \ Part 47's learning to rank; \ a cheap stage picks "
                             r"candidates, \ a heavy one orders the survivors", 12.4, font_size=19,
                             color=WHITE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The newest post is rarely the one a reader most wants. <bookmark mark='a'/> Here are six candidates, "
            "newest first, with made-up numbers. <bookmark mark='b'/> Facebook's EdgeRank, described in 2010, "
            "scored each one as a product: the reader's affinity with the author, a weight for the kind of post, "
            "and a decay with age. <bookmark mark='c'/> Sorted by score, the order changes completely: a close "
            "friend's photo from sixteen hours ago outranks a stranger's from an hour ago. <bookmark mark='d'/> "
            "Modern feeds replace the hand-made product with learned models that predict each action a reader "
            "might take, Part 47's learning to rank, in two stages: a cheap one to choose candidates, and an "
            "expensive one to order the survivors."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(hdr[0]), LaggedStart(*[FadeIn(r[0]) for r in rows], lag_ratio=0.2), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(hdr[1:]), FadeIn(side), LaggedStart(*[FadeIn(r[1]) for r in rows], lag_ratio=0.2),
                      run_time=2)
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(r[2], LEFT), FadeIn(r[3])) for r in rows],
                                  lag_ratio=0.2), run_time=2)
            vo.wait_until("c")
            self.play(*[rows[i].animate.set_y(top - 0.62 * k) for k, i in enumerate(order)], run_time=2)
            self.play(Indicate(rows[order[0]], color=YES))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def paging(self):
        head = label(r"Paging through a moving list", font_size=36).to_edge(UP, buff=0.3)
        ids = list(range(120, 111, -1))              # illustrative post IDs, newest first
        new = [122, 121]
        page = 4
        h = 0.34
        x_list = 0.0
        y0 = 2.2

        def col(seq):
            return VGroup(*[post_chip(str(i), DATA, h=h, size=16) for i in seq]).arrange(DOWN, buff=0.05)
        lst = col(ids).move_to([x_list, 0, 0]).align_to([0, y0, 0], UP)
        lt = label(r"the timeline, \ newest first", font_size=17, color=GREY_B).next_to(lst, UP, buff=0.12)
        fresh = VGroup(*[post_chip(str(i), HEAD, h=h, size=16) for i in new]).arrange(DOWN, buff=0.05)
        # page 1 is the same for both readers
        p1 = ids[:page]
        after = ids[:]
        after[:0] = new
        off2 = after[page:2 * page]                   # offset 4, limit 4, read after the new posts arrived
        cur2 = [i for i in after if i < p1[-1]][:page]  # cursor: everything older than the last one seen
        dup = [i for i in off2 if i in p1]

        def result(title, seq, color, x):
            t = label(title, font_size=18, color=color)
            chips = VGroup(*[post_chip(str(i), NO if (color == NO and i in dup) else color, h=h, size=16)
                            for i in seq]).arrange(DOWN, buff=0.05)
            return VGroup(t, chips).arrange(DOWN, buff=0.15).move_to([x, 0.6, 0])
        r1 = result(r"page 1", p1, GREY_A, -2.4)
        ro = result(r"page 2 by offset 4", off2, NO, -4.9)
        rc = result(rf"page 2 after \texttt{{{p1[-1]}}}", cur2, YES, 2.6)
        bo = wrapped_label(rf"{len(dup)} posts shown twice; \ and the server still walks past the first rows to "
                           r"skip them \ (Part 43)", 3.0, font_size=17, color=NO).next_to(ro, DOWN, buff=0.25)
        bc = wrapped_label(rf"the cursor \texttt{{{p1[-1]}}} is a position in the data, \ not a count of rows; \ "
                           r"one index seek \ (Part 35)", 3.0, font_size=17, color=YES).next_to(rc, DOWN, buff=0.25)
        foot = wrapped_label(r"a ranked feed changes between pages too: \ its cursor names a snapshot of the ranked "
                             r"list, \ kept in a cache for the session, \ and a position in it", 12.4, font_size=19,
                             color=HEAD).to_edge(DOWN, buff=0.35)
        ill = note(r"illustrative IDs", font_size=16).to_corner(UR, buff=0.4).shift(DOWN * 0.5)
        with self.voiceover(
            "A reader scrolls, and the app asks for the next page. <bookmark mark='a'/> Here is a timeline, "
            "newest first, and the first page of four. <bookmark mark='b'/> While the reader looks at it, two new "
            "posts arrive at the top. <bookmark mark='c'/> If the next page is requested by offset, skip four and "
            f"take four, the list has moved: the reader sees {len(dup)} posts again, and the database still walks "
            "past every skipped row, the problem of Part 43. <bookmark mark='d'/> A cursor instead says where the "
            "last page ended: everything older than this post. It is a position in the data, found with one index "
            "seek, and new posts at the top cannot disturb it. <bookmark mark='e'/> A ranked feed reorders "
            "between pages as well, so its cursor names a snapshot of the ranked list, cached for the session, and "
            "a position within it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lst), FadeIn(lt), FadeIn(ill))
            vo.wait_until("a")
            self.play(*[Indicate(lst[i], color=WHITE) for i in range(page)])
            self.play(FadeIn(r1))
            vo.wait_until("b")
            fresh.next_to(lst, UP, buff=0.05).shift(UP * 0.5)
            self.play(FadeOut(lt), FadeIn(fresh, shift=DOWN * 0.3),
                      lst.animate.shift(DOWN * len(new) * (h + 0.05)), run_time=1.2)
            self.play(fresh.animate.next_to(lst, UP, buff=0.05))
            vo.wait_until("c")
            self.play(FadeIn(ro), FadeIn(bo))
            vo.wait_until("d")
            self.play(FadeIn(rc), FadeIn(bc))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def ryw(self):
        head = label(r"Read your own writes", font_size=36).to_edge(UP, buff=0.3)
        y = 1.5
        user = block(r"you", r"post, \ then look", WHITE, w=1.7).move_to([-5.6, y, 0])
        leader = block(r"leader", r"takes writes", DATA).move_to([-1.9, y + 0.8, 0])
        replica = block(r"replica", r"serves reads", LAM).move_to([-1.9, y - 1.0, 0])
        rep = link(leader.get_bottom(), replica.get_top(), GREY_B)
        lag = label(r"lag: \ a second, \ sometimes more", font_size=16, color=GREY_B).next_to(rep, RIGHT, buff=0.15)
        tl = VGroup(*[post_chip(s, DATA, w=1.6) for s in ("older 1", "older 2", "older 3")]).arrange(
            DOWN, buff=0.06).move_to([3.2, y, 0])
        tlt = label(r"your timeline", font_size=17, color=GREY_B).next_to(tl, UP, buff=0.12)
        miss = label(r"your post is missing: \ you post it again", font_size=18, color=NO).next_to(tl, DOWN,
                                                                                                 buff=0.2)
        fixes = VGroup(
            wrapped_label(r"\textbf{1.} \ for a minute after you write, \ read from the leader", 3.9, font_size=18,
                          color=WHITE),
            wrapped_label(r"\textbf{2.} \ carry your last write's log position; \ a replica answers only once it "
                          r"has applied it \ (Part 39's session guarantees)", 3.9, font_size=18, color=YES),
            wrapped_label(r"\textbf{3.} \ the app shows your own post itself, \ before the server does", 3.9,
                          font_size=18, color=HEAD),
        ).arrange(RIGHT, buff=0.35, aligned_edge=UP).to_edge(DOWN, buff=1.0)
        foot = wrapped_label(r"only the writer needs this; \ everyone else may see the post a second late", 12.4,
                             font_size=19, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "One more anomaly, from Part 39's replication. <bookmark mark='a'/> You post. The write goes to the "
            "leader, and replicas catch up a moment later. <bookmark mark='b'/> You open your timeline at once, "
            "the read lands on a replica that has not caught up, and your post is not there. So you post it again. "
            "<bookmark mark='c'/> There are three cures. Read from the leader for a minute after you write. Or carry "
            "the position of your last write, and have a replica answer only once it has applied that position, "
            "one of Part 39's session guarantees. Or let the app show your own post itself. "
            "<bookmark mark='d'/> Only the writer needs the guarantee. Everyone else can see the post a second "
            "late, and the feed stays cheap."
        ) as vo:
            self.play(FadeIn(head), FadeIn(user), FadeIn(leader), FadeIn(replica), GrowArrow(rep), FadeIn(lag),
                      FadeIn(tl), FadeIn(tlt))
            vo.wait_until("a")
            w = Dot(user.get_center(), radius=0.11, color=HEAD)
            self.play(FadeIn(w))
            self.play(w.animate.move_to(leader.get_center()), run_time=0.9)
            self.play(w.animate.move_to(rep.get_center()), run_time=2.5, rate_func=linear)
            vo.wait_until("b")
            r = Dot(user.get_center(), radius=0.11, color=LAM)
            self.play(FadeIn(r))
            self.play(r.animate.move_to(replica.get_center()), run_time=0.9)
            self.play(r.animate.move_to(tl.get_left()), run_time=0.9)
            self.play(FadeOut(r), FadeIn(miss))
            self.play(w.animate.move_to(replica.get_center()), run_time=0.8)
            self.play(FadeOut(w))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in fixes], lag_ratio=0.5), run_time=3)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


def num(x, digits=0):
    return f"{x:,.{digits}f}".replace(",", "{,}")


_ = (KERN, NO)
