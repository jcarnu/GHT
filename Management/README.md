# Setup

~~~
python -m venv mgt
source mgt/bin/activate
pip3 install -r requirements.txt
~~~

Copy `fact_template.xlsx` file into this directory (such a file is a standard invoice file)
# toml files

ght.toml file contains all necessary path definitions for dropbox target tree, sqlite file for vcards and pointer to season tomlfile (saisons.toml)

The latter structure is such as :

~~~toml
[saisons]
2022-2023 = [
  {nom="NOM prénom2", tarif=120.0},
  {nom="NOM2 prénom2, tarif=225.0},
]
~~~

Each season key is an array of dictionnaries containing "nom" and "tarif" keys matching the given Hapkido student name and year price for invoice to be edited.
Each invoice is stored on another synchronized dropbox folder in `Trésorier/Saison <seasonkey>/Factures/F<short season>-<4 zeros padded invoice nr>_<Nom>.{xlsx,pdf}`

Vcards ar located in Dropbox root folder in `Communication/Listes/<saison>/GHT*.vcf` files.
