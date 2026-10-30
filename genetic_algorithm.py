import sys
import random
import math

#Individual class, specifies max values of genomes and genome decoding methods
class Individual: 
    max_speed = 40 #m/s
    max_angle = 90 #degrees
    num_bits = 10

    def __init__(self,angle,speed):
        self.speed = speed
        self.angle = angle

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



#input genome int representation, mutation rate
# chance to flip a bit in the genome depending on mutation rate
# use during crossover
def mutation(p1, m):
    genome1 = p1.speed
    genome2 = p1.angle
    num_mutations = 0

    for i in range(Individual.num_bits):
    #chance for speed mutation
        if(random.randint(0,1) < m):
            genome1 ^= (1 << i)
            num_mutations+=1

    #chance for angle mutation
        if(random.randint(0,1) < m):
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

def main():
    individuals = gen_individuals(2)
    p1 = individuals[0]
    p2 = individuals[1]
    p3 = crossover(p1,p2)

    print("p1 speed ",Individual.get_speed(p1))
    print("p2 speed ",Individual.get_speed(p2))
    print("p3 speed ",Individual.get_speed(p3))

    

    print("\n\np1 ang ",Individual.get_angle(p1))
    print("p2 ang ",Individual.get_angle(p2))
    print("p3 ang ",Individual.get_angle(p3))

    num_mutations = mutation(p3,0.0001)

    print("\nmutation\np3 speed ",Individual.get_speed(p3))
    print("p3 ang ",Individual.get_angle(p3))
    print(num_mutations)

    return

if __name__ == "__main__":
        main()