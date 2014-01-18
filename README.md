# GCOMP Practical 1 : Core and pan genomes


A pipeline for metagenomic analysis using MGA Gene Finder and CD-HIT to compute
the core and pan genomes. Tested with a set of 21 strains of E. Coli
-------------------------------------------------------------------------------

Usage :
./mga.sh [folder containing the .fna sequences files for each strain]


Content :
mga.sh
Bash script to run the whole pipeline analysis.

mgaParser.py
Parser for MGA Gene Finder
Output: - An amino-acid sequence file of all the proteins contained in the genome
          set
        - PDF plot of protein size distrubution by strain and number of prodicted
          proteins by strain

cdhitParser.py :
Parser for the clustering results (.clstr file) of CD-HIT
Output : PDF Plot of core and pan genomes

(All PDF plots are stored in the same folder where the genome set resides)


Example with provided data (4 genomes) :

./mga.sh example_data

Note:  CD-HIT being very computationnaly demanding, it takes several minute
up to 2h to process the 4 genomes, depending on the machine.
