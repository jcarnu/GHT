import vobject
import sqlite3
import os
import tomli
import pathlib
import requests

with open("ght.toml", mode="rb") as fp:
    config = tomli.load(fp)

    full =    []
    enfants = []
    dremil =  []
    toulouse =[]

    lists={
        "Club":full,
        "Enfants":enfants,
        "Dremil":dremil,
        "Toulouse":toulouse
    }
    saison = "2022-2023"
    outputdir = pathlib.Path(config["dropbox"]["path"], "Communication/Listes", saison)
    if not outputdir.exists():
        os.makedirs(outputdir)

    result = requests.post(f'{config["garradin"]["url"]}/api/sql',
                data=f"select nom,email,telephone,cours_enfant,site from membres where saison_valide='{saison}'",
                auth=(config['garradin']['user'], config['garradin']['passwd']))
    if result.status_code == 200:
        cursor = result.json()['results']
        for r  in cursor:
            print(r)
            u = vobject.newFromBehavior('vcard')
            u.add("fn").value=r['nom']
            u.add("email").value=r['email']
            if r['telephone']:
                ph = u.add("tel")
                ph.type_param = "cell"
                ph.value = r['telephone']
            full.append(u)
            if r['cours_enfant'] == 1 :
                enfants.append(u)
                dremil.append(u)
            else:
                if "Toulouse" in r['site']:
                    toulouse.append(u)
                if "Drémil" in r['site']:
                    dremil.append(u)


        for nom, liste in lists.items():
            outfile =pathlib.Path(outputdir, f"GHT_{saison}_{nom}.vcf")
            with open(outfile,"w") as f:
                f.write("".join([x.serialize() for x in liste]))
                print(f"{outfile} generated")
    else:
        print(f"Error querying {config['garradin']['url']}/sql/api : {result.status_code}, {result.reason}")
