# 🅰️ AOC — AndyAI Obsidian Cockpit

**Version:** 0.4.0  
**Status:** HOST CHECK READY  
**Home:** `kolundzic/andyai-second-brain/modules/aoc`

## Glavno pravilo

> **Obsidian prikazuje i predlaže. AndyAI kontroliše šta sme da se izvrši.**

AOC je jednostavan ekran za rad sa AndyAI sistemom. Obsidian nije mesto koje samo odlučuje šta sme da se uradi.

## Šta je do sada provereno

- `AOC-RECON-01A` — proverili smo šta Obsidian može.
- `AOC-KORMILO-PROOF-01B` — definisali smo šta KORMILO mora da pokaže.
- `AOC-OBSIDIAN-READONLY-ADAPTER-01C` — napravili smo adapter koji samo čita.
- `AOC-KORMILO-LIVE-VAULT-01D` — mali Obsidian vault daje tačan KORMILO pregled. Testovi: **6/6 PASS**.
- `AOC-OBSIDIAN-HOST-CHECK-01E` — skripta za proveru na pravom Mac/HP računaru je spremna. **Još nije PASS dok se tamo ne pokrene.**

## 01E — šta sada radimo

Na računaru na kome stvarno radi Obsidian:

1. proverimo da li radi `obsidian` komanda
2. prikažemo poznate vaultove
3. izaberemo vault
4. kroz read-only adapter pročitamo četiri AOC beleške
5. proverimo da li dobijamo isti KORMILO rezultat

AOC i dalje ne menja beleške i nema pravo da izvršava akcije.

## Jednostavne komande

Iz foldera `modules/aoc`:

```bash
python3 scripts/host_check.py --list
```

Zatim:

```bash
python3 scripts/host_check.py --vault "VAULT NAME"
```

## Fajlovi za 01E

- `canon/AOC-OBSIDIAN-HOST-CHECK-01E.md` — šta proveravamo
- `scripts/host_check.py` — prava host provera preko Obsidian CLI-ja
- `tests/test_host_check.py` — testovi skripte
- `evidence/AOC-OBSIDIAN-HOST-CHECK-01E-PENDING.md` — status dok ne pokrenemo proveru na pravom računaru

## PASS uslov za 01E

Mora da pokaže:

- Obsidian verziju
- pravi vault
- trenutni projekat i repo
- tačno 3 sledeća koraka
- izvore korišćenih beleški
- `authority_state = HUMAN_REQUIRED`
- `execution_allowed = false`

Tek tada 01E zaključavamo kao PASS.
