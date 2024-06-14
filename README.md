# Highest Score on Ticket to Ride

## Project description
Purpose of this analysis is to find the highest possible score you can get by playing the game "Ticket to Ride (USA)".

You can check details of the game [here](https://cdn.1j1ju.com/medias/2c/f9/7f-ticket-to-ride-rulebook.pdf)

## :world_map: Found results
- It'd very time consuming to calculate all possible Destination Ticket combinations (about 3 million sec on my pc)
- All found scores were $\leq$ 275. And all of the top scores had very similar paths

## Highest score: 275
![275](/plots/score_275.png)

> [!NOTE]
> It is not guaranteed that this is the highest score possible. The first algorithm test_combinations() I made, found me 232 points. But this algorithm highly depends on the order of Destination Tickets. This motivated me to define test_combinations_shuffle() which gave me other much higher scores comparing to 232.
Considering the fact that finding scores 270-275 is relatively easy with this new function (finds 1-2 each minute) and since all of these found new scores were just rearrangements of the Destination Ticket orders, we can say that all found solutions for 270,272,273,274,275 are unique. And it's not very likely that there's a higher point

## Which kind of scores wasn't included
- Since this version is only for single-player, no longest train point is added (10 points)
- In the end of the game using some trains (without a Destination Ticket) just to get some extra points (this will not affect our score since all found high scores had 45 trains)

## Other high scores 270-274
![274](/plots/score_274.png)
![273](/plots/score_273.png)
![272](/plots/score_272.png)
![270](/plots/score_270.png)

## About the plots

**Trains:** Total number of trains used

**Points(p1+p2):**
```
 p1: total points collected from Destination Tickets
 p2: total points collected from Routes 
```
**Target Cities:** Beginning or end of the selected Destination Tickets

**Other Cities:** All other visited cities that are not targeted

**The text on top:** Selected Destination Tickets with corresponding points

## Thanks to
[Rob217](https://github.com/Rob217/TicketToRideAnalysis) for gathering all the .txt files and city_locations.json file I've used in my code.
