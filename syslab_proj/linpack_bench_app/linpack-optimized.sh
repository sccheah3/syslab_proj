#/bin/bash

#################################
# System Lab Linpack 
# Author: Kenneth Ching
# Rev 1.2 9/28/2018
################################

# Rev 1.2: Includes numactl and numastat check. Revised Processor detection
# Rev 1.1: Enabled zip packager. Detected error with single socket testing, enabled proper processor count theoretical calculations
# Rev 1.0: Initial build


#syinfo file check  
if [ -e sysinfo ]
then
	rm -f sysinfo
fi
FILE="sysinfo_$(date +%Y%m%d_%H%M%S)"

echo System Lab Linpack v1.1
echo This script will optimize HPL.dat configuration for Linpack, currently only for Intel platforms
read -p "Please input your name: " -e name 
echo Tester: "$name" >> $FILE

#System Information
echo ---------------System Information--------------- | tee -a $FILE
ipmitool fru | grep -i "Product Part" | awk '{print "System Name: "$5}' | tee -a $FILE
dmidecode -t baseboard | grep -i Product | awk '{print "Motherboard: "$3}' | tee -a $FILE
dmidecode -t bios | grep -i Release | awk '{print "BIOS ver: "$3}' | tee -a $FILE
ipmitool mc info | grep -i "Firmware Revision" | awk '{print "IPMI ver: "$4}' | tee -a $FILE 
cat /etc/redhat-release | awk '{print "OS: "$0}' | tee -a $FILE

#Processor Information
echo --------------Processor Information-------------- | tee -a $FILE
dmidecode -t processor | grep Version | awk 'NR==1{$1=""; print "Processor: "$0}' | tee -a $FILE
dmidecode -t processor | grep -i Current| awk 'NR==1{$1=$2=""; print "Frequency: "$0}' | tee -a $FILE
dmidecode -t processor | grep -i "Status: Populated" | wc -l | awk '{print "Processor Count: "$0}' | tee -a $FILE
dmidecode -t processor | grep -i "Core enabled" | awk 'NR==1{print "Cores per Processor: "$3}' >> $FILE

#Processor count
COUNT="$(dmidecode -t processor | grep -i "Status: Populated" | wc -l | awk '{print}')"
CORE="$(dmidecode -t processor | grep -i "Core enabled" | awk 'NR==1{print$3}')"
if [[ "$COUNT" > "1" ]]
then
	CORES="$(($COUNT * $CORE))"
	echo "Total Core Count: "$CORES | tee -a $FILE
else
	echo "Total Core Count: "$CORE | tee -a $FILE
fi


#Memory Information
echo --------------Memory Information--------------- | tee -a $FILE
dmidecode -t memory | grep -F "Size" | grep -Fv "No Module Installed" | wc -l | awk '{print "Number of DIMMs: "$0}' | tee -a $FILE
dimm_slots=$(dmidecode -t memory | grep -i "^[[:blank:]]*locator" | grep -io "DIMM[a-zA-Z][0-9]$")
dimm_slot_count=$(dmidecode -t memory | grep -i "^[[:blank:]]*locator" | grep -io "DIMM[a-zA-Z][0-9]$" | wc -l)
echo Total DIMM Slots: $(echo "$dimm_slot_count") | tee -a $FILE
echo DIMM Slots per channel: $(echo $dimm_slots | grep -io "[0-9]$") | tee -a $FILE
#cat /proc/meminfo | grep -i MEMtotal | awk '{print "Memory Total: "$2" "$3}' | tee -a $FILE
dmidecode -t memory | grep -F "Configured Clock" | grep -Fv "Unknown" | awk NR==1'{print "Configured Clock Speed: "$4" MHz"}' | tee -a $FILE
dmidecode -t memory | grep -F Manufacturer | grep -Fv "NO DIMM" | grep -Fv "Dimm" | awk '{$1="";print "DIMM Manufacturer: "$0}' >> $FILE
dmidecode -t memory | grep -F "Part Number" | grep -Fv "NO DIMM" | grep -Fv "Dimm" | awk '{$1=$2=i"";print "DIMM P/N: "$0}' >> $FILE


