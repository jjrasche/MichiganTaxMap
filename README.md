# Michigan Tax Map

Collection of tools to display Google [fusion table](https://developers.google.com/maps/documentation/javascript/fusiontableslayer) based map displaying Michigan property taxes by county, locality, and school district.

## Application
[MillageDataV2.html](https://jjrasche.github.io/MichiganTaxMap/MillageDataV2.html)

## Methodology

milageDate.py: webscrapes property tax data for 2017

matchGISToTaxData.py: associates scraped tax data with unioned school district and municipalities GIS

MillageDataV2.html: markup invoking fusion tables seeded with results from matchGISToTaxData.py
