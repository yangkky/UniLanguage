# What is UniLanguage?
[PAPER](bioxiv), [CITATION](bioxiv)
UniLanguage is a dataset of proteins that has been scraped from UniProt (2019-10-01) for the purpose of language modeling.
Language modeling is the task of generating the next token in a sentence given the past tokens.
Language models have proven important for learning context and has pushed state-of-the-art in natural language processing, which is why we are now developing language modeling datasets to investigate this technology within the protein domain.
Proteins have a high similarity to text: discrete symbols (amino acids), dictionary of up to 25 symbols (similar to characters), average length of 335 (like a paragraph), and access to large databases of unlabelled sequences in UniProt (akin English Wikipedia).
Moreover, proteins have many supervised prediction tasks with limited data available.
However, many priors within language cannot be assume for protein sequence.
E.g. many proteins are more than 90% identical; ruining the i.i.d. assumption of SGD and train-/val-/test set splits, different domains of life (zebrafish vs. ebola virus) might not have much in common; corresponding to mixing chinese with english, 99% of UniProt has not been experimentally validated, and many proteins are represented only as fragments; often noncontigous.
We provide a language modeling dataset that takes all these concerns into account.

# What is a Protein? (explanation for the ML researcher)
Your body consist of many cells with different functions.
A cell contains DNA, DNA is a cook book for all the functions your cell can express.
When you cell wants to express a function it copies subsection of the the DNA (a genome) and turns it into RNA, being the specific function recipe from your DNA cook book.
The RNA, using its function recipe, then builds the protein. The protein consists of amino acids.
Cells can contain thoudsands of proteins, below you can see the Ebola virus ([taken from PDB](https://pdb101.rcsb.org/motm/178)), notice that it has many copies of the same protein. E.g. the broccoli shaped surface of Glycoprotein.

# Process of creating dataset
We scrape all of UniProt, 250M proteins as of 2019-10-01.
The proteins with experimental evidence (high quality, 1% of UniProt) are homology partitioned, with 20% homology, into train-, validation-, and test set with 60% train, 10% validation and 30% test for each domain on both full proteins and fragments.

Predicted proteins (low quality, 99% of UniProt) are homology compared against the validation and testset with 20% homology, if they do not overlap they are kept as a predicted training set.
This removes about 50% of the predicted proteins (about 100 million!), which truly indicates the amount of overlap in proteins.

# The task
Build a language model that can predict the next amino acid in a protein sequence.
Resources on building a language model: [Karpathy blogpost](http://karpathy.github.io/2015/05/21/rnn-effectiveness/), [Jurafsky & Martin](https://web.stanford.edu/~jurafsky/slp3/), [AWD-LSTM](https://github.com/salesforce/awd-lstm-lm), [fairseq](https://github.com/pytorch/fairseq/tree/master/examples/language_model)
Train it on a training set, e.g. high quality eukarya, and test it on the testset.
See if you can beat our performance.
If you can, please submit a technical report, e.g. to arxiv, and send it to us.
This way we can keep track of current state-of-the-art on this language modeling dataset.

# Description of properties - Amino acids, Homology, Domain, Fragments, Quality, Uniprot

## Amino acids (ML explanation)
Amino acids are ... and contains 25 different symbols. They always start with M and We add SoP to the end of proteins. 

[A: ... M: Myio...]

## Homology

## Domain

## Fragments
Show an example

## Quality

## Uniprot

# Overview of datasets and results
Our task contains multiple datasets for training and testing. We provide the simple version (only Eukarya) and the full version (all datasets, including fragments).
Notice that the full dataset also contains fragments for validation and testing. This is a result of our homology partitioning, we provide them, but do not use them in our own results.

## Simple (ML reseachers)
For simplicity we of having one validation and testset, we provide links here to the Eukarya validation, test, high quality train, and low quality train.

| Link     | Partitions | Domain   | Quality | Samples | Mean Length | Fragments |
|----------|------------|----------|---------|---------|-------------|-----------|
| Download | Train      | Eukarya  | High    |         |             | No        |
| Download | Train      | Eukarya  | Low     |         |             | No        |
| Download | Valid      | Eukarya  | High    |         |             | No        |
| Download | Test       | Eukarya  | High    |         |             | No        |

## Simple results
| Training set | Validation perplexity | Test perplexity |
|--------------|-----------------------|-----------------|
| High quality |                       |                 |
| Low quality  |                       |                 |
| Combined     |                       |                 |

## All datasets
| Link     | Partitions | Domain   | Quality | Samples | Mean Length | Fragments |
|----------|------------|----------|---------|---------|-------------|-----------|
| Download | Train      | Eukarya  | High    |         |             | No        |
| Download | Train      | Eukarya  | High    |         |             | Yes       |
| Download | Train      | Eukarya  | Low     |         |             | No        |
| Download | Train      | Eukarya  | Low     |         |             | Yes       |
| Download | Valid      | Eukarya  | High    |         |             | No        |
| Download | Valid      | Eukarya  | High    |         |             | Yes       |
| Download | Test       | Eukarya  | High    |         |             | No        |
| Download | Test       | Eukarya  | High    |         |             | Yes       |
| Download | Train      | Bacteria | High    |         |             | No        |
| Download | Train      | Bacteria | High    |         |             | Yes       |
| Download | Train      | Bacteria | Low     |         |             | No        |
| Download | Train      | Bacteria | Low     |         |             | Yes       |
| Download | Valid      | Bacteria | High    |         |             | No        |
| Download | Test       | Bacteria | High    |         |             | No        |
| Download | Train      | Archaea  | High    |         |             | No        |
| Download | Train      | Archaea  | High    |         |             | Yes       |
| Download | Train      | Archaea  | Low     |         |             | No        |
| Download | Train      | Archaea  | Low     |         |             | Yes       |
| Download | Valid      | Archaea  | High    |         |             | No        |
| Download | Test       | Archaea  | High    |         |             | No        |
| Download | Train      | Virus    | High    |         |             | No        |
| Download | Train      | Virus    | High    |         |             | Yes       |
| Download | Train      | Virus    | Low     |         |             | No        |
| Download | Train      | Virus    | Low     |         |             | Yes       |
| Download | Valid      | Virus    | High    |         |             | No        |
| Download | Test       | Virus    | High    |         |             | No        |

## Results all data
| Domain   | Training set          | Validation perplexity | Test perplexity |
|----------|-----------------------|-----------------------|-----------------|
| Eukarya  | Euk_exp, Euk_pred     |                       | 14.28           |
| Bacteria | Bact_exp, Bact_pred   |                       | 9.93            |
| Archaea  | Arch_exp, Arch_pred   |                       | 15.92           |
| Virus    | Virus_exp, Virus_pred |                       | 17.17           |
| Mean     |                       |                       | 14.32           |
Please see the result section of our [paper]() for extended results

# Citation
[PAPER](bioxiv)
PUT IN CITATION
