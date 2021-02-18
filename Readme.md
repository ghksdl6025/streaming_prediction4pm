# Process predictive monitoring with streaming data

## Framework
<p align="center">
    <img src="./img/Framework.jpg">
</p>

### BAC activity occurance: F('Authorization Requested')[1]

<p align="center">

### Case length with activity occurred

| Occured activity | Number of cases |
|-|-|
| Authorization Requested | 12499 |
| Pending Request for Acquittance of heirs | 2119 |
| BackOffice Adjustment Requested | 3320 |
||
| Total cases | 32429 |  
</p>

### Occured activity index/prefix length
__Authorization Requested__
| Prefix | Cases |
|-|-|
| 0 | 5 |
| 1 | 37 |
| 2 | 12457 |
  
__Pending Request for acquittance of heirs__  
| Prefix | Cases |
|-|-|
| 4 | 3 |
| 5 | 8 |
| 6 | 1414 |
| 7 | 12 |
| 8 | 595 |
| 10 | 70 |
| 12 | 13 |
| 14 | 2 |
| 16 | 2 |
  
__Back-Office Adjustment Requested__
| Prefix | Cases |
|-|-|
| 2 | 5 |
| 3 | 53 |
| 4 | 2036 |
| 5 | 114 |
| 6 | 1046 |
| 7 | 18 |
| 8 | 38 |
| 9 | 1 |
| 10 | 8 |
| 11 | 1 |
## Continuous evaluation of HTC, HATC, EFDT  by prefix length and bin updates

### Accuracy comparison between last updated streaming and offline prediction

<p align="cener">
    <img src="./img/last_acc_streaming.png">
</p>


[1]Galanti, Riccardo, et al. "Explainable predictive process monitoring." 2020 2nd International Conference on Process Mining (ICPM). IEEE, 2020.