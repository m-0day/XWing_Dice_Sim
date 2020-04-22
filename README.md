# XWing_Dice_Sim

I made a fully interactive custom dice roll probability calculator for the popular table-top miniatures game Star Wars: X-Wing. Why? Because there are too many modifiers for me to keep track of. Also Why? I wanted to teach my 8 year old about probabilities.

# Click Here for fully interactive binder:
[My Binder](https://mybinder.org/v2/gh/m-0day/XWing_Dice_Sim/master)

(Remember to run all of the cells to generate the plot)

![X-Wing The Tabletop Game](/swz-logotreatment2.png)

![Screen Shot](/Capture.PNG)



The widget accurately plots dice rolls for 1-5 attack dice, 1-5 defense dice, target lock (yes/no), attack focus (yes/no), defense focus (yes/no) and 0-2 defensive evade tokens. All in all this is 600 different plots in one widget.

## But Why Do This?

A) this is a fun game that I play it with my 8 year old so I value the bonding. My son has a built-in sense of probabilities but this is the perfect opportunity to teach him about probability theory. And 
B) I would be tempted forever do this anyway but try to do it in my head, do it badly, and then feel not so great about it.

### Teaching opportunity.

To get an idea how obfuscated the probabilities of certain encounters can get consider this.
An attacker and defender roll dice, one after the other.
The attacker has a 0.5 chance of landing an unmodified hit.
The defender has a 0.375 chance of evading a hit without using dice modifications.
Attackers and defenders may modify one or all of their rolled dice from a "focus" to a "hit" or may re-roll blank dice. Defenders can change one rolled die to an evade per evade token.

To further drive the point home, let's ask ourselves, if I roll 3 red dice and my opponent rolls 2 green dice, what is the distribution of outcomes? Well the below shows the final calculation.

![Outcomes](/counting.jpg)

Great, so now what are my odds ("never tell me the odds") of rolling 2 hits with 3 dice? Let's see.

![Hits math](/hits_pdf.jpg)

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

## How many hits will I score?
If you have M attack dice and your opponent has N defense dice how many hits will you score on him?

Below is the example of M = 1 to 3 attack dice and N = 1 to 3 defense dice, without modifications. So if you rolled one attack die your opponent rolled 1 defense die and so on.

![Resolved Hits](/Figure_3.png)

~~I'm working on this for the moment. Eventually I will show M = 1 to 6 attack dice, unmodified, target lock, focus, and target lock + focus against N = 1 to 6 defense dice, unmodified, focus, and 1 evade.

~~So quick math that will be 6x6x4x3 plots or 432 plots. yikes, 24 pages of subplots.

The widget accurately plots dice rolls for 1-5 attack dice, 1-5 defense dice, target lock (yes/no), attack focus (yes/no), defense focus (yes/no) and 0-2 defensive evade tokens. All in all this is 600 different plots in one widget.

- [x] Accurately Calculate Attack Dice
- [x] Accurately Calculate Defense Dice
- [x] Visualize both of the above
- [x] Accurately Calculate Resolved Hits
- [x] Make Plotly interactive viz for Resolved hits combinations to condense all ~~432 plots.~~ 600 plots.
