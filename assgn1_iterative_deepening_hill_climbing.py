import random

def read_input():
    f = open("input_assignment1", "r")
    task_lengths = [float(length) for length in f.readline().split(' ')]
    processor_speeds = [float(speed) for speed in f.readline().split(' ')]
    third_line = f.readline().split(' ')
    deadline, target = float(third_line[0]), float(third_line[1])
    return task_lengths, processor_speeds, deadline, target


def solve_using_iterative_deepening(task_lengths, processor_speeds, deadline, target):
    def dfs(limit, sum_lengths_uptil_now, task_to_assign, assignments, processors_time_taken_up):
        if sum_lengths_uptil_now >= target:
            return assignments
        if limit == 0:
            return False

        for j in range(0, len(processor_speeds)):
            speed = processor_speeds[j]
            length = task_lengths[task_to_assign]
            time = float(length/speed)
            if processors_time_taken_up[j] + time > deadline:
                continue
            new_assignments = assignments[:]
            new_assignments[task_to_assign] = j
            new_processors_time_taken_up = processors_time_taken_up[:]
            new_processors_time_taken_up[j] += time
            result = dfs(limit-1, sum_lengths_uptil_now + length, task_to_assign+1, new_assignments, new_processors_time_taken_up)
            if result:
                return result

        result = dfs(limit-1, sum_lengths_uptil_now, task_to_assign+1, assignments, processors_time_taken_up)
        return result

    temp_task_lengths = sorted(task_lengths, reverse=True)
    s = 0.0
    q = 0
    while q < len(temp_task_lengths):
        s += temp_task_lengths[q]
        if s >= target:
            break
        q += 1

    if q == len(task_lengths):
        return False

    for i in range(q, len(task_lengths)):
        assign = [None for j in range(len(task_lengths))]
        time_taken = [0.0 for j in range(len(processor_speeds))]
        result = dfs(i+1, 0.0, 0, assign, time_taken)
        if result:
            return result

    return False


def solve_using_hill_climbing(task_lengths, processor_speeds, deadline, target, restarts):
    def hill_climbing(assignment, sum_lengths, processors_time_taken_up, current_cost):
        max_overflow = 0.0
        for time in processors_time_taken_up:
            max_overflow = max(max_overflow, (time - deadline))

        if target - sum_lengths <= 0.0:
            cost = max_overflow
        else:
            cost = max_overflow + target - sum_lengths
        if max_overflow == 0.0 and sum_lengths >= target:
            return assignment

        if current_cost is not None:
            if cost >= current_cost:
                return False

        for l in range(len(assignment)):

            for m in range(len(processor_speeds)+1):
                temp_assignment = assignment[:]
                temp_processors_time_taken_up = processors_time_taken_up[:]
                if assignment[l] == m:
                    continue
                temp_assignment[l] = m
                if m == 0:
                    s = sum_lengths - task_lengths[l]
                    temp_processors_time_taken_up[assignment[l]-1] -= float(task_lengths[l]/processor_speeds[assignment[l]-1])
                elif assignment[l] == 0:
                    s = sum_lengths + task_lengths[l]
                    temp_processors_time_taken_up[m - 1] += float(task_lengths[l]/processor_speeds[m-1])
                else:
                    temp_processors_time_taken_up[assignment[l] - 1] -= float(
                        task_lengths[l] / processor_speeds[assignment[l] - 1])
                    temp_processors_time_taken_up[m - 1] += float(task_lengths[l] / processor_speeds[m - 1])

                result = hill_climbing(temp_assignment, s, temp_processors_time_taken_up, cost)
                if result is False:
                    continue
                elif result is None:
                    return None

                else:
                    return result

            if l == len(assignment) - 1:
                break

            for m in range(l+1, len(assignment)):
                if assignment[l] == assignment[m]:
                    continue
                temp_assignment = assignment[:]
                temp_processors_time_taken_up = processors_time_taken_up[:]
                temp_assignment[m] = assignment[l]
                temp_assignment[l] = assignment[m]
                s = sum_lengths
                if assignment[l] != 0:
                    temp_processors_time_taken_up[assignment[l] - 1] -= float(
                        task_lengths[l] / processor_speeds[assignment[l] - 1])
                    temp_processors_time_taken_up[assignment[l] - 1] += float(
                        task_lengths[m] / processor_speeds[assignment[l] - 1])
                else:
                    s += task_lengths[l] - task_lengths[m]

                if assignment[m] != 0:
                    temp_processors_time_taken_up[assignment[m] - 1] -= float(
                        task_lengths[m] / processor_speeds[assignment[m] - 1])
                    temp_processors_time_taken_up[assignment[m] - 1] += float(
                        task_lengths[l] / processor_speeds[assignment[m] - 1])
                else:
                    s += task_lengths[m] - task_lengths[l]

                result = hill_climbing(temp_assignment, s, temp_processors_time_taken_up, cost)
                if result is False:
                    continue
                elif result is None:
                    return None
                else:
                    return result

        return None

    for i in range(restarts):
        no_of_processors = len(processor_speeds)
        initial_assignment = []
        for j in range(len(task_lengths)):
            initial_assignment.append(random.randint(0, no_of_processors))
        processors_time_taken_up = [0.0 for k in range(len(processor_speeds))]
        s_lengths = 0.0

        for k in range(len(initial_assignment)):
            if initial_assignment[k] != 0:
                processors_time_taken_up[initial_assignment[k]-1] += float(task_lengths[k]/processor_speeds[initial_assignment[k]-1])
                s_lengths += task_lengths[k]

        solution = hill_climbing(initial_assignment, s_lengths, processors_time_taken_up, None)
        if solution is not None:
            return solution

    return None


def print_solution(solution, id_or_hc):
    if not solution:
        print('No Solution')

    else:
        s = ""
        if id_or_hc == 'hc':
            for ele in solution:
                s += str(ele) + " "

        else:
            for ele in solution:
                if ele is None:
                    s += "0 "
                else:
                    s += str(ele+1) + " "
        print(s)
    print('\n')


if __name__ == '__main__':
    tasks, processors, d, t = read_input()
    sol = solve_using_iterative_deepening(tasks, processors, d, t)
    print('Iterative deepening solution: ')
    print_solution(sol, 'id')
    restarts = 10
    sol = solve_using_hill_climbing(tasks, processors, d, t, restarts)
    print('Hill climbing solution: ')
    print_solution(sol, 'hc')