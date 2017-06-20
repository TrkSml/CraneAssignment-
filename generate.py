"""pour liberer les grues faire un trruc du genre :
pour chercher quelle crane, on raisonne comme pour les quays : on calcule la distance la plus courte 
"""
import random as rdm 
from load import * 
from core import Solution

quay_nb = lambda x : "RORO" if x in [2,3,4,5] else "PC"
modulo_quay = lambda x : 1 if x > 7 else x

ls_boats = [] 
ls_cranes_used = []
ls_assignement = []
quays  = [Quay(quay_nb(x),x) for x in range(1,7)]
cranes = [Crane(x) for x in range(1,7)]
cranes_queued = []
nb_crane = lambda : 2 if (rdm.random() > 0.7) else 1
verif = lambda  boat, quay : (boat.type_boat == quay.type_quay)

def sepererator() :
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


def merge_quay_crane_assignement() : 
	global ls_boats 
	ls_boats = read_csv(PATH)
	for boat in ls_boats : 
		if boat.type_boat == "PC" : 
			nb_crane_assgn = 1
			service_time = boat.capa_cont /nb_crane_assgn
			service_time = datetime.timedelta(0,60 * service_time)
			
		if boat.type_boat == "RORO" : 
			manu = boat.capa_remor
			min_total = ( 40 / 60 ) *  boat.capa_cont 
			delta_assignement = max(datetime.timedelta(0,60 * min_total), datetime.timedelta(0,60 *  manu  ))
			service_time = datetime.timedelta(0,60 *  manu  )
			
		Q = assign_quay(boat, service_time)
		C = assign_crane(boat, service_time)
		boat.starting_time = max(Q.time_freed - service_time, C.time_freed - service_time)
		boat.ending_time = max(Q.time_freed, C.time_freed)
		boat.ending_time = boat.departure if abs(boat.ending_time-boat.arrival_time) > abs(boat.departure-boat.arrival_time) else boat.ending_time 
		B = boat
		time = (B.arrival_time, B.ending_time)
		print(str(B.type_boat)+"  :: arrive à "+str(B.arrival_time)+" servi à : "+str(B.starting_time)+" fini à : "+str(B.ending_time)+" au quai N° : "+str(Q.lib))
		sepererator()
	


def assign_quay(boat, service_duration) : 
	global quays 
	global cranes

	#creation de la liste des quays concernes 
	concerned = [quay for quay in quays if verif(boat, quay)]
	ls_quays_free = [quay for quay in concerned if quay.queue == False] 
	ls_quays_busy = [quay for quay in concerned if quay.queue == True] 
	#on cree une liste contenant des tuple (quay_busy, boat)
	if len(ls_quays_free) == 0 : 
		distance = []
		#print(concerned[0].type_quay)
		for busy in ls_quays_busy : 
			distance.append((abs(boat.arrival_time - busy.time_freed), busy ))
		q = min(distance, key=lambda x: x[0]) 
		q = q[1]
		q.time_freed = max(q.time_freed, boat.arrival_time)
		q.time_freed += service_duration
		q.queue = True
	else : 
		q = concerned[0]
		#del quays[0] 
		q.time_freed = max(q.time_freed, boat.arrival_time)
		q.time_freed +=  service_duration
		q.queue = True
		ind = quays.index(q)
		quays[ ind ] = q
		
		
	return q

def assign_crane(boat, service_duration): 
	global cranes 
	global cranes_queued
	service_time = boat.arrival_time
	if len(cranes) == 0 : 
		distance = [] 
		for crane in cranes_queued : 
			distance.append((abs(crane.time_freed - boat.arrival_time), crane))
		c = min(distance, key=lambda x: x[0])
		c[1].time_freed =boat.arrival_time + service_duration
		cranes_queued[cranes_queued.index(c[1])] = c[1]
		return c[1]
	else : 
		c = cranes[0]
		del cranes[0]
		c.time_freed =boat.arrival_time + service_duration 
		c.queue = True
		cranes_queued.append(c)
		return c



def generate() : 
	merge_quay_crane_assignement()

if __name__ == "__main__" : 
	generate()