# NBA-Best

The application NBA Best looks at NBA player stats and salaries to put together a 5-man roster based on user input (budget, scoring priority, injury history, offensive/defensive focus, etc.).

We used the Beautiful Soup python library to parse data from the website "HoopsHype" for salary and player statistics for all NBA players in the year 2021-2022. If a player has salary information for the 2022-2023 basketball season, we also collected this information.

To find the best lineup based on the user's inputs, the model first finds the player with the highest value for each statistic based on position. The model then normalizes all of the statistics based on the maxmium value for that statistic by player position. 

To create his lineup, the user will first be prompted to put in the number of guards, forwards, and centers he would like on his team. He can put up to 5 players at any position but the total number of players at the three positions must add up to 5. The user will then be prompted to put in which salary year he would like to look at (2021-2022 or 2022-2023) and his salary budget. After these values are inputted, the user will assign a weight to each player statistic to indicate the importance the user puts on each statistic relative to the other statistics.