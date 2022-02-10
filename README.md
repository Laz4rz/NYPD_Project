# README
### JST Analysis
Biblioteka została stworzona w celu analizowania i czyszczenia danych pochodzących z arkuszów populacji oraz dochodów Jednostek Samorządu Terytorialnego udostępnianych na stronach rządowych. 

Dochody:
https://www.gov.pl/web/finanse/udzialy-za-2020-r
Populacja:
https://stat.gov.pl/obszary-tematyczne/ludnosc/ludnosc/ludnosc-stan-i-struktura-ludnosci-oraz-ruch-naturalny-w-przekroju-terytorialnym-stan-w-dniu-31-12-2020,6,29.html

#### Instalowanie biblioteki
Bibliotekę można zainstalować pobierając plik .whl z repozytorium oraz wywołując ```pip package_path```. 
```
!pip install JST_analysis-0.0.3-py3-none-any.whl
```

#### Importowanie i ścieżki
```
from JST_analysis import (
    load_income_excel,
    save_to_excel,
    compare_incomes,
    load_population_excel,
    population_income_merge,
    calculate_JST,
    calculate_tax_mean,
    calculate_estimates,
)

import pandas as pd # by wyswietlac dobrze dfy
pd.set_option('expand_frame_repr', False)
```

#### Porównanie dochodów JST
Porówanie dochodów można uzyskać poprzez wczytanie plików zawierających dochód przy wykorzystaniu funkcji ```load_income(file_path, only_important=False)```, gdzie polecam wybranie ```only_important=True```, co spowoduje ładniejsze przedstawienie danych.

```
gminy_income_2019 = load_income_excel(file_path=gminy_2019, only_important=True)
powiaty_income_2019 = load_income_excel(file_path=powiaty_2019, only_important=True)
NPP_income_2019 = load_income_excel(file_path=NPP_2019, only_important=True)
wojewodztwa_income_2019 = load_income_excel(file_path=wojewodztwa_2019, only_important=True)

gminy_income_2020 = load_income_excel(file_path=gminy_2020, only_important=True)
powiaty_income_2020 = load_income_excel(file_path=powiaty_2020, only_important=True)
NPP_income_2020 = load_income_excel(file_path=NPP_2020, only_important=True)
wojewodztwa_income_2020 = load_income_excel(file_path=wojewodztwa_2020, only_important=True)
```

Ważnym elementem dataframe'ów tworzonych z wykorzystaniem funkcji pochodzących z biblioteki ```JST_analysis``` jest posiadanie atrybutów pozwalających innym funkcjom rozpoznać typ dataframe'a i zastosować do niego dodatkowe funkcje, jak na przykład zapisanie w formie pliku Excel raportu z integralnością danych, który tworzony jest w atrybucie ```df.attrs["integrity_report"]``` .

Porównanie dochodów realizowanie jest poprzez funkcję ```compare_income(df1, df2)```, gdzie podanie dataframe'ów o tym samym ```.attrs["JST_type"``` spowoduje stworzenie nowego dataframe'a rozszerzonego o kolumny statystyk porówaniania.

```
gminy_income_compare_2019_2020 = compare_incomes(df1=gminy_income_2019, df2=gminy_income_2020)
```

Wywołanie funkcji ```save_to_excel(df, file_path)``` na dowolnym dataframe'ie spowoduje zapisanie go do pliku z określonym rozszerzeniem (WAŻNE: należy podać ścieżkę z rozszerzeniem), w przypadku gdy dataframe posiada atrybut z raportem integralności, będzie on również zapisany w formie osobnego pliku.

```
save_to_excel(df=NPP_income_compare_2019_2020, file_path=r"data/reports/powiaty_income_comparison_2019_2020.xlsx")
```

#### Łączenie danych dochodów i populacji
Operacje na danych zawierających ludność oraz dochód rozpoczynamy od wykorzystania funkcji ```load_population_excel(file_path)```, która utworzy dataframe z rozbiciem populacji na gminy należące do powiatów, należących do województw.

```
population = load_population_excel(file_path=populacja_2020)
```

Następnie należy połączyć go z plikiem dochodów (WAŻNE: ```.attrs["JST_type"]``` musi być "Gminy", by uniknąć problemów z łączeniem), niezależnie od poziomu JST, który chcemy analizować później - jest to podstawa.  

```
income_population = population_income_merge(gmina_income_df=gminy_income_2020, populations_df=population)
```

#### Średni dochód opodatkowany
W celu obliczenia średniego dochodu opodatkowanego dla gmin, należy wywołać funkcję ```calculate_tax_mean(df)```, która spowoduje rozszerzenie obecnego dataframe'a o kolumnę ze średnim dochodem.

```
income_population_mean = calculate_tax_mean(df=income_population)
```

#### Średnia i wariancja
Otrzymujemy ją poprzez wywołanie funkcji ```calculate_JST(df, JST_type)```, gdzie dataframe bazowy dla operacji na ludności/dochodzie, czyli podobnie jak wcześniej - ten utworzony z ```population_income_merge(gmina_income_df, population_df)```.

```
powiat_statistics = calculate_JST(df=income_population, JST_type="powiat")
save_to_excel(df=powiat_statistics, file_path=r"data/reports/wojewodztwo_statistics.xlsx")
```

#### Estymaty
Estymaty otrzymujemy przez podanie dataframe bazowy dla operacji dochód/populacja, dochodów oraz wybranie poziomu JST dla, którego chcemy je uzyskać.

```
powiat_estimates = calculate_estimates(df_income_population=income_population, df_income=powiaty_income_2020, JST_level="powiat")

save_to_excel(df=powiat_estimates, file_path=r"data/reports/powiat_estimates.xlsx")
```

#### Testowanie
Wszystkie testy można włączyć jednocześnie wywołując z poziomu repozytorium ```python -m unittest```. Poziom wywołania unittest jest ważny z uwagi na możliwy konflikt ścieżek.

#### Profilowanie
Uzyskano przez wywołanie funkcji:
```
python -m cProfile -s tottime tests/main_routine.py > ./examples/profiler.txt
```

Po analizie wyników profilowania można zauważyć, że zdecydowana większość czasu została stracona przez funkcje wczytujące pliki Excelowe z biblioteki pandas. Rozwiązaniem byłoby znalezienie biblioteki specjalizującej się w efektywnym czasowo wczytywaniu i potencjalnie przechowywania lub początkowe przetwarzanie danych w innym formacie plików. W przypadku częstego wykorzystywania biblioteki na tych samych danych można pokusić się o skorzystanie z biblioteki pickle, co powinno znacząco skrócić czas ponownego ładowania arkuszów. 

