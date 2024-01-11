# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 08:45:19 2023

@author: DELL
"""

import tkinter as tk
import random
import time
from collections import deque
from PIL import Image, ImageTk 
from tkinter import filedialog   
from tkinter import messagebox
import cv2

def count_inversions(puzzle):
    # Flatten the puzzle into a 1D list
    flattened_puzzle = [item for row in puzzle for item in row]
    
    # Count inversions
    inversions = 0
    for i in range(len(flattened_puzzle)):
        for j in range(i+1, len(flattened_puzzle)):
            if flattened_puzzle[i] and flattened_puzzle[j] and flattened_puzzle[i] > flattened_puzzle[j]:
                inversions += 1
    
    return inversions

def is_solvable(puzzle):
    # Check if the puzzle is solvable based on the inversion count
    inversions = count_inversions(puzzle)
    return inversions % 2 == 0


class PuzzleGame:
    def __init__(self, master):
        self.points = 0
        self.steps = 0
        self.puzzle_pieces_root = None
        self.puzzle_pieces = None
        self.master = master
        self.master.title("Puzzle Game")
        self.master.geometry("850x490")
        self.create_puzzle()
        self.empty_cell = (2, 2)  # Empty cell initially at the bottom-right
        self.create_widgets()
        self.update_display()
        
        self.master.bind('<Up>', self.move_by_key)
        self.master.bind('<Down>', self.move_by_key)
        self.master.bind('<Left>', self.move_by_key)
        self.master.bind('<Right>', self.move_by_key)

    def create_puzzle(self):
        # Create a solvable puzzle
        self.puzzle = [[0]*3 for _ in range(3)]
        nums = list(range(1, 9))
        for i in range(3):
            for j in range(3):
                if nums:
                    self.puzzle[i][j] = nums.pop(0)            
                    
    def ShowImg(self,filename):
        print(filename)
        img24 = cv2.imread(filename)
        (h24, w24, d24) = img24.shape
        r24 = float(200) / w24 
        dim24 = (int(290), int(h24 * r24))
        rd24 = cv2.resize(img24, dim24)
        img24_rgb = cv2.cvtColor(rd24, cv2.COLOR_BGR2RGB)  
        img24_pil = Image.fromarray(img24_rgb) 
        img24_tk = ImageTk.PhotoImage(img24_pil)

        # Hiển thị ảnh trên cửa sổ
        lblAnhGoc = tk.Label(self.master, image=img24_tk)
        lblAnhGoc.image = img24_tk  
        lblAnhGoc.place(x = 550, y = 280)
            
    def shuffle_puzzle(self):
        while(True):
            self.puzzle = [[0]*3 for _ in range(3)]
            nums = list(range(1, 9))
            random.shuffle(nums)
            for i in range(3):
                for j in range(3):
                    if nums:
                        self.puzzle[i][j] = nums.pop(0)
                        
            if is_solvable(self.puzzle):
                break
        self.puzzle_shuffle_root = [row[:] for row in self.puzzle]
        
        if self.puzzle_pieces is not None:
            img_temp_pieces = [row[:] for row in self.puzzle_pieces_root]
            for i in range(3):
                for j in range(3):
                    v = self.puzzle[i][j] - 1
                    if v != -1:
                        x = v % 3
                        y = v // 3
                    else:
                        x = 2
                        y = 2
                    img_temp_pieces[i][j]= self.puzzle_pieces_root[y][x]
            self.puzzle_pieces = img_temp_pieces
            self.puzzle_pieces_shuffle_root = [row[:] for row in img_temp_pieces]
        self.steps = 0
        self.points = -1
        self.update_points()
        self.update_display()

    def create_widgets(self):
        self.buttons = [[tk.Button(self.master, text=str(self.puzzle[i][j]), width=10, height=4,  font=('Arial', 14),bg='blue', fg='white', relief=tk.RAISED, bd=3, padx=20, pady=10,
                    activebackground="#8bbaff", highlightbackground="#a5b1c2",
                   highlightcolor="#a5b1c2", highlightthickness=2, command=lambda i=i, j=j: self.move(i, j)) for j in range(3)] for i in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].grid(row=i, column=j)
        self.buttons[2][2].configure(bg='white', fg='white')
        
        btshuffle= tk.Button(self.master,text="Shuffle", width=13, height=2,  font=('Arial',10),bg='yellow', fg='black', relief=tk.RAISED, bd=3, command=self.shuffle_puzzle)
        btshuffle.place(x=550, y=5)
        btsolvebfs= tk.Button(self.master,text="Solve BFS", width=13, height=2,  font=('Arial',10),bg='green', fg='white', relief=tk.RAISED, bd=3, command=self.slovebfs)
        btsolvebfs.place(x=700, y=5)
        btsolvedfs= tk.Button(self.master,text="Solve DFS", width=13, height=2,  font=('Arial',10),bg='red', fg='white', relief=tk.RAISED, bd=3, command=self.slovedfs)
        btsolvedfs.place(x=550, y=60)
        btsolveID= tk.Button(self.master,text="Solve ID", width=13, height=2,  font=('Arial',10),bg='pink', fg='black', relief=tk.RAISED, bd=3, command=self.sloveID)
        btsolveID.place(x=700, y=60)
        btsolveUCS= tk.Button(self.master,text="Solve UCS", width=13, height=2,  font=('Arial',10),bg='floralwhite', fg='black', relief=tk.RAISED, bd=3, command=self.sloveucs)
        btsolveUCS.place(x=550, y=115)
        btsolveGreedy= tk.Button(self.master,text="Solve Greedy", width=13, height=2,  font=('Arial',10),bg='silver', fg='white', relief=tk.RAISED, bd=3, command=self.slovegreedy)
        btsolveGreedy.place(x=700, y=115)
        btsolveAStar= tk.Button(self.master,text="Solve A Star", width=13, height=2,  font=('Arial',10),bg='black', fg='white', relief=tk.RAISED, bd=3, command=self.sloveAStar)
        btsolveAStar.place(x=550, y=170)
        btsolveHillClimbing= tk.Button(self.master,text="Hill Climbing", width=13, height=2,  font=('Arial',10),bg='white', fg='black', relief=tk.RAISED, bd=3, command=self.sloveHillClimbing)
        btsolveHillClimbing.place(x=700, y=170)
        btsolveBeamSearch= tk.Button(self.master,text="Beam Search", width=13, height=2,  font=('Arial',10),bg='pink', fg='black', relief=tk.RAISED, bd=3, command=self.sloveBeamSearch)
        btsolveBeamSearch.place(x=550, y=225)
        btImg= tk.Button(self.master,text="Image", width=13, height=2,  font=('Arial', 10),bg='green', fg='white', relief=tk.RAISED, bd=3, command= lambda: self.Image(3,3))
        btImg.place(x=700, y=225)
        btReset= tk.Button(self.master,text="Reset", width=13, height=2,  font=('Arial', 9),bg='brown', fg='white', relief=tk.RAISED, bd=3, command= self.reset)
        btReset.place(x=400, y=440)
        
        self.lblSteps = tk.Label(self.master,text="Steps: {}".format(self.steps), font=('Arial', 14), fg='red')
        self.lblSteps.place(x=10, y=440)
        
        self.lblPoints = tk.Label(self.master,text="Points: {}".format(self.points), font=('Arial', 14), fg='red')
        self.lblPoints.place(x=150, y=440)
        
    def reset(self):
        self.puzzle = [row[:] for row in self.puzzle_shuffle_root]
        if self.puzzle_pieces is not None:
            self.puzzle_pieces = [row[:] for row in self.puzzle_pieces_shuffle_root]
        self.steps = 0
        self.points = -1
        self.update_points()
        self.update_display()
        
    def create_puzzle_pieces(self, rows, cols):
        puzzle_width, puzzle_height = self.image.size
        piece_width = puzzle_width // cols
        piece_height = puzzle_height // rows

        puzzle_pieces = []

        for i in range(rows):
            row_pieces = []
            for j in range(cols):
                left = j * piece_width
                upper = i * piece_height
                right = left + piece_width
                lower = upper + piece_height
                piece_image = self.image.crop((left, upper, right, lower))
                if self.puzzle[i][j] == 0:
                    piece_image = piece_image.convert("L")
                piece_photo = ImageTk.PhotoImage(piece_image)
                row_pieces.append(piece_photo)
            puzzle_pieces.append(row_pieces)
        
        return puzzle_pieces
        
    def Image(self,rows,cols):
        # Load hình ảnh
        input_file = filedialog.askopenfilename(title="Open Image File",
                                                filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png")))
        if input_file:
            self.ShowImg(input_file)
            self.image = Image.open(input_file)
            self.image = self.image.resize((600, 600))  # Điều chỉnh kích thước hình ảnh nếu cần
            self.puzzle_pieces = self.create_puzzle_pieces(rows, cols)
            self.puzzle_pieces_root = self.puzzle_pieces
            # đặt các button
            for i in range(rows):
                for j in range(cols):
                    self.buttons[i][j].config(image=self.puzzle_pieces[i][j], width=171, height=136)
        else:
            messagebox.showerror("Sorry","Không tìm thấy file của bạn !!")
            
    def sloveAStar(self):
        t=0;
        solution = self.AStar_search(PuzzleState(self.puzzle))
        print("Priority: {}".format(solution.Heuristic))
        for step, state in enumerate(solution.path):
            print(f"Step {step}:")
            for row in state:
                print(row)
                for i in range(3):
                    for j in range(3):
                        num = state[i][j]
                        if(num == 0):
                            t=1
                            self.move(i, j)
                            self.master.update()
                            break 
                if t == 1:
                        t = 0
                        break
            time.sleep(0.1)
                            
            print()
            
    def AStar_search(self, initial_state):
        queue = deque([initial_state])  
  
        visited = set()  # Lưu trữ các trạng thái đã xem
        visited.add(tuple(map(tuple, initial_state.puzzle)))
        self.update_points()
        while queue:
            current_state = queue.popleft()  
  
            if self.is_goal_state(current_state.puzzle):
                return current_state  # Nếu đạt được trạng thái mục tiêu, trả về kết quả
  
            # Sinh các trạng thái kế tiếp và thêm vào queue
            for move in self.generate_moves(current_state):
                if tuple(map(tuple, move.puzzle)) not in visited:
                    queue.append(move)
                    visited.add(tuple(map(tuple, move.puzzle))) 
                    self.update_points()
                    move.path = current_state.path + [move.puzzle]
                    move.cost = current_state.cost + 1
                    move.setHeuristic(self.Heuristic(move.puzzle))
                    
            sorted_queue_list = sorted(list(queue), key=lambda item: item.Priority())
            queue = deque(sorted_queue_list)
        return None
            
    def slovegreedy(self):
        result = self.greedy_search(PuzzleState(self.puzzle))
        if result is None:
            messagebox.showerror("Sorry", "Số bước lớn hơn 1000 nên không thể tìm dược !!")
            return
        t = 0
        for step, state in enumerate(result.path):
            print(f"Step {step}:")
            for row in state:
                for i in range(3):
                    for j in range(3):
                        num = state[i][j]
                        if(num == 0):
                            t=1
                            self.move(i, j)
                            self.master.update()
                            break 
                if t == 1:
                        t = 0
                        break
            time.sleep(0.1)
         
    def greedy_search(self, initial_state, MAX_DEPTH = 1000):
            stack = [(initial_state)]  # Stack để lưu trữ các trạng thái cần xem xét
      
            visited = set()  # Lưu trữ các trạng thái đã xem
            
            while stack:
                current_state = stack.pop()  # Lấy trạng thái hiện tại từ stack
      
                if self.is_goal_state(current_state.puzzle):
                    return current_state  # Nếu đạt được trạng thái mục tiêu, trả về kết quả
                
                if current_state.moves >= MAX_DEPTH: #giúp không bị treo máy
                    continue
                
                schedule = self.generate_moves(current_state)
                schedule = sorted(schedule , key=lambda x: self.Heuristic(x.puzzle), reverse=True)
                # Sinh các trạng thái kế tiếp và thêm vào stack
                for move in schedule:
                    print(self.Heuristic(move.puzzle))
                    if tuple(map(tuple, move.puzzle)) not in visited:
                        stack.append(move)
                        visited.add(tuple(map(tuple, move.puzzle))) 
                        self.update_points()
                        move.path = current_state.path + [move.puzzle]
                        move.setHeuristic(self.Heuristic(move.puzzle))
                print()
                        
            return None
    
    def Heuristic(self,puzzle):
        h = 0
        for x in range(3):
            for y in range(3):
                v = puzzle[x][y] - 1
                if v == -1 :
                    v = 8
                y_g = v % 3
                x_g = v //3
                h = h + abs(x_g - x) + abs(y_g - y)
        return h   
    
    def sloveucs(self):
        t=0;
        solution = self.ucs_puzzle(PuzzleState(self.puzzle))
        print("Cost: {}".format(solution.cost))
        for step, state in enumerate(solution.path):
            print(f"Step {step}:")
            for row in state:
                print(row)
                for i in range(3):
                    for j in range(3):
                        num = state[i][j]
                        if(num == 0):
                            t=1
                            self.move(i, j)
                            self.master.update()
                            break 
                if t == 1:
                        t = 0
                        break
            time.sleep(0.1)
                            
            print()
    
    def ucs_puzzle(self,initial_state):
        queue = deque([initial_state])  
  
        visited = set()  # Lưu trữ các trạng thái đã xem
        visited.add(tuple(map(tuple, initial_state.puzzle)))
        self.update_points()
        
        while queue:
            current_state = queue.popleft()  
  
            if self.is_goal_state(current_state.puzzle):
                return current_state  # Nếu đạt được trạng thái mục tiêu, trả về kết quả
  
            # Sinh các trạng thái kế tiếp và thêm vào queue
            for move in self.generate_moves(current_state):
                if tuple(map(tuple, move.puzzle)) not in visited:
                    queue.append(move)
                    visited.add(tuple(map(tuple, move.puzzle)))
                    self.update_points()
                    move.path = current_state.path + [move.puzzle]
                    move.cost = current_state.cost + 1
            sorted_queue_list = sorted(list(queue), key=lambda item: item.cost)
            queue = deque(sorted_queue_list)
        return None
    
    def sloveID(self):
        d = 5
        t = 0
        result = self.ID_search(PuzzleState(self.puzzle),d)
        if result is not None:
            for step, state in enumerate(result.path):
                print(f"Step {step}:")
                for row in state:
                    for i in range(3):
                        for j in range(3):
                            num = state[i][j]
                            if(num == 0):
                                t=1
                                self.move(i, j)
                                self.master.update()
                                break 
                        if t == 1:
                            t = 0
                            break
                time.sleep(0.1)

        
    def ID_search(self, initial_state, depth_limit):
        visited = set()  # Lưu trữ các trạng thái đã xem
        
        state_eq_limit = [initial_state]
        
        while state_eq_limit:
            stack = state_eq_limit
            state_eq_limit = []
            while stack:
                current_state = stack.pop()  # Lấy trạng thái hiện tại từ stack
      
                if self.is_goal_state(current_state.puzzle):
                    return current_state  # Nếu đạt được trạng thái mục tiêu, trả về kết quả
                
                # Sinh các trạng thái kế tiếp và thêm vào stack
                for move in self.generate_moves(current_state):
                    if tuple(map(tuple, move.puzzle)) not in visited and move.moves <= depth_limit:
                        stack.append(move)
                        visited.add(tuple(map(tuple, move.puzzle)))
                        self.update_points()
                        move.path = current_state.path + [move.puzzle]
                        if move.moves == depth_limit:
                            state_eq_limit.append(move)
            depth_limit = depth_limit + 5

        return None
    
    def sloveBeamSearch(self):
        result = self.BeamSearch(PuzzleState(self.puzzle),2)
        if result is None:
            messagebox.showerror("Sorry", "Không thể tìm được path với Beam Search !!")
            return
        t = 0
        for step, state in enumerate(result.path):
            print(f"Step {step}:")
            for row in state:
                for i in range(3):
                    for j in range(3):
                        num = state[i][j]
                        if(num == 0):
                            t=1
                            self.move(i, j)
                            self.master.update()
                            break 
                if t == 1:
                        t = 0
                        break
            time.sleep(0.1)
    
    def BeamSearch(self, initial_state, k):
        queue = deque([initial_state])  
  
        visited = set()  # Lưu trữ các trạng thái đã xem
        visited.add(tuple(map(tuple, initial_state.puzzle)))
        self.update_points()
        while queue:
            k_loop = k
            current_state = queue.popleft()  
  
            if self.is_goal_state(current_state.puzzle):
                return current_state  # Nếu đạt được trạng thái mục tiêu, trả về kết quả
            
            schedule = self.generate_moves(current_state)
            schedule = sorted(schedule , key=lambda x: self.Heuristic(x.puzzle), reverse=True)
            # Sinh các trạng thái kế tiếp và thêm vào queue
            for move in schedule:
                if tuple(map(tuple, move.puzzle)) not in visited:
                    visited.add(tuple(map(tuple, move.puzzle))) 
                    move.path = current_state.path + [move.puzzle]
                    self.update_points()
                    if k_loop > 0:
                        queue.append(move)
                        k_loop = k_loop - 1
                        
                    
        return None
    
    def sloveHillClimbing(self):
        result = self.HillClimbing(PuzzleState(self.puzzle))
        if result is None:
            messagebox.showerror("Sorry", "Không thể tìm được path với Hill Climbing !!")
            return
        t = 0
        for step, state in enumerate(result.path):
            print(f"Step {step}:")
            for row in state:
                for i in range(3):
                    for j in range(3):
                        num = state[i][j]
                        if(num == 0):
                            t=1
                            self.move(i, j)
                            self.master.update()
                            break 
                if t == 1:
                        t = 0
                        break
            time.sleep(0.1)
    
    def HillClimbing(self, initial_state):
        stack_initial = [(initial_state)]
        visited = set()  # Lưu trữ các trạng thái đã xem
        self.update_points()
        while stack_initial:
            stack = [stack_initial.pop()]
            while stack:
                current_state = stack.pop()  # Lấy trạng thái hiện tại từ stack
      
                if self.is_goal_state(current_state.puzzle):
                    return current_state  # Nếu đạt được trạng thái mục tiêu, trả về kết quả
                
                # Sinh các trạng thái kế tiếp và thêm vào stack
                for move in self.generate_moves(current_state):
                    if tuple(map(tuple, move.puzzle)) not in visited:
                        visited.add(tuple(map(tuple, move.puzzle))) 
                        move.path = current_state.path + [move.puzzle]
                        if self.Heuristic(move.puzzle) < self.Heuristic(current_state.puzzle):
                            stack.append(move)
                        else: 
                            stack_initial.append(move)
                        self.update_points()

        return None
    
    def slovedfs(self):
        result = self.dfs_search(PuzzleState(self.puzzle))
        if result is None:
            messagebox.showerror("Sorry", "Số bước lớn hơn 1000 nên không thể tìm dược !!")
            return
        t = 0
        for step, state in enumerate(result.path):
            print(f"Step {step}:")
            for row in state:
                for i in range(3):
                    for j in range(3):
                        num = state[i][j]
                        if(num == 0):
                            t=1
                            self.move(i, j)
                            self.master.update()
                            break 
                if t == 1:
                        t = 0
                        break
            time.sleep(0.1)
        
    def dfs_search(self, initial_state, MAX_DEPTH = 1000):
        stack = [(initial_state)]  # Stack để lưu trữ các trạng thái cần xem xét
  
        visited = set()  # Lưu trữ các trạng thái đã xem
        self.update_points()
        
        while stack:
            current_state = stack.pop()  # Lấy trạng thái hiện tại từ stack
  
            if self.is_goal_state(current_state.puzzle):
                return current_state  # Nếu đạt được trạng thái mục tiêu, trả về kết quả
            
            if current_state.moves >= MAX_DEPTH: #giúp không bị treo máy
                continue
        
            # Sinh các trạng thái kế tiếp và thêm vào stack
            for move in self.generate_moves(current_state):
                if tuple(map(tuple, move.puzzle)) not in visited:
                    stack.append(move)
                    visited.add(tuple(map(tuple, move.puzzle))) 
                    move.path = current_state.path + [move.puzzle]
                    self.update_points()
        return None
    
    def update_points(self):
        self.points = self.points + 1
        self.lblPoints.config(text="Points: {}".format(self.points))
        self.master.update()
                    
                      
    def generate_moves(self, state):
        # Tìm vị trí ô trống (số 0)
        empty_cell = [(i, j) for i in range(3) for j in range(3) if state.puzzle[i][j] == 0][0]
        empty_row, empty_col = empty_cell

        # Các hướng di chuyển hợp lệ (trên, dưới, trái, phải)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        valid_moves = []

        for direction in directions:
            new_row, new_col = empty_row + direction[0], empty_col + direction[1]
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                
                # Tạo một bản sao của ma trận
                new_puzzle = [row[:] for row in state.puzzle]
                # Tráo đổi ô trống với ô kề cạnh
                new_puzzle[empty_row][empty_col], new_puzzle[new_row][new_col] = new_puzzle[new_row][new_col], new_puzzle[empty_row][empty_col]
                # Tạo một trạng thái mới với bước di chuyển tăng lên
                new_state = PuzzleState(new_puzzle, moves=state.moves + 1)
                valid_moves.append(new_state)

        return valid_moves
        
    def slovebfs(self):
        t=0;
        solution = self.bfs_puzzle(PuzzleState(self.puzzle))
        for step, state in enumerate(solution.path):
            print(f"Step {step}:")
            for row in state:
                for i in range(3):
                    for j in range(3):
                        num = state[i][j]
                        if(num == 0):
                            t=1
                            self.move(i, j)
                            self.master.update()
                            break 
                if t == 1:
                        t = 0
                        break
            time.sleep(0.1)
                            
            print()

    # Hàm để kiểm tra xem một trạng thái có phải là trạng thái đích hay không
    def is_goal_state(self,state):
        goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        
        return state == goal_state

    # Hàm thực hiện BFS để giải puzzle
    def bfs_puzzle(self,initial_state):
        queue = deque([initial_state])  
  
        visited = set()  # Lưu trữ các trạng thái đã xem
        visited.add(tuple(map(tuple, initial_state.puzzle)))
        self.update_points()
        while queue:
            current_state = queue.popleft()  
  
            if self.is_goal_state(current_state.puzzle):
                return current_state  # Nếu đạt được trạng thái mục tiêu, trả về kết quả
  
            # Sinh các trạng thái kế tiếp và thêm vào queue
            for move in self.generate_moves(current_state):
                if tuple(map(tuple, move.puzzle)) not in visited:
                    queue.append(move)
                    visited.add(tuple(map(tuple, move.puzzle))) 
                    move.path = current_state.path + [move.puzzle]
                    self.update_points()
                    
        return None

    def update_display(self):
        self.lblSteps.config(text="Steps: {}".format(self.steps))
        for i in range(3):
            for j in range(3):
                num = self.puzzle[i][j]
                text = str(num) if num != 0 else ""
                
                if self.puzzle_pieces is not None:
                    self.buttons[i][j].config(text=text, bg='blue', fg='white', image= self.puzzle_pieces[i][j])
                else:
                    self.buttons[i][j].config(text=text, bg='blue', fg='white')
                if num == 0:
                    self.empty_cell = (i,j)
                    self.buttons[i][j].configure(bg='white', fg='white') 
                
    def move(self, i, j):
        if (i, j) == self.empty_cell:
            return

        row, col = self.empty_cell

        # Check if the clicked cell is adjacent to the empty cell
        if (i == row and abs(j - col) == 1) or (j == col and abs(i - row) == 1):
            self.steps = self.steps + 1
            # Swap the clicked cell with the empty cell
            self.puzzle[row][col], self.puzzle[i][j] = self.puzzle[i][j], self.puzzle[row][col]
            self.empty_cell = (i, j)
            if self.puzzle_pieces is not None:
                tempImg = self.puzzle_pieces[i][j]
                self.puzzle_pieces[i][j] = self.puzzle_pieces[row][col]
                self.puzzle_pieces[row][col] = tempImg
                self.buttons[i][j].config(image=self.puzzle_pieces[i][j])
                self.buttons[row][col].config(image=self.puzzle_pieces[row][col])
            self.buttons[i][j].configure(bg='white', fg='white')
            self.buttons[row][col].configure(bg='blue', fg='white')
            self.update_display()
        print(self.puzzle)
            
    def move_by_key(self, event):
        row, col = self.empty_cell
    
        if event.keysym == 'Up' and row < 2:
            self.move(row + 1, col)
        elif event.keysym == 'Down' and row > 0:
            self.move(row - 1, col)
        elif event.keysym == 'Left' and col < 2:
            self.move(row, col + 1)
        elif event.keysym == 'Right' and col > 0:
            self.move(row, col - 1)

class PuzzleState:
    def __init__(self, puzzle, moves=0, path = [], cost = 0):
        self.puzzle = puzzle  
        self.moves = moves 
        self.path = path
        self.cost = cost
    def setHeuristic(self, heu):
        self.Heuristic = heu
    def Priority(self):
        return self.cost + self.Heuristic
        

if __name__ == "__main__":
    root = tk.Tk()
    game = PuzzleGame(root)
    root.mainloop()
