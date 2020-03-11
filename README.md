# XWing_Dice_Sim
This accurately simulates the vast combinations of modified dice rolls in the popular table-top miniatures game Star Wars: X-Wing of which I am already a huge fan.

[X-Wing The Tabletop Game](https://www.fantasyflightgames.com/en/products/x-wing/)

To get an idea how obfuscated the probabilities of certain encounters can get consider this.
An attacker and defender roll dice, one after the other.
The attacker has a 0.5 chance of landing an unmodified hit.
The defender has a 0.375 chance of evading a hit without using dice modifications.
Attackers and defenders may modify one or all of their rolled dice from a "focus" to a "hit" or may re-roll blank dice. Defenders can change one rolled die to an evade per evade token.

The sim accurately simulates attack rolls with or without re-rolls (target lock) and with or without modification (focus).

![Attack Dice pdfs](/Figure_1.png)

Moral of the story: Given the choice between Focus and Target Lock always choose Focus because it can be used for defense as well. If you can choose both, always choose both target lock and focus.

There are other much more sophisticated dice simulators out there such as [X-Wing Dice Calculator](http://xwing.gateofstorms.net/2/multi/), but I wanted something to show to my 7 year old that would make sense to him.
