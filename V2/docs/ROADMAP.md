# V2 Roadmap

## 0. Current state

V2 has moved beyond a workshop display. It now registers real root-level WS texts as raw sources, provides a reproducible processing pipeline, includes a case builder, separates generated candidates from curated scholarly files, and has GitHub Actions checks installed.

Current real raw sources:

```text
1674_坤輿圖說_WS.txt
1799_地球圖説_WS.txt
```

## 1. Completed infrastructure layer

- raw source manifest exists;
- document metadata seed exists;
- raw source validation exists;
- full-source segmentation command exists;
- segment validation exists;
- lexicon export exists;
- KWIC generation exists;
- candidate evidence generation exists;
- case config exists;
- case builder exists;
- Makefile pipeline exists;
- smoke tests exist;
- GitHub Actions workflow exists;
- release manifest generation exists;
- license and release policy exists;
- contribution guide exists.

## 2. Near-term research work

The next work is not more scaffolding. It is scholarly review.

- Run `make all` inside `V2/`.
- Inspect generated full segments.
- Inspect generated KWIC rows.
- Select useful evidence candidates.
- Review candidate claims manually.
- Add reviewer and review date when claims are accepted.
- Promote reviewed rows into curated case files.
- Rewrite the interpretive note as a small digital essay.

## 3. Medium-term corpus expansion

Add more Ming-Qing Western Learning texts only when real sources are available and can be registered. Do not create placeholder texts.

For each new text:

- register raw source;
- add metadata;
- generate segments;
- update lexicon if needed;
- build or extend a research case;
- preserve uncertainty and source notes.

## 4. Long-term research platform

The long-term goal is a small but reliable research platform:

- publishable curated case releases;
- stable corpus releases;
- teaching modules;
- authority crosswalks;
- a scholarly interface that links evidence, claims, and source segments.

## 5. Maturity threshold

V2 now meets the minimum technical threshold for a real, reproducible, extensible, and maintainable DH repository. It is not yet a finished scholarly article. The decisive next threshold is human review of evidence and claims.
