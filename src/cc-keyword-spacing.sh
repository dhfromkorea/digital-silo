#!/bin/bash
#
# /usr/local/bin/cc-keyword-spacing
#
# Display distance in hh:mm:ss of instances of a phrase in a text file, used to help segment digitized files
#
# Written 2017-02-06 FFS
#
# Changelog:
#
#	2017-02-06 Forked from cc-update-timestamps-fix-jumps
#
# -------------------------------------------------------------------------------------------------------------------

SCRIPT=`basename $0`

# Help screen
if [ "$1" = "-h" -o "$1" = "--help" -o "$1" = "help" ] ; then
  echo -e "\n\tDisplay the distance in hh:mm:ss of instances of one or more phrases in a text file."
  echo -e "\n\tUsed to help segment digitized files -- could be used to add a tag for splitting."
  echo -e "\n\tSyntax (set the minimums to 0 to see all matches):"
  echo -e "\n\t\t$SCRIPT <filename> <phrase> [<minimum distance in seconds>] [<minimum show length in seconds>] [s d n]"
  echo -e "\n\tAdd s for simulation, d for debug, or n for normal."
  echo -e "\n\tOptionally add a minimum distance, default 20 seconds, to skip adjacent mentions."
  echo -e "\tThe script will select the last of two or more instances that are too close together."
  echo -e "\n\tOptionally add a minimum show length, default 900 seconds (15 minutes), to set show boundaries."
  echo -e "\tThe script will select the first of two or more instances that are too close together."
  echo -e "\n\tExample (add multiple phrases in single quotes separated by a pipe):"
  echo -e "\n\t\t$SCRIPT 2004-02-16_0000_US_00006712_V10_VHSP2_MB19_E4_KP.txt3 \'CAPTION|Caption\' 20 1700 d"
  echo -e "\n\tThe script is experimental.\n"
   exit
fi

# Get the file name (keeps full path and extension)
if [ -z "$1" ]
  then echo -e "\n\tUsage: $SCRIPT <filename> <phrase>\n" ; exit
  else FIL=$1
fi

# Verify presence
if [ ! -f "$FIL" ] ; then echo -e "\tNot found in the current directory \t\t\t $FIL" ; exit ; fi

# Get the key phrase
if [ -z "$2" ]
  then echo -e "\n\tUsage: $SCRIPT <filename> <phrase>\n" ; exit
  else KEY="$2"
fi

# Size of window for hits to be adjacent (select the last)
if [ -z "$3" ]
  then MaxAdjacent="20"
  else MaxAdjacent="$3"
fi

# Size of window for hits to belong to the same show (select the first)
if [ -z "$4" ]
  then MinShowLen="900"
  else MinShowLen="$4"
fi

# Script mode
if [ -z "$5" ] ; then MODE=d ; else
  case $5 in
    s ) MODE=s ;;
    d ) MODE=d ;;
    n ) MODE=n ;;
    * ) echo -e "\n\t\"$5\" is not a supported script mode. See $SCRIPT -h for more.\n" ; exit ;;
  esac
fi

# OSX customizations (use GNU Core Utilities from MacPorts coreutils)
if [ "$(uname)" = "Darwin" ]
  then DAT="gdate" MV="gmv" SED="gsed" STAT="gstat" SEQ="gseq" TEE="gtee"
  else DAT="date"  MV="mv"  SED="sed"  STAT="stat"  SEQ="seq"  TEE="tee"
fi

# Log
LOG=/tmp/$( $DAT +%F )-$SCRIPT.log

# A. Preparations

# The header timestamp, derived from the filename
TOP="$( grep -a 'TOP|' $FIL | cut -d"|" -f2 )"

# Convert to a valid date
TOPd="$( echo $TOP | $SED -r 's/([0-9]{4})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2}).*/\1-\2-\3 \4:\5:\6/' )"

# Convert to the base time in seconds (unix epoch)
TOPs="$( $DAT -ud "$TOPd" +%s )"

# Get the LBT line number
LBT=$( $SED -n '/^LBT/=' $FIL | $SED '1q' )

# Make sure the LBT exists
if [ -z "$LBT" ] ; then echo -e "No local broadcast time -- please fix! \t\t\t$FIL" ; exit ; else FST=$[ LBT + 1 ] ; fi

# The end timestamp
ENT="$( grep -a 'END|' $FIL | cut -d"|" -f2 )"

# Convert to a valid date
ENTd="$( echo $ENT | $SED -r 's/([0-9]{4})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2}).*/\1-\2-\3 \4:\5:\6/' )"

# Convert to unix epoch
ENTs="$( $DAT -ud "$ENTd" +%s )"

# File duration in seconds
DUR=$[ENTs-TOPs]

