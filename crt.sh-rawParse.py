#!/usr/bin/python3

import argparse
import re

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', '--domain', required=True, help='Domain to search for')
  parser.add_argument('-i', '--input', required=True, help='Input file')
  parser.add_argument('-o', '--output', required=True, help='Output file')
  args = parser.parse_args()

  with open(args.input, 'r') as infile:
    text = infile.read()

  domain_pattern = rf'\b\w+\.{re.escape(args.domain)}\b'
  matches = re.findall(domain_pattern, text)

  unique_matches = sorted(set(match.lower() for match in matches))

  with open(args.output, 'w') as outfile:
    for match in unique_matches:
      outfile.write(match + '\n')

if __name__ == '__main__':
  main()
