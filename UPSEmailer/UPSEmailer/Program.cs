using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Diagnostics;
using System.Windows.Forms;
using System.Threading;

namespace UPSEmailer
{
    class Program
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
        static void Main(string[] args)
        {
            //powerisOut is tripped when the battery flag is turned on
            Boolean powerIsOut = false; //start the script with the power not being out
            Boolean isRunningOnBattery;
            Boolean sentEmail = false; //to keep track if we sent an email

            while (true) //keep on evaluating the condition
            {
                isRunningOnBattery = (System.Windows.Forms.SystemInformation.PowerStatus.PowerLineStatus == PowerLineStatus.Offline); //true when on battery
               
                if (isRunningOnBattery && !sentEmail) //if the email hasnt been sent yet
                {
                    SendBatteryEmail();
                    powerIsOut = !powerIsOut;
                    sentEmail = !sentEmail;
                }

                else
                {
                    if (powerIsOut && isRunningOnBattery == false) //the powerisOut flag is set and we are off of battery, send another email
                    {
                        sendPowerBackEmail();
                        powerIsOut = !powerIsOut;
                        sentEmail = !sentEmail; //reset the sent email status
                    }
                }
                

                Thread.Sleep(60000); //sleep for 1 minute before evaluating again
             /*   Console.WriteLine("Looped");
                Console.WriteLine("powerOut status" + powerIsOut);
                Console.WriteLine("Send Email status" + sentEmail);
                Console.WriteLine("Running on battery status" + isRunningOnBattery); */
            }


        }
 
    }
}
