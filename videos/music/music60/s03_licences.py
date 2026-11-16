from __future__ import annotations

from videos.music.music60.common import *  # noqa: F403


class Licences(SoundScene):
    def construct(self):
        chapter(self, 2, r"Licences and collecting societies", r"Who has to ask whom, \ and who collects?")
        self.four()
        self.societies()
        self.flows()
        self.gaps()

    # ------------------------------------------------------------------
    def four(self):
        rows_ = [
            (r"mechanical", r"copying the composition: \ a CD, \ a download, \ an on-demand stream", r"composition", TUNE),
            (r"performance", r"playing it in public: \ radio, \ a bar, \ a concert, \ a stream", r"composition \ (and in some countries, \ the recording)", TUNE),
            (r"synchronization", r"putting music to pictures: \ film, \ television, \ an advertisement, \ a game", r"both, \ negotiated", BLUE),
            (r"master use", r"using the recording itself: \ a sample, \ or the recording in a film", r"recording", BLUE),
        ]
        g = VGroup()
        for name, what, whose, col in rows_:
            g.add(VGroup(label(name, font_size=21, color=col), label(what, font_size=17, color=WHITE), label(whose, font_size=16, color=GREY_A)))
        for r in g:
            r[0].move_to([-4.6, 0, 0])
            r[1].move_to([0.4, 0, 0])
            r[2].move_to([4.9, 0, 0])
        g.arrange(DOWN, buff=0.55)
        for r in g:
            r[0].set_x(-5.0)
            r[1].set_x(0.0)
            r[2].set_x(4.8)
        top = VGroup(label(r"licence", font_size=16, color=GREY_A).set_x(-5.0), label(r"for", font_size=16, color=GREY_A).set_x(0.0),
                     label(r"of which work", font_size=16, color=GREY_A).set_x(4.8)).next_to(g, UP, buff=0.4)
        for t in top:
            t.set_y(g.get_top()[1] + 0.4)
        head = label(r"four licences", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Using music means asking permission, and there are four main kinds. <bookmark mark='a'/> A mechanical licence, to "
            "copy the composition: a CD, a download, an on-demand stream. <bookmark mark='b'/> A performance licence, to play it "
            "in public: on the radio, in a bar, at a concert, in a stream; in many countries the recording earns from performance "
            "too. <bookmark mark='c'/> A synchronization licence, to put music to pictures, negotiated with both owners. "
            "<bookmark mark='d'/> And a master use licence, to use the recording itself: a sample, or the original recording in "
            "a film. An on-demand stream needs permissions for both rights layers, including composition reproduction and performance and use of the recording; these four labels are not an exhaustive one-to-one checklist."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top))
            for mark, r in zip("abcd", g):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def societies(self):
        items = [
            (r"1847, \ Paris: \ three songwriters refuse to pay for their drinks at a café whose orchestra plays their songs unpaid", WHITE),
            (r"they win in court, \ and in 1851 found SACEM, \ the first society to collect for performance", WHITE),
            (r"1914: \ ASCAP in New York; \ PRS in London; \ in 1917 the US Supreme Court rules a restaurant must pay for the music it plays", WHITE),
            (r"a society sells one blanket licence for its whole catalogue, \ samples or counts what is played, \ and divides the money", WHITE),
            (r"no venue could ask every songwriter; \ no songwriter could watch every venue", TUNE),
        ]
        rows_scene(self, r"collecting societies", items,
                   "Performance is licensed by collecting societies, and the story of the first is a good one. "
                   "<bookmark mark='b'/> In 1847 three songwriters in Paris refused to pay for their drinks at a café whose orchestra "
                   "played their songs without paying them. <bookmark mark='c'/> They won in court, and in 1851 the society SACEM was "
                   "founded to collect for performance. <bookmark mark='d'/> In 1914 came ASCAP in New York and the Performing Right "
                   "Society in London, and in 1917 the Supreme Court ruled that a restaurant with an orchestra must pay for its music "
                   "even though it charged nothing to hear it. <bookmark mark='e'/> A society sells one blanket licence for its whole "
                   "catalogue, samples or counts what is played, and divides the money. <bookmark mark='f'/> The reason is "
                   "arithmetic: no venue could ask every songwriter, and no songwriter could watch every venue.", marks="bcdef")

    # ------------------------------------------------------------------
    def flows(self):
        def node(t, col, pos, w=2.6):
            r = RoundedRectangle(width=w, height=0.7, corner_radius=0.12, stroke_color=col, stroke_width=2.5).move_to(pos)
            return VGroup(r, label(t, font_size=16, color=col).move_to(pos))
        you = node(r"you", WHITE, [-5.4, 0, 0], 1.4)
        svc = node(r"the service", GREY_A, [-3.2, 0, 0], 2.2)
        lab = node(r"label or distributor", BLUE, [0.2, 1.4, 0], 3.0)
        art = node(r"artist, \ producer", BLUE, [4.0, 1.4, 0], 2.6)
        pub = node(r"publisher", TUNE, [0.2, -0.6, 0], 2.4)
        soc = node(r"societies; \ the MLC", TUNE, [0.2, -1.9, 0], 2.8)
        wri = node(r"songwriters", TUNE, [4.0, -1.2, 0], 2.6)
        arrows = VGroup(Arrow(you.get_right(), svc.get_left(), buff=0.08, color=GREY_B),
                        Arrow(svc.get_right(), lab.get_left(), buff=0.08, color=BLUE),
                        Arrow(lab.get_right(), art.get_left(), buff=0.08, color=BLUE),
                        Arrow(svc.get_right(), pub.get_left(), buff=0.08, color=TUNE),
                        Arrow(svc.get_right(), soc.get_left(), buff=0.08, color=TUNE),
                        Arrow(pub.get_right(), wri.get_left(), buff=0.08, color=TUNE),
                        Arrow(soc.get_right(), wri.get_left(), buff=0.08, color=TUNE))
        n1 = label(r"the recording's money \ (about four fifths of what reaches rights holders)", font_size=15, color=BLUE).next_to(lab, UP, buff=0.25)
        n2 = label(r"the composition's: \ mechanical and performance", font_size=15, color=TUNE).next_to(soc, DOWN, buff=0.25)
        head = label(r"where a stream's money flows", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "So a stream's money flows like this. <bookmark mark='a'/> You pay the service. <bookmark mark='b'/> The recording's "
            "share, about four fifths of what reaches the rights holders, goes to the label or the distributor, and from them, "
            "on the terms of a contract, to the artist and producer. <bookmark mark='c'/> The composition's share goes two ways: "
            "the mechanical part to publishers and, in America since 2021, through the Mechanical Licensing Collective; the "
            "performance part through the societies; and from both, to the songwriters."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(you), FadeIn(svc), GrowArrow(arrows[0]))
            vo.wait_until("b")
            self.play(FadeIn(lab), FadeIn(art), GrowArrow(arrows[1]), GrowArrow(arrows[2]), FadeIn(n1))
            vo.wait_until("c")
            self.play(FadeIn(pub), FadeIn(soc), FadeIn(wri), *[GrowArrow(a) for a in arrows[3:]], FadeIn(n2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gaps(self):
        items = [
            (r"US AM and FM radio pays songwriters, \ but not the performers or owners of the recording: \ a rare exception among large countries", WHITE),
            (r"satellite and internet radio do pay for recordings, \ through SoundExchange", WHITE),
            (r"unmatched money: \ a stream whose song cannot be traced to its writers is held, \ then shared out by market share", WHITE),
            (r"in 2021 the MLC received more than \$400 million of such money from the services", WHITE),
            (r"metadata is money: \ missing ownership metadata can delay, misdirect or prevent payments until corrected", TUNE),
        ]
        rows_scene(self, r"gaps", items,
                   "The pipes leak. <bookmark mark='b'/> American AM and FM radio pays songwriters for performance, but nothing to "
                   "the performers or owners of the recording, a rare exception among large countries. <bookmark mark='c'/> "
                   "Satellite and internet radio do pay for recordings, through SoundExchange. <bookmark mark='d'/> And when a "
                   "stream cannot be matched to its writers, its money is held, and if nobody claims it, shared out by market share, "
                   "mostly to the largest publishers. <bookmark mark='e'/> In 2021 the Mechanical Licensing Collective received more "
                   "than four hundred million dollars of such unmatched money from the services. <bookmark mark='f'/> Metadata is "
                   "money: missing ownership metadata can delay, misdirect or prevent payments until corrected.", marks="bcdef")
