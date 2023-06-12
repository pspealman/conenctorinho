# conectorinho
A small script that takes the RGI ARO hits and finds them in a MaxBin2 bin output file, then outputs the connection.


Example
```
conectorinho.py -rgi <path to rgi file> -zip <path to zipped MaxBin2 bin file> -out <output_path>
```

Demo
```
conectorinho.py -rgi demo/rgi_output.txt -zip demo/MaxBin2_output.zip -out demo/results
```

Expected output of the Demo should look like the folders in the /demo/expected_results folder
