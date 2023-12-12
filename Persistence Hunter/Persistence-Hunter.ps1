<#

.DESCRIPTION
    This script hunts for persistence mechanisms via CrowdStrike's PSFalcon API . 

.OUTPUTS
    5 csv files

.NOTES
    Author: Dimitris 'DruidDruid' Binichakis , NVISO                    
    Version: 1.0
    Changelog:

.EXAMPLE
    C:\PS> .\Persistence-Hunter.ps1

    [+] Script is running, please wait for it to finish. Once a report gets generated, you will be notified via the command line

    Directory: C:\Users\MyUser\Desktop


    Mode                 LastWriteTime         Length Name
    ----                 -------------         ------ ----
    -a----        11/28/2023  12:43 PM         226276 My_Group_Registry_keys_hunter.csv
    -a----        11/28/2023  12:45 PM        3129168 My_Group_Scheduled_tasks_hunter.csv
    -a----        11/28/2023  12:47 PM          47302 My_Group_Startup_folders_hunter.csv
    -a----        11/28/2023  12:49 PM         192795 My_Group_Wmi_hunter.csv
    -a----        11/28/2023  12:52 PM        2489223 My_Group_Services_hunter.csv

    [+] The script has finished running.

#>

#Requires -Modules PSFalcon

Write-Host "[+] Script is running, please wait for it to finish. Once a report gets generated, you will be notified via the command line"

# Enter your group ID below
$group_ID = '12345678910'

#Enter your group name below, this only affects the report name in the reports that get generated
$group_name = 'My_Group'

$delimiter = '_'
   

            # Registry keys 
