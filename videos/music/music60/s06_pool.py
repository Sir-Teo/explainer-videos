from __future__ import annotations

from videos.music.music60.common import *  # noqa: F403


class Pool(SoundScene):
    def construct(self):
        chapter(self, 5, r"Dividing the pool", r"Does your subscription pay for the music you play?")
        self.population()
        self.two_ways()
        self.bots()
        self.reforms()

    # ------------------------------------------------------------------
    def population(self):
        d = load("pool")
        u, f, s = d["users"], d["fees_by_kind"], d["streams_by_kind"]
        names = [("heavy", r"heavy listeners", r"mostly the charts", BLUE), ("light", r"light listeners", r"mostly niche artists", TUNE),
                 ("free", r"free listeners", r"ads pay little", GREY_B), ("bot", r"bot accounts", r"one fake artist, \ all month", EAR)]
        g = VGroup()
        for k, n, what, col in names:
            g.add(VGroup(label(n, font_size=19, color=col), label(what, font_size=15, color=GREY_A), label(f"{u[k]:,}", font_size=18, color=WHITE),
                         label(rf"\${f[k]:,.0f}", font_size=18, color=WHITE), label(f"{s[k] / 1e6:.2f}M", font_size=18, color=WHITE)))
        g.arrange(DOWN, buff=0.4)
        for r in g:
            r[0].set_x(-4.6)
            r[1].set_x(-1.6)
            r[2].set_x(1.3)
            r[3].set_x(3.2)
            r[4].set_x(5.2)
        top = VGroup(*[label(t, font_size=15, color=GREY_A).move_to([x, g.get_top()[1] + 0.45, 0]) for t, x in
                       ((r"users", 1.3), (r"pay in", 3.2), (r"streams", 5.2))])
        note = label(rf"one month: \ a pool of \${d['pool']:,.0f}, \ {sum(s.values()) / 1e6:.1f}M streams, \ {100 * d['rate']:.2f} cents a stream on average",
                     font_size=17, color=GREY_A).to_edge(DOWN, buff=0.5)
        head = label(r"a simulated service", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "How should a service divide its money among artists? To see what is at stake, Monochord simulates a month. "
            "<bookmark mark='a'/> Heavy listeners stream for hours a day, mostly the charts. <bookmark mark='b'/> Light "
            "listeners pay the same fee, play far less, and mostly niche artists: jazz, classical, local scenes. "
            "<bookmark mark='c'/> Free listeners are paid for by advertising, which brings in little. <bookmark mark='d'/> And "
            "twenty bot accounts pay full price and stream one fake artist all month, a track every three minutes. "
            "Twenty artists are stars, two hundred are niche."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top), FadeIn(note))
            for mark, r in zip("abcd", g):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def two_ways(self):
        d = load("pool")
        pr, uc = d["pro_rata"], d["user_centric"]
        top = max(max(pr.values()), max(uc.values()))
        groups = [("chart", r"the 20 chart stars", BLUE), ("niche", r"the 200 niche artists", TUNE), ("fraud", r"the fake artist", EAR)]
        W = 5.2
        bars = VGroup()
        for i, (k, n, col) in enumerate(groups):
            y = 1.3 - 1.25 * i
            b1 = Rectangle(width=W * pr[k] / top, height=0.38, stroke_width=0, fill_color=col, fill_opacity=0.45).move_to([-1.0 + W * pr[k] / top / 2, y + 0.22, 0])
            b2 = Rectangle(width=W * uc[k] / top, height=0.38, stroke_width=0, fill_color=col, fill_opacity=0.95).move_to([-1.0 + W * uc[k] / top / 2, y - 0.22, 0])
            t1 = label(rf"\${pr[k]:,.0f}", font_size=15, color=WHITE).next_to(b1, RIGHT, buff=0.12)
            t2 = label(rf"\${uc[k]:,.0f} \ ({d['change'][k]:+.0f}\%)", font_size=15, color=col).next_to(b2, RIGHT, buff=0.12)
            nm = label(n, font_size=18, color=col).move_to([-3.6, y, 0])
            bars.add(VGroup(nm, b1, t1, b2, t2))
        key = VGroup(label(r"pale: \ pro rata \ (one pool, \ by share of all streams)", font_size=16, color=GREY_A),
                     label(r"solid: \ user-centric \ (each fee, \ by that user's own listening)", font_size=16, color=GREY_A)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        head = label(r"the same month, \ divided two ways", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Now divide the month two ways. <bookmark mark='a'/> Pro rata, as the services do: all the fees go into one pool, "
            "and each artist gets their share of all the streams. <bookmark mark='b'/> User-centric: each listener's fee is "
            "divided among the artists that listener played. <bookmark mark='c'/> Pro rata, the heavy listeners' hours decide "
            "where the light listeners' money goes. User by user, the niche artists' payout here more than doubles, "
            f"{say(d['change']['niche'])} percent, and the stars' falls by {say(-d['change']['chart'])}. <bookmark mark='d'/> Our "
            "population was built so that the two kinds of listener differ sharply; studies of real services' data have found "
            "smaller shifts, with results varying across genres, listener groups and pool designs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*[b[0] for b in bars])))
            vo.wait_until("a")
            self.play(*[FadeIn(VGroup(b[1], b[2])) for b in bars], FadeIn(key[0]))
            vo.wait_until("b")
            self.play(*[FadeIn(VGroup(b[3], b[4])) for b in bars], FadeIn(key[1]))
            vo.wait_until("c")
            self.play(Indicate(bars[1], color=TUNE, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bots(self):
        d = load("pool")
        pr, uc = d["pro_rata"], d["user_centric"]
        lines = VGroup(
            label(rf"the bot farm pays in \${d['bot_fees']:,.0f}", font_size=24, color=WHITE),
            label(rf"pro rata, \ it takes out \${pr['fraud']:,.0f}: \ {pr['fraud'] / d['bot_fees']:.1f} times what it paid", font_size=24, color=EAR),
            label(rf"user-centric, \ it gets back its own \${uc['fraud']:,.0f}, \ and nothing more", font_size=24, color=TUNE),
            label(r"in a pool, \ every fake stream is paid for by every real listener", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.5)
        head = label(r"why fraud pays", font_size=26, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            f"The bots show the pool's weakness. <bookmark mark='a'/> The farm pays in {say(d['bot_fees'])} dollars. "
            f"<bookmark mark='b'/> Pro rata, its fake artist takes out {say(pr['fraud'])}, almost eight times what it paid, "
            "because its streams claim a share of everyone's fees. <bookmark mark='c'/> User by user, it gets back exactly its own "
            "fees, and this particular self-funded bot strategy has no positive gross return in our user-centric model; stolen accounts, subsidies and other fraud remain possible. <bookmark mark='d'/> In a pool, every fake stream is paid for by every real listener."
        ) as vo:
            self.play(FadeIn(head))
            for mark, ln in zip("abcd", lines):
                vo.wait_until(mark)
                self.play(FadeIn(ln))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reforms(self):
        items = [
            (r"SoundCloud \ (2021): \ `fan-powered' user-centric payment for some independent artists", WHITE),
            (r"Deezer with Universal \ (2023): \ an `artist-centric' pool, \ weighting artists with real audiences and streams listeners chose", WHITE),
            (r"Spotify \ (2024): \ a track earns only after 1,000 streams a year; \ penalties for artificial streams; \ minimum lengths for noise", WHITE),
            (r"each change moves money between kinds of artist; \ none is neutral", WHITE),
            (r"the division of a pool is a choice, \ not a law of nature", TUNE),
        ]
        rows_scene(self, r"reforms \ (dated)", items,
                   "The services have begun to change the rules, and each change is dated and disputed. <bookmark mark='b'/> "
                   "In 2021 SoundCloud began paying some independent artists user by user. <bookmark mark='c'/> In 2023 Deezer, "
                   "with Universal, introduced an artist-centric pool that weights artists with real audiences, and streams "
                   "listeners actively chose. <bookmark mark='d'/> In 2024 Spotify stopped paying tracks with fewer than a thousand "
                   "streams a year, penalized artificial streams, and set minimum lengths for noise tracks. <bookmark mark='e'/> "
                   "Each change moves money between kinds of artist; none is neutral. <bookmark mark='f'/> The division of a pool is "
                   "a choice, not a law of nature.", marks="bcdef")
