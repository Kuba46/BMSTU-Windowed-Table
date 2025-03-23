namespace MainWindow
{
    public partial class MainWindow : Form
    {
        public MainWindow()
        {
            InitializeComponent();
            this.Load += new EventHandler(MainWindow_Load);
            this.FormClosing += new FormClosingEventHandler(MainWindow_FormClosing);
        }
    }
}
