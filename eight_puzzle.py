
initial_state_matrix = []
END = []
def read_input_matrices():
    """Reads the input matrices from the user."""
    print("Nhập vào ma trận ban đầu:")
    for row in range(3):
        initial_state_matrix.append([int(x) for x in input().split()])

    print("Nhập vào ma trận đích:")
    for row in range(3):
        END.append([int(x) for x in input().split()])

    return initial_state_matrix, END

puzzle = read_input_matrices()
for row in puzzle[0]:
        for element in row:
            print(element, end=' ')
        print()

