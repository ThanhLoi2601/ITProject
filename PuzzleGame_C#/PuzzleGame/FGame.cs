using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Collections;
using System.IO;
using System.Threading;
using static System.Windows.Forms.VisualStyles.VisualStyleElement.ProgressBar;

namespace PuzzleGame
{
    public partial class FGame : Form
    {

        Point EntityPoint;
        ArrayList images;
        string linkImg;
        ImageProcess imgProc = new ImageProcess();
        int sec;
        int min;
        int steps = 0;
        bool checkTool = false;
        int[][] puzzle = new int[4][];
        int puzz_n = 4;
        PuzzleSovle sovle = new PuzzleSovle();

        public FGame()
        {
            EntityPoint.X = 450;
            EntityPoint.Y = 450;
            InitializeComponent();
        }

        private void btSGame_Click(object sender, EventArgs e)
        {
            checkTool = false;
            sec = 0;
            min = 0;
            steps = 0;
            lbSteps.Text = "00";
            btSolve.Enabled = true;
            btSolveBfs.Enabled = true;
            btSolveDfs.Enabled = true;
            btSolveIDS.Enabled = true;
            btShuffle.Enabled = true;
            btShuffle3x3.Enabled = true;
            imgProc.Stack.Clear();

            images = new ArrayList();

            foreach (Button b in panel.Controls)
                b.Enabled = true;

            Random rnd = new Random();
            int num = (rnd.Next()) % 5;
            linkImg = num.ToString() + ".jpg";

            pBOriginal.Image = Image.FromFile(Path.Combine(Application.StartupPath, "images", linkImg));

            EntityPoint = imgProc.ImageStart(pBOriginal.Image, images, panel, EntityPoint, 0, false);
            foreach (Button b in panel.Controls)
            {
                if (!b.Enabled) MessageBox.Show("Thông báo", "Lỗi !!");
                int i = b.Location.Y / 150;
                int j = b.Location.X / 150;
                puzzle[i][j] = Int32.Parse(b.Text);
            }

            timeCount.Start();

        }

        private void button_Click(object sender, EventArgs e)
        {
            MoveButton((Button)sender);
            if (imgProc.Stack.Count <= 600)
                btBack.Enabled = false;
            else btBack.Enabled = true;
        }

        private void MoveButton(Button btn)
        {
            if (((btn.Location.X == EntityPoint.X - 150 || btn.Location.X == EntityPoint.X + 150) && btn.Location.Y == EntityPoint.Y)
                || ((btn.Location.Y == EntityPoint.Y - 150 || btn.Location.Y == EntityPoint.Y + 150) && btn.Location.X == EntityPoint.X))
            {
                puzzle[btn.Location.Y / 150][btn.Location.X / 150] = 0;
                puzzle[EntityPoint.Y / 150][EntityPoint.X / 150] = Int32.Parse(btn.Text);
                Point swap = btn.Location;
                btn.Location = EntityPoint;
                EntityPoint = swap;
                imgProc.pushStack(EntityPoint);
                steps++;
                if (steps > 0)
                    lbSteps.Text = steps.ToString();
            }
        }
        private void FGame_Load(object sender, EventArgs e)
        {
            pBOriginal.Image = Image.FromFile(Path.Combine(Application.StartupPath, "images", "logo.jpg"));
            int x = 0;
            for (int y = 0; y < puzz_n; y++)
            {
                puzzle[y] = new int[puzz_n];
            }
            for (int i = 0; i < puzz_n; i++)
            {
                for (int j = 0; j < puzz_n; j++)
                {
                    puzzle[j][i] = x;
                    x++;
                }
            }
        }

        private void timeCount_Tick(object sender, EventArgs e)
        {
            sec++;
            if (sec >= 60)
            {
                min++;
                lbmin.Text = min.ToString();
                sec = 0;
            }
            lbsec.Text = sec.ToString();
        }

        private void btEGame_Click(object sender, EventArgs e)
        {
            MessageBoxGame messBox;
            timeCount.Stop();
            int count = imgProc.CheckWin(images, panel);
            foreach (Button b in panel.Controls)
                if (b.Enabled == true)
                    b.Enabled = false;
                else
                {
                    messBox = new MessageBoxGame("You haven't started yet!!");
                    messBox.ShowDialog();
                    return;
                }

            string result;
            if (count == 15)
                result = "You win !!";
            else
                result = "You fail !!";
            string Ann = "END GAME \n" +
                "Time: " + lbmin.Text + " : " + lbsec.Text + "\n" +
                "Photo in place: " + count + "/15 \n" +
                "Result: " + result + "\n" +
                "Number of steps: " + steps;
            if (checkTool)
                Ann += "\nUse a solution tool !!";
            messBox = new MessageBoxGame(Ann);

            messBox.ShowDialog();

            lbmin.Text = "00";
            lbsec.Text = "00";
            steps = -600;
            lbSteps.Text = "00";
            btBack.Enabled = false;
            btSolve.Enabled = false;
        }

