#   Semestrální práce Předmětu NI-EVY, semestr B251 - suffixové automaty pro řešení LCF

Cílem semestrální práce je implementovat a použít suffixový automaton a k němu požadované metody. Implementace, pokud nemáte povoleno jinak, bude napsaná v jazyku C++, vyjímečně pak v jazyku Python. Ve složkách cpp a python jsou připravená rozhraní pro oba jazyky. Semestrální práce může být ohodnocena celkem až 20 body. 20 bodů ze semestrální práce není dostačující podmínka pro udělení zápočtu - student musí úspěšně napsat zápočtový test na požadovaný minimální počet 10ti bodů.


##  Zadání

**Suffixový automat** je deterministický konečný automat $M = (Q,\Sigma,\delta,q_0,F)$, kde
-   $Q$ je neprázdná množina stavů automatu
-   $\Sigma$ je neprázdná množina vstupních symbolů (abeceda)
-   $\delta$ je přechodová funkce $Q \times \Sigma \rightarrow Q$
-   $q_0$ je počáteční stav automatu
-   $F$ je množina koncových stavů 

a platí, že pro text T, $L(M_T) = \{T[i\ldots|T|-1] | 0\leq i \leq |T|-1\}$

1.  Vytvořte datovou strukturu suffixového automatu $M_T$ pro text $T$, která bude mít implementované následující metody.

|Název metody           |Popis     |
|------------           |-----     |
|$n\_states()$          | Vrátí $ |Q| $ |
|$n\_transitions()$     | Vrátí $ |\delta| $ |
|$build(T)$     | Vytvoří datovou strukturu nad textem $T$ |
|$count(P)$       | Vrátí počet výskytů vzorku P v textu $T$| 
|$match\_all(P)$       | Vrátí všechny pozice $i$ v textu $T$, kde $T[i\ldots i+\|P\|-1]=P$ | 
|$match\_first(P)$       | Vrátí první pozici $i$ v textu $T$, kde $T[i\ldots i+\|P\|-1]=P$, -1 pokud pozici nenalezne | 
|$match\_last(P)$       | Vrátí poslední pozici $i$ v textu $T$, kde $T[i\ldots i+\|P\|-1]=P$, -1 pokud pozici nenalezne | 


Dále každý stav automatu $p$ má uloženou hodnotu **suffix_link** $sl(p)$ 

| | |
|-           |-     |
|$label(q)$ | je nejdelší slovo w takové, že $(q_0,w)\vdash^*(q,\varepsilon)$  -> není třeba implementovat
|$suffix\_link(p)$         | $q$ takove, ze $label(p) =u, label(q) = v$ a $v$ je nejdelší vlastní suffix $u$
|           |     |


**!!Pokud nebude splněna 1. část zadání, nelze hodnotit ani následující části zadání (tudíž není možné použít implementaci suffixového automatu z externích balíčků)!!**

2.  Použijte Váš suffixový automat pro následující problém:

    Jsou dána dvě slova $x$ a $y$ nad stejnou abecedou $\Sigma$ a platí, že $|x| \leq |y|$.
    Nechť $LCF(x,y)$ značí nejdelší podřetězce, které se vyskytují jak ve slově $x$, tak i ve slově $y$.
    Navrhněte a implementujte algoritmus pro $LCF(x,y)$, s použitím suffixového automatu M pouze pro slovo $x$.
    Výsledek vraťte jako dvojici $(I,l)$, kde $I$ je množina pozic v textu $x$ a $l$ je délka. Analyzujte časovou a paměťovou složitost Vašeho algoritmu.

3.  Nechte proběhnout experimenty

    Pro každý dataset vytvořte suffixový automat, změřte dobu jeho konstrukce a velikost automatu danou $|Q|$ a $|\delta|$. Dále pro sadu vzorků každého datasetu změřte dobu vyhledávání a normalizujte přes počet výskytů. Výsledky zaneste do grafu a porovnejte s naivním pattern matchingem bez jakéhokoliv předzpracování (změřené hodnoty implementace v *C++* v *datasets/<dataset_name>/naive.csv*)

    Můžete udělat i další experimenty dle Vašeho uvážení.

4.  Vyplňte report o Vaší semestrální práci

    V souboru README.md vyplňte a sepište všechny vaše kroky v implementaci a návrhu algoritmu.
    Report můžete psát v českém, slovenském či anglickém jazyce. Implementace a grafy ponechejte v jazyce anglickém. 

5.  Odevzdejte ve svém repozitáři na GitLabu, vytvořte issue a přiřaďte jej svému opravujícímu (J. Holub)

    Jak na to? Ve svém pushnutém repozitáři v gitlabu v levém panelu klikněte na *issues*. Zde založte *new issue* a v položce *Assignees* vyberte Jan Holub. Případně okomentujte a *create issue*.


**!!Semestrální práci odevzdávejde do 14.12.2025 23:59:59. Za pozdní odevzdání bude udělena penalizace (více v sekci hodnocení)!!**

##  Hodnocení projektu

Hodnocení projektu probíhá ve 4 fázích.
1.   Implementace prochází automatizovanými testy, které jsou Vám dostupné ve složce $test$. 
Pro spuštění testů: 

-    **Python testy**

       Pro python jsou testy pro pytest. Pokud nemáte, nainstalujte:

        ```shell
        pip install pytest
        ```
        
        Všechny testy lze bez předchozího nastavení spustit najednou pomocí ze složky python

        ``` shell
        PYTHONPATH=. pytest
        ```

        Nebo jednotlivě

        ``` shell
        PYTHONPATH=. pytest text/<test_name>
        ```

-    **Cpp testy**
    
        Prostředí ukliďte a zkompilujte
        ``` shell
        make clean && make
        ```

        Testy spusťte pomocí

        ```shell
        make test
        ```

        Testy kontrolují výstupní hodnoty funkcí ze zadání v částech 1. a 2. 
   
Tato část je hodnocena 8 body.

-------------------------------
2.  Spusťte experimenty a výsledná data zpracujte do grafů.

    Tato část je hodnocena 6 body.

3.  Vyhodnocení výsledků a popis implementace v reportu práce.

    Tato část je hodnocena až 6ti body.

4.  V případě dotazů hodnotícího, může dojít k ústní formě obhajoby semestrální práce.


**Penalizace**
1.  Vzhled implementačního kódu
Je důležité aby Váš kód byl dobře čitelný a okomentovaný. Pokud tak nebude, hodnotící si nárokuje snížení celkového počtu bodů o až 3 body.
2.  Pozdní odevzdání
Pokud dojde bez předchozí omluvy k pozdnímu odevzdání práce, může být celkový počet bodů snížen až do 2 body s každým začínajícím týdnem zpoždění.

##  Závěrečné připomínky
Ano, AI je dnes dostatečně mocné, aby všechny úkoly zvládnulo samo a internet je plný již hotových a vysvětlených implementací. Cílem semestrální práce je, abyste si datovou strukturu vyzkoušeli za sebe. Proto očekáváme, že nebudete AI ani implementace z internetu nadmíru používat a zneužívat. 

V případě, že naleznete nějakou chybu, o které si myslíte, že by měli vědět všichni, pište do společné e-mailové konverzace (bude vytvořena nejpozději s automatizovaným vytvářením repozitářů).

Přeji hodně zdaru