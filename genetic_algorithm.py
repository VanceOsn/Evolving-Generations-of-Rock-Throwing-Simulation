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

    def get_speed(speed):
        return math.pow(2,Individual.num_bits)*Individual.max_speed

    def get_angle(angle):
        return math.pow(2,Individual.num_bits)*Individual.max_angle


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
def mutation(genome, m):
    for i in range(Individual.num_bits):
        if(random.randint(0,1) < m):
            genome ^= (1 << i)