#Make Total Memory into GB
MEM="$(cat /proc/meminfo | grep -i MEMtotal | awk '{print $2}')"
#MEMGB=$(bc <<< "scale=5; $MEM / 1000000")
MEMGB=$(expr $MEM/1000000 | bc)
echo Total Memory: "$MEMGB" GB | tee -a $FILE

#Set Processor Family
read -p "What is the Intel Processor Family this system is using? (1=CascadeLake/SkyLake, 2=Broadwell/Haswell, 3=SandyBridge/IvyBridge): " -e processor
echo --------------Processor Family---------------- >> $FILE
if [ "$processor" == 1 ]; then
    NB=384; FLOPS=32; echo Processor is CascadeLake/Skylake Family | tee -a $FILE
elif [ "$processor" == 2 ]; then
	NB=192; FLOPS=16; echo Processor is Broadwell/Haswell Family | tee -a $FILE
elif [ "$processor" == 3 ]; then
	NB=256; FLOPS=8; echo Processor is IvyBridge/SandyBridge Family | tee -a $FILE
else
	echo "No Processor Family was selected"
        exit 1
fi

#Linpack Optimization
preN=$(bc <<< "scale=5; ($MEMGB * 1024 * 1024 * 1024)/8")
preN2=$(bc <<< "scale=5; sqrt($preN)")
preN3=$(bc <<< "scale=5; $preN2 * 0.8")
preN4=$(bc <<< "scale=0; $preN3 / $NB")
N=$(bc <<< "$preN4 * $NB")

#Confirmation
echo Draft of HPL.dat changes:
echo --------------------HPL.dat-------------------- | tee -a $FILE
echo Block Size NB  will be set to $NB 
echo Block Size = $NB >> $FILE
echo Problem Size N will be set to $N 
echo Problem Size = $N >> $FILE
echo The following parameters will also be changed: NBMINs=4, BCASTs=1, DEPTHs=1, SWAP=2, swapping threshold=64, L1=0, U=0

read -p "HPL.dat will be written with the parameters shown above. Write it? Y/N: " -e prompt 
if [ $prompt == 'Y' ] || [ $prompt == 'y' ] || [ $prompt == 'yes' ]; then
	echo HPL.dat has been configured
else
	exit 1;
fi

#Edit HPL.dat
#Replace Problem Size
sed -i "6s/.*"Ns"/$N       Ns/g" HPL.dat
sed -i "8s/.*NBs/$NB          NBs/g" HPL.dat
sed -i "s/.*NBMINs (>= 1)/4            NBMINs (>= 1)/g" HPL.dat
sed -i "s/.*BCASTs (0=1rg,1=1rM,2=2rg,3=2rM,4=Lng,5=LnM)/1            BCASTs (0=1rg,1=1rM,2=2rg,3=2rM,4=Lng,5=LnM)/g" HPL.dat
sed -i "s/.*DEPTHs (>=0)/1            DEPTHs (>=0)/g" HPL.dat
sed -i "s/.*SWAP (0=bin-exch,1=long,2=mix)/2            SWAP (0=bin-exch,1=long,2=mix)/g" HPL.dat
sed -i "s/.*swapping threshold/64           swapping threshold/g" HPL.dat
sed -i "s/.*L1 in (0=transposed,1=no-transposed) form/0            L1 in (0=transposed,1=no-transposed) form/g" HPL.dat
sed -i "s/.*U  in (0=transposed,1=no-transposed) form/0            U  in (0=transposed,1=no-transposed) form/g" HPL.dat

echo ---------------Linpack Theoretical Score--------------- | tee -a $FILE
FREQUENCY="$(dmidecode -t processor | grep -i Current| awk 'NR==1{$1=$2=$4=""; print$0}')"
FREQ="$(bc <<< "scale=2; $FREQUENCY / 1000" )"
if [[ "$COUNT" > "1" ]]
then
        Theoretical="$(bc <<< "$CORES * $FLOPS * $FREQ")"
        echo Theoretical Score = $Theoretical GFLOPS | tee -a $FILE
