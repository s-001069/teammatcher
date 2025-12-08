from encode_student_data import encode_student, label_encode
from fitness_function import make_fitness_func
import numpy as np
import pygad


def get_csv_data():
    pass

def get_student_data():
    pass

def get_teacher_inputs():
    # team_size, weights for: availability (unique weight), commitment, age, sex, job, bachelor, exp, role
    return [4, 0, 0.5, 0.5, 0.8, 0.2, 0.1]

def prepare_data(students):
    get_csv_data()
    get_student_data()

    # add student id to data

    # every student that is not in data but is in csv fill with 0s and add to student data

    # parameters all obligatory or need to fill data gaps with 0?

    # encode job and BSc
    encoded_list = []
    bachelors = []
    jobs = []

    for enc, bach, job in students:
        encoded_list.append(enc)
        bachelors.append(bach)
        jobs.append(job)

    students_base = np.vstack(encoded_list)   # shape (N, 33)

    # encode bachelor and job and append in array
    bach_encoded, bach_map = label_encode(bachelors)
    job_encoded, job_map   = label_encode(jobs)
    students_encoded = np.column_stack([students_base, bach_encoded, job_encoded])

    return students_encoded

def match(students):  
    students_encoded = prepare_data(students)

    homogeneous_idx   = list(range(0, 29))      # availability & commitment
    heterogeneous_idx = list(range(29, 35))     # age, sex, exp, role, bachelor, job

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



### TEST
if __name__ == "__main__":
    student1 = {
        "avail_mon": ["07:00-09:00", "18:00-20:00"],
        "avail_tue": ["14:00-20:00"],
        "avail_wed": ["10:00-20:00"],
        "avail_thu": ["09:00-11:00", "20:00-22:00"],
        "avail_fri": ["17:00-23:00"],
        "avail_sat": ["06:00-08:00", "18:00-23:00"],
        "avail_sun": ["17:00-22:00"],

        "commitment": "regular",   # minimal/regular/high
        # "work_type": "sync",       # sync/async

        "age": 25,
        "sex": "F",
        "job": "student",
        "bachelor": "CS",
        "exp": "intermediate", # beginner/intermediate/advanced
        "role": "leader"
    }

    student2 = {
        "avail_mon": ["08:00-10:00"],
        "avail_tue": ["18:00-22:00"],
        "avail_wed": ["09:00-12:00"],
        "avail_thu": ["14:00-18:00"],
        "avail_fri": ["19:00-23:00"],
        "avail_sat": ["10:00-14:00"],
        "avail_sun": ["14:00-18:00"],
        "commitment": "high",
        # "work_type": "async",
        "job": "developer",
        "bachelor": "SE",
        "age": 30,
        "sex": "M",
        "exp": "advanced",
        "role": "support",
    }

    student3 = {
        "avail_mon": ["16:00-20:00"],
        "avail_tue": ["08:00-12:00"],
        "avail_wed": ["13:00-17:00"],
        "avail_thu": ["18:00-22:00"],
        "avail_fri": ["08:00-12:00"],
        "avail_sat": ["12:00-16:00"],
        "avail_sun": ["18:00-22:00"],
        "commitment": "minimal",
        "work_type": "async",
        "age": 22,
        "sex": "F",
        "job": "designer",
        "bachelor": "Art",
        "exp": "beginner",
        "role": "support",
    }

    student4 = {
        "avail_mon": ["09:00-13:00"],
        "avail_tue": ["09:00-13:00"],
        "avail_wed": ["09:00-13:00"],
        "avail_thu": ["09:00-13:00"],
        "avail_fri": ["09:00-13:00"],
        "avail_sat": ["15:00-19:00"],
        "avail_sun": ["15:00-19:00"],
        "commitment": "regular",
        "work_type": "sync",
        "age": 28,
        "sex": "M",
        "job": "researcher",
        "bachelor": "Math",
        "exp": "intermediate",
        "role": "leader",
    }

    student5 = {
        "avail_mon": ["18:00-22:00"],
        "avail_tue": ["18:00-22:00"],
        "avail_wed": ["18:00-22:00"],
        "avail_thu": ["18:00-22:00"],
        "avail_fri": ["18:00-22:00"],
        "avail_sat": ["10:00-12:00", "14:00-16:00"],
        "avail_sun": ["10:00-12:00", "14:00-16:00"],
        "commitment": "high",
        "work_type": "sync",
        "age": 35,
        "sex": "F",
        "job": "manager",
        "bachelor": "Business",
        "exp": "advanced",
        "role": "leader",
    }

    student6 = {
        "avail_mon": ["07:00-11:00"],
        "avail_tue": ["07:00-11:00"],
        "avail_wed": ["07:00-11:00"],
        "avail_thu": ["07:00-11:00"],
        "avail_fri": ["07:00-11:00"],
        "avail_sat": ["18:00-22:00"],
        "avail_sun": ["18:00-22:00"],
        "commitment": "minimal",
        "work_type": "async",
        "age": 20,
        "sex": "other",
        "job": "intern",
        "bachelor": "CS",
        "exp": "beginner",
        "role": "support",
    }

    student7 = {
        "avail_mon": ["12:00-16:00"],
        "avail_tue": ["12:00-16:00"],
        "avail_wed": ["12:00-16:00"],
        "avail_thu": ["12:00-16:00"],
        "avail_fri": ["12:00-16:00"],
        "avail_sat": ["08:00-12:00"],
        "avail_sun": ["08:00-12:00"],
        "commitment": "regular",
        "work_type": "sync",
        "age": 27,
        "sex": "F",
        "job": "engineer",
        "bachelor": "EE",
        "exp": "intermediate",
        "role": "support",
    }

    student8 = {
        "avail_mon": ["10:00-14:00"],
        "avail_tue": ["10:00-14:00"],
        "avail_wed": ["10:00-14:00"],
        "avail_thu": ["10:00-14:00"],
        "avail_fri": ["10:00-14:00"],
        "avail_sat": ["16:00-20:00"],
        "avail_sun": ["16:00-20:00"],
        "commitment": "high",
        "work_type": "async",
        "age": 24,
        "sex": "M",
        "job": "student",
        "bachelor": "CS",
        "exp": "intermediate",
        "role": "leader",
    }

    students = [
        encode_student(student1), 
        encode_student(student2), 
        encode_student(student3), 
        encode_student(student4), 
        encode_student(student5), 
        encode_student(student6), 
        encode_student(student7), 
        encode_student(student8)
    ]
    print(match(students))