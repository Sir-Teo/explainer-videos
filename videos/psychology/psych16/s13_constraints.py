from __future__ import annotations

from videos.psychology.psych16.common import *  # noqa: F403


class Constraints(VoiceoverScene):
    def construct(self):
        self.card()
        self.garcia()
        self.misbehavior()
        self.watching()

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
        rows = rows_of([
            (r"Bandura, \ Ross and Ross, \ 1961: \ 72 nursery-school children", WHITE),
            (r"some watched an adult punch and kick an inflatable doll; \ some a quiet adult; \ some no one", CS),
            (r"left with the doll, \ those who had seen the aggressive model copied it, \ blow for blow", INHIB),
            (r"no reward was given to anyone: \ learning without reinforcement, \ by observation", CR),
            (r"monkeys learn to fear snakes by watching another monkey's fear, \ but not to fear flowers", YOU),
        ], 12.4, 28, 0.4).move_to([0, -0.1, 0])
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
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
