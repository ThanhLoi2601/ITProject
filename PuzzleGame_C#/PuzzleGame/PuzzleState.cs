using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PuzzleGame
{
    class PuzzleState
    {
        private int[][] puzzle;
        private int move = 0;
        private List<PuzzleState> path;

        public int[][] Puzzle { get => puzzle; set => puzzle = value; }
        public int Move { get => move; set => move = value; }
        internal List<PuzzleState> Path { get => path; set => path = value; }

        public PuzzleState(int[][] puzzle)
        {
            this.puzzle = puzzle;
            path = new List<PuzzleState>();
        }
        public PuzzleState(int[][] puzzle, int move)
        {
            this.puzzle = puzzle;
            path = new List<PuzzleState>();
            this.move = move;
        }
    }
}