        private void btSolve_Click(object sender, EventArgs e)
        {
            try
            {
                EntityPoint = imgProc.sweep(EntityPoint, images, panel);
                checkTool = true;
            }
            catch (Exception ex)
            {
                MessageBoxGame messBox = new MessageBoxGame(ex.ToString());

                messBox.ShowDialog();
            }
        }

        private void btBack_Click(object sender, EventArgs e)
        {
            Point s = imgProc.Stack.Pop();
            imgProc.SimulateButtonClick(s, panel);
        }

        private void btSolveBfs_Click(object sender, EventArgs e)
        {
            //int[][] temp  = new int[][] { new int[] { 1, 5, 9, 13 }, new int[] { 2, 6, 10, 0 }, new int[] { 3, 7, 11, 14 }, new int[] { 4, 8, 12, 15 } };
            PuzzleState listpuzzle = sovle.BFS_Puzzle(new PuzzleState(puzzle));
            foreach (PuzzleState p in listpuzzle.Path)
            {
                for (int i = 0; i < puzz_n; i++)
                {
                    for (int j = 0; j < puzz_n; j++)
                    {
                        Console.Write(p.Puzzle[i][j] + " ");
                        if (p.Puzzle[i][j] == 0)
                        {
                            Move(i, j);
                            Thread.Sleep(50);
                            break;
                        }
                    }
                    Console.WriteLine();
                }
                Console.WriteLine();
            }
            checkTool = true;
        }

        private void Move(int i, int j)
        {
            foreach (Button b in panel.Controls)
            {
                if (b.Location.X / 150 == j && b.Location.Y / 150 == i)
                {
                    MoveButton(b);
                    return;
                }
            }
        }

        private void btShuffle_Click(object sender, EventArgs e)
        {
            imgProc.Stack.Clear();
            int tempsteps = steps;
            EntityPoint = imgProc.ImageStart(pBOriginal.Image, images, panel, EntityPoint, 600, false);
            steps = tempsteps;
            lbSteps.Text = steps.ToString();
        }

        private void btSolveDfs_Click(object sender, EventArgs e)
        {
            PuzzleState listpuzzle = sovle.DFS_Puzzle(new PuzzleState(puzzle));
            if (listpuzzle is null)
            {
                MessageBox.Show("SỐ BƯỚC DI CHUYỂN ĐÃ LỚN HƠN 1000 !!!","Sorry",MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            foreach (PuzzleState p in listpuzzle.Path)
            {
                for (int i = 0; i < puzz_n; i++)
                {
                    for (int j = 0; j < puzz_n; j++)
                    {
                        Console.Write(p.Puzzle[i][j] + " ");
                        if (p.Puzzle[i][j] == 0)
                        {
                            Move(i, j);
                            Thread.Sleep(50);
                            break;
                        }
                    }
                    Console.WriteLine();
                }
                Console.WriteLine();
            }
            checkTool = true;
        }

        private void btShuffle3x3_Click(object sender, EventArgs e)
        {
            imgProc.Stack.Clear();
            int tempsteps = steps;
            EntityPoint = imgProc.ImageStart(pBOriginal.Image, images, panel, EntityPoint, 600, true);
            steps = tempsteps;
            lbSteps.Text = steps.ToString();
        }

        private void btSolveIDS_Click(object sender, EventArgs e)
        {
            PuzzleState listpuzzle = sovle.IDS_Puzzle(new PuzzleState(puzzle),5);

            foreach (PuzzleState p in listpuzzle.Path)
            {
                for (int i = 0; i < puzz_n; i++)
                {
                    for (int j = 0; j < puzz_n; j++)
                    {
                        Console.Write(p.Puzzle[i][j] + " ");
                        if (p.Puzzle[i][j] == 0)
                        {
                            Move(i, j);
                            Thread.Sleep(50);
                            break;
                        }
                    }
                    Console.WriteLine();
                }
                Console.WriteLine();
            }
            checkTool = true;
        }

        private void lbSteps_TextChanged(object sender, EventArgs e)
        {
            int step = int.Parse(lbSteps.Text);
            if (step == 0)
                btBack.Enabled = false;
            else if (step > 0)
                btBack.Enabled = true;
        }
    }
}
