from collections import defaultdict
import copy


def create_atom(atom, atom_map, atom_count):
    if atom in atom_map:
        return atom_map[atom], atom_map, atom_count

    atom_map[atom] = atom_count
    atom_count += 1
    return atom_map[atom], atom_map, atom_count


def front_end():
    with open('input_assignment2') as file:
        lines = [line.rstrip('\n') for line in file]
    no_of_holes = int(lines[0].split(' ')[0])
    empty_hole = int(lines[0].split(' ')[1])

    # Store the holes that lie in a row in a set
    holes_in_row = []
    for i in range(1, len(lines)):
        line = lines[i]
        line_split = line.split(' ')
        holes_in_row.append(line_split[0] + ' ' + line_split[1] + ' ' + line_split[2])
        holes_in_row.append(line_split[2] + ' ' + line_split[1] + ' ' + line_split[0])

    first_hole_in_jump = defaultdict(list)
    second_hole_in_jump = defaultdict(list)
    third_hole_in_jump = defaultdict(list)
    for possible_jump in holes_in_row:
        first_hole_in_jump[int(possible_jump.split(' ')[0])].append(possible_jump)
        second_hole_in_jump[int(possible_jump.split(' ')[1])].append(possible_jump)
        third_hole_in_jump[int(possible_jump.split(' ')[2])].append(possible_jump)

    clause_list = []
    atom_map = {}
    atom_count = 1
    for item in holes_in_row:
        item_split = item.split(' ')
        for time in range(1, no_of_holes - 1):
            s = 'Jump(' + item_split[0] + ',' + item_split[1] + ',' + item_split[2] + ',' + str(time) + ')'
            atom_map[s] = atom_count
            atom_count += 1

    for hole in range(1, no_of_holes + 1):
        for time in range(1, no_of_holes):
            s = 'Peg(' + str(hole) + ',' + str(time) + ')'
            atom_map[s] = atom_count
            atom_count += 1

    for time in range(1, no_of_holes-1):
        for possible_jump in holes_in_row:
            s = possible_jump.split(' ')
            x = 'Jump(' + s[0] + ',' + s[1] + ',' + s[2] + ',' + str(time) + ')'
            atom_x = atom_map[x]

            a = 'Peg(' + s[0] + ',' + str(time) + ')'
            atom_a = atom_map[a]

            b = 'Peg(' + s[1] + ',' + str(time) + ')'
            atom_b = atom_map[b]

            c = 'Peg(' + s[2] + ',' + str(time) + ')'
            atom_c = atom_map[c]

            # Adding Precondition axioms to the list of clauses
            clause_list.append(str(-1 * atom_x) + ' ' + str(atom_a))
            clause_list.append(str(-1 * atom_x) + ' ' + str(atom_b))
            clause_list.append(str(-1 * atom_x) + ' ' + str(-1 * atom_c))

            a1 = 'Peg(' + s[0] + ',' + str(time+1) + ')'
            atom_a1 = atom_map[a1]

            b1 = 'Peg(' + s[1] + ',' + str(time+1) + ')'
            atom_b1 = atom_map[b1]

            c1 = 'Peg(' + s[2] + ',' + str(time+1) + ')'
            atom_c1 = atom_map[c1]

            # Adding Causal axioms to the list of clauses
            clause_list.append(str(-1 * atom_x) + ' ' + str(-1 * atom_a1))
            clause_list.append(str(-1 * atom_x) + ' ' + str(-1 * atom_b1))
            clause_list.append(str(-1 * atom_x) + ' ' + str(1 * atom_c1))

    for hole in range(1, no_of_holes+1):
        for time in range(1, no_of_holes - 1):
            first_hole_jumps = first_hole_in_jump[hole]
            second_hole_jumps = second_hole_in_jump[hole]
            third_hole_jumps = third_hole_in_jump[hole]

            peg_atom_1 = 'Peg(' + str(hole) + ',' + str(time) + ')'
            atom_peg1 = atom_map[peg_atom_1]

            peg_atom_2 = 'Peg(' + str(hole) + ',' + str(time+1) + ')'
            atom_peg2 = atom_map[peg_atom_2]

            frame_axiom_clause_a = str(-1 * atom_peg1) + ' ' + str(atom_peg2)
            frame_axiom_clause_b = str(atom_peg1) + ' ' + str(-1 * atom_peg2)

            for fhj in first_hole_jumps:
                s = fhj.split(' ')
                jump = 'Jump(' + s[0] + ',' + s[1] + ',' + s[2] + ',' + str(time) + ')'
                atom = atom_map[jump]
                frame_axiom_clause_a += (' ' + str(atom))

            for shj in second_hole_jumps:
                s = shj.split(' ')
                jump = 'Jump(' + s[0] + ',' + s[1] + ',' + s[2] + ',' + str(time) + ')'
                atom = atom_map[jump]
                frame_axiom_clause_a += (' ' + str(atom))

            for thj in third_hole_jumps:
                s = thj.split(' ')
                jump = 'Jump(' + s[0] + ',' + s[1] + ',' + s[2] + ',' + str(time) + ')'
                atom = atom_map[jump]
                frame_axiom_clause_b += (' ' + str(atom))

            # Adding Frame axiom clauses
            clause_list.append(frame_axiom_clause_a)
            clause_list.append(frame_axiom_clause_b)

    holes_in_row = list(holes_in_row)

    for time in range(1, no_of_holes - 1):
        for i in range(len(holes_in_row)-1):
            s1 = holes_in_row[i].split(' ')
            jump1 = 'Jump(' + s1[0] + ',' + s1[1] + ',' + s1[2] + ',' + str(time) + ')'
            atom_jump1 = atom_map[jump1]
            for j in range(i + 1, len(holes_in_row)):
                s2 = holes_in_row[j].split(' ')
                jump2 = 'Jump(' + s2[0] + ',' + s2[1] + ',' + s2[2] + ',' + str(time) + ')'
                atom_jump2 = atom_map[jump2]

                # Adding "No two actions at a time" clause
                clause_list.append(str(-1 * atom_jump1) + ' ' + str(-1 * atom_jump2))

    for hole in range(1, no_of_holes+1):
        peg = 'Peg(' + str(hole) + ',1)'
        peg_atom = atom_map[peg]

        # Adding Starting state clause
        if hole == empty_hole:
            clause_list.append(str(-1*peg_atom))
        else:
            clause_list.append(str(peg_atom))

    for hole1 in range(1, no_of_holes):
        peg1 = 'Peg(' + str(hole1) + ',' + str(no_of_holes-1) + ')'
        peg1_atom = atom_map[peg1]

        for hole2 in range(hole1 + 1, no_of_holes+1):
            peg2 = 'Peg(' + str(hole2) + ',' + str(no_of_holes - 1) + ')'
            peg2_atom = atom_map[peg2]

            # Adding Ending state clause A
            clause_list.append(str(-1 * peg1_atom) + ' ' + str(-1 * peg2_atom))

    clause = ""
    for hole in range(1, no_of_holes+1):
        peg = 'Peg(' + str(hole) + ',' + str(no_of_holes - 1) + ')'
        peg_atom = atom_map[peg]
        if clause == "":
            clause += str(peg_atom)

        else:
            clause += (" " + str(peg_atom))

    # Adding Ending state clause B
    clause_list.append(clause)

    output_list = clause_list
    reverse_atom_map = {}
    for key in atom_map:
        reverse_atom_map[atom_map[key]] = key

    output_list.append("0")

    for i in range(1, atom_count):
        output_list.append(str(i) + ' ' + reverse_atom_map[i])

    output_list = [output + '\n' for output in output_list]

    file = open("front_end_output", "w")
    file.writelines(output_list)
    file.close()


