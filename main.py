from math import log2
from random import choices, randint, random, shuffle
from copy import copy

file = "input.in"
with open(file) as f:
    population_dimension = int(f.readline())
    a, b = [int(i) for i in f.readline().split()]
    c2, c1, c0 = [int(i) for i in f.readline().split()]
    number_of_decimals = int(f.readline())
    crossover_probability = float(f.readline())
    mutation_probability = float(f.readline())
    generations = int(f.readline())
chromosome_size = int(log2((b - a) * (10 ** number_of_decimals)) + 0.999)
pc1 = "x^2" if c2 == 1 else ("" if c2 == 0 else str(c2) + "x^2")
pc2 = " + x" if c1 == 1 else ("" if c1 == 0 else " + " + str(c1) + "x")
pc3 = "" if c0 == 0 else (" + " + str(c0))
print("Population dimension:", population_dimension)
print(f"Interval [{a},{b}]")
print(f"Function: " + pc1 + pc2 + pc3)
print("Number of decimals:", number_of_decimals)
print("Crossover Probability:", crossover_probability)
print("Mutation Probability:", mutation_probability)
print("Number of generations:", generations)
print("Chromosome size:", chromosome_size)


def chromosome_to_string(chromosome):  # functie care transforma un cromozom in string(pentru afisare)
    return "".join([str(i) for i in chromosome])


def chromosome_to_int(chromosome):  # functie care transforma un cromozom in int pe baza (c5 - s28)
    return round((((b - a) / (2 ** len(chromosome) - 1)) * sum(
        [chromosome[i] * (2 ** (len(chromosome) - i - 1)) for i in range(len(chromosome))]) + a), number_of_decimals)


def f(x):  # f
    return c2 * x ** 2 + c1 * x + c0


def generate_chromosome():  # functie care genereaza un cromozom sub forma unei liste de 0 si 1
    return choices([0, 1], k=chromosome_size)


def generate_population():  # functie care genereaza populatie sub forma unei liste de cromozomi
    return [generate_chromosome() for _ in range(population_dimension)]


def crossover(g, a, b, c=None, print=False):  # functie care face crossover intre 2 sau 3 cromozomi
    p = randint(1, len(a) - 1)
    if c != None:
        if print:
            g.write(f"\n{chromosome_to_string(a)} - {chromosome_to_string(b)} - {chromosome_to_string(c)} : punct {p}")
        return a[:p] + b[p:], b[:p] + c[p:], c[:p] + a[p:]
    if print:
        g.write(f"\n{chromosome_to_string(a)} - {chromosome_to_string(b)} : punct {p}")

    return a[:p] + b[p:], b[:p] + a[p:]


def mutate(chromosome, type, probability):  # functie de mutatie dupa cele 2 metode prezentate in curs

    if type == "1":  # c5 - s45
        u = random()
        if u < probability:
            p = randint(0, len(chromosome) - 1)
            chromosome[p] = 1 - chromosome[p]
            return True
        return False
    if type == "2":  # c5 - s46
        modified = False
        for i in chromosome:
            u = random()
            if u < probability:
                chromosome[i] = 1 - chromosome[i]
                modified = True
        return modified


def bs(u, intervals):  # functia de cautare binara
    return binary_search(u, intervals, 0, len(intervals) - 1)


def binary_search(u, intervals, l, r):  # cb propriu-zisa
    if r - l < 1:
        return -1
    if r - l == 1 and intervals[l] <= u and u < intervals[r]:
        return r
    mid = (l + r + 1) // 2
    if u < intervals[mid]:
        return binary_search(u, intervals, l, mid)
    else:
        return binary_search(u, intervals, mid, r)


def print_population(population, g):
    for j, c in enumerate(population):
        b = chromosome_to_string(c)
        x = chromosome_to_int(c)
        v = f(x)
        g.write(f"  {j + 1}: {b}  x = {x}  f = {v}\n")


# x = chromosome_to_int([0,0,0,0,0,1,1,1,0,1,0,0,1,0,0,1,1,1,0,0,0,1])
# print(x)
# print(f(x))