$commands = 'ZwBpACAALQBwAGEAdABoACAAJwBSAGUAZwBpAHMAdAByAHkAOgA6AEgASwBFAFkAXwBMAE8AQwBBAEwAXwBNAEEAQwBIAEkATgBFAFwAUwBvAGYAdAB3AGEAcgBlAFwATQBpAGMAcgBvAHMAbwBmAHQAXABXAGkAbgBkAG8AdwBzAFwAQwB1AHIAcgBlAG4AdABWAGUAcgBzAGkAbwBuAFwAUgB1AG4AXAAnACAALQBlAGEAIABzAGkAbABlAG4AdABsAHkAYwBvAG4AdABpAG4AdQBlACAAfAAgAG8AdQB0AC0AcwB0AHIAaQBuAGcAIAA7AA0ACgANAAoAZwBpACAALQBwAGEAdABoACAAJwBSAGUAZwBpAHMAdAByAHkAOgA6AEgASwBFAFkAXwBMAE8AQwBBAEwAXwBNAEEAQwBIAEkATgBFAFwAUwBvAGYAdAB3AGEAcgBlAFwATQBpAGMAcgBvAHMAbwBmAHQAXABXAGkAbgBkAG8AdwBzAFwAQwB1AHIAcgBlAG4AdABWAGUAcgBzAGkAbwBuAFwAUgB1AG4ATwBuAGMAZQBcACcAIAAtAGUAYQAgAFMAaQBsAGUAbgB0AGwAeQBDAG8AbgB0AGkAbgB1AGUAIAB8ACAAbwB1AHQALQBzAHQAcgBpAG4AZwA7AA0ACgANAAoAZwBpACAALQBwAGEAdABoACAAJwBSAGUAZwBpAHMAdAByAHkAOgA6AEgASwBFAFkAXwBMAE8AQwBBAEwAXwBNAEEAQwBIAEkATgBFAFwAUwBvAGYAdAB3AGEAcgBlAFwATQBpAGMAcgBvAHMAbwBmAHQAXABXAGkAbgBkAG8AdwBzAFwAQwB1AHIAcgBlAG4AdABWAGUAcgBzAGkAbwBuAFwAUABvAGwAaQBjAGkAZQBzAFwARQB4AHAAbABvAHIAZQByAFwAUgB1AG4AXAAnACAALQBlAGEAIABzAGkAbABlAG4AdABsAHkAYwBvAG4AdABpAG4AdQBlACAAfAAgAG8AdQB0AC0AcwB0AHIAaQBuAGcAOwA=' ,

            # Scheduled tasks
               'cwBjAGgAdABhAHMAawBzACAALwBxAHUAZQByAHkAIAAvAGYAbwAgAGMAcwB2ACAALwB2ACAAfAAgAGMAbwBuAHYAZQByAHQAZgByAG8AbQAtAGMAcwB2ACAAfAAgAHMAZQBsAGUAYwB0ACAAVABhAHMAawBOAGEAbQBlACwAIAAnAFQAYQBzAGsAIABUAG8AIABSAHUAbgAnACwAIABBAHUAdABoAG8AcgAgAHwAIABmAGwAIAB8ACAAbwB1AHQALQBzAHQAcgBpAG4AZwA7ACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAA=',
               
            # Startup Folders
               'ZwBjAGkAIAAtAHAAYQB0AGgAIAAnAEMAOgBcAFUAcwBlAHIAcwBcACoAXABBAHAAcABEAGEAdABhAFwAUgBvAGEAbQBpAG4AZwBcAE0AaQBjAHIAbwBzAG8AZgB0AFwAVwBpAG4AZABvAHcAcwBcAFMAdABhAHIAdAAgAE0AZQBuAHUAXABQAHIAbwBnAHIAYQBtAHMAXABTAHQAYQByAHQAdQBwAFwAKgAnACAALQBlAGEAIABzAGkAbABlAG4AdABsAHkAYwBvAG4AdABpAG4AdQBlACAAfAAgAHMAZQBsAGUAYwB0ACAAZgB1AGwAbABuAGEAbQBlACwATABlAG4AZwB0AGgALABDAHIAZQBhAHQAaQBvAG4AVABpAG0AZQAsAEwAYQBzAHQAVwByAGkAdABlAFQAaQBtAGUALABMAGEAcwB0AEEAYwBjAGUAcwBzAFQAaQBtAGUALABNAG8AZABlACAAfAAgAGYAbAAgAHwAIABvAHUAdAAtAHMAdAByAGkAbgBnADsADQAKAGcAYwBpACAALQBwAGEAdABoACAAJwBDADoAXABQAHIAbwBnAHIAYQBtAEQAYQB0AGEAXABNAGkAYwByAG8AcwBvAGYAdABcAFcAaQBuAGQAbwB3AHMAXABTAHQAYQByAHQAIABNAGUAbgB1AFwAUAByAG8AZwByAGEAbQBzAFwAUwB0AGEAcgB0AHUAcABcACoAJwAgAC0AZQBhACAAcwBpAGwAZQBuAHQAbAB5AGMAbwBuAHQAaQBuAHUAZQAgAHwAIABzAGUAbABlAGMAdAAgAGYAdQBsAGwAbgBhAG0AZQAsAEwAZQBuAGcAdABoACwAQwByAGUAYQB0AGkAbwBuAFQAaQBtAGUALABMAGEAcwB0AFcAcgBpAHQAZQBUAGkAbQBlACwATABhAHMAdABBAGMAYwBlAHMAcwBUAGkAbQBlACwATQBvAGQAZQAgAHwAIABmAGwAIAB8ACAAbwB1AHQALQBzAHQAcgBpAG4AZwA7AA==' ,
   
            # WMI
               'RwBlAHQALQBXAG0AaQBPAGIAagBlAGMAdAAgAC0AbgBhAG0AZQBzAHAAYQBjAGUAIAAnAHIAbwBvAHQAXABzAHUAYgBzAGMAcgBpAHAAdABpAG8AbgAnACAALQBjAGwAYQBzAHMAIABfAF8ARQB2AGUAbgB0AEMAbwBuAHMAdQBtAGUAcgAgAHwAIABmAGwAIAB8ACAAbwB1AHQALQBzAHQAcgBpAG4AZwANAAoARwBlAHQALQBXAG0AaQBPAGIAagBlAGMAdAAgAC0AbgBhAG0AZQBzAHAAYQBjAGUAIAAnAHIAbwBvAHQAXABzAHUAYgBzAGMAcgBpAHAAdABpAG8AbgAnACAALQBjAGwAYQBzAHMAIABfAF8ARQB2AGUAbgB0AEYAaQBsAHQAZQByACAAfAAgAGYAbAAgAHwAIABvAHUAdAAtAHMAdAByAGkAbgBnAA0ACgBHAGUAdAAtAFcAbQBpAE8AYgBqAGUAYwB0ACAALQBuAGEAbQBlAHMAcABhAGMAZQAgACcAcgBvAG8AdABcAHMAdQBiAHMAYwByAGkAcAB0AGkAbwBuACcAIAAtAGMAbABhAHMAcwAgAF8AXwBGAGkAbAB0AGUAcgBUAG8AQwBvAG4AcwB1AG0AZQByAEIAaQBuAGQAaQBuAGcAIAB8ACAAZgBsACAAfAAgAG8AdQB0AC0AcwB0AHIAaQBuAGcA' ,
              
            # Services
               'ZwB3AG0AaQAgAHcAaQBuADMAMgBfAHMAZQByAHYAaQBjAGUAIAB8AHMAZQBsAGUAYwB0ACAAbgBhAG0AZQAsAHAAYQB0AGgAbgBhAG0AZQAsAHMAdABhAHQAZQAsAHMAdABhAHQAdQBzACwAcwB0AGEAcgB0AG0AbwBkAGUAfAAgAGYAbAAgAHwAIABvAHUAdAAtAHMAdAByAGkAbgBnADsA' 
      



$names = 'Registry_keys' , 'Scheduled_tasks' , 'Startup_folders' , 'Wmi' , 'Services'
   
$i = 0

foreach ($command in $commands){
   
    $ExportName = "_hunter.csv"
   
    $ExportName = $group_name + $delimiter + $names[$i] + $ExportName
   
    $Arguments = '-Raw=```powershell.exe -Enc ' + $command + '```'
   
    Invoke-FalconRtr -Command 'runscript' -Argument $Arguments -Timeout 60 -GroupId $group_ID  -ea silentlyContinue -WarningAction silentlyContinue  | Export-Csv -Path $ExportName
   
    $i++
   
        if (Test-Path $ExportName) {

            Get-ChildItem $ExportName       
        }
    
   }
    
Write-Host "[+] The script has finished running."
$curDir = Get-Location
Write-Host "You can find the files generated at the following location: $curDir"
