from copy import deepcopy
from colorama import Fore, Back, Style

BEGIN = []
END = []
MOVE_DIRECTIONS = {"U": [-1, 0], "D": [1, 0], "L": [0, -1], "R": [0, 1]}

# unicode for draw puzzle in command promt or terminal
left_down_angle = '\u2514'
right_down_angle = '\u2518'
right_up_angle = '\u2510'
left_up_angle = '\u250C'

middle_junction = '\u253C'
top_junction = '\u252C'
bottom_junction = '\u2534'
right_junction = '\u2524'
left_junction = '\u251C'

#bar color
bar = Style.BRIGHT + Fore.CYAN + '\u2502' + Fore.RESET + Style.RESET_ALL
dash = '\u2500'

#Line draw code
first_line = Style.BRIGHT + Fore.CYAN + left_up_angle + dash + dash + dash + top_junction + dash + dash + dash + top_junction + dash + dash + dash + right_up_angle + Fore.RESET + Style.RESET_ALL
middle_line = Style.BRIGHT + Fore.CYAN + left_junction + dash + dash + dash + middle_junction + dash + dash + dash + middle_junction + dash + dash + dash + right_junction + Fore.RESET + Style.RESET_ALL
last_line = Style.BRIGHT + Fore.CYAN + left_down_angle + dash + dash + dash + bottom_junction + dash + dash + dash + bottom_junction + dash + dash + dash + right_down_angle + Fore.RESET + Style.RESET_ALL

class Node:
    def __init__(self, current_node, previous_node, g, h, move):
        self.current_node = current_node
        self.previous_node = previous_node
        self.g = g
        self.h = h
        self.move = move

    def f(self):
        return self.g + self.h

def read_input_matrices():
    print("Nhập vào ma trận ban đầu:")
    for row in range(3):
        BEGIN.append([int(x) for x in input().split()])

    print("Nhập vào ma trận đích:")
    for row in range(3):
        END.append([int(x) for x in input().split()])

    return BEGIN, END
def print_puzzle(array):
    print(first_line)
    for a in range(len(array)):
        for i in array[a]:
            if i == 0:
                print(bar, Back.RED + ' ' + Back.RESET, end=' ')
            else:
                print(bar, i, end=' ')
        print(bar)
        if a == 2:
            print(last_line)
        else:
            print(middle_line)
def get_inv_count(arr):
    inv_count = 0
    for i in range(0, 9):
        for j in range(i + 1, 9):
            if arr[j] < arr[i]: #Ô sau nhỏ hơn ô trước thì tính là 1 cặp đảo chiều
                inv_count += 1
    return inv_count
 
     

def is_solvable(BEGIN, END) :
    #mảng chứa các vị trí
    position_arr = get_position_matrix(BEGIN, END)
    inv_count = 0
    # Đếm số lượng đảo chiều 
    for i in range(0, 9):
        for j in range(i + 1, 9):
            if position_arr[j] < position_arr[i]: 
                inv_count += 1
    return (inv_count % 2 == 0)
def get_position_matrix(BEGIN, END):
    n = len(END)
    # Khởi tạo từ điển để lưu trữ chỉ số của mỗi giá trị.
    index_dict = {}
    index = 0
    
    for row in range(n):
        for col in range(n):
            value = END[row][col]
            index_dict[value] = index  # Lưu chỉ số (vị trí) vào từ điển
            index += 1
        
    # Khởi tạo ma trận position_matrix với các phần tử ban đầu là 0
    position_matrix = [[0 for _ in range(n)] for _ in range(n)]
    
    for row in range(n):
        for col in range(n):
            value = BEGIN[row][col]
            position_matrix[row][col] = index_dict[value]  
    position_array = [element for row in position_matrix for element in row]     
    return position_array
def simple_check(BEGIN, END):
    for direction in MOVE_DIRECTIONS:
        new_matrix = move_emty_tile(deepcopy(BEGIN), direction)  # kiểm tra xem ma trận mưới có = ma trận đích ko với mỗi bước di chuyển
        if new_matrix == END:
           return True
    return False
def get_pos(current_state, element):
    for row in range(len(current_state)):
        if element in current_state[row]:
            return (row, current_state[row].index(element))
 #trả về hàng,cột của phần tử
