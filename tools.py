#IMPORT script from sdtools
from sdtools.dohourly import hourlymain
from sdtools.run import startMonitoring
from sdtools.opentix import opentix
from sdtools.closedtix import pen_ac22
from sdtools.gethandledtix import handledtix
from sdtools.sdworkorder import getallworkorder
import pyfiglet


paul_art = pyfiglet.figlet_format("SD-TOOLS")
print(paul_art)
print("Please choose script to run:")
print("1. Hourly")
print("2. Check Closed Tickets")
print("3. Owned Ticket Status")
print("4. Run Ticket Monitor")
print("5. My Handled Tickets")
print("6. SDs Work Order")
choice = input("Enter your choice (1/2/3/4/5/6): ")


if choice == '1':
    hourlymain()
elif choice == '2':
    pen_ac22()
elif choice == '3':
    opentix()
elif choice == '4':
    startMonitoring()
elif choice == '5':
    handledtix()   
elif choice == '6':
    getallworkorder()  
else:
    print("Invalid choice. Exiting...")