# Hours and minutes
DUR="$( date -d "+$DUR seconds"\ $(date +%F) +%H:%M:%S )"

# Initialize
n=0 TP1=$TOP.000 TP1r=0 DF0=0 DF1=0 MIN=$MaxAdjacent

# Welcome
echo -e "\nInstances of \"$KEY\" with a $MaxAdjacent"s" adjacency window and a $MinShowLen"s" minimum show length in $FIL ($DUR):\n"

# B. Find the lines with the search phrase
readarray -t KEYS < <( egrep -i "$KEY" $FIL )

# C. Get the distribution
echo -e "\tkeyword \toccured_at \telapsed_since_last \tinstances\n"

# Loop over the lines
for t in `seq 0 ${#KEYS[@]}` ; do #echo "${KEYS[$t]}"

  # Extract the start and end timestamp
  if [ "${KEYS[$t]}" ] ; then IFS="|" read TS1 TS2 PT TXT <<< "${KEYS[$t]}" ; fi #; echo -e "$TS1|$TS2|$PT|$TXT"

  # Convert to a valid date and drop milliseconds
  TS1d="$( echo $TS1 | $SED -r 's/([0-9]{4})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2}).*/\1-\2-\3 \4:\5:\6/' )" #; echo -e "\t$TS1d"
  TS2d="$( echo $TS2 | $SED -r 's/([0-9]{4})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2}).*/\1-\2-\3 \4:\5:\6/' )" #; echo -e "\t$TS2d"

  # Convert to seconds (unix epoch)
  TS1u="$[ $( $DAT -ud "$TS1d" +%s 2>/dev/null ) ]" #; echo -e "\t$TS1u"
  TS2u="$[ $( $DAT -ud "$TS2d" +%s 2>/dev/null ) ]" #; echo -e "\t$TS2u"

  # Relative time
  TS1r=$[ TS1u - TOPs ]
  TS2r=$[ TS2u - TOPs ]

  # Subtract the previous end time from the current start time to get the distance in seconds
  DF0=$[ TS1r - TP2r ]

  # Debug
  #echo -e "Round a$t  \tTS1r $TS1r   \tTP1r $TP1r   \tDF0 $DF0   \tDF1 $DF1   \tMIN $MIN"

  # If the minimum show length is met, switch to adjacent (except in the first round)
  if [ $DF1 -gt $MinShowLen -a $t -gt 0 ] ; then MIN=$MaxAdjacent ; fi

  # Debug
  #echo -e "Round b$t  \tTS1r $TS1r   \tTP1r $TP1r   \tDF0 $DF0   \tDF1 $DF1   \tMIN $MIN"

  # Print when the present difference is not adjacent and last difference was large enough, identifying the end of a show
  if [[ $DF0 -gt $MaxAdjacent && $DF1 -gt $MIN && $t -gt 0 ]]
    # Reformat the output to hh:mm:ss and select output mode
    then n=$[n+1] TS="$( date -d "+$TP2r seconds"\ $(date +%F) +%H:%M:%S )" DIF="$( date -d "+$DF1 seconds"\ $(date +%F) +%H:%M:%S )"
      case $MODE in
        s ) echo -e "\t$KEY \t$TS \t$DIF" ;;
        d ) echo -e "\t$KEY \t$TS \t$DIF \t${KEYS[$[t-1]]}" ;;
        n ) echo -e "$TP1|$TP2|SEG_04|Type=End of show by captioner ID"

	    # Find the line number of $TP1
            if [ "$TP1" = "$TOP.000" ] ; then LOC=$FST ; else LOC="$( sed -rn "/$TP1/=" $FIL | sed '$!d' )" ; fi #; echo "LOC is $LOC"

            # Insert the tag after the line
            sed ""$LOC"a $TP1|$TP2|SEG_04|Type=End of show by captioner ID" < $FIL > ${FIL%3}4

            # Use the end time as the start time of the next show
            TP1=$TP2 ;;

      esac

      # Switch to minimum show length after locating a show boundary (a cutpoint) ; also reset the difference value
      MIN=$MinShowLen DF1=$DF0

    # Skip instances that are too close together and cumulate the difference value
    else DF1=$[DF1+DF0]
  fi

  # Debug
  #echo -e "Round c$t  \tTS1r $TS1r   \tTP1r $TP1r   \tDF0 $DF0   \tDF1 $DF1   \tMIN $MIN\n"

  # Keep the times for next round
  TP1r=$TS1r TP2r=$TS2r TP2=$TS2

done

# Receipt
echo -e "\nDetected $n instances of \"$KEY\" with a $MaxAdjacent"s" adjacency window and a $MinShowLen"s" minimum show length in $FIL.\n"

# EOF

