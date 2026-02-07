Sta je uradjeno:

Dodate su funkcionalnosti za:

* Proveru pobede - check\_victory. Ona prolazi kroz sve parove pronadjenih ostrva, trazi najkraci put izmedju 2 ostrva iste boje, ako korisnik koji spoji 2 ostrva putanjom cija je duzina veca ili jednaka minimalnom trazenom putu za pobedu, npr za N=5 je 7, za N=7 je 10, za N=9 je 13.
* Vracanje ostrva - get\_island\_groups. Vraca sve grupe ostrva iste boje tako sto vraca grupe koje dodiruju ivicu table proveravajuci da li q, r ili q+r dostizu obod table.
* Funkcije za vracanje susednih polja get\_neighbours(pozicija) koja vraca 6 susednih polja za datu poziciju
* get\_shortest\_path\_length koja koristi BFS da bi vratila najkracu distance izmedju startnog cvora jednog ostrva I bilo kog cvora ciljnog ostrva, kretajuci se o figurama iste boje.

* Dodate su neke pripreme za sledeci korak, poput:

1. apply\_move koja kreira kopoiju table I simulira potez
2. get\_next\_states koja generise sva moguca buduca stanja tabele na osnovu trenutnih validnih poteza
3. get\_all\_valid\_moves vraca istu svih praznih polja, odnosno gde nije igrano.


---

## Treca faza

1. Razdvojeni fajlovi, sada svako ima svoju duznost
2. Dodat minmax sa alfabeta odsecanjem