def davis_putnam():
    with open('front_end_output') as file:
        lines = [line.rstrip('\n') for line in file]

    add_clauses = True
    clauses = []
    atom_map_list = []
    for line in lines:
        if line == "0":
            add_clauses = False
            continue

        if add_clauses:
            line_split = line.split(' ')
            clauses.append([int(atom) for atom in line_split])

        else:
            atom_map_list.append(line)

    count_atoms_map = {}
    for clause in clauses:
        for literal in clause:
            if literal < 0:
                if -1*literal not in count_atoms_map:
                    count_atoms_map[-1*literal] = 1
            else:
                if literal not in count_atoms_map:
                    count_atoms_map[literal] = 1

    no_of_atoms = len(count_atoms_map)
    V = [None]
    for i in range(no_of_atoms):
        V.append(None)

    solution = dp1(no_of_atoms, clauses, V)
    output_list = []
    if solution is not None:
        for i in range(1, len(solution)):
            if solution[i] is True:
                output_list.append(str(i) + ' T')
            else:
                output_list.append(str(i) + ' F')

    output_list.append("0")
    output_list.extend(atom_map_list)
    output_list = [output + '\n' for output in output_list]
    file = open("davis_putnam_output", "w")
    file.writelines(output_list)
    file.close()


def dp1(no_of_atoms, S, V):

    while True:

        if len(S) == 0:
            for i in range(1, no_of_atoms + 1):
                if V[i] is None:
                    V[i] = True

            return V

        for clause in S:
            if len(clause) == 0:
                return None

        literal_map = {}
        for clause in S:
            for literal in clause:
                literal_map[literal] = 1

        flag = False
        for literal in literal_map:
            if (-1*literal) not in literal_map:
                if literal < 0:
                    V[-1*literal] = False

                else:
                    V[literal] = True

                clauses_to_pop = []
                for i in range(0, len(S)):
                    clause = S[i]
                    for l in clause:
                        if l == literal:
                            clauses_to_pop.append(i)
                            break

                for i in reversed(clauses_to_pop):
                    S.pop(i)

                flag = True
                break

        if flag:
            continue

        flag = False
        for clause in S:
            if len(clause) == 1:
                literal = clause[0]
                if literal < 0:
                    V[-1 * literal] = False
                    S = propagate(-1*literal, S, V)

                else:
                    V[literal] = True
                    S = propagate(literal, S, V)
                flag = True
                break

        if flag:
            continue

        break

    for i in range(1, no_of_atoms + 1):
        if V[i] is None:
            S_temp = copy.deepcopy(S)
            V_temp = copy.deepcopy(V)

            V[i] = True

            S = propagate(i, S, V)

            V = dp1(no_of_atoms, S, V)

            if V is not None:
                return V

            S = S_temp[:]
            V = V_temp[:]
            V[i] = False

            S = propagate(i, S, V)
            return dp1(no_of_atoms, S, V)


