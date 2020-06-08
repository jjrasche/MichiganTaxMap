# Michigan Tax Map

Collection of tools to display Google [fusion table](https://developers.google.com/maps/documentation/javascript/fusiontableslayer) based map displaying Michigan property taxes by county, locality, and school district.

## Application
[MillageDataV2.html](https://jjrasche.github.io/MichiganTaxMap/MillageDataV2.html)

## Methodology

milageDate.py: webscrapes property tax data for 2017

matchGISToTaxData.py: associates scraped tax data with unioned school district and municipalities GIS

MillageDataV2.html: markup invoking fusion tables seeded with results from matchGISToTaxData.py

## Development Notes
- Google appears to be caching the kml file pulls 


### regex to add styles to placemarks
```txt
00-18		14f500		(primary'><value>17|primary'><value>16|primary'><value>15|primary'><value>14|primary'><value>13|primary'><value>12)
18-20		00f03e		(primary'><value>18|primary'><value>19)
20-24		00ee5e		(primary'><value>20|primary'><value>21|primary'><value>22|primary'><value>23)
24-28		00ed7d		(primary'><value>24|primary'><value>25|primary'><value>26|primary'><value>27)
28-32		00eb9c		(primary'><value>28|primary'><value>29|primary'><value>30|primary'><value>31)
32-35		00e9bb		(primary'><value>32|primary'><value>33|primary'><value>34)
35-38		00e7d9		(primary'><value>35|primary'><value>36|primary'><value>37)
38-41		00d5e6		(primary'><value>38|primary'><value>39|primary'><value>40)
41-46		00c5e5		(primary'><value>41|primary'><value>42|primary'><value>43|primary'><value>44|primary'><value>45)
46-50		00a4e3		(primary'><value>46|primary'><value>47|primary'><value>48|primary'><value>49)
50-57		0085e1		(primary'><value>50|primary'><value>51|primary'><value>52|primary'><value>53|primary'><value>54|primary'><value>55|primary'><value>56)
57-66		0065e0		(primary'><value>57|primary'><value>58|primary'><value>59|primary'><value>60|primary'><value>61|primary'><value>62|primary'><value>63|primary'><value>64|primary'><value>65)
66-72		0046de		(primary'><value>66|primary'><value>67|primary'><value>68|primary'><value>69|primary'><value>70|primary'><value>71)
72-79		0037dd		(primary'><value>72|primary'><value>73|primary'><value>74|primary'><value>75|primary'><value>76|primary'><value>77|primary'><value>78)
79-95		0019db		(primary'><value>79|primary'><value>80|primary'><value>81|primary'><value>82|primary'><value>83|primary'><value>84|primary'><value>85|primary'><value>86|primary'><value>87|primary'><value>88|primary'><value>89|primary'><value>90|primary'><value>91|primary'><value>92|primary'><value>93|primary'><value>94)
95-15		0500da		(primary'><value>95|primary'><value>96|primary'><value>97|primary'><value>98|primary'><value>99|primary'><value>100|primary'><value>101|primary'><value>102|primary'><value>103|primary'><value>104|primary'><value>105|primary'><value>106|primary'><value>107|primary'><value>108|primary'><value>109|primary'><value>110)
```