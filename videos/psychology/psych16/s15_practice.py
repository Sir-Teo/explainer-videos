from __future__ import annotations

from videos.psychology.psych16.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.exposure()
        self.training()
        self.cm()
        self.loot()

    def card(self):
        card = chapter_card(14, r"In practice: \ therapy, \ training and games",
                            r"Where does the science of conditioning earn its keep?",
                            lit={1991: r"contingency management", 2018: r"loot boxes"}, part=PART,
                            scale=("person", "group"), marr=("what",))
        with self.voiceover("Chapter fourteen. In practice: therapy, training and games."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def exposure(self):
        head = heading(r"Exposure therapy is extinction")
        rows = rows_of([
            (r"a phobia or a trauma memory: \ a cue that predicts danger, \ and avoidance that keeps the "
             r"prediction from being tested", WHITE),
            (r"exposure: \ meet the cue, \ repeatedly, \ without the feared outcome; \ the prediction error does "
             r"the work", CR),
            (r"among the best-supported treatments for anxiety disorders \ (Parts 40 and 42)", CS),
            (r"but extinction is bound to context, \ so fear returns: \ renewal, \ recovery, \ relapse", INHIB),
            (r"so therapists now vary the places, \ times and cues, \ and aim to violate expectations, \ not just "
             r"to calm", YOU),
        ], 12.4, 28, 0.38).move_to([0, -0.1, 0])
        with self.voiceover(
            "The most important use of conditioning is in treating fear. <bookmark mark='a'/> A phobia, or the fear "
            "after a trauma, behaves like a conditioned response: a cue predicts danger, and avoiding the cue keeps "
            "the prediction from ever being tested. <bookmark mark='b'/> Exposure therapy is extinction. The patient "
            "meets the feared cue, again and again, and the feared outcome doesn't come. The prediction error does the "
            "work. <bookmark mark='c'/> It's among the best-supported treatments for anxiety disorders, and Parts 40 "
            "and 42 weigh the evidence. <bookmark mark='d'/> But chapter eight applies to patients too. Extinction is "
            "tied to its context, and fear treated in a clinic can return at home, or months later. "
            "<bookmark mark='e'/> So modern exposure is designed around Bouton's results: practice in many places, "
            "at different times, with varied cues, and arrange sessions to violate the patient's predictions as "
            "strongly as possible, rather than simply to bring the fear down."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def training(self):
        head = heading(r"Training animals, \ and wards")
        rows = rows_of([
            (r"the clicker: \ a sound paired with food becomes a reward that can be delivered at the exact moment", CS),
            (r"shaping by successive approximation, \ in zoos, \ guide-dog schools and laboratories", CR),
            (r"reward-based training now preferred to punishment, \ which teaches fear of the trainer", US),
            (r"token economies: \ psychiatric wards in the 1960s paid patients in tokens for self-care and work", WHITE),
            (r"they changed behaviour on the ward, \ and often not after discharge; \ and raised hard questions of "
             r"consent", INHIB),
        ], 12.4, 28, 0.38).move_to([0, -0.1, 0])
        with self.voiceover(
            "Skinner's methods are everywhere animals are trained. <bookmark mark='a'/> A clicker is a conditioned "
            "reinforcer: a sound paired with food until the sound itself rewards, and unlike food it can be "
            "delivered at the exact instant of the right movement. <bookmark mark='b'/> Shaping by successive "
            "approximation trains dolphins, guide dogs and laboratory monkeys. <bookmark mark='c'/> Trainers have "
            "largely moved from punishment to reward, partly because punishment teaches a lesson nobody intended: "
            "fear of the trainer. <bookmark mark='d'/> People were trained too. In the 1960s some psychiatric wards "
            "ran token economies, paying patients in tokens, exchangeable for privileges, for dressing, cleaning and "
            "work. <bookmark mark='e'/> Behaviour on the ward changed, often a great deal. It often didn't last after "
            "discharge, where nobody paid tokens, and the practice raised hard questions about consent that helped "
            "shape today's rules for patients' rights."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def cm(self):
        p = archive.PRENDERGAST_2006.data
        head = heading(r"Contingency management for addiction")
        rows = rows_of([
            (r"a clean urine test earns a voucher or a draw for a prize, \ immediately, \ every time", WHITE),
            (rf"a meta-analysis of {p['comparisons']} comparisons: \ $d$ = {p['d']:.2f} on average; \ about "
             rf"{p['d_cocaine']:.2f} for cocaine and {p['d_opiates']:.2f} for opiates", CR),
            (rf"prize-based programmes: \ $d$ = {p['prize_end']:.2f} at the end of treatment, \ "
             rf"{p['prize_3mo']:.2f} three months on, \ none detectable at six", US),
            (r"among the strongest treatments for stimulant use, \ and among the least used: \ paying people is "
             r"unpopular", YOU),
        ], 12.4, 28, 0.4).move_to([0, -0.1, 0])
        tag = published_tag(archive.PRENDERGAST_2006.cite)
        with self.voiceover(
            "The plainest application of the law of effect is in treating addiction. <bookmark mark='a'/> In "
            "contingency management, a urine test free of the drug earns a reward: a voucher, or a draw from a bowl "
            "of prizes, given at once, every time. <bookmark mark='b'/> A 2006 meta-analysis of forty-seven "
            "comparisons found an average effect of about point four standard deviations, and larger for cocaine and "
            "opiates. <bookmark mark='c'/> The effects fade after the rewards stop: for prize-based programmes, about "
            "point four six at the end of treatment, a third of a standard deviation three months later, and nothing "
            "detectable at six. Extinction, again. <bookmark mark='d'/> For stimulants such as cocaine and "
            "methamphetamine, where no medicine works well, it's among the strongest treatments there are, and among "
            "the least used, because paying people not to take drugs strikes many as wrong."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def loot(self):
        p = archive.ZENDLE_CAIRNS_2018.data
        head = heading(r"Variable ratios, \ for sale")
        rows = rows_of([
            (r"a loot box: \ pay, \ and receive a random prize; \ sometimes a rare one", WHITE),
            (r"a variable-ratio schedule, \ chapter three's highest and most persistent rate", US),
            (r"plus near-misses, \ celebratory sounds and lights: \ conditioned reinforcers", CS),
            (rf"{num(p['gamers'])} gamers surveyed: \ spending on loot boxes tracked problem gambling, \ "
             rf"$\eta^2$ = {p['eta2_loot']:.3f}; \ other in-game spending far less", INHIB),
            (r"a survey cannot say which causes which; \ some countries regulate loot boxes as gambling; \ Part 52",
             GREY_A),
        ], 12.4, 28, 0.38).move_to([0, -0.1, 0])
        tag = published_tag(archive.ZENDLE_CAIRNS_2018.cite)
        with self.voiceover(
            "And conditioning is used on all of us. <bookmark mark='a'/> In many video games you can pay for a loot "
            "box: a random prize, usually ordinary, now and then rare. <bookmark mark='b'/> That's a variable-ratio "
            "schedule, the one that in chapter three produced the highest and most persistent responding. "
            "<bookmark mark='c'/> The boxes open with sounds, lights and near-misses, conditioned reinforcers paired "
            "with winning, as in a slot machine. <bookmark mark='d'/> In 2018 David Zendle and Paul Cairns surveyed "
            "over seven thousand gamers. The more people spent on loot boxes, the more severe their problem gambling, "
            "a link much stronger than for other spending in games. <bookmark mark='e'/> A survey can't say whether "
            "the boxes cause gambling problems or attract people who already have them. Some countries now treat "
            "paid loot boxes as gambling. How products are designed around minds is Part 52."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
