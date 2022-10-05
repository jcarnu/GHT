from openpyxl import Workbook
from openpyxl import load_workbook
from datetime import date
import tomli
import os
import pathlib

with open("ght.toml", mode="rb") as fp:
    config = tomli.load(fp)
    fact_date = date.today().strftime('%d/%m/%Y')
    adresse1 = config['ght']['adresse1']
    adresse2 = config['ght']['adresse2']
    outputfiles = []
    adh = tomli.load(open(config['adh']['file'],mode="rb"))
    ADH = adh['saisons']
    for saison, adh_data in ADH.items():
        year = f"{saison[2:4]}{saison[-2:]}"
        idx = 0
        outdir = pathlib.Path(config["dropbox"]["path"], "Trésorier", f"Saison {saison}", "Factures")
        if not outdir.exists():
            os.makedirs(outdir)
        for adh_x in adh_data:
            wb = load_workbook(filename="fact_template.xlsx")
            sh = wb.active
            idx = idx + 1
            adh = adh_x['nom']
            fact_name = f"F{year}-{idx:04}"
            sh['C3'] = adresse1
            sh['C4'] = adresse2
            sh['D9'] = adh.strip()
            sh['C17'] = fact_name
            sh['C18'] = sh['A24'] = fact_date
            sh['C24'] = f"Cotisation adhérent au club GHT - saison {saison}"
            sh['D24'] = sh['F24'] = sh['F33'] = adh_x['tarif']
            excel_filename = f"{fact_name}_{adh.strip().replace(' ','_')}.xlsx"
            outfilename = pathlib.Path(outdir, excel_filename)
            wb.save(filename = outfilename)
            outputfiles.append(f'"{outfilename}"')
        print(f'libreoffice --headless --outdir "{outdir}" --print-to-file {" ".join(outputfiles)}')
        os.system(f'cd "{outdir}"; libreoffice --headless  --print-to-file *.xlsx')
