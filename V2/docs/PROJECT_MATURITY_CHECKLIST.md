# V2 项目成熟度检查表
# V2 Project Maturity Checklist

本检查表用于判断 V2 是否真正从一次性产品转变为可扩展、可维护、可复核的人文学术项目。

This checklist evaluates whether V2 has moved from a one-off product to an extensible, maintainable, and reviewable humanities research project.

---

## A. 项目结构 / Project Structure

- [x] 有清晰的 V2 README。
- [x] 有项目级配置文件。
- [x] 有文献 metadata seed。
- [x] 有领域词表 seed。
- [x] 有 schema。
- [x] 有统一 CLI 入口。
- [x] 有 smoke tests。
- [x] 有研究案例模板。
- [x] 有维护计划。

- [x] Clear V2 README.
- [x] Project-level configuration.
- [x] Document metadata seed.
- [x] Domain lexicon seed.
- [x] Schemas.
- [x] Unified CLI entry point.
- [x] Smoke tests.
- [x] Research case template.
- [x] Maintenance plan.

---

## B. 可运行性 / Executability

- [x] 能验证 document metadata。
- [x] 能验证 segment JSONL。
- [x] 能导出 lexicon JSON。
- [x] 能从 sample segment 生成 KWIC。
- [x] 能生成 release manifest。
- [ ] GitHub Actions CI 已实际安装到 `.github/workflows/`。

- [x] Can validate document metadata.
- [x] Can validate segment JSONL.
- [x] Can export lexicon JSON.
- [x] Can generate KWIC from sample segments.
- [x] Can generate a release manifest.
- [ ] GitHub Actions CI is installed under `.github/workflows/`.

---

## C. 学术可信度 / Scholarly Reliability

- [x] README 明确声明 sample data 不能作为古籍证据引用。
- [x] claim review 表包含 evidence quote 和 review status 字段。
- [x] 维护计划要求 raw data 不覆盖。
- [ ] 已接入经过来源核验的真实《坤輿圖說》文本。
- [ ] 已接入经过来源核验的真实《地球圖説》文本。
- [ ] 第一个正式 case 已完成人工复核。

- [x] README clearly states that sample data cannot be cited as source evidence.
- [x] Claim review table includes evidence quote and review status fields.
- [x] Maintenance plan requires raw data not to be overwritten.
- [ ] Source-verified *Kunyu Tushuo* text has been added.
- [ ] Source-verified *Diqiu Tushuo* text has been added.
- [ ] The first formal case has completed human review.

---

## D. 可扩展性 / Extensibility

- [x] 新增文献流程已定义。
- [x] 新增研究案例流程已定义。
- [x] 研究案例模板已建立。
- [x] CLI 可继续扩展子命令。
- [ ] 已完成第二个非 pilot 文献案例。
- [ ] 已建立 authority crosswalk 的真实样例。

- [x] Workflow for adding new texts is defined.
- [x] Workflow for adding research cases is defined.
- [x] Research case template is established.
- [x] CLI can be extended with new subcommands.
- [ ] A second non-pilot text case has been completed.
- [ ] A real authority crosswalk sample has been created.

---

## 当前判断 / Current Assessment

V2 已经达到“可维护项目脚手架”的标准，但尚未达到“成熟研究项目”的标准。

V2 now meets the standard of a maintainable project scaffold, but not yet the standard of a mature research project.

下一阶段的关键不是继续增加宣言式文档，而是接入真实核验文本、跑通正式 case、安装 CI，并完成至少一个人工复核的研究案例。

The next stage should not focus on adding more manifesto-style documents. It should add source-verified texts, run a formal case, install CI, and complete at least one human-reviewed research case.
