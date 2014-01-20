"""
Original Author : Louis VERNY
Modified and adapted for the pipeline analysis by Madjid BESSOL


Python script to parse clustering output of CD-HIT and plot core and pan genomes
for the aligned sequences
"""
import numpy as np
import sys
import os
import getopt
import commands
import pylab as plt


def main(argv=None):

    ### ARG MANAGER
    try:
        if argv is None:
            argv = sys.argv;
            if len(argv) <= 1:
                print "No input file provided";
        try:
            help_message = 'CD-HIT Clustering output parser'; #-o [fasta output] ';
            opts, args = getopt.getopt(argv[1:], "hi:", ["help","input="]);
        except getopt.error:
            print 'CD-HIT Clustering output parser \n usage: python cdhitParser.py -i [CD-HIT .clstr output]';
        for option, value in opts:
            if option in ("-h", "--help"):
                raise Usage(help_message);
            if option in ("-i", "--input"):
                inputFile  = value;

        try:
            inputFile #checks if input exists otherwise raises exception
        except:
            print "Input file not specified";

    except:
        print "\tfor help use --help or -h";
        return 2;

    ### END ARG MANAGER

    infile = open(inputFile, 'r')
    clust = []
    nbClust = -1

    # Parse the CDHIT file
    # We get the list of the clusters, and for each cluster,
    # the sequences (ids) that it contains
    for line in infile:
        if line[0] == '>':
            nbClust += 1
            clust.append([])
        else:
            clust[nbClust].append(line.split(' ')[1].split('|')[1])

    # We then transform the data to be indiced by strains
    # instead of cluster id
    strain = []
    strainCl = []

    for x in xrange(len(clust)):
        for y in clust[x]:
            if y not in strain:
                strain.append(y)

    for i in xrange(len(strain)):
        strainCl.append([])
        for j in xrange(len(clust)):
            if strain[i] in clust[j]:
                strainCl[i].append(j)

    # Basic counteing routines to find core and pan genomes

    core = []
    pan = []

    for i in xrange(len(strainCl[0])):
        core.append(strainCl[0][i])
        pan.append(strainCl[0][i])

    core_gen = [len(core)]
    pan_gen = [len(pan)]

    for k in xrange(1,len(strainCl)):
        for CO in core:
            if CO not in strainCl[k]:
                core.remove(CO)

            if len(strainCl[0])!= len(strainCl[0]):
                print 'error'
                sys.exit()

        for PA in xrange(len(strainCl[k])):
            if strainCl[k][PA] not in pan:
                pan.append(strainCl[k][PA])

        core_gen.append(len(core))
        pan_gen.append(len(pan))

    new_families = [core_gen[0]]
    for i in xrange(1, len(strain)):
        new_families.append(pan_gen[i] - pan_gen[i-1])

    # Plotting routines
    plt.plot(core_gen, '-o', color='SteelBlue',
        label = "Core genome", alpha=.75, linewidth=2)
    plt.plot(pan_gen, '-o', color='DarkRed',
        label = "Pan genome", alpha=.75, linewidth=2)
    plt.bar(range(len(new_families)), new_families,
        align='center', width = .2, alpha=.5, label="New gene families")
    plt.xticks(range(len(strain)), tuple(xrange(1, len(strain)+1)))
    plt.ylabel('Number of gene families')
    plt.xlabel('E. Coli strains')
    plt.xlim(-1, 22)
    plt.legend(loc = 'upper left')

    genome_dir = os.path.dirname(os.path.realpath(inputFile))
    plt.savefig(genome_dir + '/' + 'core_pan_genomes.pdf')

if __name__ == "__main__":
    main()
