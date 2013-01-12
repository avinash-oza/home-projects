using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Diagnostics;
using System.Windows.Forms;
using System.Threading;
using System.IO;
using System.IO.Compression;

namespace DirectoryLister
{
    internal class Program
    {
        public static void DirListRun()
        {

            System.Diagnostics.Process pProcess = new System.Diagnostics.Process();

            //strCommand is path and file name of command to run
            pProcess.StartInfo.FileName = "dirlist.bat";

            //strCommandParameters are parameters to pass to program
            pProcess.StartInfo.Arguments = null;

            pProcess.StartInfo.UseShellExecute = false;

            //Set output of program to be written to process output stream
            pProcess.StartInfo.RedirectStandardOutput = true;

            //Optional
            pProcess.StartInfo.WorkingDirectory = null;

            //Start the process
            pProcess.Start();

            //Get program output
            string strOutput = pProcess.StandardOutput.ReadToEnd();

            //Wait for process to finish
            pProcess.WaitForExit();
            string fileName = "fileList-" + DateTime.Now.Date.ToString("d", CultureInfo.CreateSpecificCulture("de-DE"));

            TextWriter tw = new StreamWriter(fileName + ".txt");
            tw.WriteLine(strOutput);
            tw.Close();
            //compress the file
            
            FileInfo filepath = new FileInfo(fileName + ".txt");
            Compress(filepath);
            //delete the textfile and keep only the GZ file
            File.Delete(fileName+".txt");
        }
        public static void Compress(FileInfo fi)
        {
            // Get the stream of the source file.
            using (FileStream inFile = fi.OpenRead())
            {
                // Prevent compressing hidden and 
                // already compressed files.
                if ((File.GetAttributes(fi.FullName)
                    & FileAttributes.Hidden)
                    != FileAttributes.Hidden & fi.Extension != ".gz")
                {
                    // Create the compressed file.
                    using (FileStream outFile =
                                File.Create(fi.FullName + ".gz"))
                    {
                        using (GZipStream Compress =
                            new GZipStream(outFile,
                            CompressionMode.Compress))
                        {
                            // Copy the source file into 
                            // the compression stream.
                            inFile.CopyTo(Compress);
                        }
                    }
                }
            }
        }
        private static void Main(string[] args)
        {

            DirListRun();
        }

    }
}