else
	Theoretical="$(bc <<< "$CORE * $FLOPS * $FREQ")"
	echo Theoretical Score = $Theoretical GFLOPS | tee -a $FILE
fi


echo -n "Ready to run Linpack? Y/N: "; read -e prompt1
if [ $prompt1 == "Y" ] || [ $prompt1 == "y" ] || [ $prompt1 == "yes" ]; then	
	echo Running Linpack...
else
        exit 1;
fi
echo Linpack results will be shown in output

#Run Linpack
numactl --interleave=all ./xhpl_intel64_static | tee output;


# Output Linpack Score
echo --------------------Linpack score------------------- | tee -a $FILE
echo Theoretical Score = $Theoretical GFLOPS
L=$(cat output | grep -i e+ | awk '{print $7}')
L1=$(echo $L | cut -f1 -d "e")
L2=$(echo $L | sed 's/^.*+/ /')
if [ $L2 == 01 ]; then
        Linpack=$(bc <<< "$L1 * 10" | cut -c 1-9); echo Linpack score = $Linpack GFLOPs | tee -a $FILE
elif
   [ $L2 == 02 ]; then
        Linpack=$(bc <<< "$L1 * 100" | cut -c 1-9); echo Linpack score = $Linpack GFLOPs | tee -a $FILE
elif
   [ $L2 == 03 ]; then
        Linpack=$(bc <<< "$L1 * 1000" | cut -c 1-9); echo Linpack score = $Linpack GFLOPs | tee -a $FILE
elif
   [ $L2 == 04 ]; then
        Linpack=$(bc <<< "$L1 * 10000" | cut -c 1-9); echo Linpack score = $Linpack GFLOPs | tee -a $FILE
elif
   [ $L2 == 05 ]; then
        Linpack=$(bc <<< "$L1 * 100000" | cut -c 1-9); echo Linpack score = $Linpack GFLOPs | tee -a $FILE
else
   echo Error!; exit 1
fi

# Calculuate efficiency
echo ---------------------Efficiency---------------------- | tee -a $FILE
Efficiency=$(echo "$Linpack/$Theoretical" | bc -l)
TotalE=$(bc <<< "scale=3; $Efficiency * 100")
TotalEFF=$(echo $TotalE | cut -c 1-5)
echo Efficiency: $TotalEFF% | tee -a $FILE
echo Results have been compiled in $FILE  
echo Linpack snapshot has been compiled in output

# Numastat check
if [[ "$COUNT" > "1" ]]
then
	NUMA_miss0="$(numastat | grep -i numa_miss | awk '{print $2}')"
	NUMA_miss1="$(numastat | grep -i numa_miss | awk '{print $3}')"
	NUMA_foreign0="$(numastat | grep -i numa_foreign | awk '{print $2}')"
	NUMA_foreign1="$(numastat | grep -i numa_foreign | awk '{print $3}')"
if [ $NUMA_miss0 == 0 ] && [ $NUMA_miss1 == 0 ] && [ $NUMA_foreign0 == 0 ] && [ $NUMA_foreign1 == 0 ]; then
	echo numastat data is clean
else
	echo numastat reports data was crossing during stress, performance maybe hindered
fi
fi

#Zip creation
echo -n "Would you like to create a zip of the results? Y/N: "; read -e tarball
if [ $tarball == "Y" ] || [ $tarball == "y" ] || [ $tarball == "yes" ]; then
        cp $FILE sysinfo
    yum -y install zip
	zip -r linpack_$FILE.zip sysinfo HPL.dat output
        echo zip file linpack_$FILE.zip has been created!

    echo -n "Upload results to DB? Y/N: "; read -e send
    if [ $send == "Y" ] || [ $send == "y" ] || [ $send == "yes" ]; then
    	filepath=$(pwd)/linpack_$FILE.zip
    	curl --form file=@$filepath http://172.16.118.50:8000/linpack_bench/upload_zipfile/
    fi
else
        exit
fi