def run_evolution():
    with open("Evolution.txt", "w") as g:
        population = generate_population()  # pentru primul pas, generam o populatie
        fmax = float('-inf')  # maximul tuturor generatiilor
        maxgen = 0  # generatia la care apare maximul
        maxstreak = 0
        elitist = 1  # variabila care determina daca va fi aplicat criteriul elitist in selectarea urmatoarei generatii 0-false 1-true
        for i in range(generations):
            firstgen = i == 0  # afisarea pasilor se va face doar pentru prima generatie
            if firstgen:
                g.write("Populatia initiala:\n")
                print_population(population, g)
            fs = [f(chromosome_to_int(x)) for x in population]  # lista in care stocam f(x) pentru fiecare cromozom
            sumfs = sum(fs)  # ∑f(x)
            probabilities = [ff / sumfs for ff in fs]  # probabilitatea de selectie pentru fiecare cromozom
            if firstgen:  # dupa formula f(xi)/∑f(x)
                g.write("\nProbabilitati selectie:\n")
                for j, p in enumerate(probabilities):
                    g.write(f"  cromozom {j + 1} - probabilitate {p}\n")
            s = 0
            intervals = []
            # print(probabilities)
            for j in range(len(probabilities)):
                intervals.append(s)  # generarea intervalelor de selectie
                s += probabilities[j]
            else:
                # intervals.append(s) #capatul din dreapta era calculat in unele cazuri ca fiind ≠ 1
                intervals.append(1)
            if firstgen:
                g.write("\n Intervale probabilitati: \n")
                g.write(str(intervals))
            next_generation = []
            for _ in range(elitist, population_dimension):
                u = random()
                index = bs(u, intervals)  # selectarea cromozomilor
                if firstgen:
                    g.write(f"\nu = {u} - selectam cromozomul {index}")
                next_generation.append(copy(population[index - 1]))
            if elitist:
                m = max(population, key=lambda x: f(chromosome_to_int(x)))
                next_generation.insert(0, m)
                if firstgen:
                    g.write(f"\nIn urma criteriului elitist a fost selectat cromozomul {population.index(m) + 1}")
            if firstgen:
                g.write("\n\nDupa selectie:\n")
                print_population(next_generation, g)
                g.write(f"\nProbabilitatea de incrucisare {crossover_probability}")
            # determinarea  cromozomilor care participa la incrucisare folosind selectia proportionala
            crossover_indexes = []
            for j, c in enumerate(next_generation):
                if j >= elitist:
                    b = chromosome_to_string(c)
                    u = random()
                    if firstgen:
                        g.write(f"\n  {j + 1}: {b}  u = {u} ")
                    if u < crossover_probability:
                        crossover_indexes.append(j)
                        if firstgen:
                            g.write(f" < {crossover_probability} - participa")
                elif firstgen:
                    g.write(f"\n  {j + 1}: {chromosome_to_string(c)}  nu participa")

            if firstgen:
                g.write("\n")
            shuffle(crossover_indexes)
            # print(crossover_indexes)
            lci = len(crossover_indexes)
            # incrucisarea pz
            for ind in range(0, lci - 1, 2):
                if lci % 2 == 1 and ind == lci - 3:  # daca au fost selectati pentru incrucisare un nr
                    if firstgen:  # impar de parinti vom face incrucisare intre cei 3 parinti
                        g.write(
                            f"\nCrossover intre cromozomii {crossover_indexes[ind]}, {crossover_indexes[ind + 1]}, {crossover_indexes[ind + 2]}")
                    next_generation[crossover_indexes[ind]], next_generation[crossover_indexes[ind + 1]], \
                    next_generation[crossover_indexes[ind + 2]] = crossover(
                        g, next_generation[crossover_indexes[ind]], next_generation[crossover_indexes[ind + 1]],
                        next_generation[crossover_indexes[ind + 2]], firstgen)
                    if firstgen:
                        g.write(
                            f"\nRezultat - {chromosome_to_string(next_generation[crossover_indexes[ind]])} - {chromosome_to_string(next_generation[crossover_indexes[ind + 1]])} - {chromosome_to_string(next_generation[crossover_indexes[ind + 2]])}")
                else:
                    if firstgen:
                        g.write(f"\nCrossover intre cromozomii {crossover_indexes[ind]}, {crossover_indexes[ind + 1]}")
                    next_generation[crossover_indexes[ind]], next_generation[crossover_indexes[ind + 1]] = crossover(g,
                                                                                                                     next_generation[
                                                                                                                         crossover_indexes[
                                                                                                                             ind]],
                                                                                                                     next_generation[
                                                                                                                         crossover_indexes[
                                                                                                                             ind + 1]],
                                                                                                                     print=firstgen)
                    if firstgen:
                        g.write(
                            f"\nRezultat - {chromosome_to_string(next_generation[crossover_indexes[ind]])} - {chromosome_to_string(next_generation[crossover_indexes[ind + 1]])}")
            if firstgen:
                g.write("\n\nDupa crossover:\n")
                print_population(next_generation, g)
                g.write(f"\nProbabilitatea de mutatie {mutation_probability}")
            nr = 0
            # mutatia cromozomilor
            for j in range(elitist, len(next_generation)):  # mutatia cromozomilor
                m = mutate(next_generation[j], "2", mutation_probability)
                if m:
                    nr += 1
                    if firstgen:
                        if nr == 1:
                            g.write(f"\nAu fost modificati cromozomii:\n")
                        g.write(f"{j + 1}\n")
            if firstgen:
                if nr == 0:
                    g.write("\nIn urma mutatiei nu a fost modificat niciun cromozom")
                g.write("\n\nDupa mutatie:\n")
                print_population(next_generation, g)
                g.write("\nEvolutia maximului:")
            fs = [f(chromosome_to_int(c)) for c in next_generation]
            maxx = max(fs)
            if maxx > fmax:
                fmax = maxx  # calcularea maximului tuturor generatiilor
                maxgen = i + 1
                maxstreak = 0
            else:
                maxstreak += 1
            performance = sum(fs) / len(fs)
            g.write(f"\nMaximum value = {maxx} | Performance = {performance}")
            population = next_generation  # asignarea populatiei pentru urmatoarea generatie
            if maxstreak >= 20:
                g.write(f"\nEvolutia s-a terminat prematur in generatia {i + 1} deoarece maximul nu se imbunatatea")
                break
        g.write(f'\n\nValoarea maxima {fmax} a fost gasita in generatia {maxgen}')


if __name__ == "__main__":
    run_evolution()
