from __future__ import annotations

import numpy as np

from videos.psychology.psych16.common import *  # noqa: F403


def bobo(height: float = 0.9) -> VGroup:
    """Bandura's inflatable clown: a weighted round base, a tall body and a round head."""
    base = Ellipse(width=0.55 * height, height=0.32 * height, stroke_width=0, fill_color=INHIB, fill_opacity=0.9)
    body = Ellipse(width=0.42 * height, height=0.62 * height, stroke_color=WHITE, stroke_width=2.5,
                   fill_color=INHIB, fill_opacity=0.35).next_to(base, UP, buff=-0.12 * height)
    head = Circle(radius=0.15 * height, stroke_color=WHITE, stroke_width=2.5, fill_color=WHITE,
                  fill_opacity=0.15).next_to(body, UP, buff=-0.04 * height)
    nose = Dot(head.get_center() + DOWN * 0.02 * height, radius=0.035 * height, color=INHIB)
    return VGroup(base, body, head, nose)


class Constraints(VoiceoverScene):
    def construct(self):
        self.card()
        self.garcia()
        self.misbehavior()
        self.watching()
        self.performance()
        self.social()

    def card(self):
        card = chapter_card(12, r"Biology's limits", r"Can any cue be linked to any outcome?",
                            lit={1961: r"Breland \& Breland", 1966: r"Garcia \& Koelling"}, part=PART,
                            scale=("brain", "mind"), marr=("what",))
        with self.voiceover("Chapter twelve. Biology's limits."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def garcia(self):
        head = heading(r"Bright, \ noisy, \ tasty water, \ 1966")
        cells = VGroup()
        txt = [[(r"avoided", CR), (r"not avoided", GREY_B)], [(r"not avoided", GREY_B), (r"avoided", CR)]]
        for i in range(2):
            for j in range(2):
                sq = Square(1.6, stroke_color=GREY_B, stroke_width=2).move_to([-2.4 + 1.6 * j, 0.7 - 1.6 * i, 0])
                t, c = txt[i][j]
                cells.add(VGroup(sq, label(t, font_size=24, color=c).move_to(sq)))
        top = VGroup(label(r"then illness", font_size=24, color=US).next_to(cells[0], UP, buff=0.15),
                     label(r"then shock", font_size=24, color=INHIB).next_to(cells[1], UP, buff=0.15))
        side = VGroup(label(r"the taste", font_size=24, color=CS).next_to(cells[0], LEFT, buff=0.2),
                      label(r"the light and click", font_size=24, color=YOU).next_to(cells[2], LEFT, buff=0.2))
        keep_in_frame(side)
        rows = rows_of([
            (r"rats drank water that was flavoured, \ and lit and clicked as they licked", WHITE),
            (r"illness made them avoid the taste, \ not the light and sound; \ shock, \ the reverse", CR),
            (r"one pairing can be enough, \ with hours between the drink and the sickness", US),
            (r"not every cue is equally linkable to every outcome: \ taste goes with the gut", YOU),
        ], 5.2, 24, 0.32).move_to([3.7, 0.0, 0])
        keep_in_frame(rows)
        tag = historical_tag(archive.GARCIA_KOELLING_1966.cite)
        with self.voiceover(
            "Every result so far assumed that any cue can be linked to any outcome, the same rule for a tone and a "
            "taste, for food and shock. John Garcia broke that assumption. <bookmark mark='a'/> With Robert Koelling, "
            "in 1966, he gave rats water that was flavoured, and that also flashed a light and made a click whenever "
            "they licked. Then some rats were made mildly ill, with X-rays or a lithium injection, and others got a "
            "shock. <bookmark mark='b'/> The sick rats came to avoid the taste, but not the light and click. The "
            "shocked rats avoided the light and click, but not the taste. <bookmark mark='c'/> And with illness, one "
            "pairing could be enough, with hours between the drink and the sickness, a delay that would make any other "
            "conditioning impossible. Journals turned the work down at first: it didn't fit the laws. "
            "<bookmark mark='d'/> But it fits an animal's life. Sickness usually comes from something eaten, hours "
            "earlier, and pain from something seen or heard. If you've ever been unable to face a food after a bout "
            "of sickness that probably wasn't its fault, you've met Garcia's effect."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(top), FadeIn(side), *[FadeIn(c[0]) for c in cells])
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(*[FadeIn(c[1]) for c in cells], FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def misbehavior(self):
        head = heading(r"The misbehaviour of organisms")
        rows = rows_of([
            (r"the Brelands, \ Skinner's students, \ trained thousands of animals for shows and advertisements", WHITE),
            (r"a raccoon paid to drop coins in a box began rubbing them together, \ as raccoons rub food", INHIB),
            (r"pigs carrying tokens to a bank began rooting them along the ground", INHIB),
            (r"the reinforced act drifted toward the animal's natural food behaviour: \ ``instinctive drift''", US),
            (r"preparedness: \ some links are learned easily, \ like fear of snakes; \ others hardly at all", YOU),
        ], 12.4, 28, 0.4).move_to([0, -0.1, 0])
        tag = historical_tag(archive.BRELAND_1961.cite)
        with self.voiceover(
            "The same lesson came from the most practical animal trainers of their day. <bookmark mark='a'/> Keller "
            "and Marian Breland had studied with Skinner, and went into business training animals for fairs and "
            "television. <bookmark mark='b'/> A raccoon was to earn food by dropping coins into a box. It learned, "
            "and then began holding on to the coins and rubbing them together, as raccoons rub and wash their food, "
            "even though that cost it its reward. <bookmark mark='c'/> Pigs carrying wooden tokens to a piggy bank "
            "began dropping them and rooting them along the ground. <bookmark mark='d'/> The reinforced behaviour "
            "drifted back toward the species' own way of handling food. In 1961 they published it, under a title "
            "that teased their teacher: The Misbehavior of Organisms. <bookmark mark='e'/> Martin Seligman later "
            "called the general idea preparedness. Evolution makes some links easy to learn, like fear of snakes or "
            "of heights, and others hard, which is why phobias of electrical sockets are rare."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def watching(self):
        head = heading(r"Learning by watching")
        sub = label(r"Bandura, \ Ross and Ross, \ 1961: \ 72 nursery-school children", font_size=24, color=GREY_A)
        sub.move_to([0, 2.62, 0])
        adult = VGroup(little_person(1.0, color=WHITE), bobo(0.85)).arrange(RIGHT, buff=0.25, aligned_edge=DOWN)
        hit = VGroup(*[Line(ORIGIN, 0.22 * np.array([np.cos(a), np.sin(a), 0]), color=INHIB, stroke_width=3)
                       for a in np.linspace(0, 2 * PI, 7)[:-1]]).move_to(adult[1].get_left() + UP * 0.45 + LEFT * 0.05)
        f1 = VGroup(adult, hit, little_person(0.55, color=YOU).next_to(adult, LEFT, buff=0.35, aligned_edge=DOWN))
        toys = VGroup(Square(0.38, stroke_color=US, stroke_width=3), Circle(radius=0.2, stroke_color=CS, stroke_width=3),
                      Triangle(stroke_color=CR, stroke_width=3).scale(0.24)).arrange(RIGHT, buff=0.18)
        cross = Cross(toys, stroke_color=INHIB, stroke_width=4)
        f2 = VGroup(little_person(0.55, color=YOU), VGroup(toys, cross)).arrange(RIGHT, buff=0.35, aligned_edge=DOWN)
        mallet = VGroup(Line(ORIGIN, UP * 0.55, color=GREY_B, stroke_width=4),
                        Rectangle(width=0.32, height=0.16, stroke_width=0, fill_color=US, fill_opacity=1).shift(UP * 0.6))
        f3 = VGroup(little_person(0.55, color=YOU), mallet, bobo(0.85)).arrange(RIGHT, buff=0.18, aligned_edge=DOWN)
        strip = trial_strip([(r"1. \ watch a model", f1, ""), (r"2. \ toys withheld", f2, ""),
                             (r"3. \ alone with the doll", f3, "")], frame_w=3.1, frame_h=1.75, buff=0.7, font_size=22)
        strip.move_to([0, 1.05, 0])
        A = axes([-0.6, 2.6], [0, 1.0], x_length=5.0, y_length=1.9, xticks=[], yticks=[], xlabel=r"",
                 ylabel=r"imitative aggression", center=[-3.2, -1.75, 0], font_size=19)
        ax = A.ax
        bars, names = VGroup(), VGroup()
        for i, (h, c, nm) in enumerate(((0.85, INHIB, r"aggressive \\ model"), (0.07, CS, r"quiet \\ model"),
                                        (0.06, GREY_B, r"no \\ model"))):
            top = ax.c2p(i, h)[1]
            bars.add(Rectangle(width=0.8, height=max(top - ax.c2p(i, 0)[1], 0.03), stroke_width=0, fill_color=c,
                               fill_opacity=0.85).move_to(ax.c2p(i, 0), aligned_edge=DOWN))
            names.add(Tex(r"\begin{tabular}{c}" + nm + r"\end{tabular}", font_size=19, color=c).next_to(
                ax.c2p(i, 0), DOWN, buff=0.12))
        sch = note(r"schematic: \ the direction of the result", font_size=19).next_to(A, UP, buff=0.05).shift(RIGHT * 0.6)
        cards = point_cards([
            (r"No reward, \ to anyone", r"learning by observation, \ which neither Pavlov's nor Skinner's account "
             r"allowed", CR),
            (r"Monkeys too", r"fear of snakes, \ learned from another monkey's fear; \ not fear of flowers", YOU),
        ], width=6.3, cols=1, font_size=20, buff=0.22)
        cards.move_to([3.35, -2.0, 0])
        tag = historical_tag(archive.BANDURA_1961.cite)
        with self.voiceover(
            "One last limit, of a different kind. <bookmark mark='a'/> In 1961 Albert Bandura, Dorothea Ross and "
            "Sheila Ross ran an experiment with seventy-two children at the Stanford nursery school. "
            "<bookmark mark='b'/> Some watched an adult attack an inflatable clown doll, punching it, kicking it, "
            "hitting it with a mallet. Others watched a quiet adult, or no one. <bookmark mark='c'/> Later, left in a "
            "room with the doll, the children who had seen the attack reproduced it, often move for move. "
            "<bookmark mark='d'/> Nobody was rewarded for anything. The children learned by watching, which neither "
            "Pavlov's nor Skinner's account allowed. How far a doll made to be hit tells us about real aggression is "
            "still argued. <bookmark mark='e'/> Animals do it too. Monkeys raised in a laboratory, with no fear of "
            "snakes, acquire it by watching another monkey react to one. Shown the same reaction to a flower, edited "
            "into the film, they don't learn to fear flowers. Observation and preparedness, together."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(sub, shift=DOWN * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(strip.frames[0]), run_time=1.2)
            vo.wait_until("c")
            self.play(GrowArrow(strip.arrows[0]), FadeIn(strip.frames[1]), GrowArrow(strip.arrows[1]),
                      FadeIn(strip.frames[2]), run_time=1.6)
            self.play(FadeIn(A), FadeIn(names), FadeIn(sch),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.3), run_time=1.6)
            vo.wait_until("d")
            self.play(FadeIn(cards.cards[0], shift=UP * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(cards.cards[1], shift=UP * 0.15))
        self.clear_scene()

    def performance(self):
        head = heading(r"Learning is not doing, \ 1965")
        chain = flow_chain([(r"a film: \ an adult attacks the doll", INHIB),
                            (r"the ending: \ rewarded, \ punished, \ or nothing", US),
                            (r"alone with the doll", CS),
                            (r"then juice and stickers for each act shown", CR)],
                           box_w=2.75, box_h=1.05, buff=0.5, font_size=21)
        chain.move_to([0, 2.05, 0])
        A = axes([-0.6, 2.6], [0, 1.0], x_length=6.4, y_length=2.6, xticks=[], yticks=[], xlabel=r"",
                 ylabel=r"the model's acts reproduced", center=[-2.6, -1.0, 0], font_size=19)
        ax = A.ax
        # schematic heights: the pattern of Bandura (1965), not its means
        free, paid = (0.55, 0.22, 0.52), (0.82, 0.78, 0.8)
        bars0, bars1, names = VGroup(), VGroup(), VGroup()
        for i, nm in enumerate((r"model \\ rewarded", r"model \\ punished", r"no \\ consequence")):
            for j, (h, c, grp) in enumerate(((free[i], GREY_B, bars0), (paid[i], CR, bars1))):
                x = i - 0.2 + 0.4 * j
                grp.add(Rectangle(width=0.36, height=ax.c2p(x, h)[1] - ax.c2p(x, 0)[1], stroke_width=0, fill_color=c,
                                  fill_opacity=0.85).move_to(ax.c2p(x, 0), aligned_edge=DOWN))
            names.add(Tex(r"\begin{tabular}{c}" + nm + r"\end{tabular}", font_size=19, color=GREY_A).next_to(
                ax.c2p(i, 0), DOWN, buff=0.12))
        lg = legend([(GREY_B, r"left to play"), (CR, r"offered a reward to show them")], font_size=19)
        lg.next_to(A, UP, buff=0.12).align_to(A, LEFT).shift(RIGHT * 0.6)
        sch = note(r"schematic: \ the pattern of the result, \ not its means", font_size=19)
        sch.next_to(names, DOWN, buff=0.12)
        cards = point_cards([
            (r"Vicarious reinforcement", r"what happens to the model changes what the watcher does", US),
            (r"Learning and performance", r"reward decides what we do with what we know, \ not whether we "
             r"learn it", CR),
        ], width=4.9, cols=1, font_size=20, buff=0.22)
        cards.move_to([4.15, -1.15, 0])
        tag = published_tag(r"Bandura (1965); \ the bars are schematic")
        with self.voiceover(
            "Bandura then asked what the watching had actually taught. <bookmark mark='a'/> In 1965 he showed "
            "sixty-six nursery-school children a short film of an adult attacking the doll, with one of three "
            "endings. In one, another adult rewarded the model with sweets and praise. In another, the model was "
            "scolded and spanked. In the third, nothing followed. <bookmark mark='b'/> Then each child was left with "
            "the doll. Those who had seen the model punished copied fewer of the attacks than the others. What "
            "happened to the model worked on the watchers, which Bandura called vicarious reinforcement. "
            "<bookmark mark='c'/> Then came the twist. An experimenter came back and offered every child fruit juice "
            "and stickers for each of the model's acts they could show. The differences between the groups almost "
            "vanished. The children who had seen the punishment had learned the acts as well as anyone; they had "
            "simply not chosen to perform them. <bookmark mark='d'/> That is the distinction between learning and "
            "performance. On this view, reward decides what we do with what we know, not whether we learn it, and "
            "the learning itself can happen by watching alone."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(chain.boxes[0]), GrowArrow(chain.arrows[0]), FadeIn(chain.boxes[1]), run_time=1.4)
            vo.wait_until("b")
            self.play(GrowArrow(chain.arrows[1]), FadeIn(chain.boxes[2]), FadeIn(A), FadeIn(names), FadeIn(sch),
                      FadeIn(lg[0]), run_time=1.2)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars0], lag_ratio=0.3), run_time=1.4)
            self.play(FadeIn(cards.cards[0], shift=UP * 0.15))
            vo.wait_until("c")
            self.play(GrowArrow(chain.arrows[2]), FadeIn(chain.boxes[3]), FadeIn(lg[1]), run_time=1.2)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars1], lag_ratio=0.3), run_time=1.4)
            vo.wait_until("d")
            self.play(FadeIn(cards.cards[1], shift=UP * 0.15))
        self.clear_scene()

    def social(self):
        head = heading(r"Social learning, \ and what became of the doll")
        card_ = theory_card(r"Social learning theory", r"Albert Bandura, \ 1977",
                            r"we learn from what others do and from what happens to them; \ attention, \ memory, \ "
                            r"the means and the motive decide what we copy; \ and self-efficacy, \ the belief that we "
                            r"can, \ decides whether we try", r"learning by watching: \ solid", "replicated",
                            width=5.6, font_size=21, color=CR)
        card_.move_to([-3.45, -0.2, 0])
        checks = verdict_row([
            (r"Bandura, \ Ross and Ross, \ 1963: \ a model on film, \ even one dressed as a cartoon cat, \ "
             r"copied like one in the room", "replicated"),
            (r"Anderson and colleagues, \ 2010: \ violent video games, \ small effects on aggression", "contested"),
            (r"Ferguson; \ Hilgard, \ Engelhardt and Rouder, \ 2017: \ the effects overstated, \ once bias "
             r"and weak measures are allowed for", "contested"),
        ], width=6.6, font_size=20)
        checks.move_to([3.3, 0.35, 0])
        doll = label(r"a doll made to be hit cannot settle it", font_size=21, color=GREY_B)
        doll.next_to(checks, DOWN, buff=0.45)
        tag = published_tag(r"Bandura, \ Ross \& Ross (1963); \ Bandura (1977); \ Anderson et al.\ (2010); \ "
                            r"Ferguson \& Kilburn (2010); \ Hilgard, \ Engelhardt \& Rouder (2017)")
        with self.voiceover(
            "Bandura built these results into a theory. <bookmark mark='a'/> In his 1977 book, Social Learning "
            "Theory, people learn from what others do and from what happens to them. Whether an act is copied "
            "depends on attention, on memory, on being able to do it, and on a reason to. The same year he added "
            "self-efficacy: a person's belief that they can carry out an action, which shapes whether they try it, "
            "and how long they keep going. <bookmark mark='b'/> Imitation itself has a good record. In 1963 the same "
            "team found that children copied an aggressive model on film, even one dressed as a cartoon cat, much as "
            "they copied one in the room, and imitation of models has been found in many settings since. "
            "<bookmark mark='c'/> The leap from the doll to violence in the world is another matter. In 2010 Craig "
            "Anderson and colleagues pooled studies of violent video games and found small effects on aggressive "
            "thoughts, feelings and behaviour. <bookmark mark='d'/> Christopher Ferguson argued that the effects "
            "shrink once weak measures and unpublished studies are allowed for, and in 2017 a reanalysis by Joseph "
            "Hilgard, Christopher Engelhardt and Jeffrey Rouder found the experimental effects overstated. "
            "<bookmark mark='e'/> So children learn by watching, and that is solid. Whether watching violence makes "
            "for violence is still argued, and a doll made to be hit cannot settle it. That is where the Ledger "
            "takes over."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(card_.box), FadeIn(card_.name), FadeIn(card_.claim), run_time=1.4)
            vo.wait_until("b")
            self.play(FadeIn(checks.rows[0], shift=RIGHT * 0.15))
            self.play(FadeIn(card_.verdict), FadeIn(card_.status))
            vo.wait_until("c")
            self.play(FadeIn(checks.rows[1], shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(checks.rows[2], shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(doll, shift=UP * 0.1))
        self.clear_scene()
