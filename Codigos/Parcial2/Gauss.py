A = [[0, 2, 3], [7, -1, 20],[1, -14, 8]]
c = [-1,0,1]
B = [[1, -4, 9],[7, 5, 0],[1,8,120]]
d = [4, -2, 8]

def merge(a1, b1):
    for i in range(len(b1)):
        a1[i].append(b1[i])
    return a1


def gauss(matrix):
    print("Stage 0")
    print_matrix(matrix)
    print("--------------")
    input("(press enter to start)\n")
    for i in range(len(matrix) - 1):
        # Check if row starts with value different than zero
        if matrix[i][i] == 0:
            for j in range(i+1, len(matrix)):
                if matrix[j][i] != 0:
                    aux = matrix[i]
                    matrix[i] = matrix[j]
                    matrix[j] = aux
                    break

        # Modify rows
        for j in range(i+1, len(matrix)):
            if matrix[j][i] != 0:
                multiplier = matrix[j][i]/matrix[i][i]
                matrix[j][i] = 0
                for z in range(i+1, len(matrix[j])):
                    matrix[j][z] -= multiplier*matrix[i][z]

        print("Stage " + str(i + 1))
        print_matrix(matrix)
        print("--------------")
        input("(press enter to continue)\n")

    return matrix


def det(matrix):
    def cut_matrix(index):
        aux = []
        for z in range(length):
            aux1 = []
            if z != 0:
                for k in range(length):
                    if k != index:
                        aux1.append(matrix[z][k])
                aux.append(aux1)
        return aux
    length = len(matrix)
    if length == 2:
        return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
    elif length == 1:
        return matrix[0][0]

    row = matrix[0]
    determinant = 0
    sign = 1
    for i in range(length):
        if row[i] != 0:
            determinant += row[i]*sign*det(cut_matrix(i))
        if sign > 0:
            sign = -1
        else:
            sign = 1

    return determinant


def print_matrix(matrix):
    length = len(matrix)
    spaces = 10
    for i in range(length):
        string = ""
        for j in range(len(matrix[i])):
            elem = str(round(matrix[i][j], 5))
            if elem[-2:] == ".0":
                elem = elem[:-2]
            string += elem + " "*(spaces - len(elem) + 5)
        print(string)


def ui(matrix_a, vector_b):
    length = len(matrix_a)
    if length != len(vector_b):
        print("A and b do not have the same dimensions.")
        return

    for i in range(len(matrix_a)):
        if length != len(matrix_a[i]):
            print("The A matrix is not square.")
            return

    det1 = det(matrix_a)
    if det1 == 0:
        print("The determinant of A is zero, therefore the system doesn't"
              " have a unique solution.")
        return
    else:
        print("The determinant is " + str(det1) + ".")

    input("(press enter to solve)\n")

    sol = gauss(merge(matrix_a, vector_b))

    # Find solution vector
    vector = [0]*length
    for i in range(length):
        j = length - i - 1
        solution_row = sol[j]
        vector[j] = solution_row[-1]
        for z in range(j+1, length):
            vector[j] -= solution_row[z]*vector[z]
        vector[j] = vector[j]/solution_row[j]

    i = 1
    print("Solution: ")
    for elem in vector:
        print("x" + str(i) + " = " + str(round(elem, 5)))
        i += 1

    return 0


ui(B, d)
