import pulp

class Level:    
    def __init__(self, bachelor, master):
        self.bachelor = bachelor
        self.master = master

    def compatible(self, student):
        return (self.bachelor and student.bachelor) or (self.master and student.master)

Bachelor = Level(True, False)
Master = Level(False, True)


class Student():
    def __init__(self, name, id, level, priorities, weight):
        self.name = name
        self.id = id
        self.level = level
        self.priorities = priorities
        self.weight = weight

class Topic():
    def __init__(self, id, level):
        self.id = id
        self.level = level
        self.capacity = 2

    def compatible(self, student):
        return self.level.compatible(student.level)

def read_files():
    #TODO, wenn file besteht: Read Topics
    topics = [
        Topic(0, Level(True, True)),
        Topic(1, Level(True, True)),
        Topic(2, Level(False, True)),
        Topic(3, Level(True, False))
    ]

    #TODO, wenn file besteht: Read Students
    students = []
    for i in range(6):
        students.append(Student("name" + str(i), i, Bachelor, {0: 5, 1: 5, 2: 5, 3: 5}, 1))
    students.append(Student("name" + str(6), 6, Master, {0: 5, 1: 5, 2: 5, 3: 5}, 1))
    students.append(Student("name" + str(7), 7, Master, {0: 5, 1: 5, 2: 5, 3: 5}, 1))
    
    return {
        "students": students,
        "topics": topics 
    }

def get_list_of_ids(l):
    return [e.id for e in l]

def solve(data):
    # Generate Data
    students = data['students']
    topics = data['topics']

    # Initialisiere Solver
    prob = pulp.LpProblem("StudentTopicAssignment", pulp.LpMaximize) # Problem initialisieren
    choices = pulp.LpVariable.dicts("Choice", (get_list_of_ids(students), get_list_of_ids(topics)), 0, 1, pulp.LpBinary) # Entscheidungsvariablen

    # Zielfunktion
    prob += pulp.lpSum([choices[student.id][topic.id] * student.priorities[topic.id] * student.weight
                        for student in students for topic in topics])

    # Einschränkungen
    for student in students:
        prob += pulp.lpSum([choices[student.id][topic.id] for topic in topics]) == 1, f"OneTopicPerStudent_{student}"

    for topic in topics:
        prob += pulp.lpSum([choices[student.id][topic.id] for student in students]) <= topic.capacity, f"Capacity_{topic}"

    # Studienlevel
    for topic in topics:
        for student in students:
            if not topic.compatible(student):
                prob += pulp.lpSum(choices[student.id][topic.id]) == 0, f"Level_Missmatch_{student.id}_{topic.id}"
    
    # Problem lösen
    prob.solve()

    return choices

def print_result(data, inp):
    for student in inp['students']:
        for topic in inp['topics']:
            if pulp.value(data[student.id][topic.id]) == 1:
                print(f"Student {student.name} wurde dem Thema {topic.id} zugewiesen.")


if __name__ == "__main__":
    # Read limesurvey export    
    data_in = read_files()

    # Solve problem
    data_out = solve(data_in)

    # Pretty print result
    print_result(data_out, data_in)