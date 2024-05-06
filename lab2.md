# Ćwiczenie 1
## Zad 1.1
a - rodzenstwo
b - kuzynostwo
c - rodzic rodzicow
d - przybrany syn
e - przybrane rodzenstwo
f - x jest szwagrem y

# Ćwiczenie 2
:- discontiguous rodzic/2.
% rodzic(rodzic, potomek).
mezczyzna(jan).
mezczyzna(marek).
mezczyzna(henryk).
rodzic(henryk, jan).
rodzic(jan, helena).
rodzic(ewa, helena).
rodzic(jan, marek).
rodzic(ewa, marek).

rodzic(marek, ala).
rodzic(helena, ola).

kobieta(X) :- \+mezczyzna(X).
% ojciec(X,Y) – X jest ojcem Y
ojciec(X, Y) :- rodzic(X, Y), mezczyzna(X).
matka(X,Y) :- rodzic(X,Y), kobieta(X).
corka(X,Y) :- rodzic(Y,X), kobieta(X).

rodzenstwo(X, Y) :- rodzic(Z, X), rodzic(Z, Y), X \= Y. 

% brat_rodzony(X,Y) – X jest rodzonym bratem Y
brat_rodzony(X,Y) :- rodzenstwo(X, Y), mezczyzna(X), X \= Y.

% brat_przyrodni(X,Y) – X jest przyrodnim bratem Y
brat_przyrodni(X,Y) :- rodzic(Z,X), rodzic(Z, Y), mezczyzna(X), X \= Y.

kuzyn(X, Y) :- rodzic(A, X), rodzic(B, Y), rodzenstwo(A, B).

% dziadek_od_strony_ojca(X,Y) – X jest dziadkiem od strony ojca dla Y
dziadek_od_strony_ojca(X,Y) :- ojciec(Z, Y), ojciec(X, Z).

% dziadek_od_strony_matki(X,Y) – X jest dziadkiem od strony matki dla Y
dziadek_od_strony_matki(X,Y) :- matka(Z, Y), ojciec(X, Z).

% dziadek(X,Y) – X jest dziadkiem Y
dziadek(X,Y) :- rodzic(Z, Y), ojciec(X, Z).

% babcia(X,Y) – X jest babcią Y
babcia(X,Y) :- rodzic(Z, Y), matka(X, Z).

% wnuczka(X,Y) – Y jest wnuczką X
wnuczka(X,Y) :- babcia(X, Y), kobieta(Y).

% przodek_do2pokolenia_wstecz(X,Y) – X jest przodkiem Y do drugiego pokolenia wstecz
przodek_do2pokolenia_wstecz(X, Y) :- babcia(X,Y); dziadek(X, Y).

% przodek_do3pokolenia_wstecz(X,Y) - X jest przodkiem Y do trzeciego pokolenia wstecz
przodek_do3pokolenia_wstecz(X,Y) :- przodek_do2pokolenia_wstecz(Z, Y), rodzic(X, Z).
