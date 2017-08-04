"""PA et PB sont deux parents (deux solutions). La mutaion est le cas particulier 
	mutation(adam) == crossover(adam, adam) la mutation est la forme quadratique associée à la la forme bilinéaire symétrique de la fnc crossover. 
"""

import random as rdm
from load import Boat
import datetime
from generate import merge_quay_crane_assignement, sepererator, crisis_time, compute_time


NB_POPULATION = 10
MUTATION_CROSSOVER = 0.7   #70% chance for a mutation
PARENT_CHOICE      = 0.5

choose = lambda chance : rdm.random() < chance

def pick_up(PA, PB) : 
	x = rdm.choice(PA.list_boat)
	y = rdm.choice(PB.list_boat)
	while (x == y) or (x.type_boat != y.type_boat) : 
		y = rdm.choice(PB.list_boat)
	return x,y 

def update(new_boat, quay) : 
	new_boat.starting_time = max(new_boat.arrival_time, quay.starting_time)
	new_boat.ending_time   = new_boat.starting_time 
	return new_boat

def crossover(PA, PB) : 
	"""prends deux solutions en entrée. """
	gene_one, gene_two = pick_up(PA, PB) 
	ind_A = PA.list_boat.index(gene_one)
	ind_B = PB.list_boat.index(gene_two)
	gene_quay_one = PA.list_quays[ind_A]
	gene_quay_two = PA.list_quays[ind_B]
	service_time_A = compute_time(gene_one)
	service_time_B = compute_time(gene_two)
	# dans ce qui suit, les quays ne "bougent" pas contrairement aux boats
	gene_quay_one.starting_time = max(gene_two.arrival_time, gene_quay_one.starting_time)
	gene_quay_two.starting_time = max(gene_one.arrival_time, gene_quay_two.starting_time)
	gene_quay_one.time_freed += service_time_B
	gene_quay_two.time_freed += service_time_A
	PA.list_boat[ind_A] = update(gene_one, gene_quay_two)
	PB.list_boat[ind_B] = update(gene_two, gene_quay_one)
	PA.list_quays[ind_A] = gene_quay_one
	PB.list_quays[ind_A] = gene_quay_two
	return PA if max(PA.performance, PB.performance) == PA.performance else PB
	
	
#def mutation(adam) : 
	#global crisis_time
	#ls_boats_to_permute = adam.list_boat
	#ls_quays_to_permute = adam.list_quays
	#ls_times_to_permute = adam.list_time
	#crisis              = adam.crisis_time
	#print(ls_times_to_permute)
	#x = rdm.sample(adam.list_boat, 2)
	#while ( (x[0].type_boat != x[1].type_boat) and (x[0] != x[1]) ):
		#x = rdm.sample(set(adam.list_boat), 2) 
	#gene_one = x[0]
	#gene_two = x[1]
	#ind_gene_boat_one = adam.list_boat.index(gene_one)
	#ind_gene_boat_two = adam.list_boat.index(gene_two)
	#gene_quay_one = adam.list_quays[ind_gene_boat_one]
	#gene_quay_two = adam.list_quays[ind_gene_boat_two]
	#gene_time_one = ls_times_to_permute[ind_gene_boat_one]
	#gene_time_two = ls_times_to_permute[ind_gene_boat_two]
	#first_to_arrive = min(gene_time_one[0], gene_time_two[0])
	#sepererator()
	#print("on va permuter un "+str(gene_one.type_boat)+" ; "+str(gene_one.starting_time)+" avec un "+str(gene_two.type_boat)+" ; "+str(gene_two.starting_time)+ " le premier arrive à : "+str(gene_one.arrival_time)+" et le deuxieme arrive à : "+str(gene_two.arrival_time)+"   on sera à court de crane à apartir de : "+str(adam.crisis_time))
	#if  gene_one.type_boat == "PC" :
		#if gene_one.arrival_time > gene_quay_two.time_freed : 
			#gene_one.starting_time = gene_quay_two.time_freed
		#else : 
			#gene_one.starting_time = gene_one.arrival_time
		#if gene_two.arrival_time > gene_quay_two.time_freed : 
			#gene_two.starting_time = gene_quay_two.time_freed 
		#else : 
			#gene_two.starting_time = gene_two.arrival_time
		#if gene_one.starting_time > crisis_time : 
			#print("pas de probleme pour les grues")
		#else : 
			#print("pas de grue, il faut attendre")
	##print("finalement le premier PC va commencer à "+ str(gene_one.starting_time)+"  alors qu'il est arrivé à "+str(gene_one.arrival_time))
	#print(gene_two)
	#print(adam.list_boat[ind_gene_boat_one])
	#adam.list_boat[ind_gene_boat_one] = gene_two
	#print(adam.list_boat[ind_gene_boat_one])
	#adam.list_boat[ind_gene_boat_two] = gene_one
	#adam.list_quays[ind_gene_boat_one] = gene_quay_two
	#adam.list_quays[ind_gene_boat_two] = gene_quay_one
	##adam.list_boat  = adam.list_boat
	##adam.list_quays = adam.list_quays
	#return adam 

class Solution : 
	"""la classe solution permet de definir une solution au probleme (ie) une solution represntable sous forme de GANTT. Elle est caracterisee par un float Performance qui nous informe sur le rendement """
	def __init__(self, list_boat, list_time, list_quays, crisis) :
		"""On la remplir avec un vecteur de bateaux et un autre vecteur sur les heures de departs et darrivee. Finalement un troisieme vecteur sur le nombre de grues. """
		self.list_boat   = list_boat                   
		self.list_time   = list_time                   
		self.list_quays  = list_quays 
		self.lenght = len(list_boat)
		self.crisis_time = crisis
		self.performance = self.compute()
	def compute(self) : 
		S = datetime.timedelta(seconds = 0 )
		for elem in self.list_boat : 
			S += abs(elem.ending_time - elem.arrival_time)
		return S

def seek_and_give_birth(ls_solution) : 
	couple = find_besties(ls_solution)
	child  = compute_next_indiv(couple[0], couple[1])
      
def compute_next_indiv(sol_parent_1,sol_parent_2) : 
	if (choose(MUTATION_CROSSOVER)) : 
		child = crossover(sol_parent_1, sol_parent_2)
	else : 
		if (choose(PARENT_CHOICE)) : 
			child = crossover(sol_parent_1, sol_parent_1)
		else : 
			child = crossover(sol_parent_2, sol_parent_2)
	return child

def generate() : 
	list_boat, list_time, list_quays, crisis = merge_quay_crane_assignement()
	adam = Solution(list_boat, list_time, list_quays, crisis)
	return adam

if __name__ == "__main__" : 
	sol = generate()
	#mutated = mutation(sol)
	#print(mutated.list_boat == sol.list_boat)
	#for elem in mutated.list_boat
	#print(mutated.list_boat)
	sepererator()
	#for i in range(50000) : 
		#sol = crossover(sol, sol)
		#print(sol.performance)
	
	