# Executable Examples

Small q snippets that should run as-is in a scratch KDB-X/q process. Prefer adapting these before inventing syntax.

## Lists and Rank

```q
xs:10 20 30 40
xs where xs>20
count enlist 42
nested:(1 2 3;10 20 30)
nested[1;2]
```

## Dictionaries and Keyed Lookup

```q
d:`IBM`MSFT!101 250f
d`IBM
key d

quotes:([sym:`IBM`MSFT] bid:100.9 249.8; ask:101.1 250.2)
quotes `IBM
quotes ([] sym:`IBM`MSFT)
```

## Tables and q-sql

```q
trades:([] time:09:30 09:31 09:32; sym:`IBM`IBM`MSFT; px:101 102 250f; size:100 50 200)
meta trades
select vwap:size wavg px, volume:sum size by sym from trades where size>50
update notional:px*size from trades
```

## Functional q-sql

```q
trades:([] sym:`IBM`MSFT`IBM; px:101 250 103f; size:100 200 50)
?[trades;enlist (>;`size;50);0b;`sym`px!`sym`px]
?[trades;();enlist[`sym]!enlist `sym;enlist[`vwap]!enlist (wavg;`size;`px)]
```

## Joins

```q
trades:([] sym:`IBM`MSFT`IBM; px:101 250 103f; size:100 200 50)
inst:([] sym:`IBM`MSFT; sector:`tech`software)
trades lj `sym xkey inst
ej[`sym;trades;inst]
```

## Time-Series Join

```q
quotes:([] time:09:30:00.000 09:30:01.000 09:30:02.000; sym:`IBM`IBM`IBM; bid:100 101 102f; ask:101 102 103f)
trades:([] time:09:30:01.500 09:30:02.500; sym:`IBM`IBM; px:101.2 102.4)
aj[`sym`time;trades;quotes]
```

## CSV I/O

```q
p:`$":/tmp/prices.csv"
p 0:("sym,px";"IBM,101.5";"MSFT,250.25");
prices:("SF";enlist ",") 0:p
prices
```
