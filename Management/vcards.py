import vobject
import sqlite3
import os
import tomli
import pathlib

with open("ght.toml", mode="rb") as fp:
    config = tomli.load(fp)

    db = sqlite3.connect(config['garradin']['db_path'])
    cursor = db.cursor()

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
    cursor.execute(f"select nom,email,telephone,cours_enfant,site from membres where saison_valide='{saison}'")
    for r  in cursor:
        u = vobject.newFromBehavior('vcard')
        u.add("fn").value=r[0]
        u.add("email").value=r[1]
        if r[2]:
            ph = u.add("tel")
            ph.type_param = "cell"
            ph.value = r[2]
        full.append(u)
        if r[3] == 1 :
            enfants.append(u)
            dremil.append(u)
        else:
            if "Toulouse" in r[4]:
                toulouse.append(u)
            if "Drémil" in r[4]:
                dremil.append(u)


    for nom, liste in lists.items():
        outfile =pathlib.Path(outputdir, f"GHT_{saison}_{nom}.vcf")
        with open(outfile,"w") as f:
            f.write("".join([x.serialize() for x in liste]))
            print(f"{outfile} generated")
