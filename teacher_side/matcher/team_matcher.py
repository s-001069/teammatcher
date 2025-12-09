from teacher_side.matcher.encoder import encode_student
from teacher_side.matcher.fitness_function import make_fitness_func
from student_side.models import StudentProfile, Task

import numpy as np
import pygad


def get_csv_data():
    """ gets teacher uploaded csv data """
    pass

def get_student_data():
    """ 
        Gets student data from DB 
        Returns:
            - list of StudentProfile objects
    """
    return StudentProfile.objects.all()

def get_tasks():
    """ 
        Gets tasks from DB
        Returns:
            - list of task names
    """
    return list(Task.objects.filter(active=True).values_list("name", flat=True))

def get_teacher_inputs(): # fix weights
    # team_size, weights for: availability (unique weight), commitment, age, sex, job, bachelor, exp, role
    return [4, 1, 0.5, 0.5, 0.8, 0.2, 0.1, 0.5, 0.6, 1]

def prepare_data(students, tasks):
    """ 
        Encodes student data
        Args:
            - students: list of StudentProfile objects
        Returns:
            - encoded student data as numpy array
            - list of student IDs in the same order as encoded data
            - list of indices of homogeneous features
            - list of indices of heterogeneous features
    """
    get_csv_data()

    # every student that is not in data but is in csv fill with 0s and add to student data
    # every student that is in student data but not in csv ignore

    # encode all students
    encoded_list = []
    id_list = []

    for student in students:
        encoded, homogeneous_idx, heterogeneous_idx = encode_student(student, tasks)
        encoded_list.append(encoded)
        id_list.append(student.student_id)

    return np.vstack(encoded_list), id_list, homogeneous_idx, heterogeneous_idx

def match():  
    students = get_student_data()
    tasks = get_tasks()

    students_encoded, students_ids, homogeneous_idx, heterogeneous_idx = prepare_data(students, tasks)
    teacher_inputs = get_teacher_inputs()

    n_teams=4
    team_size = teacher_inputs[0]
    weights   = teacher_inputs[1:]  # (w_avail, w_commit, w_age, w_sex, w_job, w_bach)

    fitness_func = make_fitness_func(students_encoded, team_size, weights, homogeneous_idx, heterogeneous_idx)
    gene_space = list(range(n_teams))

    ga_instance = pygad.GA(
        num_generations=200,
        num_parents_mating=20,
        fitness_func=fitness_func,
        sol_per_pop=40,
        num_genes=students_encoded.shape[0],
        gene_space=gene_space,
        mutation_probability=0.1,
        crossover_type="single_point",
        mutation_type="random",
        keep_parents=2,
        stop_criteria=["saturate_50"]
    )

    ga_instance.run()
    best_solution, best_fitness, best_idx = ga_instance.best_solution()
    return best_solution, best_fitness
