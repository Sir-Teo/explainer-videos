from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs45.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load


class Hook(VoiceoverScene):
    def construct(self):
        self.utility()
        self.zoom()
        self.price()
        self.plan()

    def utility(self):
        head = label(r"Computing as a utility", font_size=38).to_edge(UP, buff=0.35)
        quote = wrapped_label(r"``computing may someday be organized as a public utility, \ just as the telephone "
                              r"system is a public utility''", 10.0, font_size=26, color=WHITE)
        who = label(r"John McCarthy, \ MIT's centennial, \ 1961", font_size=20, color=GREY_B)
        q = VGroup(quote, who).arrange(DOWN, buff=0.25).next_to(head, DOWN, buff=0.45)
        steps = [(r"1960s", r"time-sharing: \ one mainframe, \ many terminals", GREY_A),
                 (r"1990s", r"own your servers, \ or rent a rack in someone's building", DATA),
                 (r"March 2006", r"Amazon S3: \ storage by the gigabyte-month", YES),
                 (r"August 2006", r"Amazon EC2: \ a computer by the hour", HEAD),
                 (r"today", r"by the second, \ or by the request", KERN)]
        rows = VGroup()
        for t, d, c in steps:
            rows.add(VGroup(label(t, font_size=21, color=c), label(d, font_size=21, color=GREY_A)).arrange(
                RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(q, DOWN, buff=0.55)
        for r in rows:
            r[1].align_to(rows[0][1], LEFT).shift(RIGHT * 0.9)
        with self.voiceover(
            "In 1961, at a celebration of MIT's centennial, John McCarthy predicted that computing might one day be "
            "organized as a public utility, like the telephone system. <bookmark mark='a'/> Time-sharing came "
            "first, many terminals on one mainframe. Then decades in which a company bought its servers, or rented "
            "space for them in someone else's building. <bookmark mark='b'/> In 2006 Amazon began selling storage "
            "by the gigabyte-month, with S3, and computers by the hour, with EC2. <bookmark mark='c'/> Today a "
            "computer can be rented by the second, and a function can be billed per request."
        ) as vo:
            self.play(FadeIn(head), FadeIn(q))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[4]))
        self.wait(0.4)
        self.clear_scene()

    def zoom(self):
        head = label(r"Under the abstraction", font_size=36).to_edge(UP, buff=0.3)
        levels = [(r"a region", r"several buildings, \ tens of kilometres apart", GREY_A, 6.4, 3.2),
                  (r"a building", r"tens of megawatts, \ tens of thousands of servers", DATA, 5.2, 2.6),
                  (r"a rack", r"about forty servers, \ a switch, \ shared power", YES, 4.0, 2.0),
                  (r"a server", r"tens to hundreds of cores", HEAD, 2.9, 1.45),
                  (r"a virtual machine", r"a slice of the server", LAM, 1.9, 0.95),
                  (r"a container", r"a process with walls", KERN, 1.0, 0.5)]
        boxes = VGroup()
        for name, _, col, w, h in levels:
            boxes.add(Rectangle(width=w, height=h, stroke_color=col, stroke_width=2))
        boxes.move_to([-3.0, -0.4, 0])
        for b in boxes[1:]:
            b.move_to(boxes[0])
        legend = VGroup(*[VGroup(label(n, font_size=21, color=c), label(d, font_size=18, color=GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06) for n, d, c, _, _ in levels]).arrange(DOWN, aligned_edge=LEFT,
                                                                                     buff=0.22)
        legend.to_edge(RIGHT, buff=0.6).shift(DOWN * 0.3)
        note_ = note(r"orders of magnitude, \ not a particular provider's numbers", font_size=16).to_edge(DOWN,
                                                                                                    buff=0.2)
        with self.voiceover(
            "Under the word cloud is a physical hierarchy. <bookmark mark='a'/> A region is a few buildings some "
            "distance apart. A building draws tens of megawatts and holds tens of thousands of servers. A rack "
            "holds a few dozen of them, sharing a switch and a power feed. <bookmark mark='b'/> A server is sliced "
            "into virtual machines, and a virtual machine runs containers, which are processes with walls around "
            "them. <bookmark mark='c'/> Every layer is a scheduling problem and a failure domain, and this part goes "
            "down through all of them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(note_))
            vo.wait_until("a")
            for k in range(3):
                self.play(Create(boxes[k]), FadeIn(legend[k]), run_time=0.8)
            vo.wait_until("b")
            for k in range(3, 6):
                self.play(Create(boxes[k]), FadeIn(legend[k]), run_time=0.8)
            vo.wait_until("c")
            self.play(Indicate(boxes, color=WHITE, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    def price(self):
        j = load("job")
        b = j["bill"]
        head = label(r"The Job gets a price", font_size=36).to_edge(UP, buff=0.3)
        rows = [(r"one on-demand server, \ billed per second \ (one-minute minimum)", b["ec2"], DATA),
                (r"the same server at a spot discount", b["spot"], YES),
                (r"sixteen functions, \ billed per gigabyte-second", b["lambda"], HEAD)]
        tiles = VGroup()
        for t, v, c in rows:
            frame = RoundedRectangle(width=4.1, height=2.2, corner_radius=0.15, stroke_color=c, stroke_width=2,
                                     fill_color=BG, fill_opacity=1)
            val = label(rf"\${v:.5f}", font_size=40, color=c)
            d = wrapped_label(t, 3.7, font_size=18, color=GREY_A)
            VGroup(val, d).arrange(DOWN, buff=0.25).move_to(frame)
            tiles.add(VGroup(frame, val, d))
        tiles.arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.8)
        top = label(rf"counting {j['bytes'] / 1e6:.1f} MB of novels: \ {j['seconds']:.2f} s on one core of this "
                    r"machine", font_size=22, color=WHITE).next_to(head, DOWN, buff=0.3)
        foot = wrapped_label(rf"{j['prices']['date']}; \ the spot discount is a typical value, \ not a quote; \ "
                             r"cold starts and reading the text from storage not included", 12.4, font_size=17,
                             color=GREY_B).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "And the Job gets a price. <bookmark mark='a'/> Counting the words of our thirty novels takes "
            f"{j['seconds']:.1f} seconds on one core of the machine that renders this video. <bookmark mark='b'/> "
            "Rented as a server at Amazon's list price, billed by the second with a one-minute minimum, that costs "
            f"about {100 * b['ec2']:.2f} cents. At a typical spot discount, about a third of that. Split across "
            "sixteen functions billed by the gigabyte-second, it costs about three thousandths of a cent. "
            "<bookmark mark='c'/> The prices are list prices for one region, dated, and they leave things out. But "
            "the shape is the point: in the cloud, every design decision in this series has a bill attached."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(top))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.5), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ The Cloud", font_size=36).to_edge(UP, buff=0.3)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"the warehouse-scale computer: \ power, \ cooling, \ failure",
            r"microVMs and containers: \ isolation, \ shrunk",
            r"reconciliation loops and bin packing",
            r"autoscaling as control; \ Erlang C",
            r"eleven nines from erasure codes, \ derived",
            r"networks, \ infrastructure as code, \ cost and carbon",
        ], font_size=25).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 45 of Computer Science, Built, and the start of Act Nine, Systems at Scale. "
            "<bookmark mark='a'/> We will open the warehouse-scale computer and its power bill; shrink virtual "
            "machines into micro-VMs and processes into containers; watch control loops reconcile what is with "
            "what should be; pack containers into machines, a problem that is NP-hard; scale a service as a "
            "feedback controller; derive where the famous eleven nines of storage durability come from; and price "
            "it all."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()


_ = (KERN, LAM, NO, YES)
