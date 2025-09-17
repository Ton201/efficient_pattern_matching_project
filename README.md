#   Semestrální práce Předmětu NI-EVY, semestr B251 - Compact Suffix Trie

Cílem semestrální práce je implementovat a použít suffixovou trii tak, jak je definovaná v přednáškách. Implementace, pokud nemáte povoleno jinak, bude napsaná v jazyku C++, vyjímečně pak v jazyku Python. Ve složkách cpp a python jsou připravená rozhraní pro oba jazyky. Semestrální práce může být ohodnocena celkem až 20 body. 20 bodů ze semestrální práce není dostačující podmínka pro udělení zápočtu - student musí úspěšně napsat zápočtový test na požadovaný minimální počet 10ti bodů.


##  Zadání

1.  Vytvořte datovou strukturu kompaktní suffixové trie, která bude mít následující metody.

build   -   vytvorit z textu T datovou strukturu, pridat SL a WL a udelat ji kompaktni???
match_all
match_first
match_last
compact


Statisticke funkce
#nodes


**Není povoleno používat externí balíčky, které mají stejné nebo podobné datové struktury již implementované.**

2.  Použijte Vaši datovou strukturu pro vyhledávání v textu.


3.  Vyplňte report o Vaší semestrální práci
V souboru REPORT.md vyplňte a sepište všechny vaše myšlenky k semestální práci.
Report můžete sepsat i v českém či slovenském jazyce. Implementace a grafy jsou ale v jazyce anglickém. 


4.  Odevzdejte ve svém repozitáři na GitLabu, vytvořte issue a přiřaďte jej svému opravujícímu (J. Holub)
Jak na to?


Semestrální práci odevzdávejde do 14.12.2025 23:59:59. Za pozdní odevzdání bude udělena penalizace (více v sekci hodnocení)

##  Opakování definic
# Suffix Tries, Suffix Links, and Weiner Links

### Suffix trie

A **suffix trie** for a string $T$ is a rooted trie that stores **all suffixes** of $T$ as root-to-leaf paths (often using a unique endmarker like “$$ \$ $$” so every suffix is unique).

**Properties**

* Each edge is labeled by a **single character**.
* The string spelled from the root to a node $v$ is the node’s **path-label**.
* A pattern $P$ occurs in $T$ **iff** there is a path from the root whose label is $P$. All occurrences correspond to starting indices found under that node’s subtree.
* Worst-case space is $O(n^2)$ (many explicit nodes), which is why compressed variants (suffix **trees**) are preferred for large inputs.

**Example** for $T=$ `banana$`: the trie contains paths for

```
banana$, anana$, nana$, ana$, na$, a$, $
```

---

### Suffix links

A **suffix link** “drops the first character.”

**Definition**
For a node $v$ whose path-label is $S = a\alpha$ (with $a$ a single character), the suffix link of $v$ points to the node whose path-label is $\alpha = S[1:]$. The root’s suffix link points to itself.

**Intuition / uses**

* Jump from $S$ to its proper suffix $\alpha$ in $O(1)$, aiding linear-time construction and fast backtracking.
* In a compressed suffix **tree**, suffix links are defined for internal nodes; in an explicit suffix **trie**, you can define them for all nodes.
* Aho–Corasick’s “failure” links are suffix links on a pattern trie.

---

### Weiner links (left-extension links)

A **Weiner link** (also called a *reverse suffix link*) “prepends one character.”

**Definition**
For a node $v$ with path-label $\alpha$ and a character $a$, if the string $a\alpha$ occurs in $T$, there is a Weiner link from $v$ labeled $a$ to the node whose path-label is $a\alpha$.

**Key facts**

* Weiner links are the **left-extension counterpart** of suffix links (suffix links remove the first character; Weiner links add one on the left).
* In a suffix tree, they are central to **Weiner’s right-to-left linear-time construction**: process $T$ from right to left, follow suffix links, and realize new left extensions via Weiner links.
* Equivalently: there is a Weiner link $v \xrightarrow{a} w$ **iff** the suffix link of $w$ points to $v$.

**Small example** on `banana$`:

* Node `ana` has a Weiner link labeled `b` to `bana` (since `bana` occurs), and one labeled `n` to `nana`.
* Correspondingly, the suffix link of `bana` (drop `b`) goes to `ana`, and the suffix link of `nana` (drop `n`) also goes to `ana`.


##  Očekávaná paměťová a časová složitost

Dle přednášek je ...

##  Hodnocení projektu

Hodnocení projektu probíhá ve 3 fázích.
1.   Implementace prochází automatizovanými testy, které jsou Vám dostupné ve složkách test. Pro spuštění testů 
```
spuste takto pro python
```

```
spuste takto pro cpp
```

    V teto casti muzete ziskat az ... bodu

2.  Použití datové struktury pro získání odpovědí na 2. část zadání
Výstupem se myslí grafy na daných datasetech, které budou viditelné v reportu

Pro spuštění automatizovaného vyhodnocení výsledků do grafů spuste skript
```
takto
``` 

Tato část je hodnocena ... body

3.  Vyhodnocení výsledků a popis implementace v reportu práce.

Tato část je hodnocena až 6ti body.

Penalizace
1.  Vzhled implementačního kódu
Je důležité aby Váš kód byl dobře čitelný a okomentovaný. Pokud tak nebude, hodnotící si nárokuje snížení celkového počtu bodů o až 3 body.
2.  Pozdní odevzdání
Pokud dojde před předchozí omluvy k pozdnímu odevzdání práce, může být celkový počet bodů snížen až do 2 body s každým začínajícím týdnem zpoždění.