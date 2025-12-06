import numpy as np

def parse_time(t):
    """ 
    Converts time to float 
    """
    
    h, m = map(int, t.split(":"))
    return h + m / 60.0   # 0–24


def encode_time_ranges(ranges):
    """
    Converts time ranges to tuple<float>: (start1, end1, start2, end2)
    """

    if len(ranges) == 0:
        return 0.0, 0.0, 0.0, 0.0

    if len(ranges) == 1:
        # duplicates single range
        ranges = [ranges[0], ranges[0]]

    s1_str, e1_str = ranges[0].split("-")
    s2_str, e2_str = ranges[1].split("-")
    
    return (
        parse_time(s1_str),
        parse_time(e1_str),
        parse_time(s2_str),
        parse_time(e2_str),
    )


def label_encode(values):
    """ 
    Converts a sequence of categorical values into integer labels
    """
    uniq = {v: i for i, v in enumerate(sorted(set(values)))}
    return np.array([uniq[v] for v in values], dtype=int), uniq


def encode_student(student_data):
    """
    Encodes a student's data into integers and floats
    """

    commit_map = {"minimal": 0, "regular": 1, "high": 2}
    # work_map = {"async": 0, "sync": 1}
    experience_map = {"beginner": 0, "intermediate": 1, "advanced": 2}
    role_map = {"support": 0, "leader": 1}
    sex_map = {"M": 0, "F": 1, "other": 2}

    # job_encoded, job_map = label_encode([student_data["job"]])
    # bach_encoded, bach_map = label_encode([student_data["bachelor"]])

    day_keys = [
        "avail_mon", "avail_tue", "avail_wed", "avail_thu",
        "avail_fri", "avail_sat", "avail_sun"
    ]
    student_encoded = np.zeros((33), dtype=float)

    # 7 days of 4 columns each (2 timeranges)
    for day_idx, key in enumerate(day_keys):
        start1, end1, start2, end2 = encode_time_ranges(student_data[key])

        base = day_idx * 4
        student_encoded[base + 0] = start1
        student_encoded[base + 1] = end1
        student_encoded[base + 2] = start2
        student_encoded[base + 3] = end2

    offset = 28
    student_encoded[offset + 0] = commit_map[student_data["commitment"]]
    # student_encoded[offset + 1] = work_map[student_data["work_type"]]

    student_encoded[offset + 1] = student_data["age"]
    student_encoded[offset + 2] = sex_map[student_data["sex"]]
    student_encoded[offset + 3] = experience_map[student_data["exp"]]
    student_encoded[offset + 4] = role_map[student_data["role"]]

    # homogeneous_idx = list(range(0, 29))
    # heterogeneous_idx = list(range(29, 33))

    return student_encoded, student_data['bachelor'], student_data['job']


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

    print(encode_student(student1))
    print(encode_student(student2))
