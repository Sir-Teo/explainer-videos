from __future__ import annotations

from videos.psychology.psych14.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.solid()
        self.statistics()
        self.molyneux()
        self.infant()
        self.commits()
        self.rivals()

    def card(self):
        card = chapter_card(14, r"Frontier: \ where priors come from", r"Are the visual system's assumptions learned?",
                            lit={1688: r"Molyneux", 2011: r"Held", 2024: r"Vong"}, part=PART, scale=("mind",),
                            marr=("what",))
        with self.voiceover("Chapter fourteen. The frontier: where priors come from."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def solid(self):
        head = heading(r"What is solid, \ and what is argued")
        left = rows_of([
            (r"what is solid", MODEL),
            (r"images underdetermine scenes; \ perception adds assumptions", WHITE),
            (r"many illusions follow from good assumptions misapplied", WHITE),
            (r"cues are weighted by reliability, \ often near the optimum", WHITE),
            (r"a ventral hierarchy, \ with face-selective regions", WHITE),
        ], 5.6, 26, 0.3)
        right = rows_of([
            (r"what is argued", BAD),
            (r"where the priors come from: \ genes, \ infancy, \ or a lifetime", WHITE),
            (r"whether the brain represents probabilities, \ or only acts as if it did", WHITE),
            (r"how much is inference, \ and how much is rich information in the light", WHITE),
            (r"what deep networks do and do not explain", WHITE),
        ], 5.6, 26, 0.3)
        g = VGroup(left, right).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to([0, 0.4, 0])
        with self.voiceover(
            "Here's where things stand. <bookmark mark='a'/> Solid: images don't determine the scenes that made them, "
            "and perception adds assumptions to close the gap. Many illusions follow from good assumptions used in the "
            "wrong place. Cues are weighted by their reliability, often close to the optimum. And there's a hierarchy "
            "of areas for objects, with regions selective for faces. <bookmark mark='b'/> Argued: where the priors "
            "come from; whether the brain represents probabilities, or merely acts as if it did; how much of seeing "
            "is inference at all; and what deep networks explain. Let's take them in turn."
        ) as vo:
            self.play(FadeIn(head), FadeIn(left[0]), FadeIn(right[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in left[1:]], lag_ratio=0.8), run_time=6.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in right[1:]], lag_ratio=0.8), run_time=6.0)
        self.clear_scene()

    def statistics(self):
        head = heading(r"Priors as the statistics of the world")
        rows = rows_of([
            (r"if priors are learned, \ they should match the world's statistics", WHITE),
            (r"edges in photographs: \ nearby edges tend to continue smoothly, \ as the Gestalt law says", LIKE),
            (r"2006: \ Stocker and Simoncelli fit observers' speed prior from their own judgments: \ heavy-tailed, \ peaked at zero", PRIOR),
            (r"the light-from-above prior moved after an hour or two of training", PRIOR),
            (r"the open part: \ is a prior learned in a lifetime, \ in infancy, \ or by evolution?", BAD),
        ], 12.6, 28, 0.38).move_to([0, -0.1, 0])
        with self.voiceover(
            "If priors are summaries of the world, they should match its statistics. <bookmark mark='a'/> In some "
            "cases they've been checked. <bookmark mark='b'/> Measured in photographs of natural scenes, nearby edges "
            "tend to continue smoothly, at about the rates that predict how people group contours: the law of good "
            "continuation, found in the world. <bookmark mark='c'/> In 2006, Alan Stocker and Eero Simoncelli went "
            "the other way, and fitted each observer's speed prior from their own judgments of speed at different "
            "contrasts. It came out peaked at zero, with heavier tails than a normal distribution. "
            "<bookmark mark='d'/> And chapter seven's light-from-above prior moved after an hour or two of training. "
            "<bookmark mark='e'/> What isn't known is the timescale: whether a given prior is learned in a lifetime, "
            "in infancy, or over evolution, and the answer may be different for each."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def molyneux(self):
        head = heading(r"Molyneux's question, \ answered")
        rows = rows_of([
            (r"1688: \ William Molyneux asks John Locke: \ a man born blind, \ who knows a cube and a sphere by touch,", WHITE),
            (r"is made to see: \ can he tell which is which by sight alone?", WHITE),
            (r"2011: \ Held and colleagues test children in India after cataract surgery, \ within 48 hours", LIKE),
            (r"matching a felt shape to a seen one: \ near chance at first; \ much better within days", POST),
            (r"some links between the senses are learned, \ and quickly; \ the Müller-Lyer illusion was there at once", PRIOR),
        ], 12.6, 28, 0.38).move_to([0, -0.1, 0])
        with self.voiceover(
            "One question about where perception comes from is over three hundred years old. "
            "<bookmark mark='a'/> In 1688, the Irish scientist William Molyneux wrote to the philosopher John Locke. "
            "Suppose a man born blind, who has learned to tell a cube from a sphere by touch, <bookmark mark='b'/> "
            "were suddenly made to see. Could he tell, by sight alone, which was the cube? Locke and Molyneux thought "
            "not. <bookmark mark='c'/> In 2011, Richard Held, Pawan Sinha and colleagues finally asked, with children "
            "in India born with cataracts and treated in Project Prakash. Within two days of surgery, they could see "
            "the shapes clearly, and could match one seen shape to another. <bookmark mark='d'/> But matching a "
            "shape they'd felt to one they saw was near chance. Within days, it was much better. "
            "<bookmark mark='e'/> So some links between the senses must be learned, and are learned quickly. And "
            "recall that the Müller-Lyer illusion was there from the start. Some assumptions seem to need experience; "
            "others don't."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def infant(self):
        head = heading(r"How much can one childhood teach?")
        rows = rows_of([
            (r"head cameras on infants record what one child sees and hears, \ week after week", WHITE),
            (r"2024: \ Vong and colleagues train a network on 61 hours from one child, \ aged 6 to 25 months", POST),
            (r"about 1\% of the child's waking hours: \ the network learns many word-object pairings", POST),
            (r"so some of vision's knowledge can be learned from one child's experience, \ with a generic learner", PRIOR),
            (r"whether infants learn that way is a different question: \ Part 30", GREY_A),
        ], 12.6, 28, 0.38).move_to([0, -0.1, 0])
        tag = published_tag(archive.VONG_2024.cite)
        with self.voiceover(
            "A new kind of evidence comes from cameras worn on infants' heads. <bookmark mark='a'/> Some families "
            "have recorded what one child sees and hears, an hour or two a week, for years. "
            "<bookmark mark='b'/> In 2024, Wai Keen Vong, Brenden Lake and colleagues trained a network on sixty-one "
            "hours of video from one child, recorded between six and twenty-five months of age. "
            "<bookmark mark='c'/> That's about one percent of the child's waking hours. From it, the network learned "
            "to link many words to the objects they name, and its visual features carried over to new images. "
            "<bookmark mark='d'/> So a fair amount of what vision knows can be learned from one child's experience, by "
            "a learner with no built-in knowledge of objects. <bookmark mark='e'/> Whether infants actually learn that "
            "way, and what they bring with them, is the subject of Part 30, the infant mind."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def commits(self):
        head = heading(r"What does \lq\lq Bayesian\rq\rq\ commit you to?")
        rows = rows_of([
            (r"at Marr's first level: \ the task is inference, \ and the optimum is a benchmark", POST),
            (r"at the second: \ does the brain represent whole distributions? \ population codes might", PRIOR),
            (r"the critics: \ with the prior and the loss free, \ almost any data can be fitted afterward", BAD),
            (r"the defence: \ fix them in advance, \ from separate measurements, \ as Ernst and Banks did", LIKE),
            (r"Part 58 takes the strongest version: \ the brain as a machine for prediction", GREY_A),
        ], 12.6, 28, 0.38).move_to([0, -0.1, 0])
        with self.voiceover(
            "What does calling perception Bayesian commit you to? It depends on the level. "
            "<bookmark mark='a'/> At Marr's first level, it says what the problem is, inference under uncertainty, "
            "and gives a benchmark, the best possible answer, to compare people with. That's uncontroversial, and "
            "useful. <bookmark mark='b'/> At the second level it says much more: that the brain represents whole "
            "probability distributions, not single guesses. Some theorists argue that the noisy firing of populations "
            "of neurons could carry exactly that. Whether it does is open. <bookmark mark='c'/> The critics, Jeffrey "
            "Bowers and Colin Davis among them in 2012, point out that with the prior, the likelihood and the loss "
            "all free to choose, a Bayesian model can be fitted to almost any data after the fact. "
            "<bookmark mark='d'/> The defence is to fix them in advance from separate measurements, as Ernst and Banks "
            "did, so that the model can fail. <bookmark mark='e'/> Part 58 takes the boldest version: the brain as a "
            "machine for prediction, from vision to everything else."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def rivals(self):
        head = heading(r"Is it inference at all?")
        rows = rows_of([
            (r"James Gibson, \ 1979: \ the image on one retina is poor, \ but the light around a moving animal is rich", WHITE),
            (r"as you move, \ the flow of the optic array specifies the layout, \ with no need to guess", LIKE),
            (r"and what you see is what you can do: \ affordances, \ a surface to walk on, \ a gap to pass through", PRIOR),
            (r"today's synthesis: \ rich information, \ and inference wherever it runs out", POST),
        ], 12.6, 28, 0.42).move_to([0, -0.1, 0])
        with self.voiceover(
            "A last challenge, to the whole chapter. <bookmark mark='a'/> James Gibson argued, in his book of 1979, "
            "that the inverse problem is an artefact of the laboratory. A single image on one still retina is poor. "
            "But an animal moves, and the light around it changes in structured ways as it does. "
            "<bookmark mark='b'/> The flow of that light specifies the layout of the world, with no need to guess. "
            "<bookmark mark='c'/> And what an animal perceives, he said, isn't geometry but possibilities for action: "
            "a surface to walk on, a gap to pass through, a branch to grasp. He called them affordances, and the word "
            "is now used by designers everywhere. <bookmark mark='d'/> Most researchers now hold both views at once. "
            "There's far more information in the light than a single picture suggests, and inference fills in "
            "wherever that information runs out, which, in a dim room, a blur, a glance or a picture, is often."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
