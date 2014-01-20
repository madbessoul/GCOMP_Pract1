#! /bin/bash

# Script to process multiple sequences files with MGA
# and alter the results to add a strain id (1st column)
# in order to merge all results in a single file

# Input : directory containing nucleotide sequences (
# multiple .fna files) of macrobial strains

# Execution command line : ./mga.sh [directory]
# ([directory] without ending slash '/''
# NB : If permission issues arise, use the following
# command line :
#   chmod u+x mga.sh

# Tested on OS X 10.9, with Python 2.7.3
# REQUIRMENTS :
#  - mga_osx and cd-hit (symlinked)
#  - python 2.4+ with Matplolib, Numpy and Biopython

rm $1/*.mga 2> errlog.txt
echo "== Running MGA Gene Finder"
for file in $1/*.fna
do
  # Get strain identifier from genome file
  strain=`basename $file .fna`

  # Run MGA and store results in temporary file
  mga_osx -s ${file} > $1/${strain}_tmp.mga 2> errlog.txt

  # Alter the MGA result by adding a [strain] field
  # at the beginning and make it easier to process
  # all genomes at once
  awk -v column=1 -v value=${strain} '
    BEGIN {
        FS = OFS = "\t";
    }
    {
    if(substr($1, 0, 1) != "#")
        {
            for ( i = NF + 1; i > column; i-- ) {
                $i = $(i-1);
            }
            $i = value;
            print $0;
        }
    }
    ' $1/${strain}_tmp.mga > $1/${strain}.mga && rm $1/${strain}_tmp.mga
done

echo "== Merging MGA results"
# Merge MGA results into one single file and remove temporary files
cat $1/*.mga > $1/allgenomes.mga
rm $1/NC*.mga

# Run mgaParser script
# Output :
#   - Amino-acid multi-fasta file of predited protein seqs. for each strain
#   - Protein size distribution by strain
#   - Number of predicted proteins by strain

echo "== Running mgaParser.py"
python mgaParser.py -i $1/allgenomes.mga

# Concatenate all .faa (amino-acid fasta files) and remove individual
# files.

echo "== Merging amino-acid sequences"
rm $1/allseqs.faa
cat $1/*.faa > $1/allseqs.faa
rm $1/NC*.faa

# Running CD-HIT on the amino-sequence file
# Output : fasta file with representative aa sequences
#          .clst file with gene families
echo "== Finding gene families with CD-HIT"
cd-hit -i $1/allseqs.faa -o $1/ecoli-cdhit -c 0.4 -n 2

# Todo : Python script to parse CD-HIT output and plot core and pan genomes
python cdhitParser.py --input $1/ecoli-cdhit.clstr


