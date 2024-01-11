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
using Image = System.Drawing.Image;
using static System.Net.Mime.MediaTypeNames;

namespace PuzzleGame
{
    class ImageProcess
    {
        Stack<Point> stack = new Stack<Point>();
        
        public Stack<Point> Stack { get { return stack; } }
        public void pushStack(Point p)
        {
            stack.Push(p);
        }
        public Point ImageStart(Image original, ArrayList images, Panel pan, Point entity, int num_loop, bool puzzle3x3)
        {

            cropImageTomages(images, original, 600, 600);

            return AddImagesToButtons(images, pan, entity, num_loop, puzzle3x3);

        }

        private void cropImageTomages(ArrayList images, Image orginal, int w, int h)
        {
            Bitmap bmp = new Bitmap(w, h);

            Graphics g = Graphics.FromImage(bmp);

            g.DrawImage(orginal, 0, 0, w, h);

            g.Dispose();

            int movd = 0, movr = 0;

            for (int i = 0; i < 15; i++)
            {
                Bitmap piece = new Bitmap(150, 150);

                for (int j = 0; j < 150; j++)
                    for (int k = 0; k < 150; k++)
                        piece.SetPixel(j, k,
                            bmp.GetPixel(j + movr, k + movd));

                images.Add(piece);

                movd += 150;

                if (movd == 600)
                {
                    movd = 0;
                    movr += 150;
                }
            }
        }

        private Point AddImagesToButtons(ArrayList images, Panel panel, Point s, int num_loop, bool puzzle3x3)
        {
            int i = 14;
            int[] arr = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14 };

            foreach (Button b in panel.Controls)
            {
                if (i >= 0 && arr[i] < images.Count)
                {
                    b.Image = (Image)images[arr[i]];
                    i--;
                }
            }

            return Shuffle(num_loop, s, panel, puzzle3x3);
        }

        private Point Shuffle(int num_loop, Point s, Panel panel, bool puzzle3x3)
        {
            for (int i = 0; i < num_loop; i++)
            {
                List<Point> list = new List<Point>();

                if (puzzle3x3 == false)
                {
                    if (s.Y - 150 >= 0)
                        list.Add(new Point(s.X, s.Y - 150));
                    if (s.Y + 150 < 600)
                        list.Add(new Point(s.X, s.Y + 150));
                    if (s.X - 150 >= 0)
                        list.Add(new Point(s.X - 150, s.Y));
                    if (s.X + 150 < 600)
                        list.Add(new Point(s.X + 150, s.Y));
                } else
                {
                    if (s.Y - 150 > 0)
                        list.Add(new Point(s.X, s.Y - 150));
                    if (s.Y + 150 < 600)
                        list.Add(new Point(s.X, s.Y + 150));
                    if (s.X - 150 > 0)
                        list.Add(new Point(s.X - 150, s.Y));
                    if (s.X + 150 < 600)
                        list.Add(new Point(s.X + 150, s.Y));
                }

                Random random = new Random();
                int randomIndex = random.Next(0, list.Count);

                Point randomElement = list[randomIndex];
                SimulateButtonClick(randomElement, panel);

                s = randomElement;
            }
            return s;
        }

        public bool SimulateButtonClick(Point buttonLocation, Panel panel)
        {
            foreach (Button b in panel.Controls)
            {
                if (b.Location == buttonLocation)
                {
                    b.PerformClick();
                    return true;
                }
            }
            return false;
        }

        public int CheckWin(ArrayList images, Panel panel)
        {
            int count = 0;
            try
            {
                foreach (Button b in panel.Controls)
                {
                    if (!b.Enabled) return 0;
                    int i = (b.Location.X / 150) * 4 + b.Location.Y / 150;
                    if (b.Location.X == 450 && b.Location.Y == 450)
                        continue;
                    else if (b.Image == (Image)images[i])
                        count++;
                }
            }
            catch (Exception ex)
            {
                MessageBoxGame messBox = new MessageBoxGame(ex.ToString());

                messBox.ShowDialog();
                return -1;
            }
            return count;
        }

        public Point sweep(Point s, ArrayList images, Panel panel)
        {
            while (CheckWin(images, panel) != 15 && stack.Count >0)
            {
                s = stack.Pop();
                SimulateButtonClick(s, panel);
                Thread.Sleep(50);
            }
            return s;
        }
    }
}
