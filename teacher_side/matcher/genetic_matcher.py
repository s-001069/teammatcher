""" Genetic algorithm student matcher """

import numpy as np
import pygad

from teacher_side.matcher.fitness_function import make_fitness_func
from teacher_side.matcher.encoder import encode_student
from student_side.models import StudentProfile, Task


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

def prepare_data(df):
    """ 
        Encodes student data
        Args:
            - df: pandas Dataframe containing student data from uploaded CSV
        Returns:
            - encoded student data as numpy array
            - list of student IDs in the same order as encoded data
            - list of indices of homogeneous features
            - list of indices of heterogeneous features
    """

    students = get_student_data()
    db_student_map = {getattr(s, 'student_id', str(s)): s for s in students}
    tasks = get_tasks()

    vector_size = 21 + 7 + len(tasks)

    # encode all students
    encoded_list = []
    id_list = []

    for index, row in df.iterrows():
        csv_id = str(row['username']).strip()
        
        if csv_id in db_student_map:
            student = db_student_map[csv_id]
            encoded = encode_student(student, tasks)         
        else: # student did not fill form
            encoded = np.zeros(vector_size, dtype=float)
            encoded[0:21] = 1 # assumes full availability
            encoded[28:] = 1 #assumes all tasks preferred
            
        encoded_list.append(encoded)
        id_list.append(csv_id)

    return np.vstack(encoded_list), id_list

def match(df, team_template):  
    """ 
        Matches students into teams using genetic algorithm
        Args:
            - df: pandas Dataframe containing student data from uploaded CSV
            - team_template: TeamTemplate object
        Returns:
            - best solution (team assignments)
            - best fitness score
    """
    students_encoded, student_ids = prepare_data(df)
    homogeneous_idx = list(range(0, 22))     # availability & commitment
    heterogeneous_idx = list(range(22, len(students_encoded[0]))) # rest features

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
    best_solution, best_fitness, _ = ga_instance.best_solution()

    print(best_solution)
    print(type(best_solution))

    # builds team names from template or default names 'Team X'
    template_names = team_template.team_names if team_template else []
    n_teams_used = int(max(best_solution)) + 1

    team_names = []
    for team_index in range(n_teams_used):
        if team_index < len(template_names):
            team_names.append(template_names[team_index])
        else:
            team_names.append(f"Team {team_index + 1}")
    team_assignments = [team_names[int(t)] for t in best_solution]

    target_col = None

    if 'mode' in df.columns:
        mode_idx = df.columns.get_loc('mode')
        cols_after_mode = df.columns[mode_idx+1:]
        
        # finds the first empty column in slice (after 'mode' column)
        for col in cols_after_mode:
            if df[col].isnull().all():
                target_col = col
                break
    
    if target_col: # adds results to first empty column after 'mode'
        df[target_col] = team_assignments
    else: # creates new column 'teams'
        print("No empty column found after 'mode'. Creating 'teams' column.")
        df['teams'] = team_assignments

    return df, target_col
