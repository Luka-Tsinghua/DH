# Scholarly Interface Design

## Interface as Argument

The V2 website should not be a simple display layer. Each page should work as a scholarly argument.

Recommended page structure:

1. Research Question
2. Corpus Scope
3. Evidence
4. Method
5. Interpretation
6. Uncertainty
7. Reuse

## Core Components

### EvidenceCard

Shows:

- document title;
- segment id;
- evidence quote;
- cleaning version;
- verification status.

### ClaimCard

Shows:

- claim text;
- subject / predicate / object;
- evidence quote;
- confidence;
- human verification status.

### KWICTable

Shows:

- term;
- left context;
- right context;
- document;
- segment id.

### AuthorityBadge

Shows:

- CBDB;
- CHCD;
- BDCC;
- match status;
- confidence.

### MethodNote

Shows:

- data source;
- extraction rule;
- limitation;
- reproducible command.

## Transparency Requirements

The web interface should make the following visible:

- OCR uncertainty;
- unmatched authority candidates;
- low-confidence LLM candidates;
- contested cleaning rules;
- missing source information;
- license limits.

This improves project credibility and makes the site useful for later researchers.
