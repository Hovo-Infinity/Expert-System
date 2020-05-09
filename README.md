# Multi-criteria decision making support system
## based on fuzzy set theory methods

Based on Fuzzy logic theory

### Work mechanism

```mermaid
graph LR
A[Open file] --> B[Calculate result]
B --> C(Save result image)
C --> D[Show image in UI]
```

## Requirements
- Python 3.x
- numpy
- matplotlib
- tkinter
- product
- CSV
- pillow
- deepcopy
- any editor to save CSV file

## How to use

Clone or download repository
Open termianl, go to repository folder and run
`python GUI.py`

## How to fill CSV file 

|    | Alternative 1 | Alternative 2 | Alternative 3| ... | Alternative N|  View |
|-|-----------------|-----------------|-----------|-----|--|-
|Criteria 1|  10 | 15 | 11| ... | 12 | U
|Criteria 2| 2.3 | 2.4| 2.0| ... | 1.8 | N
|...|...|...|...|...|...| ...
|Criteria N| 9000| 1000| 1100| ...| 1150| U
