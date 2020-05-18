# Surrogate Generation System

The Surrogate Generation System replaces privacy-sensitive information by synthetically generated surrogates (e.g., a person originally named 'Irene Adler' is renamed to 'Buffy Summers'. For further information see our [paper](https://www.aclweb.org/anthology/R19-1030/).

## Usage

To use the Surrogate Generation System first edit the parameters in [param.conf](SurrogateGeneration/param.conf).
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

#### German Language Module ([lang/de](SurrogateGeneration/lang/de))
We implemented a German language module (further described in our [paper](https://www.aclweb.org/anthology/R19-1030)).

Requirements:
- [spacy v2.1.*](https://spacy.io/) with a German model linked via the shortcut 'de' ([How to install](https://spacy.io/usage), [Shortcut link](https://spacy.io/usage/models#usage-link))
- [Levenshtein](https://github.com/ztane/python-Levenshtein/)

##### Sources for Substitute Lists
- [female.json](SurrogateGeneration/lang/de/subLists/female.json), [male.json](SurrogateGeneration/lang/de/subLists/male.json), [female_nick.json](SurrogateGeneration/lang/de/subLists/female_nick.json), [male_nick.json](SurrogateGeneration/lang/de/subLists/male_nick.json)
   - Jörg Michael: <ftp://ftp.heise.de/pub/ct/listings/0717-182.zip> ([GNU Lesser General Public License (LGPL)](https://www.gnu.org/licenses/lgpl-3.0))
- [family.json](SurrogateGeneration/lang/de/subLists/family.json)
   - Deutscher Familienatlas (DFA): <http://www.namenforschung.net/fileadmin/user_upload/dfa/Inhaltsverzeichnisse_etc/Index_Band_I-V_Gesamt_Stand_September_2016.pdf>
- [org.json](SurrogateGeneration/lang/de/subLists/org.json)
   - [OpenStreetMap contributors](http://www.openstreetmap.org/): <https://www.datendieter.de/item/Liste_von_deutschen_Firmennamen_.txt> ([Open Data Commons Open Database License (ODbL)](https://opendatacommons.org/licenses/odbl/))
- [street.json](SurrogateGeneration/lang/de/subLists/street.json)
   - [OpenStreetMap contributors](http://www.openstreetmap.org/): <https://www.datendieter.de/item/Liste_von_deutschen_Strassennamen_.csv> ([Open Data Commons Open Database License (ODbL)](https://opendatacommons.org/licenses/odbl/))
- [city_rec.json](SurrogateGeneration/lang/de/subLists/city_rec.json), [city.json](SurrogateGeneration/lang/de/subLists/city.json)
   - GeoNames: <http://download.geonames.org/export/dump/> ([Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/))
   - Statistik Austria — data.statistik.gv.at: <https://www.statistik.at/strasse/suchmaske.jsp> ([Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/))
   - OpenGeoDB: <http://www.fa-technik.adfc.de/code/opengeodb/PLZ.tab>
   - Amtliche Vermessung Schweiz / swisstopo: <https://www.cadastre.ch/de/services/service/registry/plz.html>


#### Requirements of a Language Module
To build a language module follow the structure of the German language module in the [lang/de](SurrogateGeneration/lang/de) package. All the requirements have to be properties of the specific language object (see class 'German').

##### Substitute Lists
Appropriate substitutes for the categories FEMALE, MALE, FAMILY, STREET, CITY and ORG are required. They have to be provided as dictionaries where the key is the first letter and the values are lists with names starting with this first letter and named after their category (see [lang/de/__init__.py](SurrogateGeneration/lang/de/__init__.py)).

##### Date Formats
You also have to provide your own date formats as done in the file [lang/de/dateFormats.py](SurrogateGeneration/lang/de/dateFormats.py).

##### (Distributional Letter-to-Letter Mappings)
Optionally you can define first letter mappings depending on their frequency (see [lang/de/freqMaps.py](SurrogateGeneration/lang/de/freqMaps.py)). Otherwise the mappings will be inherted from the file [lang/langDefaults.py](SurrogateGeneration/lang/langDefaults.py), which are frequency independent.

##### (Extensional Functions)
Functions for a different treatment of a specific language-dependent category will also be the default ones (replacing each entity by the unchanged entry of the substitute list) if you do not overwrite them in your own language module as shown in the German class in [lang/de/__init__.py](SurrogateGeneration/lang/de/__init__.py).


## Citation

If you use or extend the Surrogate Generation System please cite:

```
@inproceedings {Eder19,
	author = {Eder, Elisabeth and Krieg-Holz, Ulrike and Hahn, Udo},
	title = {De-identification of emails: pseudonymizing privacy-sensitive data in a {German} email corpus},
	booktitle = {Proceedings of the International Conference Recent Advances in Natural Language Processing, RANLP 2019. Varna, Bulgaria, 2-4 September, 2019},
	year = {2019},
	publisher = {Incoma Ltd.},
	pages = {259--269},
	editor = {Angelova, Galia and Mitkov, Ruslan and Nikolova, Ivelina and Temnikova, Irina},
    url = {https://www.aclweb.org/anthology/R19-1030},
    doi = {10.26615/978-954-452-056-4_030},
}
```
