from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs37.common import (ACKC, DATA, HEAD, KERN, LAM, NO, PART, SEG, YES, box, grid_table, load, mono)


class Dns(VoiceoverScene):
    def construct(self):
        self.card()
        self.hierarchy()
        self.caching()
        self.kaminsky()

    def card(self):
        card = chapter_card(12, r"Names", r"How does a name become an address, a billion times a second?",
                            lit=(1983, 2008), extra=((1983, r"Mockapetris: \ DNS"), (2005, r"DNSSEC"),
                                                     (2008, r"Kaminsky: \ cache poisoning")), part=PART)
        with self.voiceover("Chapter twelve. Names."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def hierarchy(self):
        head = label(r"A distributed, \ cached tree", font_size=36).to_edge(UP, buff=0.3)
        root = box(1.6, 0.6, r"root \ .", HEAD, font_size=20).move_to([0, 1.8, 0])
        tlds = VGroup(*[box(1.3, 0.55, t, KERN, font_size=19) for t in (r".com", r".org", r".de", r".jp")]).arrange(
            RIGHT, buff=0.6).move_to([0, 0.6, 0])
        doms = VGroup(box(2.6, 0.55, r"gutenberg.org", LAM, font_size=18),
                      box(2.6, 0.55, r"example.de", LAM, font_size=18)).arrange(RIGHT, buff=1.4).move_to([0.9, -0.6, 0])
        edges = VGroup(*[Line(root.get_bottom(), t.get_top(), color=GREY_D, stroke_width=1.8) for t in tlds],
                       Line(tlds[1].get_bottom(), doms[0].get_top(), color=GREY_D, stroke_width=1.8),
                       Line(tlds[2].get_bottom(), doms[1].get_top(), color=GREY_D, stroke_width=1.8))
        res = box(2.2, 0.7, r"your resolver", DATA, font_size=19).move_to([-5.0, -1.9, 0])
        steps = VGroup(
            label(r"1. \ root: \ ``ask .org's servers, \ here''", font_size=19, color=HEAD),
            label(r"2. \ .org: \ ``ask gutenberg.org's servers, \ here''", font_size=19, color=KERN),
            label(r"3. \ gutenberg.org: \ ``152.19.134.47, \ good for 300 s''", font_size=19, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([2.6, -2.3, 0])
        with self.voiceover(
            "Programs name machines by names, not numbers. In the early ARPANET, every host downloaded one file, "
            "hosts dot t x t, listing every name; by 1983 that no longer scaled, and Paul Mockapetris designed the "
            "domain name system. <bookmark mark='a'/> Names form a tree. Thirteen root servers, answered by well over "
            "a thousand machines around the world, know who runs each top-level domain; each of those knows who runs each domain beneath it; and each domain "
            "answers for its own names. <bookmark mark='b'/> To find gutenberg dot org, a resolver asks a root "
            "server, which refers it to the servers for dot org; asks one of those, which refers it to Gutenberg's "
            "own servers; and asks them. <bookmark mark='c'/> The answer comes with a time to live: how many "
            "seconds it may be cached. Three round trips the first time; none for the next five minutes. The whole "
            "system is held together by caching, over UDP, one datagram each way."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(root), LaggedStart(*[FadeIn(t) for t in tlds], lag_ratio=0.15), Create(edges[:4]))
            self.play(FadeIn(doms), Create(edges[4:]))
            vo.wait_until("b")
            self.play(FadeIn(res), FadeIn(steps[0]))
            self.play(FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
        self.wait(0.4)
        self.clear_scene()

    def caching(self):
        d = load("dns")
        head = label(r"A day of lookups", font_size=36).to_edge(UP, buff=0.3)
        rows = [[r"lookups", f"{d['lookups']:,}"], [r"answered from the cache", f"{d['hits']:,} \\ "
                                                                                   f"({d['hit_rate'] * 100:.0f}\\%)"],
                [r"round trips to servers", f"{d['trips']:,}"],
                [r"round trips per lookup", f"{d['trips_per_lookup']:.2f} \\ (3 without a cache)"]]
        tab = grid_table([r"", r""], rows, widths=[4.6, 4.6], row_h=0.46, font_size=21, mono_cols=())
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        tab.cells[2][1].set_color(YES)
        tab.cells[4][1].set_color(YES)
        lines = VGroup(
            wrapped_label(r"our resolver, \ 2{,}000 names requested with Zipf popularity, \ TTLs of 1 minute to 1 "
                          r"day", 12.4, font_size=20, color=GREY_A),
            wrapped_label(r"the root and TLD referrals are cached for two days, \ so almost every miss costs only "
                          r"the last one or two round trips", 12.4, font_size=21, color=WHITE),
            wrapped_label(r"the TTL is a dial: \ long TTLs make lookups fast and the servers idle; \ short ones let "
                          r"an address change quickly, \ which is how CDNs steer users \ (chapter 14)", 12.4,
                          font_size=21, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "We gave our resolver a day of lookups: fifty thousand of them, for two thousand names whose popularity "
            "falls off as a power law, each with a time to live between a minute and a day. "
            "<bookmark mark='a'/> Fifty-six percent were answered from the cache without sending a packet. The "
            "rest needed nought point eight seven round trips on average, not three, because the referrals from "
            "the root and the top-level domains are themselves cached for two days. <bookmark mark='b'/> The time "
            "to live is a dial. Long ones make lookups fast and servers idle. Short ones let a name move to a new "
            "address within seconds, which is how content delivery networks steer each user to a nearby server, as "
            "we will see."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(lines[1]))
            vo.wait_until("b")
            self.play(FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()

    def kaminsky(self):
        d = load("dns")
        head = label(r"Kaminsky's attack \ (2008)", font_size=36).to_edge(UP, buff=0.3)
        steps = VGroup(
            wrapped_label(r"the attacker asks your resolver for a name that is not cached: \ \texttt{x123.bank.com}",
                          12.4, font_size=21, color=WHITE),
            wrapped_label(r"before the real answer arrives, \ it floods the resolver with forged replies: \ ``I am "
                          r"bank.com's server; \ and bank.com's server is \textit{at my address}''", 12.4,
                          font_size=21, color=NO),
            wrapped_label(r"a forged reply is accepted if it matches the query's 16-bit ID \ (and source port); \ "
                          r"lose the race? \ ask for \texttt{x124.bank.com} at once", 12.4, font_size=21,
                          color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(head, DOWN, buff=0.4)
        ex = d["expected_races"]
        sec = d["expected_seconds"]
        rows = [[r"fixed source port: \ 16 bits", f"{ex['fixed port']:,.0f}", f"{sec['fixed port']:.0f} s"],
                [r"random port too: \ 32 bits", f"{ex['random port']:,.0f}",
                 f"{sec['random port'] / 86400:.0f} days"]]
        tab = grid_table([r"what must be guessed", r"races needed \ (100 forgeries each)", r"at 10 races a second"],
                         rows, widths=[4.0, 3.8, 3.0], row_h=0.44, font_size=20, mono_cols=())
        tab.next_to(steps, DOWN, buff=0.45).set_x(0)
        tab.cells[1][2].set_color(NO)
        tab.cells[2][2].set_color(YES)
        foot = wrapped_label(r"the July 2008 patch randomized source ports, \ in the largest coordinated fix the "
                             r"Internet had seen; \ the real cure is \textbf{DNSSEC}: \ answers signed with the "
                             r"public keys of Part 30, \ from the root down", 12.4, font_size=21,
                             color=YES).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Caching makes DNS fast, and a poisoned cache makes it dangerous. In 2008 Dan Kaminsky found a way to "
            "poison almost any resolver in seconds. <bookmark mark='a'/> The attacker asks your resolver about a "
            "name that cannot be in its cache, a random name under bank dot com. <bookmark mark='b'/> While the "
            "resolver waits for the real answer, the attacker sends forged ones, each claiming that the server for "
            "all of bank dot com is at the attacker's address. <bookmark mark='c'/> A reply is accepted if it "
            "carries the query's sixteen-bit identifier. If the real answer wins the race, the attacker simply "
            "asks for another random name, and races again. <bookmark mark='d'/> With a hundred forgeries a race, "
            "the expected number of races is six hundred and fifty-six: about a minute. Once one succeeds, every "
            "user of that resolver is sent to the attacker for everything at the bank. <bookmark mark='e'/> The "
            "emergency fix, coordinated in secret among vendors and released together in July 2008, randomized the "
            "source port of every query as well, sixteen more bits to guess: fifty days instead of a minute. The "
            "real fix is to sign the answers, with the public keys of Part 30, from the root down: DNSSEC."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abc", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*tab.cells[0])), Create(tab.rule), FadeIn(VGroup(*tab.cells[1])))
            vo.wait_until("e")
            self.play(FadeIn(VGroup(*tab.cells[2])), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (ACKC, SEG, mono)
