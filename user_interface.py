from model_construction import select_lineup

print(
    """
You will be asked for the number of guards, forwards, and centers you would like in the
lineup. You can have up to 5 of each position but the decision must add up to 5 or you 
run into an error. You will also be asked for the salary year you'd like to use (this
season or next season), and your budget. 
"""
)

guard, forward, center = input(
    """Enter the number of guards, forwards, and centers in the lineup separated 
    by a comma (ex. 2,2,1 would be a 2 guard, 2 forward, 1 center lineup): """
).split(",", 2)
guard = int(guard)
forward = int(forward)
center = int(center)

salaryInput = input(
    """Enter the salary year you would like to use (enter 1 for this season (2021-22) 
    or 2 for next season (2022-23)): """
)
salaryYear = 2122
if salaryInput == "2":
    salaryYear = 2223

budget = float(
    input(
        """Enter the budget of the 5-man lineup (in millions). You can use a decimal but 
    please put in a number: """
    )
)

print(select_lineup(guard, forward, center, salaryYear, budget, "Best Lineup"))

# could give option for minimum total salary or best combo under budget
# give option for salary 21/22 or 22/23
# give option for how many guards, forwards, and centers
# give option for how many lineups to output
# output salary
