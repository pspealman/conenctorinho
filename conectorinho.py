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

import pandas as pd
import argparse
import zipfile
import io

parser = argparse.ArgumentParser()
parser.add_argument('-rgi', '--rgi_file', default='demo/rgi_nudge_data_22_data_25.txt')
parser.add_argument('-zip', '--zip_path', default='demo/1165MaxBin2ondata612,data609,anddata124(bins).zip')                    
parser.add_argument('-out',"--output_path", default='demo/')

args = parser.parse_args()

df = pd.read_table(args.rgi_file, index_col=0, sep='\t')
rgi_dict = df.to_dict('index')

rgi_contig_dict = {}

for uid in rgi_dict:
    contig = rgi_dict[uid]['Contig']
    if contig.count('_') > 1:
        contig = contig.rsplit('_', 1)[0]
        
    aro = rgi_dict[uid]['Best_Hit_ARO']
    
    if contig not in rgi_contig_dict:
        rgi_contig_dict[contig] = set()
    
    if aro not in rgi_contig_dict[contig]:
        rgi_contig_dict[contig].add(aro)

output_name = ('{}/conectorinho_results.txt').format(args.output_path)

output_file = open(output_name, 'w')

header = ('bin\tcontig\taro\n')
output_file.write(header)
    
df = pd.read_table(args.rgi_file, index_col=0, sep='\t')
rgi_dict = df.to_dict('index')

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
                        for aro in rgi_contig_dict[contig_from_bin]:
                            outline = ('{isbin}\t{contig}\t{aro}\n').format(
                                isbin = filename, contig = contig_from_bin, aro = aro)
                            print(outline)
                            
                            output_file.write(outline)
                        process = True
                        
        if process:
            archive.extract(filename, args.output_path)
                
output_file.close()