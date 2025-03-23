using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Windows.Forms;

namespace MainWindow
{
    partial class MainWindow
    {
        /// <summary>
        /// Обязательная переменная конструктора.
        /// </summary>
        private System.ComponentModel.IContainer components = null;
        private System.Windows.Forms.Button closeButton;
        private System.Windows.Forms.Button loadCsvButton;
        private System.Windows.Forms.DataGridView dataGridView;
        private System.Windows.Forms.Label filePathLabel;

        /// <summary>
        /// Освободить все используемые ресурсы.
        /// </summary>
        /// <param name="disposing">истинно, если управляемый ресурс должен быть удален; иначе ложно.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Код, автоматически созданный конструктором форм Windows

        /// <summary>
        /// Требуемый метод для поддержки конструктора — не изменяйте 
        /// содержимое этого метода с помощью редактора кода.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.loadCsvButton = new System.Windows.Forms.Button();
            this.closeButton = new System.Windows.Forms.Button();
            this.dataGridView = new System.Windows.Forms.DataGridView();
            this.filePathLabel = new System.Windows.Forms.Label();
            this.SuspendLayout();

            //
            // loadCsvButton
            //
            this.loadCsvButton.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.loadCsvButton.Location = new System.Drawing.Point(540, 525);
            this.loadCsvButton.Name = "loadCsvButton";
            this.loadCsvButton.Size = new System.Drawing.Size(125, 50);
            this.loadCsvButton.TabIndex = 1;
            this.loadCsvButton.Text = "Load CSV";
            this.loadCsvButton.UseVisualStyleBackColor = true;
            this.loadCsvButton.Click += new System.EventHandler(this.loadCsvButton_Click);

            //
            // closeButton
            //
            this.closeButton.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.closeButton.Location = new System.Drawing.Point(675, 525);
            this.closeButton.Name = "closeButton";
            this.closeButton.Size = new System.Drawing.Size(125, 50);
            this.closeButton.TabIndex = 0;
            this.closeButton.Text = "Close App";
            this.closeButton.UseVisualStyleBackColor = true;
            this.closeButton.Click += new System.EventHandler(this.closeButton_Click);

            //
            // dataGridView
            //
            this.dataGridView.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom)
            | System.Windows.Forms.AnchorStyles.Left)
            | System.Windows.Forms.AnchorStyles.Right)));
            this.dataGridView.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridView.Location = new System.Drawing.Point(12, 70);
            this.dataGridView.Name = "dataGridView";
            this.dataGridView.Size = new System.Drawing.Size(776, 440);
            this.dataGridView.TabIndex = 2;

            //
            // filePathLabel
            //
            this.filePathLabel.AutoSize = true;
            this.filePathLabel.Location = new System.Drawing.Point(12, 35);
            this.filePathLabel.Name = "filePathLabel";
            this.filePathLabel.Size = new System.Drawing.Size(0, 13);
            this.filePathLabel.TabIndex = 3;

            //
            // MainWindow
            //
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(800, 600);
            this.Controls.Add(this.filePathLabel);
            this.Controls.Add(this.dataGridView);
            this.Controls.Add(this.closeButton);
            this.Controls.Add(this.loadCsvButton);
            this.Text = "CSV Viewer";

            this.ResumeLayout(false);
            this.PerformLayout();
        }

        #endregion

        private void loadCsvButton_Click(object sender, EventArgs e)
        {
            using (OpenFileDialog openFileDialog = new OpenFileDialog())
            {
                openFileDialog.Filter = "CSV Files|*.csv";
                if (openFileDialog.ShowDialog() == DialogResult.OK)
                {
                    string filePath = openFileDialog.FileName;
                    filePathLabel.Text = "Selected File: " + filePath;
                    LoadCSVData(filePath);
                }
            }
        }

        private void LoadCSVData(string filePath)
        {
            var parser = new CSVParser();
            var table = parser.ParseCSV(filePath);

            dataGridView.ColumnCount = table[0].Count;
            dataGridView.RowCount = table.Count;

            for (int i = 0; i < table.Count; i++)
            {
                for (int j = 0; j < table[i].Count; j++)
                {
                    dataGridView.Rows[i].Cells[j].Value = table[i][j];
                }
            }
        }

        private void closeButton_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void RunPythonScript()
        {
            try
            {
                string pythonPath = @"C:\Users\User\AppData\Local\Programs\Python\Python312\python.exe";

                string scriptPath = @"C:\Users\User\Desktop\Art's\Windowed-Table\PyScraper\main.py";

                ProcessStartInfo start = new ProcessStartInfo();
                start.FileName = pythonPath;
                start.Arguments = $"\"{scriptPath}\"";
                start.UseShellExecute = false;
                start.RedirectStandardOutput = true;
                start.RedirectStandardError = true;
                start.CreateNoWindow = true;

                pythonProcess = new Process { StartInfo = start };
                pythonProcess.Start();

                pythonProcess.OutputDataReceived += (sender, args) => Console.WriteLine(args.Data);
                pythonProcess.BeginOutputReadLine();

                pythonProcess.ErrorDataReceived += (sender, args) => Console.WriteLine("Error: " + args.Data);
                pythonProcess.BeginErrorReadLine();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error running script: {ex.Message}");
            }
        }

        private void MainWindow_FormClosing(object sender, FormClosingEventArgs e)
        {
            // Завершение процесса Python при закрытии формы
            if (pythonProcess != null && !pythonProcess.HasExited)
            {
                pythonProcess.Kill();
                pythonProcess.WaitForExit();
                pythonProcess.Dispose();
            }
        }

        private void MainWindow_Load(object sender, EventArgs e)
        {
            RunPythonScript();
        }

        private void PythonProcess_Exited(object sender, EventArgs e)
        {
            MessageBox.Show("Python script has finished.");
        }

        private Process pythonProcess;
    }
}