#tạo ra 1 ma trận mới ứng với bước di chuyển (lên, xuống, trái, phải)
def move_emty_tile(matrix, direction):
    empty_tile = get_pos(matrix,0); 
    new_row = empty_tile[0] + MOVE_DIRECTIONS[direction][0]
    new_col = empty_tile[1] + MOVE_DIRECTIONS[direction][1]
    if 0 <= new_row < len(matrix) and 0 <= new_col < len(matrix[0]):
        matrix[empty_tile[0]][empty_tile[1]], matrix[new_row][new_col] = matrix[new_row][new_col], matrix[empty_tile[0]][empty_tile[1]]
    return matrix


#Tính chi phí tới vị trí đích
#tính chi phí cho từng ô trong ma trận 
#= (hàng của nó trong trạng thái đích - hàng của nó trong trạng thái hiện tại) + = (cột của nó trong trạng thái đích - cột của nó trong trạng thái hiện tại)
def manhattan_distance (current_state):
    cost = 0
    for row in range(len(current_state)):
        for col in range(len(current_state[0])):
            pos = get_pos(END, current_state[row][col])
            cost += abs(row - pos[0]) + abs(col - pos[1])
    return cost
def get_adj_node(node):
    list_node = []
    empty_position = get_pos(node.current_node, 0)

    for dir in MOVE_DIRECTIONS.keys():
        new_pos = (empty_position[0] + MOVE_DIRECTIONS[dir][0], empty_position[1] + MOVE_DIRECTIONS[dir][1])
        if 0 <= new_pos[0] < len(node.current_node) and 0 <= new_pos[1] < len(node.current_node[0]):
            new_state = deepcopy(node.current_node)
            new_state[empty_position[0]][empty_position[1]] = node.current_node[new_pos[0]][new_pos[1]]
            new_state[new_pos[0]][new_pos[1]] = 0
            list_node.append(Node(new_state, node.current_node, node.g + 1, manhattan_distance (new_state), dir))

    return list_node

#Tìm nodes tốt nhất trong danh sách listNodes
def get_best_node(open_set):
    first_iter = True
    bestF = None
    best_node = None
    for node in open_set.values():
        if first_iter or node.f() < bestF:
            first_iter = False
            best_node = node
            bestF = best_node.f()
    return best_node

#Hàm tạo đường đi ngắn nhất cho bài toán
def build_path(close_set):
    node = close_set[str(END)]
    branch = list()

    while node.move:
        branch.append({
            'move': node.move,
            'node': node.current_node
        })
        node = close_set[str(node.previous_node)]
    branch.append({
        'move': '',
        'node': node.current_node
    })
    branch.reverse()

    return branch

#Hàm main để thực hiện thuật toán
def main(puzzle):
    open_set = {str(puzzle): Node(puzzle, puzzle, 0, manhattan_distance(puzzle), "")}
    closed_set = {}
    while True:
        best_node = get_best_node(open_set)
        closed_set[str(best_node.current_node)] = best_node
        if best_node.current_node == END:
            return build_path(closed_set)

        adj_node = get_adj_node(best_node) 
        print("adj", adj_node)
        for node in adj_node:
            if (str(node.current_node) in closed_set.keys() or 
                str(node.current_node) in open_set.keys() and open_set[str(node.current_node)].f() < node.f()): 
                continue
            open_set[str(node.current_node)] = node

        del open_set[str(best_node.current_node)]
puzzle = read_input_matrices()
#array = get_position_matrix(END, BEGIN)
#arr = [element for row in CHECK for element in row]
#print(CHECK)
if(simple_check(BEGIN, END)):
    print("Ma trận khởi tạo có thể trở thành ma trận đích!")
elif(is_solvable(BEGIN,END)) :
    print("Ma trận khởi tạo có thể trở thành ma trận đích!")
else :
    print("Ma trận khởi tạo không thể trở thành ma trận đích!")
    exit()
# print(puzzle)   
# print(puzzle[0])
br = main(puzzle[0])
print('Tổng số bước di chuyển : ', len(br) - 1)
print()
print(dash + dash + right_junction, "INPUT", left_junction + dash + dash)
for b in br:
    if b['move'] != '':
        letter = ''
        if b['move'] == 'U':
            letter = 'UP'
        elif b['move'] == 'R':
            letter = "RIGHT"
        elif b['move'] == 'L':
            letter = 'LEFT'
        elif b['move'] == 'D':
            letter = 'DOWN'
        print(dash + dash + right_junction, letter, left_junction + dash + dash)
    print_puzzle(b['node'])
    print()

print(dash + dash + right_junction, 'ABOVE IS THE OUTPUT', left_junction + dash + dash)
    