def propagate(A, s, v):
    pop_list = []
    for i in range(len(s)):
        clause = s[i]
        for j in range(len(clause)):
            l = clause[j]
            if (l == A and v[A] is True) or (l == (-1*A) and v[A] is False):
                pop_list.append(i)
                break

            elif (l == A and v[A] is False) or (l == (-1*A) and v[A] is True):
                pop_list.append([i,j])
                break

    for x in reversed(pop_list):
        if type(x) is list:
            s[x[0]].pop(x[1])

        else:
            s.pop(x)

    return s


def backend():
    with open('davis_putnam_output') as file:
        lines = [line.rstrip('\n') for line in file]

    if lines[0] == "0":
        print('NO SOLUTION')
        return

    flag = False
    atom_map = {}
    for line in lines:
        if line == "0":
            flag = True
            continue

        if flag is False:
            continue

        line_split = line.split(' ')
        atom_map[int(line_split[0])] = line_split[1]

    moves = {}
    count_moves = 0
    for line in lines:
        if line == "0":
            break
        line_split = line.split(' ')
        if line_split[1] == "T" and atom_map[int(line_split[0])][0] == 'J':
            moves[int(atom_map[int(line_split[0])].split(',')[-1][:-1])] = atom_map[int(line_split[0])]
            count_moves += 1

    for move in range(1, count_moves + 1):
        print(moves[move])


if __name__ == '__main__':
    # front_end()
    davis_putnam()
    backend()
