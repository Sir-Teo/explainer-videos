from __future__ import annotations

from explainer.industry.register import get
from videos.industry.industry3.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.venice()
        self.dupont()
        self.title()

    def venice(self):
        book = VGroup(
            RoundedRectangle(corner_radius=0.08, width=4.9, height=5.0, fill_color="#2A2418", fill_opacity=1,
                             stroke_color="#7A6A4A", stroke_width=2).move_to(LEFT * 2.5),
            RoundedRectangle(corner_radius=0.08, width=4.9, height=5.0, fill_color="#2A2418", fill_opacity=1,
                             stroke_color="#7A6A4A", stroke_width=2).move_to(RIGHT * 2.5)).shift(DOWN * 0.3)
        spine = Line(UP * 2.2, DOWN * 2.8, color="#7A6A4A", stroke_width=3)
        heads = VGroup(TB("what came in", 22, "#E8D7A8").move_to(book[0].get_top() + DOWN * 0.45),
                       TB("where it came from", 22, "#E8D7A8").move_to(book[1].get_top() + DOWN * 0.45))
        lines = [("cloth from Florence", "owed to the cloth merchant", 120), ("cash from a sale", "pepper sold", 80),
                 ("a ship's share", "cash paid", 200), ("cash", "a loan from a brother", 150)]
        rows_l, rows_r = VGroup(), VGroup()
        for k, (a, b, v) in enumerate(lines):
            y = 1.15 - k * 0.72
            rows_l.add(VGroup(T(a, 16, "#E8D7A8"), T(f"{v} ducats", 16, "#E8D7A8")).arrange(RIGHT, buff=0.3).move_to(
                np.array([-2.5, y - 0.3, 0])))
            rows_r.add(VGroup(T(b, 16, "#E8D7A8"), T(f"{v} ducats", 16, "#E8D7A8")).arrange(RIGHT, buff=0.3).move_to(
                np.array([2.5, y - 0.3, 0])))
        tot = VGroup(TB("550 ducats", 24, I.ACCENT).move_to(np.array([-2.5, -2.3, 0])),
                     TB("550 ducats", 24, I.ACCENT).move_to(np.array([2.5, -2.3, 0])))
        place = T(f"Venice · {get('pacioli.1494'):.0f}", 26, I.DIM).to_edge(UP, buff=0.4)
        # the printed book, closed, above the water of Venice
        cover = VGroup(RoundedRectangle(corner_radius=0.08, width=3.1, height=4.1, fill_color="#4A2E1C", fill_opacity=1,
                                        stroke_color="#C9A26B", stroke_width=3),
                       RoundedRectangle(corner_radius=0.05, width=2.6, height=3.6, fill_opacity=0,
                                        stroke_color="#C9A26B", stroke_width=1.5),
                       TB("Summa de", 26, "#E8D7A8").shift(UP * 0.75), TB("arithmetica", 26, "#E8D7A8").shift(UP * 0.3),
                       T("geometria, proportioni", 15, "#C9A26B").shift(DOWN * 0.2),
                       T("et proportionalita", 15, "#C9A26B").shift(DOWN * 0.48),
                       T("Luca Pacioli", 18, "#E8D7A8").shift(DOWN * 1.1),
                       T("Venice, 1494", 16, "#C9A26B").shift(DOWN * 1.45)).shift(DOWN * 0.1)
        waves = VGroup(*[FunctionGraph(lambda x, k=k: 0.06 * np.sin(3 * x + k), x_range=[-6.5, 6.5],
                                       color="#3B7DD8", stroke_width=2, stroke_opacity=0.6).shift(DOWN * (2.75 + 0.22 * k))
                         for k in range(4)])
        note = T("entries illustrative", 14, I.FAINT).to_corner(DR, buff=0.28)
        src = source("Pacioli, Summa de arithmetica (Venice, 1494): the first printed account of double entry")
        with self.voiceover(
            "In November 1494 a Franciscan friar and mathematics teacher, Luca Pacioli, printed a book in Venice "
            "on arithmetic and geometry. <bookmark mark='a'/> Tucked inside it was a short treatise on how the "
            "merchants of Venice kept their books. It was not his invention; he called it the method of Venice, and "
            "merchants had used it for generations. <bookmark mark='b'/> The rule is simple. Every transaction is "
            "written down twice: once for what came in, <bookmark mark='c'/> and once for where it came from. Cloth "
            "bought on credit is cloth on one side and a debt to the merchant on the other. <bookmark mark='d'/> So "
            "the two sides always add up to the same total, and a mistake shows up as a gap. Five hundred years "
            "later, every company on earth still keeps its books this way."
        ) as vo:
            self.play(FadeIn(place), FadeIn(src), FadeIn(cover, shift=UP * 0.3), run_time=1.4)
            self.play(LaggedStart(*[Create(w_) for w_ in waves], lag_ratio=0.2), run_time=1.6)
            vo.wait_until("a")
            self.play(ReplacementTransform(cover, book), FadeOut(waves), Create(spine), FadeIn(note), run_time=1.4)
            vo.wait_until("b")
            self.play(FadeIn(heads[0]))
            self.play(LaggedStart(*[FadeIn(r) for r in rows_l], lag_ratio=0.3), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(heads[1]))
            self.play(LaggedStart(*[FadeIn(r) for r in rows_r], lag_ratio=0.3), run_time=1.6)
            vo.wait_until("d")
            self.play(FadeIn(tot, shift=UP * 0.1))
            self.play(Indicate(tot, color=I.ACCENT))
        self.clear_scene()

    def dupont(self):
        top = VGroup(TB("Return on investment", 28, I.ACCENT))
        box = lambda t, c: VGroup(RoundedRectangle(corner_radius=0.1, width=3.4, height=0.9, fill_color=I.PANEL,  # noqa
                                                   fill_opacity=1, stroke_color=c, stroke_width=2),
                                  TB(t, 22, c))
        root = box("Return on investment", I.ACCENT).move_to(UP * 1.6)
        m = box("Profit per $ of sales", "#4FA3F7").move_to(LEFT * 3.2 + DOWN * 0.3)
        t = box("Sales per $ invested", "#7BD88F").move_to(RIGHT * 3.2 + DOWN * 0.3)
        times = TB("×", 40, I.TEXT).move_to(DOWN * 0.3)
        for b in (root, m, t):
            b[1].move_to(b[0])
        e1 = Line(root.get_bottom(), m.get_top(), color=I.FAINT, stroke_width=2)
        e2 = Line(root.get_bottom(), t.get_top(), color=I.FAINT, stroke_width=2)
        leaves = VGroup(
            T("price, costs, overheads", 18, I.DIM).next_to(m, DOWN, buff=0.3),
            T("stock, debts owed to it, plant", 18, I.DIM).next_to(t, DOWN, buff=0.3))
        place = T(f"Wilmington, Delaware · DuPont · {get('brown.1914'):.0f}", 24, I.DIM).to_edge(UP, buff=0.4)
        src = source("Hagley Museum and Library, The Father of ROI: Donaldson Brown")
        with self.voiceover(
            "In 1914, four centuries after Pacioli, an engineer turned financial man at the DuPont company, "
            "Donaldson Brown, asked what all those entries add up to. <bookmark mark='a'/> His answer was one number, the "
            "return on investment: how much profit each dollar put into the business earns in a year. <bookmark "
            "mark='b'/> And he split it in two. Profit per dollar of sales, which depends on prices and costs, "
            "<bookmark mark='c'/> times sales per dollar invested, which depends on how hard the plant, the stock "
            "and the money owed by customers are made to work. <bookmark mark='d'/> DuPont's managers met in a room "
            "of charts built on that split, and Brown took the method to General Motors. A century later, it is "
            "still how analysts take a company apart."
        ) as vo:
            self.play(FadeIn(place), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(root, scale=0.95))
            vo.wait_until("b")
            self.play(Create(e1), FadeIn(m))
            vo.wait_until("c")
            self.play(Create(e2), FadeIn(t), FadeIn(times))
            vo.wait_until("d")
            self.play(FadeIn(leaves))
        self.clear_scene()
        del top

    def title(self):
        card_ = part_title(PART, ASK)
        with self.voiceover(
            "Industry, Built. Part three: the accounts. What do a company's accounts say about the business "
            "underneath? This part builds a small company's books from nothing, then reads the real accounts of six "
            "very different companies: a grocer, a software maker, a bank, a power company, an airline and a drug "
            "maker."
        ):
            self.play(FadeIn(card_[0]), run_time=0.8)
            self.play(FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.2)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
