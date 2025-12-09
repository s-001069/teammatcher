import numpy as np

# def label_encode(values):
#     """ 
#     Converts a sequence of categorical values into integer labels
#     """
#     uniq = {v: i for i, v in enumerate(sorted(set(values)))}
#     return np.array([uniq[v] for v in values], dtype=int), uniq


def encode_student(student, tasks):
    """
    Encodes a student's data into numerical values
    """

    # maps for encoding categorical features
    commit_map = {
        "minimal": 0, 
        "regular": 1, 
        "high": 2
    }
    education_map = {
        "none_yet": 0, 
        "bachelor_business": 1, 
        "bachelor_cs": 2, 
        "bachelor_engineering": 3, 
        "bachelor_social": 4,
        "master_business": 5, 
        "master_other": 6, 
        "other": 7
    }
    professional_map = {
        "none": 0, 
        "internship": 1, 
        "working_student": 2, 
        "industry_business": 3, 
        "industry_it": 4, 
        "industry_other": 5
    }
    experience_map = {
        "beginner": 0, 
        "intermediate": 1, 
        "advanced": 2
    }
    lead_map = {
        "support": 0, 
        "lead": 1
    }
    sex_map = {
        "male": 0, 
        "female": 1, 
        "other": 2
    }

    n_tasks = len(tasks)

    # 7 days x 3 slots + 7 features (without tasks) + 1 * number of tasks
    student_encoded = np.zeros((7*3 + 7 + n_tasks), dtype=float)

    # --- availability encoding ---
    day_keys = [
        "availability_monday",
            "availability_tuesday",
            "availability_wednesday",
            "availability_thursday",
            "availability_friday",
            "availability_saturday",
            "availability_sunday"
    ]

    # 7 days x 3 slots
    for day_idx, key in enumerate(day_keys):
        value = getattr(student, key)
        if not value:
            continue

        base = day_idx * 3

        if "Morning" in value:
            student_encoded[base + 0] = 1
        if "Afternoon" in value:
            student_encoded[base + 1] = 1
        if "Evening" in value:
            student_encoded[base + 2] = 1

    offset = 21 # write after availability

    # --- other features encoding ---
    if student.commitment in commit_map:
        student_encoded[offset + 0] = commit_map[student.commitment]
    if student.educational_background in education_map:
        student_encoded[offset + 1] = education_map[student.educational_background]
    if student.professional_background in professional_map:
        student_encoded[offset + 2] = professional_map[student.professional_background]
    if student.age is not None:
        student_encoded[offset + 3] = student.age
    if student.sex in sex_map:
        student_encoded[offset + 4] = sex_map[student.sex]
    if student.experience_level in experience_map:
        student_encoded[offset + 5] = experience_map[student.experience_level]
    if student.lead_preference in lead_map:
        student_encoded[offset + 6] = lead_map[student.lead_preference]

    # --- preferred tasks encoding ---
    student_tasks = list(student.preferred_tasks.values_list("name", flat=True))
    
    offset += 7 # write after other features
    for task_idx, task_name in enumerate(tasks):
        student_encoded[offset + task_idx] = int(task_name in student_tasks)

    homogeneous_idx = list(range(0, 22))     # availability & commitment
    heterogeneous_idx = list(range(22, len(student_encoded)))   # rest features

    return student_encoded, homogeneous_idx, heterogeneous_idx
