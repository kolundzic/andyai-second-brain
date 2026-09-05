# 🅰️ AOC — AndyAI Obsidian Cockpit

**Version:** 0.3.0  
**Status:** READ-ONLY OBSIDIAN + KORMILO VAULT PROOF  
**Home:** `kolundzic/andyai-second-brain/modules/aoc`

## Glavno pravilo

> **Obsidian prikazuje i predlaže. AndyAI kontroliše šta sme da se izvrši.**

AOC je jednostavan ekran za rad sa AndyAI sistemom. Obsidian nije mesto koje samo odlučuje šta sme da se uradi.

## Šta je do sada provereno

- `AOC-RECON-01A` — proverili smo šta Obsidian može.
- `AOC-KORMILO-PROOF-01B` — definisali smo šta KORMILO mora da pokaže.
- `AOC-OBSIDIAN-READONLY-ADAPTER-01C` — napravili smo adapter koji samo čita.
- `AOC-KORMILO-LIVE-VAULT-01D` — napravili smo mali Obsidian vault i iz njegovih beleški sastavili KORMILO pregled.

## 01D — rezultat

KORMILO iz vaulta uspešno prikazuje:

- trenutni projekat
- trenutni repo
- gde smo stali
- poslednji kanon
- otvorene teme
- povezane projekte
- sledeća 3 koraka
- odluke koje čekaju Andyja
- izvore iz kojih je podatak pročitan

Testovi: **6/6 PASS**.

U vault smo namerno ubacili staru belešku sa opasnom instrukcijom. Sistem je nije koristio.

## Gde su fajlovi

- `vault-proof-01d/` — mali Obsidian vault za proveru
- `scripts/build_kormilo.py` — čita beleške i pravi KORMILO pregled
- `tests/test_build_kormilo.py` — testovi
- `evidence/AOC-KORMILO-LIVE-VAULT-01D-PROOF.md` — rezultat testa
- `canon/AOC-KORMILO-LIVE-VAULT-01D.md` — kratko objašnjenje proofa

## Kako se proverava

```bash
python3 scripts/build_kormilo.py vault-proof-01d
python3 -m unittest -v tests/test_build_kormilo.py
```

## Važno ograničenje

Ovaj proof radi nad pravim Obsidian-kompatibilnim folderom, ali iz ovog okruženja nemamo pristup Obsidian aplikaciji koja trenutno radi na Andyjevom MacBook-u ili HP/Omarchy računaru.

Zato je sledeći mali korak:

## `AOC–OBSIDIAN–HOST–CHECK–01E`

Na jednom stvarnom računaru povezaćemo read-only adapter sa lokalnim Obsidian vaultom i proveriti da dobijamo isti KORMILO rezultat.
