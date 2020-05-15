# XE
Get exchange rates from XE.com for any currency. 

## Quick Start
Suppose you want today’s exchange rates for Chilean Peso (CLP)  and today is 2020-05-15.  All you need to do is
```
from xe import XE
XE().get(‘CLP’, ‘2020-05-15’)
```
This  will return a  currency exchange table showing your currency vs any currency you can think of as a pandas data frame, e.g.
```
    Currency code        Currency name  Units per CLP  CLP per Unit
0             USD            US Dollar       0.001213    824.722721
1             EUR                 Euro       0.001123    890.713113
2             GBP        British Pound       0.000997   1002.660599
3             INR         Indian Rupee       0.092038     10.865076
4             AUD    Australian Dollar       0.001887    529.807326
```
## Notes
* If you choose a future date there there won’t be any data for it. The code will try the day before the one you chose. If that still doesn’t work it will try today’s date.