# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 21:45:24 2023
conenctorinho.py -rgi <path to rgi file> -zip <path to zipped MaxBin2 bin file> -out <output_path>

This will create a output folder name <output_path> which will contain the results of the analysis:
    as a tab file with the columns:
        bin  contig  aro
    and a extraction of each bin fasta that has a RGI ARO hit
    
@author: pspea
"""

#import pandas as pd
import argparse
import zipfile
import io
import pathlib

parser = argparse.ArgumentParser()
parser.add_argument('-rgi', '--rgi_file', default='demo/rgi_output.txt')
parser.add_argument('-zip', '--zip_path', default='demo/MaxBin2_output.zip')                    
parser.add_argument('-abu', '--abundance_file', default='demo/MaxBin2_abundances.txt')                    

parser.add_argument('-out',"--output_path", default='demo/results/')

args = parser.parse_args()

rgi_file = open(args.rgi_file)

rgi_contig_dict = {}

for line in rgi_file:
    if 'Contig' not in line:
        uid = line.split('\t')[0]
        contig = line.split('\t')[1]
        aro = line.split('\t')[8]
                
        if contig.count('_') > 1:
            contig = contig.rsplit('_', 1)[0]
                    
        if contig not in rgi_contig_dict:
            rgi_contig_dict[contig] = set()
        
        if aro not in rgi_contig_dict[contig]:
            rgi_contig_dict[contig].add(aro)
            
rgi_file.close()

if '/' in args.output_path:
    pathlib.Path(args.output_path).mkdir(parents=True, exist_ok=True)
    
abundance_file = open(args.abundance_file)
contig_adundance = {}
total_depth = 0

for line in abundance_file:
    contig = line.split('\t')[0]
    reads = float(line.split('\t')[1])
    total_depth += reads
    
    if contig in rgi_contig_dict:
        if contig not in contig_adundance:
            contig_adundance[contig] = {'reads':0, 'pct_abun':0}
            
        contig_adundance[contig]['reads'] += reads
        
abundance_file.close()

for contig in contig_adundance:
    contig_adundance[contig]['pct_abun'] = 100*contig_adundance[contig]['reads']/total_depth
        
    

output_name = ('{}/conectorinho_results.txt').format(args.output_path)

output_file = open(output_name, 'w')

header = ('bin\tcontig\taro\tpct_abun\n')
output_file.write(header)
    

with zipfile.ZipFile(args.zip_path, mode="r") as archive:
    for filename in archive.namelist():
        #
        process = False
        with archive.open(filename, mode="r") as fasta_file:
            for line in io.TextIOWrapper(fasta_file, encoding="utf-8"):
                #print(line.strip())
                
                if line[0] == '>':
                    contig_from_bin = line.split('>')[1].strip()
                    
                    if contig_from_bin in rgi_contig_dict:
                        pct_abun = contig_adundance[contig_from_bin]['pct_abun']
                        
                        for aro in rgi_contig_dict[contig_from_bin]:
                            outline = ('{isbin}\t{contig}\t{aro}\t{pct_abun}\n').format(
                                isbin = filename, contig = contig_from_bin, aro = aro, pct_abun = pct_abun)
                            print(outline)
                            
                            output_file.write(outline)
                        process = True
                        
        if process:
            archive.extract(filename, args.output_path)
                
output_file.close()


    