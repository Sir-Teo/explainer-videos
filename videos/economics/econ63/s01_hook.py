from __future__ import annotations

from videos.economics.econ63.common import *  # noqa: F403

HIT = ((0, 3), (1, 9), (2, 5))


def web(width=10.4, height=5.0, node_r=0.07):
    """The Island's supply web in miniature: five tiers of fourteen firms, raw materials on the left and final goods
    on the right, each firm linked to two suppliers in the tier before.  Returns (links, nodes, positions)."""
    Q = load("quake")
    pos = {}
    for t in range(5):
        for i in range(14):
            pos[(t, i)] = np.array([-width / 2 + t * width / 4, height / 2 - i * height / 13, 0])
    links = VGroup()
    for t0, j, t1, i in Q["small_links"]:
        ln = Line(pos[(t0, j)], pos[(t1, i)], stroke_width=1.0, color=GREY_D)
        ln.ends = ((t0, j), (t1, i))
        links.add(ln)
    nodes = VGroup()
    for (t, i), p in pos.items():
        d = Dot(p, radius=node_r, color=NODE)
        d.key = (t, i)
        nodes.add(d)
    return links, nodes, pos


def spread(small_links, hit, steps=3):
    """Firms reached from the hit ones within ``steps`` links, downstream and upstream, by step."""
    down, up = [set(hit)], [set(hit)]
    for _ in range(steps):
        down.append({(t1, i) for t0, j, t1, i in small_links if (t0, j) in down[-1]})
        up.append({(t0, j) for t0, j, t1, i in small_links if (t1, i) in up[-1]})
    return down[1:], up[1:]


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.chains()
        self.question()
        self.title()
        self.objectives()

    def story(self):
        cards = VGroup(
            history_card(2011, r"11 March, \ 2:46 in the afternoon", r"a magnitude 9 earthquake off north-east Japan, "
                         r"\ then a tsunami; \ about 18,000 people dead or missing", color=SHOCK, width=11.2,
                         font_size=21),
            history_card(r"far away", r"undamaged firms stop", r"a plant that makes chips for cars is hit; \ carmakers "
                         r"in other prefectures, \ and in America, \ cut production for want of parts", color=LINK,
                         width=11.2, font_size=21),
            history_card(r"0.47", r"points off Japan's growth", r"the loss travels along the links from supplier to "
                         r"customer and back, \ and adds up to about half a point of GDP growth in the year after",
                         color=GDP, width=11.2, font_size=21),
        ).arrange(DOWN, buff=0.35).move_to(UP * 0.3)
        tag = published_tag(r"Carvalho, \ Nirei, \ Saito and Tahbaz-Salehi, \ Quarterly Journal of Economics 136(2) "
                            r"(2021)", corner=DL, font_size=12)
        with self.voiceover(
            "At a quarter to three in the afternoon of the eleventh of March 2011, an earthquake of magnitude nine "
            "struck off the coast of north-east Japan. The tsunami that followed left about eighteen thousand "
            "people dead or missing. <bookmark mark='a'/> Then something stranger happened. Firms hundreds of "
            "kilometres away, with no damage at all, stopped working. A plant that made the chips that control car "
            "engines was hit, and carmakers in other prefectures, and in America, cut production for want of "
            "parts. <bookmark mark='b'/> Vasco Carvalho, Makoto Nirei, Yukiko Saito and Alireza Tahbaz-Salehi "
            "followed the loss through the records of who supplies whom. It travelled along the links, from "
            "supplier to customer and from customer back to supplier, and added up to about half a point off "
            "Japan's growth in the year after."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.1), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.1))
        self.clear_scene()

    def chains(self):
        Q = load("quake")
        links, nodes, pos = web()
        VGroup(links, nodes).shift(DOWN * 0.35)
        heads = VGroup(*[label(t, font_size=18, color=GREY_B).move_to(pos[(k, 0)] + UP * 0.12)
                         for k, t in enumerate((r"raw materials", r"parts", r"components", r"assembly",
                                                r"final goods"))])
        head = label(r"the Island's firms, \ linked to their suppliers", font_size=26, color=E.ACCENT).to_edge(UP,
                                                                                                        buff=0.35)
        hit = set(HIT)
        down, up = spread(Q["small_links"], hit)
        by_key = {d.key: d for d in nodes}
        tag = island_tag(r"the Island: \ an illustration", corner=DR, font_size=12)
        key = VGroup(label(r"red: \ hit by the disaster", font_size=17, color=SHOCK),
                     label(r"orange: \ short of an input \ (downstream)", font_size=17, color=SEED),
                     label(r"pink: \ lost a customer \ (upstream)", font_size=17, color=BANK)).arrange(
            RIGHT, buff=0.6).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Here is the Island's version, in miniature. <bookmark mark='a'/> Seventy firms in five layers, from "
            "raw materials on the left to final goods on the right; each line is a firm buying from a supplier. "
            "<bookmark mark='b'/> A disaster hits three of them. <bookmark mark='c'/> Their customers are short of "
            "a part, and so are their customers' customers: the shock flows downstream. <bookmark mark='d'/> And "
            "their suppliers have lost a buyer, and so have the suppliers' suppliers: the shock flows upstream "
            "too. <bookmark mark='e'/> Three firms hit; most of the web feels it. Whether that adds up to a "
            "recession depends on how big the firms are, how the links are arranged, and how easily a firm can "
            "replace what it has lost. That is this part."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(heads), Create(links), FadeIn(nodes), run_time=2.5)
            vo.wait_until("b")
            self.play(*[by_key[k].animate.set_color(SHOCK).scale(1.8) for k in hit], FadeIn(key[0]), run_time=1.0)
            vo.wait_until("c")
            self.play(FadeIn(key[1]))
            for step in down:
                ks = [k for k in step if k not in hit]
                ls = [ln for ln in links if ln.ends[1] in step and ln.ends[0] in (hit | set().union(*down))]
                anims = [by_key[k].animate.set_color(SEED) for k in ks] + [
                    ln.animate.set_color(SEED).set_stroke(width=1.6) for ln in ls]
                if anims:
                    self.play(*anims, run_time=0.8)
            vo.wait_until("d")
            self.play(FadeIn(key[2]))
            for step in up:
                ks = [k for k in step if k not in hit and k not in set().union(*down)]
                if ks:
                    self.play(*[by_key[k].animate.set_color(BANK) for k in ks], run_time=0.8)
            vo.wait_until("e")
            self.play(Indicate(nodes, color=WHITE, scale_factor=1.0), run_time=1.5)
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 34, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"why do some firms' troubles matter more than others'?", font_size=26, color=NODE),
            label(r"why don't millions of small shocks simply cancel out?", font_size=26, color=GDP),
            label(r"how do losses travel along supply chains, \ and between banks?", font_size=26, color=SHOCK),
            label(r"how do jobs, \ news and habits travel between people?", font_size=26, color=PEOPLE),
            label(r"and who forms the links, \ and are they the right ones?", font_size=26, color=LINK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "The question: when does a shock to one firm become a shock to everyone? <bookmark mark='a'/> Why do "
            "some firms' troubles matter more than others'? <bookmark mark='b'/> Why don't millions of small "
            "shocks simply cancel out? <bookmark mark='c'/> How do losses travel along supply chains, and between "
            "banks? <bookmark mark='d'/> How do jobs, news and habits travel between people? <bookmark mark='e'/> "
            "And who forms the links in the first place, and are they the right ones?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        links, nodes, _ = web(width=5.2, height=2.4, node_r=0.04)
        g = VGroup(links, nodes)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 63 \ $\cdot$ \ The Economy as a Network", font_size=34, color=E.ACCENT)
        VGroup(g, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part sixty-three: the economy as a network."):
            self.play(FadeIn(g), run_time=1.4)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act XII \ $\cdot$ \ The Frontier", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"input-output networks: \ Leontief's paths and Hulten's theorem",
            r"why idiosyncratic shocks need not wash out: \ big firms, \ lopsided networks, \ large shocks",
            r"supply chains measured, \ and the O-ring",
            r"financial networks: \ clearing, \ contagion, \ robust yet fragile",
            r"social networks: \ weak ties, \ diffusion, \ key players, \ and how networks form",
        ], color=E.ACCENT, font_size=28, width=13.0)
        with self.voiceover(
            "Act eleven was economics at work. Act twelve, the last, is the frontier: where the field is still "
            "finding out. By the end of this part you will know <bookmark mark='a'/> how an input-output table "
            "turns into a network, and why, to a first approximation, a sector matters by its sales and nothing "
            "else; <bookmark mark='b'/> why that approximation fails, so that small shocks need not cancel out; "
            "<bookmark mark='c'/> what the evidence from earthquakes and floods says about supply chains, and why "
            "one weak link can sink a team; <bookmark mark='d'/> how banks' debts to each other can absorb a "
            "shock or spread it; <bookmark mark='e'/> and how jobs and news travel between people, who to tell "
            "first, whom to remove, and why the networks people build are not always the ones we would choose."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
