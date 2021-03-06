import sys
import time

# Tests:
# python src/main.py test/a_example out/outa.txt
# python src/main.py test/b_little_bit_of_everything.in out/outb.txt
# python src/main.py test/c_many_ingredients.in out/outc.txt
# python src/main.py test/d_many_pizzas.in out/outd.txt
# python src/main.py test/e_many_teams.in out/oute.txt

# alg solution: O(m^2 * n)
# start with random team with largest size
# find best set of pizzas for that team
  # from first pizza:
  # if pizza is all unique ingredients, take it
  # if not, assign value to index (dictionary)
  # if no unique pizza found, add best to pizzas
  # repeat for all pizzas
# move on to next biggest team
# repeat until all teams done

# alg impl
# each time pizza served to team:
  # remove from solution pizzas list, add to teams pizza list
# each time team served:
  # remove team from unserved list, move to served list

# output impl
# print len(served)
# for each team in served, print output

# edge cases:
# too few teams for pizzas
# skip teams until one of valid size found
# ex: 10 4-team 10 3-team 1 2-team, 2 pizzas

class Team:
  def __init__(self, size):
    self.size = size
    self.num_pizzas = 0
    self.pizzas = []
    self.ingredients = []
  
  def add_pizza(self, pizza):
    if len(self.pizzas) == self.size:
      raise Exception(f"Team size is {self.size} and its been fully served!")
    self.pizzas.append(pizza)
    # add ingredients to self.ingredients 
    self.ingredients += pizza.ingredients
    self.num_pizzas += 1

  def overlapping_ingredients(self, pizza):
    # check if pizza to be added's ingredients are overlapping and how much
    a = pizza.ingredientsSet
    b = set(self.ingredients)
    # if all ingredients are unique then len(pizza.ingredients) == len(a - b) ie no of unique ingredients
    # is_unique = len(a) == num_unique
    num_unique = len(a - b)
    is_unique = len(a) == num_unique
    return (is_unique, num_unique)

  def get_score(self):
    return len(set(self.ingredients)) ** 2

  def output(self):
    return f"{self.size} " + " ".join([str(p.index) for p in self.pizzas])
    

class Pizza:
  def __init__(self, index, num_ingredients, ingredients):
    self.index = index
    self.num_ingredients = num_ingredients
    self.ingredients = ingredients
    self.ingredientsSet = set(ingredients)

class Solution:
  def __init__(self):
    self.num_pizzas = 0
    self.pizzas = []
    self.num_doub_teams = 0
    self.num_tri_teams = 0
    self.num_quad_teams = 0
    self.unserved_teams = []
    self.served_teams = []
  
  def print_debug(self):
    print("num_pizzas:", self.num_pizzas)
    print("num_doub_teams:", self.num_doub_teams)
    print("num_tri_teams:", self.num_tri_teams)
    print("num_quad_teams:", self.num_quad_teams)
    print("Pizzas: ")
    for pizza in self.pizzas:
      print(str(pizza.index), str(pizza.num_ingredients), ", ".join(pizza.ingredients))

  def read(self, input_file):
    # open file for reading
    filename = str(input_file)
    with open(filename) as fd:
      
      # read in first line, general info
      lines = fd.read().split('\n')
      n = [int(x) for x in lines[0].split()]
      self.num_pizzas = n[0]
      self.num_doub_teams = n[1]
      self.num_tri_teams = n[2]
      self.num_quad_teams = n[3]
      
      # create teams
      for i in range(0, self.num_quad_teams):
        self.unserved_teams.append(Team(4))
      for i in range(0, self.num_tri_teams):
        self.unserved_teams.append(Team(3))
      for i in range(0, self.num_doub_teams):
        self.unserved_teams.append(Team(2))
      
      # read in pizzas
      for i, l in enumerate(lines[1:]):
        line = l.split()
        if line == []:
          break
        pizza = Pizza(i, int(line[0]), line[1:])
        self.pizzas.append(pizza)

      # sort pizzas by number of ingredients
      self.pizzas.sort(key=lambda x: x.num_ingredients, reverse=True)

# alg solution: O(m^2 * n)
# start with random team with largest size
# find best set of pizzas for that team
  # from first pizza:
  # if pizza has all unique ingredients, take it
  # if not, assign value to index (dictionary)
  # if no unique pizza found, add best to pizzas
  # repeat for all pizzas
# move on to next biggest team
# repeat until all teams done
  def greedy_solve(self):
    for team in self.unserved_teams:
      # not enough pizzas to serve current team
      if len(self.pizzas) < team.size:
        continue
      # for each member, give them best pizza
      for i in range(0, team.size):
        highest_worth = [-1, None]
        found_unique = False
        for pizza in self.pizzas:
          is_unique, num_unique = team.overlapping_ingredients(pizza)
          if is_unique:
            self.pizzas.remove(pizza)
            team.add_pizza(pizza)
            found_unique = True
            break
          else:
            if num_unique > highest_worth[0]:
              highest_worth = [num_unique, pizza]
              
        if (found_unique):
          continue
        else:
          self.pizzas.remove(highest_worth[1])
          team.add_pizza(highest_worth[1])

      # team has been served
      self.served_teams.append(team)
      self.unserved_teams.remove(team)
  
  def get_score(self):
    score = 0
    for team in self.served_teams:
      score += team.get_score()
    return score

  def output(self, out_file):
    f = open(out_file, "w")
    f.write(str(len(self.served_teams)) + "\n")
    for team in self.served_teams:
      f.write(team.output() + "\n")

  def run(self, in_file = None, out_file = None):
    # we cant use out_file = sys.argv[2] because we wont be able to access that index
    self.read(in_file or sys.argv[1])
    self.greedy_solve()
    self.output(out_file or sys.argv[2])

if __name__ == "__main__":
  if sys.argv[1] == "build":
    # input and output files
    files = [
      ["test/a_example", "out/outa.txt"],
      ["test/b_little_bit_of_everything.in", "out/outb.txt"],
      ["test/c_many_ingredients.in", "out/outc.txt"],
      ["test/d_many_pizzas.in", "out/outd.txt"],
      ["test/e_many_teams.in", "out/oute.txt"]
    ]
    scores = []
    for i, v in enumerate(files, 1):
      input_f, output_f = v
      # running solution and measuring peformance
      start = time.time()
      sol = Solution()
      sol.run(input_f, output_f)
      end = time.time()
      # getting score
      score = sol.get_score()
      scores.append(score)
      red = "\x1b[91m"
      clear = "\x1b[0m"
      print(f"build {i} done. time taken : {end - start} score : {red + str(score) + clear}", flush=True)
    # make a bell sound when all builds have been finished
    green = '\x1b[32m'
    print(f'{green}ALL BUILDS DONE. TOTAL SCORE {sum(scores)}\a')
  else:
    sol = Solution()
    sol.run()
