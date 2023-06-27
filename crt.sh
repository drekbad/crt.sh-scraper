#!/bin/bash

# CRT.sh DNS subdomain lookup
#::USE::  ./crt.sh -d <domain> -o <outfile>

while getopts :hd:ho: OPTION; do
	case $OPTION in
		d)
#			echo "+ DNS subdomain enumeration for domain ${OPTARG}"
			domain=${OPTARG}
		;;
		o)
#			echo "+ Output to file ${OPTARG}"
			outfile=${OPTARG}
		;;
		h)
                        echo -en "\n+\n"
                        echo "+ Search and retrieve all subdomains of given domain from public DNS lookup site 'crt.sh'"
			echo "+ Usage: $0 -d <domain> [-o <file]"
			echo "+"
			echo "+ -d <domain>      Domain to search"
			echo "+ -o <file>        File to write to"
			echo -en "+\n\n"
			exit 0
		;;
	esac
done

echo
if [ -z "$domain" ]; then
  echo "Missing domain. Try again with -d <domain>"
else
  echo "Searching "$domain" and writing to "$outfile"."
fi

echo
curl -s "https://crt.sh/?q=$domain" | grep -i "\.$domain" | tr A-Z a-z | sort -u | cut -d ">" -f2 | cut -d "<" -f1 > $outfile

echo "done."
