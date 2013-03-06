using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace NagiosUPS
{
    class Program
    {
        public static Boolean checkBattery()
        {
            Boolean isRunningOnBattery;

            isRunningOnBattery = (System.Windows.Forms.SystemInformation.PowerStatus.PowerLineStatus ==
                                  PowerLineStatus.Offline); //true when on battery
            return isRunningOnBattery;
        }

        static int Main(string[] args)
        {
            if (checkBattery())
            {
                Console.Write("CRITICAL: System is on battery! " + System.Windows.Forms.SystemInformation.PowerStatus.BatteryLifePercent * 100 + " % remaining or " + System.Windows.Forms.SystemInformation.PowerStatus.BatteryLifeRemaining / 60 + " minutes.");
                return 2;
            }
            else
            {
                Console.Write("OK: No power outage detected.");
                return 0;
            }
        }
    }
}
