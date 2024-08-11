# pubmedy-buddy

Easily access article metadata from Pubmed.

## Arguments

|argument|shorthand|description|
|:------:|:-------:|:----------|
|`--pmid`|`-i`|a valid journal PMID|
|`--file`|`-f`|a filepath containing newline-delimited PMIDs|
|`--abstract`|`-a`|display abstract|

## Usage

Retrieve metadata from a single article:
```bash
pmb --pmid 38697854
```

Retrieve metadata from multiple articles:
```bash
pmb --pmid 39096902,39096926,39106863,39107255
```

Retrieve journal metadata from a file containing a list of PMIDs:
```bash
pmb --file /path/to/pmids
```

Only display the abstract

```bash
pmb --pmid 38697854 --abstract
pmb --pmid 39096902,39096926 --abstract
pmb --file /path/to/pmids --abstract
```
