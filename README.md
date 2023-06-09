# conenctorinho
A small script that takes the RGI ARO hits and finds them in a MaxBin2 bin output file, then outputs the connection.


Example
```
conenctorinho.py -rgi <path to rgi file> -zip <path to zipped MaxBin2 bin file> -out <output_path>
```

Demo
```
conenctorinho.py -rgi demo/rgi_nudge_data_22_data_25.txt -zip demo/1165MaxBin2ondata612,data609,anddata124(bins).zip -out demo/results
```

Expected output of the Demo should look like the folders in the /demo/expected_results folder
