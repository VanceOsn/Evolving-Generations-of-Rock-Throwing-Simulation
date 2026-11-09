import sys
import random
import math
import pymunk
import pygame

#Individual class, specifies max values of genomes and genome decoding methods
class Individual: 
    max_speed = 60 #m/s
    max_angle = 90 #degrees
    num_bits = 10

    def __init__(self,angle,speed):
        self.speed = speed
        self.angle = angle
        self.fitness = 0

    def get_speed(individual):
        return individual.speed / math.pow(2,Individual.num_bits)*Individual.max_speed

    def get_angle(individual):
        return individual.angle / math.pow(2,Individual.num_bits)*Individual.max_angle



#input: population size
#output: list of random Individuals
#generates a random population
def gen_individuals(pop):
    individuals = []
    for i in range(pop):
        r1 = random.getrandbits(Individual.num_bits)
        r2 = random.getrandbits(Individual.num_bits)

        angle_bits = r1
        speed_bits = r2
        individuals.append(Individual(angle_bits,speed_bits))

    return individuals



#input: genome int representation, mutation rate
#output:number of bits mutations on p1
# chance to flip a bit in the genome depending on mutation rate
# use during crossover
def mutation(p1, m=0.01):
    genome1 = p1.speed
    genome2 = p1.angle
    num_mutations = 0

    for i in range(Individual.num_bits):
    #chance for speed mutation
        r1 = random.random()
        r2 = random.random()

        if(r1 < m):
            genome1 ^= (1 << i)
            num_mutations+=1

    #chance for angle mutation
        if(r2 < m):
            genome2 ^= (1 << i)
            num_mutations+=1

    p1.speed = genome1
    p1.angle = genome2
    return num_mutations



#input Individual, Individual
#creates a new child individual from a single point cross over
#crossover position: num_bits // 2
def crossover(p1, p2):
    cross_point = Individual.num_bits // 2
    low_mask = (1 << cross_point) - 1
    high_mask = ~low_mask

    new_angle = (p1.angle & low_mask) | (p2.angle & high_mask)
    new_speed = (p1.speed & low_mask) | (p2.speed & high_mask)

    return Individual(new_angle, new_speed)




def random_crossover(p1,p2):
    mask = random.getrandbits(Individual.num_bits)
    inv_mask = ~mask

    new_angle = (p1.angle & mask) | (p2.angle & inv_mask)
    new_speed = (p1.speed & mask) | (p2.speed & inv_mask)

    return Individual(new_angle, new_speed)



#input: p1 (individual), target distance, height(default), gravity(default)
#output: fitness of p1 from distance from the target
#rates how fit an individual is, higher = less error/more fit
def fitness(p1, target, h=1, g=9.81):

    angle = Individual.get_angle(p1) * (math.pi/180) #convert to rad
    vx = Individual.get_speed(p1) * math.cos(angle)
    vy = Individual.get_speed(p1) * math.sin(angle)
    
    f1 = (vx/g)
    f2 = (vy + math.sqrt(math.pow(vy,2) + 2 * g * h))
    dist = f1*f2
          
    #dist = (vx / g)(vy + math.sqrt(math.pow(vy,2) + 2 * g * h))
    p1.distance = dist
    delta = math.fabs(target - dist)
    fitness = 1 / (1 + delta)
    p1.fitness = fitness

    return fitness


def sortby_fitness(population, target, h=1, g=9.81):

    for i in population:
        fitness(i,target,h,g)

    return sorted(population, key=lambda Individual: Individual.fitness, reverse=True)



def rws_selection(population, dec_best=0.6):
    num_best = int(len(population) * dec_best)
    best=[]
    for i in range(num_best):
        best.append(population[i])

    return best




def simulate_generations(pop, target, max_gen, max_plateu, dec_best=0.6, m=0.01, h=1, g=9.81, dec_elite=0.05):
    individuals = gen_individuals(pop)
    current_gen = 1
    plateau = 0

    individuals = sortby_fitness(individuals,target,h,g)
    current_best = individuals[0]

#generation loop
    while(current_gen <= max_gen and plateau <= max_plateu):
        #individuals = sortby_fitness(individuals,target)
        selected = rws_selection(individuals,dec_best)



        #perform crossovers and roll mutation
        # children = []
        # for i in range(len(selected)-1):
        #     child = random_crossover(selected[i],selected[i+1])
        #     mutation(child,m)
        #     children.append(child)
        #calculate fitness

        children = cross_until(selected, pop, m, dec_elite)

        individuals = sortby_fitness(children,target,h,g)
        print("LENGTH OF INDIVIDUALS", len(individuals))
        #new best?
        if(current_best.fitness >= individuals[0].fitness):
            plateau+=1
        else:
            current_best = individuals[0]
        current_gen+=1
        print("generation: ",current_gen," best fitness: ", current_best.fitness)

    if(plateau >= max_plateu):
        print("no improvement for ",plateau," generations")

    print("\n-best individual-\nangle: ", Individual.get_angle(current_best),"\nspeed: ", Individual.get_speed(current_best),
          "\ndistance from target: ", (1/current_best.fitness)-1)
    
    return current_best



#population must be sorted or elites will be random
def cross_until(pop, final_size, m, dec_elite):
    paired = set() # p1,p2 and p2,p1 allowed

    num_elite = int(len(pop) * dec_elite)
    new_pop = pop[:num_elite]

    count = len(new_pop)


    while(count <= final_size - num_elite):
        p1 = random.choice(pop)
        p2 = random.choice(pop)
        pair = p1,p2
        if(pair in paired):

            if(reversed(pair) in paired):
                continue
            
            child = random_crossover(p2,p1)
            pair = p2,p1
        else:
            child = random_crossover(p1,p2)

        mutation(child,m)
        new_pop.append(child)
        paired.add(pair)
        count+=1    

    return new_pop



def main():
    simulate_generations(110,20,20,10,0.1,0.01)
    # individuals = gen_individuals(50)
    # individuals = sortby_fitness(individuals,15)


    

    # sum_b = 0
    # best = rws_selection(individuals)
    # for i in best:
    #     sum_b += i.fitness

    # print("\nmutating the children...\n children:\n")
    # childs = []
    # num_mutation = 0
    # for i in range(len(best)-1):
    #     child = random_crossover(best[i],best[i+1])
    #     num_mutation += mutation(child)
    #     childs.append(child)
    # print("mutations: ", num_mutation)
    # childs = sortby_fitness(childs,15)
    # best_c = rws_selection(childs)

    # sum_c =0
    # for i in best_c:
    #     sum_c+=i.fitness

    # c_av = sum_c/len(best_c)
    # p_av = sum_b / len(best)

    # print("\n\naverage parent fitness: ",p_av)
    # print("average child fitness: ",c_av)

    return

if __name__ == "__main__":
        main()