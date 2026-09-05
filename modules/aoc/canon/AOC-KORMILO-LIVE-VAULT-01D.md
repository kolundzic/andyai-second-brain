# AOC–KORMILO–LIVE–VAULT–01D

## Šta proveravamo

Da li AOC može da pročita mali Obsidian vault i napravi jednostavan KORMILO pregled bez menjanja ijedne beleške.

## Šta smo napravili

U proof vaultu postoje četiri važeće beleške:

- `PROJECT.md` — koji je projekat i repo
- `STATUS.md` — gde smo stali i poslednji kanon
- `OPEN.md` — šta je otvoreno i koja su sledeća tri koraka
- `DECISIONS.md` — šta čeka Andyjevu odluku

Dodali smo i `STALE_NOTE.md`, staru belešku sa namerno lošom instrukcijom. Ona ne sme da utiče na rezultat.

## Pravila

1. AOC čita samo unapred dozvoljene beleške.
2. Stare beleške se ne koriste kao trenutno stanje.
3. Tekst iz beleške nikada ne postaje dozvola za izvršavanje komandi.
4. `authority_state` uvek ostaje `HUMAN_REQUIRED`.
5. `execution_allowed` ostaje `false`.
6. Uz svaku grupu pročitanih podataka čuvamo izvor i SHA-256 otisak fajla.

## Rezultat

`6/6` testova je prošlo.

KORMILO je tačno sastavio:

- trenutni projekat
- trenutni repo
- gde smo stali
- poslednji kanon
- otvorene teme
- povezane projekte
- sledeća 3 koraka
- odluke koje čekaju Andyja
- izvore

Namerno stara/opasna beleška nije ušla u rezultat.

## Status

**PASS — vault reconstruction proof**

Važno: ovo je pravi Obsidian-kompatibilan vault folder i pravi parser/test. U ovom okruženju nemamo pristup Obsidian aplikaciji koja radi na Andyjevom Mac/HP računaru, pa je sledeći korak kratka host provera: isti kod protiv lokalnog vaulta preko već napravljenog read-only adaptera.

## Sledeće

`AOC–OBSIDIAN–HOST–CHECK–01E`

Cilj: na MacBook-u ili HP/Omarchy računaru pustiti istu read-only putanju protiv stvarnog lokalnog Obsidian vaulta i uporediti rezultat sa očekivanim KORMILO pregledom.
