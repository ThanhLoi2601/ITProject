namespace PuzzleGame
{
    partial class MessageBoxGame
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(MessageBoxGame));
            this.btReS = new System.Windows.Forms.Button();
            this.btCan = new System.Windows.Forms.Button();
            this.pictureBox1 = new System.Windows.Forms.PictureBox();
            this.lbAnn = new System.Windows.Forms.Label();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).BeginInit();
            this.SuspendLayout();
            // 
            // btReS
            // 
            this.btReS.Font = new System.Drawing.Font("Snap ITC", 10.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btReS.ForeColor = System.Drawing.Color.Blue;
            this.btReS.Location = new System.Drawing.Point(36, 143);
            this.btReS.Name = "btReS";
            this.btReS.Size = new System.Drawing.Size(152, 64);
            this.btReS.TabIndex = 0;
            this.btReS.Text = "RESTART";
            this.btReS.UseVisualStyleBackColor = true;
            this.btReS.Click += new System.EventHandler(this.btReS_Click);
            // 
            // btCan
            // 
            this.btCan.Font = new System.Drawing.Font("Snap ITC", 10.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btCan.ForeColor = System.Drawing.Color.Red;
            this.btCan.Location = new System.Drawing.Point(306, 143);
            this.btCan.Name = "btCan";
            this.btCan.Size = new System.Drawing.Size(159, 64);
            this.btCan.TabIndex = 1;
            this.btCan.Text = "CANCEL";
            this.btCan.UseVisualStyleBackColor = true;
            this.btCan.Click += new System.EventHandler(this.btCan_Click);
            // 
            // pictureBox1
            // 
            this.pictureBox1.Image = ((System.Drawing.Image)(resources.GetObject("pictureBox1.Image")));
            this.pictureBox1.Location = new System.Drawing.Point(23, 25);
            this.pictureBox1.Name = "pictureBox1";
            this.pictureBox1.Size = new System.Drawing.Size(111, 92);
            this.pictureBox1.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.pictureBox1.TabIndex = 2;
            this.pictureBox1.TabStop = false;
            // 
            // lbAnn
            // 
            this.lbAnn.AutoSize = true;
            this.lbAnn.Font = new System.Drawing.Font("Snap ITC", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lbAnn.Location = new System.Drawing.Point(186, 9);
            this.lbAnn.Name = "lbAnn";
            this.lbAnn.Size = new System.Drawing.Size(81, 27);
            this.lbAnn.TabIndex = 3;
            this.lbAnn.Text = "lbAnn";
            // 
            // MessageBoxGame
            // 
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.None;
            this.BackColor = System.Drawing.Color.White;
            this.ClientSize = new System.Drawing.Size(499, 219);
            this.Controls.Add(this.lbAnn);
            this.Controls.Add(this.pictureBox1);
            this.Controls.Add(this.btCan);
            this.Controls.Add(this.btReS);
            this.Font = new System.Drawing.Font("Snap ITC", 7.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Name = "MessageBoxGame";
            this.Text = "ANNOUNCEMENT";
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button btReS;
        private System.Windows.Forms.Button btCan;
        private System.Windows.Forms.PictureBox pictureBox1;
        private System.Windows.Forms.Label lbAnn;
    }
}