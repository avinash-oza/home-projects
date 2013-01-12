using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Diagnostics;
using System.Windows.Forms;
using System.Threading;

namespace NagiosMailer
{
    internal class Program
    {
        public static void SendBatteryEmail()
        {

            System.Diagnostics.Process pProcess = new System.Diagnostics.Process();

            //strCommand is path and file name of command to run
            pProcess.StartInfo.FileName = "email.bat";

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

            Console.WriteLine(strOutput);

        }

        public static void sendPowerBackEmail()
        {

            System.Diagnostics.Process pProcess = new System.Diagnostics.Process();

            //strCommand is path and file name of command to run
            pProcess.StartInfo.FileName = "powerBack.bat";

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
            // string strOutput = pProcess.StandardOutput.ReadToEnd();

            //Wait for process to finish
            pProcess.WaitForExit();

        }

        public static void checkBattery()
        {
            //powerisOut is tripped when the battery flag is turned on
            Boolean powerIsOut = false; //start the script with the power not being out
            Boolean isRunningOnBattery;

            isRunningOnBattery = (System.Windows.Forms.SystemInformation.PowerStatus.PowerLineStatus ==
                                  PowerLineStatus.Offline); //true when on battery
        }


        public static void Main(string[] args)
        {

            switch (args[1])
            {
                case "battery" :
                    checkBattery();


            }

        }
    }
}
