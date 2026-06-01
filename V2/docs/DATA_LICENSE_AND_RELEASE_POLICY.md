# Data License and Release Policy

## 1. Material levels

V2 uses layered licensing and release rules. Do not apply one license to all materials.

### Level 0: code and project documentation

Examples:

- scripts;
- schemas;
- project documentation;
- workflow documentation;
- templates.

Recommended license: repository code/documentation license.

### Level 1: project-created metadata

Examples:

- document metadata;
- term lists;
- review logs;
- QC reports;
- release manifests.

Recommended license: CC BY 4.0 or CC BY-NC 4.0, unless another source license applies.

### Level 2: raw texts and OCR outputs

Examples:

- raw OCR;
- WS text files;
- transcribed source texts;
- source-derived text files.

Policy:

- record source for each item;
- do not assume public redistribution rights;
- do not overwrite raw files;
- check source, edition, scan provider, and database terms before public release;
- public-domain source texts still need digital-source attribution.

### Level 3: generated candidate outputs

Examples:

- full segments generated from raw source;
- KWIC files;
- candidate evidence tables;
- candidate claim tables;
- case build reports.

Policy:

- mark as generated or candidate;
- keep reproducible scripts and parameters;
- do not cite as reviewed scholarship;
- promote rows to curated case files only after human review.

### Level 4: curated scholarly outputs

Examples:

- reviewed evidence tables;
- reviewed claims;
- interpretive notes;
- digital essays;
- article drafts.

Policy:

- author retains scholarly responsibility;
- cite source files, document ids, segment ids, and evidence quotes;
- public release may use CC BY-NC-ND 4.0 or another author-selected license.

### Level 5: external authority data

Examples:

- CBDB crosswalks;
- CHCD links;
- BDCC links;
- Ricci-related authority links;
- other external identifiers.

Policy:

- publish only minimal crosswalks when allowed;
- do not republish third-party database records;
- keep original source and license notes;
- store uncertain or restricted authority notes internally.

## 2. Prohibited actions

- Do not mark all data as MIT.
- Do not overwrite raw sources.
- Do not publish generated candidate claims as final conclusions.
- Do not remove source notes.
- Do not bundle third-party database records without checking rights.

## 3. Recommended release types

```text
code-release
metadata-release
generated-candidate-release
curated-case-release
research-report-release
```

Each release should state scope, source basis, review status, and license notes.

## 4. Citation fields

Every release should include:

- version;
- release date;
- commit hash;
- data scope;
- source list;
- license note;
- citation suggestion.

Every case-level claim should preserve:

- document id;
- segment id;
- source file;
- evidence quote;
- review status;
- reviewer when available;
- review date when available.
