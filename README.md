# gmxpy

[![Python](https://img.shields.io/badge/Python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue)](https://badge.fury.io/py/gmxpy) 
[![PyPI version](https://badge.fury.io/py/gmxpy.svg)](https://badge.fury.io/py/gmxpy)
[![License](https://img.shields.io/pypi/l/ansicolortags.svg)](https://img.shields.io/pypi/l/ansicolortags.svg) 


Author: Goosang Yu  
Contact: gsyu93@gmali.com  

Wrapping GROMACS by python script for me  
Since 2023. 07. 12.  
Tested GROMCAS ver. 2023.1

## Installation

```python
pip install gmxpy
```
*This package does not include GROMACS. You need to install GROMCAS separately. Also, gmxpy is currently being developed based on GROMACS version 2023.1. If you use a version that is too old, it may not be compatible.*

## You don need to use XMGRACE anymore!
GROMACS by default generates graphs of data in the form of xmgrace files (.xvg). Xmgrace produces visually appealing plots, but it can be cumbersome to handle in different languages or operating systems. The most important thing is that I am not familiar with it.

One of the functions included in gmxpy, called 'xvg2df', converts it into a much simpler DataFrame format.

```python
import gmxpy as gmx

df_xvg = gmx.xvg2df('interaction_energy.xvg')
df_xvg()
```
|           | Coul-SR:Protein-JZ4 | LJ-SR:Protein-JZ4 |
| --------- | ------------------- | ----------------- |
| Time (ps) |                     |                   |
| 0         | \-15.2106           | \-98.9382         |
| 10        | \-15.5369           | \-108.834         |
| 20        | \-26.0345           | \-105.193         |
| 30        | \-13.2364           | \-108.948         |
| 40        | \-13.0772           | \-109.427         |

With just a little additional effort, it can be conveniently plotted and visualized as a graph. I have freely chosen the colors that I personally like.

```python
df_xvg().plot()
```
![](docs/figures/interaction_energy.png)

## Make dataframe from gmx_MMPBSA results file
When you done your MMPB(GB)SA by [gmx_MMPBSA](https://github.com/Valdes-Tresanco-MS/gmx_MMPBSA), you will get data file containing decomposition results (DECOMP_MMPBSA_YOURSAMPLE.dat)

```
| Run on Fri Oct 27 19:17:14 2023\n
| GB non-polar solvation energies calculated with gbsa=2
idecomp = 3: Pairwise decomp adding 1-4 interactions to Internal.
Energy Decomposition Analysis (All units kcal/mol): Generalized Born model

DELTAS:
Total Energy Decomposition:
Resid 1,Resid 2,Internal,,,van der Waals,,,Electrostatic,,,Polar Solvation,,,Non-Polar Solv.,,,TOTAL,,
,,Avg.,Std. Dev.,Std. Err. of Mean,Avg.,Std. Dev.,Std. Err. of Mean,Avg.,Std. Dev.,Std. Err. of Mean,Avg.,Std. Dev.,Std. Err. of Mean,Avg.,Std. Dev.,Std. Err. of Mean,Avg.,Std. Dev.,Std. Err. of Mean
R:A:ARG:351,R:A:ARG:351,0.0,0.0,0.0,0.0,0.5897586551665688,0.015222429700453965,0.0,6.785105251173467,0.1751322965612053,2.9772637441705534,3.1993571192946018,0.08257952368898057,1.0425542756210526,0.6088115226883254,0.01571420872548597,4.019818019791606,7.549305000315245,0.19485727534109232
R:A:ARG:351,R:A:ASN:355,0.0,0.0,0.0,0.0,0.1863456749011414,0.0048098216301125886,0.0,0.6239917901458101,0.016106030960193803,0.01945755229846769,0.6328086828777381,0.016333606305824484,0.0033432117553630915,0.135970829538314,0.0035095820567055645,0.022800764053830778,0.9181641249441898,0.023698997416992967
...
```

This file need somethigng arrange for analysis... so I make function ```make_decomp_df``` for this.

```python
from gmxpy.analysis import make_decomp_df

df_decomp = make_decomp_df('DECOMP_MMPBSA_8SSN_K294E')

df_decomp
```
| Resid 1     | Resid 2     | Internal_Avg. | Internal_Std. Dev. | Internal_Std. Err. of Mean | van der Waals_Avg. | van der Waals_Std. Dev. | van der Waals_Std. Err. of Mean | Electrostatic_Avg. | Electrostatic_Std. Dev. | Electrostatic_Std. Err. of Mean | Polar Solvation_Avg. | Polar Solvation_Std. Dev. | Polar Solvation_Std. Err. of Mean | Non-Polar Solv._Avg. | Non-Polar Solv._Std. Dev. | Non-Polar Solv._Std. Err. of Mean | TOTAL_Avg. | TOTAL_Std. Dev. | TOTAL_Std. Err. of Mean |
| ----------- | ----------- | ------------- | ------------------ | -------------------------- | ------------------ | ----------------------- | ------------------------------- | ------------------ | ----------------------- | ------------------------------- | -------------------- | ------------------------- | --------------------------------- | -------------------- | ------------------------- | --------------------------------- | ---------- | --------------- | ----------------------- |
| R:A:ARG:351 | R:A:ARG:351 | 0             | 0                  | 0                          | 0                  | 0.589759                | 0.015222                        | 0                  | 6.785105                | 0.175132                        | 2.977264             | 3.199357                  | 0.08258                           | 1.042554             | 0.608812                  | 0.015714                          | 4.019818   | 7.549305        | 0.194857                |
| R:A:ARG:351 | R:A:ASN:355 | 0             | 0                  | 0                          | 0                  | 0.186346                | 0.00481                         | 0                  | 0.623992                | 0.016106                        | 0.019458             | 0.632809                  | 0.016334                          | 0.003343             | 0.135971                  | 0.00351                           | 0.022801   | 0.918164        | 0.023699                |
| R:A:ARG:351 | R:A:ALA:356 | 0             | 0                  | 0                          | 0                  | 0.016111                | 0.000416                        | 0                  | 0.220186                | 0.005683                        | \-0.00927            | 0.230623                  | 0.005953                          | 0.000006             | 0.001666                  | 0.000043                          | \-0.00926  | 0.319267        | 0.008241                |
| R:A:ARG:351 | R:A:VAL:357 | 0             | 0                  | 0                          | 0                  | 0.003677                | 0.000095                        | 0                  | 0.114568                | 0.002957                        | \-0.00283            | 0.11502                   | 0.002969                          | 0                    | 0                         | 0                                 | \-0.00283  | 0.162385        | 0.004191                |
| R:A:ARG:351 | R:A:LEU:359 | 0             | 0                  | 0                          | 0                  | 0.022395                | 0.000578                        | 0                  | 0.277392                | 0.00716                         | \-0.02104            | 0.290559                  | 0.0075                            | 0.000031             | 0.003792                  | 0.000098                          | \-0.02101  | 0.402351        | 0.010385                |
| ...         | ...         | ...           | ...                | ...                        | ...                | ...                     | ...                             | ...                | ...                     | ...                             | ...                  | ...                       | ...                               | ...                  | ...                       | ...                               | ...        | ...             | ...                     |
| L:B:AY7:527 | R:A:PHE:516 | 0             | 0                  | 0                          | \-0.20527          | 0.107602                | 0.002777                        | \-0.03828          | 0.02827                 | 0.00073                         | 0.077929             | 0.030734                  | 0.000793                          | \-0.05729            | 0.05616                   | 0.00145                           | \-0.22291  | 0.128359        | 0.003313                |
| L:B:AY7:527 | R:A:ILE:521 | 0             | 0                  | 0                          | \-0.68336          | 0.218584                | 0.005642                        | \-0.17155          | 0.131663                | 0.003398                        | 0.199371             | 0.118569                  | 0.00306                           | \-0.51561            | 0.13099                   | 0.003381                          | \-1.17114  | 0.310372        | 0.008011                |
| L:B:AY7:527 | R:A:SER:522 | 0             | 0                  | 0                          | \-0.09544          | 0.055133                | 0.001423                        | \-0.08589          | 0.123155                | 0.003179                        | 0.102106             | 0.116548                  | 0.003008                          | \-0.00409            | 0.02269                   | 0.000586                          | \-0.08332  | 0.179736        | 0.004639                |
| L:B:AY7:527 | R:A:VAL:525 | 0             | 0                  | 0                          | \-1.6084           | 0.812559                | 0.020973                        | \-0.48198          | 0.961192                | 0.02481                         | 0.332301             | 0.442281                  | 0.011416                          | \-1.14992            | 0.584504                  | 0.015087                          | \-2.90801  | 1.456502        | 0.037594                |
| L:B:AY7:527 | L:B:AY7:527 | 0             | 0                  | 0                          | 0                  | 2.464959                | 0.063624                        | 0                  | 2.834387                | 0.073159                        | 14.78321             | 1.878281                  | 0.048481                          | 9.8872               | 0.649812                  | 0.016772                          | 24.67041   | 4.249702        | 0.10969                 |

