# Surrogate Generation System

The Surrogate Generation System replaces privacy-sensitive information by synthetically generated surrogates (e.g., a person originally named 'Irene Adler' is renamed to 'Buffy Summers'. For further information see our [paper](http://lml.bas.bg/ranlp2019/proceedings-ranlp-2019.pdf#page=279).

## Usage

To use the Surrogate Generation System first edit the parameters in 'param.conf'.
Then run the system with: 

```
python3 main.py
```
The System was tested on Python 3.5 and 3.6. For processing DATEs [python-dateutil](https://pypi.org/project/python-dateutil/) has to be installed.

### Entities
The following privacy-sensitive categories are currently provided:
- FEMALE (female given names)
- MALE (male given names)
- FAMILY (family names)
- ORG (organization names)
- USER (user names)
- DATE (dates)
- STREET (street names)
- STREETNO (street number)
- CITY (names of cities, towns, villages or regions)
- ZIP (Zip codes)
- PASS (passwords)
- UFID (IDs, IPs, IBANs ...)
- EMAIL (email addresses)
- URL (URLs)
- PHONE (phone and fax numbers)

### Input Format
The Surrogate Generation System accepts any type of text with [BRAT](https://brat.nlplab.org/) annotations of the described entities. For each file to process the actual text without modifications ('.txt') and the annotations of the privacy-sensitive entities ('.ann') have to be provided separately. An example for the annotation format (the numbers denote the character offsets of the entities in the txt file): 
```
T1	FEMALE 6 11	Irene
T2	CITY 126 132	London
...
```
For more information see the [brat standoff format](https://brat.nlplab.org/standoff.html). 
Note: We don't handle discontinuous text-bound annotations yet.

### Language Modules
To adapt the Surrogate Generation System to a specific language a language module has to be provided which handles the language-dependent categories (FEMALE, MALE, FAMILY, ORG, STREET, CITY, DATE).

#### German Language Module ('lang/de')
We implemented a German language module (further described in our [paper](http://lml.bas.bg/ranlp2019/proceedings-ranlp-2019.pdf#page=279)).

Requirements:
- [spacy v2.1.*](https://spacy.io/) with a German model linked via the shortcut 'de' ([How to install](https://spacy.io/usage), [Shortcut link](https://spacy.io/usage/models#usage-link))
- [Levenshtein](https://github.com/ztane/python-Levenshtein/)

#### Requirements of a Language Module
To build a language module follow the structure of the German language module in the 'lang/de' package. All the requirements have to be properties of the specific language object (see class 'German').

##### Substitute Lists
Appropriate substitutes for the categories FEMALE, MALE, FAMILY, STREET, CITY and ORG are required. They have to be provided as dictionaries where the key is the first letter and the values are lists with names starting with this first letter and named after their category (see 'lang/de/\_\_init\_\_.py).

##### Date Formats
You also have to provide your own date formats as done in the file 'lang/de/dateFormats.py'.

##### (Distributional Letter-to-Letter Mappings)
Optionally you can define first letter mappings depending on their frequency (see lang/de/freqMaps.py). Otherwise the mappings will be inherted from the file 'lang/langDefaults.py', which are frequency independent.

##### (Extensional Functions)
Functions for a different treatment of a specific language-dependent category will also be the default ones (replacing each entity by the unchanged entry of the substitute list) if you do not overwrite them in your own language module as shown in the German class in 'lang/de/\_\_init\_\_.py'.


## Citation

If you use the Surrogate Generation System please cite:

```
@inproceedings {Eder19,
	address = {Shoumen, Bulgaria},
	booktitle = {Proceedings of the International Conference Recent Advances in Natural Language Processing, RANLP 2019. Varna, Bulgaria, 2-4 September, 2019},
	pages = {259--269},
	publisher = {Incoma Ltd.},
	title = {De-identification of emails: pseudonymizing privacy-sensitive data in a {German} email corpus},
	year = {2019},
	author = {Eder, Elisabeth and Krieg-Holz, Ulrike and Hahn, Udo},
	editor = {Angelova, Galia and Mitkov, Ruslan and Nikolova, Ivelina and Temnikova, Irina}
}
```
