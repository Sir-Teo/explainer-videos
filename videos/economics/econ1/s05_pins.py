from __future__ import annotations

from videos.economics.econ1.common import *  # noqa: F403


class Pins(VoiceoverScene):
    def construct(self):
        card(self, 4, r"The pin factory", r"Why are a group of specialists so much more productive than the same "
             r"people working alone?", "Chapter four. The pin factory.",
             lit={1776: r"\emph{The Wealth of Nations}", 1958: r"\emph{I, Pencil}"}, scale=("firm",),
             horizon=("a day",))
        self.line()
        self.numbers()
        self.reasons()
        self.pencil()

    # ------------------------------------------------------------------
    def line(self):
        s = load("pins")
        short = [r"draw the wire", r"straighten", r"cut", r"point", r"grind the top", r"make the head",
                 r"put it on", r"whiten", r"into the paper"]
        assert len(short) == len(s["steps"])
        chain = flow_chain([(x, E.FIRMS if k % 2 == 0 else GREY_B) for k, x in enumerate(short)], box_w=1.32,
                           box_h=0.95, buff=0.14, font_size=20).move_to(DOWN * 0.2)
        hc = history_card(1776, r"Adam Smith, \emph{The Wealth of Nations}, Book I, chapter 1",
                          r"``a very trifling manufacture'': \ the trade of the pin-maker", color=E.FIRMS, width=7.6,
                          font_size=26).to_edge(UP, buff=0.4)
        n = label(rf"about {s['operations']} distinct operations, \ ``all performed by distinct hands''", font_size=26,
                  color=GREY_A).next_to(chain, DOWN, buff=0.5)
        src = published_tag(tables.SMITH_1776.tag, corner=DL, font_size=18)
        with self.voiceover(
            "Two people gain from trade. Now watch what happens with ten. <bookmark mark='a'/> The Wealth of "
            "Nations, published by Adam Smith in 1776, opens with a factory that makes pins, which he called a very "
            "trifling manufacture. <bookmark mark='b'/> One man draws out the wire, another straightens it, a third "
            "cuts it, a fourth points it, a fifth grinds the top to take the head. Making the head takes two or "
            "three more operations, putting it on is another, whitening the pins another, and putting them into "
            "the paper is a trade by itself. <bookmark mark='c'/> In all, about eighteen distinct operations."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(src))
            vo.wait_until("b")
            for b, a in zip(chain.boxes, list(chain.arrows) + [None]):
                anims = [FadeIn(b, shift=RIGHT * 0.1)]
                if a is not None:
                    anims.append(GrowArrow(a))
                self.play(*anims, run_time=0.55)
            vo.wait_until("c")
            self.play(FadeIn(n))
        self.clear_scene()

    def numbers(self):
        s = load("pins")
        rows = VGroup(
            MathTex(rf"{s['pounds_per_day']}", r"\ \text{pounds a day}", r"\times", rf"{s['pins_per_pound']:,}".replace(",", "{,}"),
                    r"\ \text{pins a pound}", r"=", rf"{s['pins_per_day']:,}".replace(",", "{,}"), r"\ \text{pins}",
                    font_size=38),
            MathTex(rf"{s['pins_per_day']:,}".replace(",", "{,}"), r"\div", rf"{s['men']}", r"\ \text{men}", r"=",
                    rf"{s['per_person']:,}".replace(",", "{,}"), r"\ \text{pins each, a day}", font_size=38),
        ).arrange(DOWN, buff=0.35).to_edge(UP, buff=0.5)
        rows[0][6].set_color(E.FIRMS)
        rows[1][5].set_color(E.FIRMS)
        # 4,800 pins against 20, to scale: a block of 4,800 tiny pins and a row of 20
        cols, rws = 100, 48
        dx, dy, h = 0.072, 0.098, 0.07
        block = VGroup()
        for y in range(rws):
            row = VMobject(stroke_color=E.FIRMS, stroke_width=1.6)
            for x in range(cols):
                row.add_subpath(np.array([[x * dx, -y * dy, 0], [x * dx, -y * dy + h / 3, 0],
                                          [x * dx, -y * dy + 2 * h / 3, 0], [x * dx, -y * dy + h, 0]]))
            block.add(row)
        assert cols * rws == s["per_person"]
        block.move_to([1.4, -1.35, 0])
        alone = VGroup(*[Line([0, 0, 0], [0, h, 0], stroke_width=1.6, color=GREY_A).move_to([x * dx, 0, 0])
                         for x in range(s["alone_at_most"])])
        alone.next_to(block, LEFT, buff=0.7).align_to(block, UP)
        la = VGroup(label(r"alone:", font_size=24, color=GREY_A),
                    label(rf"at most {s['alone_at_most']}", font_size=24, color=GREY_A),
                    label(r"``perhaps not one''", font_size=22, color=GREY_B)).arrange(DOWN, aligned_edge=LEFT,
                                                                                       buff=0.08)
        la.next_to(alone, DOWN, buff=0.25).align_to(alone, LEFT)
        lb = label(rf"in the factory: \ {s['per_person']:,} each".replace(",", "{,}"), font_size=26,
                   color=E.FIRMS).next_to(block, UP, buff=0.15)
        ratio = label(rf"$\times\,{s['ratio_low']}$ \ at the least", font_size=34, color=E.ACCENT)
        ratio.next_to(la, DOWN, buff=0.4).align_to(la, LEFT)
        men = VGroup(*[person(0.55, E.FIRMS) for _ in range(s["men"])]).arrange(RIGHT, buff=0.25).move_to(UP * 0.4)
        with self.voiceover(
            f"Smith had seen a small factory of this kind where only {s['men']} men worked, some of them doing two "
            "or three of the operations. <bookmark mark='a'/> Between them they could make about "
            f"{s['pounds_per_day']} pounds of pins a day, at upwards of four thousand pins to the pound: forty-"
            "eight thousand pins. <bookmark mark='b'/> That's four thousand eight hundred pins a day for each man. "
            "<bookmark mark='c'/> Working alone, without the trade's training or its machines, Smith wrote, each "
            "of them certainly could not have made twenty, perhaps not one. <bookmark mark='d'/> Here are the "
            "four thousand eight hundred, to scale, against the twenty. The same men, the same hours. "
            "<bookmark mark='e'/> At the very least, the division of labour multiplied what each man made by two "
            "hundred and forty."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in men], lag_ratio=0.1))
            vo.wait_until("a")
            self.play(Write(rows[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Write(rows[1]), run_time=1.2)
            vo.wait_until("c")
            self.play(FadeOut(men), FadeIn(alone, lag_ratio=0.1), FadeIn(la), run_time=1.2)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r) for r in block], lag_ratio=0.12), FadeIn(lb), run_time=4)
            vo.wait_until("e")
            self.play(FadeIn(ratio, scale=0.8))
        self.clear_scene()

    def reasons(self):
        cards_ = point_cards([
            (r"dexterity", r"a man who only points pins gets very good at pointing pins", E.FIRMS),
            (r"no time lost switching", r"from one kind of work to another: walking, setting up, warming to it",
             E.FIRMS),
            (r"machines", r"invented, Smith noticed, by people whose whole attention was on one small task",
             E.FIRMS),
        ], width=12.6, cols=3, font_size=24).to_edge(UP, buff=1.3)
        why_head = heading(r"Why so many more pins?")
        limit = VGroup(label(r"Book I, chapter 3:", font_size=26, color=GREY_B),
                       label(r"``the division of labour is limited by the extent of the market''", font_size=32,
                             color=E.ACCENT)).arrange(DOWN, buff=0.15).next_to(cards_, DOWN, buff=0.8)
        q = label(r"48{,}000 pins a day is useless \ unless someone will buy them", font_size=28,
                  color=GREY_A).next_to(limit, DOWN, buff=0.45)
        with self.voiceover(
            "Why so many more? Smith gave three reasons. <bookmark mark='a'/> First, dexterity: a man who does nothing but point pins "
            "becomes very good at pointing pins. <bookmark mark='b'/> Second, no time is lost passing from one kind "
            "of work to another. <bookmark mark='c'/> And third, machines: people whose whole attention is on one "
            "small task are the ones who think of a machine to do it. <bookmark mark='d'/> Then, two chapters "
            "later, he added the catch: the division of labour is limited by the extent of the market. "
            "<bookmark mark='e'/> Forty-eight thousand pins a day is useless unless somebody will buy them. "
            "Specialization only pays if you can trade. Which is exactly the bargain Crusoe and Friday struck, "
            "multiplied a million times."
        ) as vo:
            self.play(FadeIn(why_head))
            for mark, c in zip("abc", cards_.cards):
                vo.wait_until(mark)
                self.play(FadeIn(c, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(limit, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(q))
        self.clear_scene()

    def pencil(self):
        r = tables.READ_1958.data
        pencil = VGroup(
            Rectangle(width=4.6, height=0.36, stroke_width=0, fill_color="#F2C14E", fill_opacity=1),
        )
        tip = Polygon([2.3, 0.18, 0], [2.3, -0.18, 0], [2.85, 0, 0], stroke_width=0, fill_color="#E8C9A0",
                      fill_opacity=1)
        lead = Polygon([2.72, 0.045, 0], [2.72, -0.045, 0], [2.85, 0, 0], stroke_width=0, fill_color="#333",
                       fill_opacity=1)
        ferrule = Rectangle(width=0.4, height=0.38, stroke_width=0, fill_color="#C9B26B", fill_opacity=1).move_to(
            [-2.5, 0, 0])
        eraser = RoundedRectangle(width=0.34, height=0.36, corner_radius=0.06, stroke_width=0, fill_color="#E58C8A",
                                  fill_opacity=1).move_to([-2.86, 0, 0])
        pencil.add(tip, lead, ferrule, eraser)
        pencil.move_to(ORIGIN)
        nodes = VGroup()
        edges = VGroup()
        targets = [pencil[0].get_center() + RIGHT * 0.6, tip.get_center(), eraser.get_center(), eraser.get_center(),
                   ferrule.get_center(), pencil[0].get_center() + LEFT * 0.6]
        positions = [(-4.6, 2.3), (4.4, 2.3), (-5.0, -1.8), (-1.2, -2.6), (2.0, -2.6), (5.0, -1.6)]
        for (what, where), (x, y), tgt in zip(r["inputs"], positions, targets):
            box = VGroup(label(what, font_size=24, color=WHITE), label(where, font_size=20, color=GREY_A))
            box.arrange(DOWN, buff=0.06).move_to([x, y, 0])
            nodes.add(box)
            edges.add(Line(box.get_center(), tgt, color=GREY_D, stroke_width=1.5).set_z_index(-1))
        quote = label(r"``not a single person on the face of this earth knows how to make me''", font_size=28,
                      color=E.ACCENT).to_edge(DOWN, buff=0.45)
        head = label(r"Leonard Read, \ \emph{I, Pencil} \ (1958)", font_size=30, color=GREY_A).to_edge(UP, buff=0.35)
        src = published_tag(tables.READ_1958.tag, corner=UR, font_size=18)
        with self.voiceover(
            "In 1958 Leonard Read told the same story from the other end, in an essay written in the voice of a "
            "pencil. <bookmark mark='a'/> Its family tree begins with a cedar of straight grain, from Northern "
            "California and Oregon. The graphite is mined in Ceylon. The part that does the erasing is made from "
            "rapeseed oil from the Dutch East Indies; the pumice in it is Italian; the ferrule is brass, from zinc "
            "and copper; the wood has six coats of lacquer, made with castor oil. Thousands of people, in many "
            "countries, who will never meet. <bookmark mark='b'/> And the punch line: not a single person on the "
            "face of this earth knows how to make me. <bookmark mark='c'/> Nobody designed the pencil's supply "
            "chain any more than anybody designed the feeding of Paris. Each person in it knows one small thing, "
            "and the next chapter is about how they get the message to do it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pencil, shift=RIGHT * 0.3), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(nd, shift=UP * 0.1), Create(e)) for nd, e in
                                    zip(nodes, edges)], lag_ratio=0.6), run_time=9)
            vo.wait_until("b")
            self.play(FadeIn(quote, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(Indicate(pencil, color=E.ACCENT, scale_factor=1.05))
        self.clear_scene()
