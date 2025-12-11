""" Genetic algorithm student matcher """

import numpy as np
import pygad

from teacher_side.matcher.fitness_function import make_fitness_func
from teacher_side.matcher.encoder import encode_student
from teacher_side.matcher.utils import get_student_data, get_tasks


def prepare_data(df):
    """ 
        Encodes student data
        Args:
            - df: pandas Dataframe containing student data from uploaded CSV
        Returns:
            - encoded student data as numpy array
            - number of tasks (int)
    """

    students = get_student_data()
    db_student_map = {getattr(s, 'student_id', str(s)): s for s in students}
    tasks = get_tasks()
    n_tasks = len(tasks)

    vector_size = 21 + n_tasks + 7

    # encode all students
    encoded_list = []

    for index, row in df.iterrows():
        csv_id = str(row['username']).strip()
        
        if csv_id in db_student_map:
            student = db_student_map[csv_id]
            encoded = encode_student(student, tasks)         
        else: # student did not fill form
            encoded = np.zeros(vector_size, dtype=float)
            encoded[0:21+n_tasks] = 1 # assumes full availability and all tasks preferred, leaves every other feature as 0

        encoded_list.append(encoded)

    return np.vstack(encoded_list)

def match(df, team_template, weights):  
    """ 
        Matches students into teams using genetic algorithm
        Args:
            - df: pandas Dataframe containing student data from uploaded CSV
            - team_template: TeamTemplate object
        Returns:
            - df with team assignments
            - target column name (str) where assignments were added
            - best fitness score
    """
    students_encoded = prepare_data(df)

    n_teams=4
    team_size = 4

    fitness_func = make_fitness_func(students_encoded, team_size, weights)
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

    return df, target_col, best_fitness
