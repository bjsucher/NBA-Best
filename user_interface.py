from model_construction import get_position_combinations

guards = get_position_combinations("guard", 8, 2, 2122)
forwards = get_position_combinations("forward", 8, 2, 2122)
centers = get_position_combinations("center", 8, 1, 2122)

all_salary = [guards[2], forwards[2], centers[2]]
all_salary_combos = list(product(*all_salary))
all_salary_combos_sum = []
for i in all_salary_combos:
    all_salary_combos_sum.append(sum(i))

for i in all_salary_combos_sum:
    if i < 80000000:
        print(i)

# could give option for minimum total salary or best combo under budget
# give option for salary 21/22 or 22/23
# give option for how many guards, forwards, and centers
# give option for how many lineups to output
# output salary
