#! /bin/bash

echo "da fare in Python con interfaccia grafica (pyqt4 o quello che è disponibile)"

PARSED_OPTIONS=$(getopt -n "$0"  -o hF:c:f: --long "help,filename:,cue:,flac:"  -- "$@")

help="Split a single flac with cue file in to different flac tracks.\n
Usage:\n
splitsingleflac.sh -f FLACFILENAME -c CUEFILENAME\n
splitsingleflac.sh -F FLACFILENAME\n
-f, --flac\n
Specify the flac filename\n\n
-c, --cue\n
Specify the cue filename\n\n
-F, --filename\n
Specify only the flac filename, cue file must have the same filename, except for the extension"

if [ $# -eq 0 ]; then
  echo -e $help
  exit 1
fi

eval set -- "$PARSED_OPTIONS"

while true;
  do
    case "$1" in
       
        -h|--help)
          echo -e $help
        shift;;
        
        -F|--filename)
            SINGLEFLAC=$2
            FILENAME="${SINGLEFLAC%.flac}"
            CUEFILE=$FILENAME.cue
        shift 2;;

        -c|--cue)
            CUEFILE=$2
        shift 2;;

        -f|--flac)
            SINGLEFLAC=$2
        shift 2;;
        
        --)
        shift
        break;;
    esac
  done

shntool split -f "$CUEFILE" -o flac -t "%n - %t" "$SINGLEFLAC"
mv "$SINGLEFLAC" "$SINGLEFLAC".bkp
cuetag "$CUEFILE" *.flac
exit 0