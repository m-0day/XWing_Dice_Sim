# XWing_Dice_Sim
This accurately simulates the vast combinations of modified dice rolls in the popular table-top miniatures game Star Wars: X-Wing of which I am already a huge fan.

[X-Wing The Tabletop Game](https://www.fantasyflightgames.com/en/products/x-wing/)

## But Why Do This? Are you insane?

Only moderately. But this is a fun game and I play it with my 7 year old. He has a built-in sense of probabilities but this is the perfect opportunity to teach him about probability theory. 

And the dice rolling in this game is FULL of probability theory.

To get an idea how obfuscated the probabilities of certain encounters can get consider this.
An attacker and defender roll dice, one after the other.
The attacker has a 0.5 chance of landing an unmodified hit.
The defender has a 0.375 chance of evading a hit without using dice modifications.
Attackers and defenders may modify one or all of their rolled dice from a "focus" to a "hit" or may re-roll blank dice. Defenders can change one rolled die to an evade per evade token.

To further drive the point home, let's ask ourselves, if I roll 3 red dice and my opponent rolls 2 green dice, what is the distribution of outcomes? Well the below shows the final calculation.

![Outcomes](/counting.jpg)

Great, so now what are my odds ("never tell me the odds") of rolling 2 hits with 3 dice? Let's see.

![Hits math](/hits pdf.jpg)

Well that is a bear. Good thing we have python to do all the heavy lifting for us.

## Attack Dice PDF
Let's get into it. Below are the probability distribution functions (pdfs) of various different combinations of number of attack (Red) dice, roll modifications (focus), and re-rolls (target lock).

![Attack Dice pdfs](/Figure_1.png)

Moral of the story: Given the choice between Focus and Target Lock always choose Focus because it can be used for defense as well. If you can choose both, always choose both target lock and focus.

## Defense Dice PDF
Below we see the the pdfs of various different combinations of number of defense (green) dice, evade tokens which add one evade result to your roll, and focus tokens which modify several of your dice in the roll.

![Defense Dice pdfs](/Figure_2.png)

And here we see a surprising result that one evade token is INFERIOR to one focus token for increasing the expected number of evades for all cases except when rolling one die.

###
There are other much more sophisticated dice simulators out there such as [X-Wing Dice Calculator](http://xwing.gateofstorms.net/2/multi/), but I wanted something to show to my 7 year old that would make sense to him in a visual way.
