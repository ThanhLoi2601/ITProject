using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PuzzleGame
{
    class PuzzleSovle
    {
        public List<PuzzleState> GetNextStates(PuzzleState state)
        {
            List<PuzzleState> nextStates = new List<PuzzleState>();

            // Tìm vị trí của số 0 (ô trống)
            int zeroRow = -1;
            int zeroCol = -1;
            for (int i = 0; i < 4; i++)
            {
                for (int j = 0; j < 4; j++)
                {
                    if (state.Puzzle[i][j] == 0)
                    {
                        zeroRow = i;
                        zeroCol = j;
                        break;
                    }
                }
                if (zeroRow != -1 && zeroCol != -1)
                    break;
            }

            // Các hướng di chuyển: (dòng, cột)
            int[][] directions = { new int[] { 0, 1 }, new int[] { 0, -1 }, new int[] { 1, 0 }, new int[] { -1, 0 } };

            // Tạo các trạng thái mới bằng cách di chuyển số 0 đến các hướng có thể
            foreach (var direction in directions)
            {
                int newRow = zeroRow + direction[0];
                int newCol = zeroCol + direction[1];

                if (newRow > 0 && newRow < 4 && newCol > 0 && newCol < 4)
                {
                    // Tạo một trạng thái mới bằng cách đổi chỗ số 0 và số kế bên
                    int[][] newState = new int[4][];
                    for (int i = 0; i < 4; i++)
                    {
                        newState[i] = new int[4];
                        for (int j = 0; j < 4; j++)
                        {
                            newState[i][j] = state.Puzzle[i][j];
                        }
                    }

                    int temp = newState[zeroRow][zeroCol];
                    newState[zeroRow][zeroCol] = newState[newRow][newCol];
                    newState[newRow][newCol] = temp;
                    nextStates.Add(new PuzzleState(newState, state.Move + 1));
                }
            }

            return nextStates;
        }

        public bool IsGoalState(int[][] state)
        {
            int[][] goalState = new int[][] { new int[] { 1, 5, 9, 13 }, new int[] { 2, 6, 10, 14 }, new int[] { 3, 7, 11, 15 }, new int[] { 4, 8, 12, 0 } };

            for (int i = 0; i < 4; i++)
            {
                for (int j = 0; j < 4; j++)
                {
                    if (state[i][j] != goalState[i][j])
                    {
                        return false;
                    }
                }
            }

            return true;
        }

        public PuzzleState BFS_Puzzle(PuzzleState initialState)
        {
            HashSet<string> visited = new HashSet<string>();
            Queue<PuzzleState> queue = new Queue<PuzzleState>();
            string initialStateString = GetStringRepresentation(initialState.Puzzle);

            queue.Enqueue(initialState);
            visited.Add(initialStateString);

            while (queue.Count > 0)
            {
                PuzzleState current = queue.Dequeue();

                if (IsGoalState(current.Puzzle))
                {
                    return current;
                }

                List<PuzzleState> nextStates = GetNextStates(current);

                foreach (PuzzleState nextState in nextStates)
                {
                    string nextStateString = GetStringRepresentation(nextState.Puzzle);

                    if (!visited.Contains(nextStateString))
                    {
                        visited.Add(nextStateString);
                        nextState.Path = current.Path.ToList();
                        nextState.Path.Add(nextState);
                        queue.Enqueue(nextState);
                    }
                }
            }

            return null;
        }

        public PuzzleState DFS_Puzzle(PuzzleState initialState)
        {
            int MAX_DEPTH = 1000;
            HashSet<string> visited = new HashSet<string>();
            Stack<PuzzleState> stack = new Stack<PuzzleState>();
            string initialStateString = GetStringRepresentation(initialState.Puzzle);

            stack.Push(initialState);
            visited.Add(initialStateString);

            while (stack.Count > 0)
            {
                PuzzleState current = stack.Pop();

                if (IsGoalState(current.Puzzle))
                {
                    return current;
                }

                if (current.Move >= MAX_DEPTH)
                    continue;

                List<PuzzleState> nextStates = GetNextStates(current);

                foreach (PuzzleState nextState in nextStates)
                {
                    string nextStateString = GetStringRepresentation(nextState.Puzzle);

                    if (!visited.Contains(nextStateString))
                    {
                        visited.Add(nextStateString);
                        nextState.Path = current.Path.ToList();
                        nextState.Path.Add(nextState);
                        stack.Push(nextState);
                    }
                }
            }

            return null;
        }

        public PuzzleState IDS_Puzzle(PuzzleState initialState, int depth_limit)
        {
            HashSet<string> visited = new HashSet<string>();
            Stack<PuzzleState> state_eq_limit = new Stack<PuzzleState>();
            string initialStateString = GetStringRepresentation(initialState.Puzzle);

            state_eq_limit.Push(initialState);
            visited.Add(initialStateString);
            while (state_eq_limit.Count > 0)
            {
                Stack<PuzzleState> stack = new Stack<PuzzleState>(new Stack<PuzzleState>(state_eq_limit));
                state_eq_limit = new Stack<PuzzleState>();

                while (stack.Count > 0)
                {
                    PuzzleState current = stack.Pop();

                    if (IsGoalState(current.Puzzle))
                    {
                        return current;
                    }

                    List<PuzzleState> nextStates = GetNextStates(current);

                    foreach (PuzzleState nextState in nextStates)
                    {
                        string nextStateString = GetStringRepresentation(nextState.Puzzle);
                         
                        if (!visited.Contains(nextStateString) && nextState.Move <= depth_limit)
                        {
                            visited.Add(nextStateString);
                            nextState.Path = current.Path.ToList();
                            nextState.Path.Add(nextState);
                            stack.Push(nextState);
                            if(nextState.Move == depth_limit)
                                state_eq_limit.Push(nextState);
                        }
                    }
                }
                depth_limit = depth_limit + 5;
            }

            return null;
        }
        private string GetStringRepresentation(int[][] state)
        {
            string result = "";
            foreach (var row in state)
            {
                foreach (var item in row)
                {
                    result += item + ",";
                }
            }
            return result.TrimEnd(',');
        }
    }
}
