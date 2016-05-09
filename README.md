# Ouput In Construction

An example of the reference table being converted can be found here: http://www.ons.gov.uk/businessindustryandtrade/constructionindustry/datasets/outputintheconstructionindustry

Please note. We use github for versioning purposes only. If anyone wants the actual data involved it will always be easily accessible via the ONS website (www.ons.gov.uk) and API service.


## Setup & Prep
1.) Download this repository with the "download ZIP" button.

2.) Unzip everything into its own folder.

3.) Drop the reference table to be converted into that folder.

4.) Open up the reference table and manually remove any cross symbols from the spreadsheet (databaker is having issues with these at the moment).

![alt tag](/images/cross.png)

The easiest way to do this is to do a replace all (against the whole workbook) with MS Excel.

![alt tag](/images/replace.png)


## Usage
1.) Double click the "Launch me from windows" file.

2.) Select your reference table then run.

## Notes:
The script has built in integrity and validation checks (is it a sound file? does it have the correct dimensions etc). IF there are any problems they should point you in the right direction.

## Structure

This recipe is intended for use with a very specific legacy output structure. If you're a visitor and running (I wouldnt advise it - use the demo), you'll need to use the WDA structure_csv_user.py file stored elsewherer on our github.



