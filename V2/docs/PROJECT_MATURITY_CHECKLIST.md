# V2 项目成熟度检查表
# V2 Project Maturity Checklist

本检查表用于判断 V2 是否真正从一次性产品转变为可扩展、可维护、可复核的人文学术项目。

This checklist evaluates whether V2 has moved from a one-off product to an extensible, maintainable, and reviewable humanities research project.

---

## A. 项目结构 / Project Structure

- [x] 有清晰的 V2 README。
- [x] 有项目级配置文件。
- [x] 有文献 metadata seed。
- [x] 有真实 raw source manifest，指向仓库根目录既有文本。
- [x] 有领域词表 seed。
- [x] 有 schema。
- [x] 有统一 CLI 入口。
- [x] 有 smoke tests。
- [x] 有研究案例模板。
- [x] 有维护计划。

- [x] Clear V2 README.
- [x] Project-level configuration.
- [x] Document metadata seed.
- [x] Real raw source manifest pointing to existing root-level texts.
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
- [x] 能从真实仓库文本摘录 segment 生成 KWIC。
- [x] 能生成 release manifest。
- [ ] GitHub Actions CI 已实际安装到 `.github/workflows/`。

- [x] Can validate document metadata.
- [x] Can validate segment JSONL.
- [x] Can generate KWIC from real repository-text excerpt segments.
- [x] Can export lexicon JSON.
- [x] Can generate a release manifest.
- [ ] GitHub Actions CI is installed under `.github/workflows/`.

---

## C. 学术可信度 / Scholarly Reliability

- [x] README 明确区分真实仓库文本摘录与 smoke-test sample。
- [x] claim review 表包含 evidence quote 和 review status 字段。
- [x] 维护计划要求 raw data 不覆盖。
- [x] 已登记仓库根目录真实《坤輿圖說》文本：`1674_坤輿圖說_WS.txt`。
- [x] 已登记仓库根目录真实《地球圖説》文本：`1799_地球圖説_WS.txt`。
- [x] 第一个 pilot case 已使用真实仓库文本摘录替换 synthetic sample。
- [ ] 已从两部完整 raw source 自动生成完整 segment JSONL。
- [ ] 第一个正式 case 已完成人工复核。

- [x] README distinguishes real repository-text excerpts from smoke-test samples.
- [x] Claim review table includes evidence quote and review status fields.
- [x] Maintenance plan requires raw data not to be overwritten.
- [x] The root-level real *Kunyu Tushuo* text is registered: `1674_坤輿圖說_WS.txt`.
- [x] The root-level real *Diqiu Tushuo* text is registered: `1799_地球圖説_WS.txt`.
- [x] The first pilot case has replaced synthetic samples with real repository-text excerpts.
- [ ] Full segment JSONL has been generated automatically from both complete raw sources.
- [ ] The first formal case has completed human review.

---

## D. 可扩展性 / Extensibility

- [x] 新增文献流程已定义。
- [x] 新增研究案例流程已定义。
- [x] 研究案例模板已建立。
- [x] CLI 可继续扩展子命令。
- [x] 已建立 authority crosswalk seed。
- [ ] 已完成第二个非 pilot 文献案例。
- [ ] 已建立外部 authority 数据库核验后的真实样例。

- [x] Workflow for adding new texts is defined.
- [x] Workflow for adding research cases is defined.
- [x] Research case template is established.
- [x] CLI can be extended with new subcommands.
- [x] Authority crosswalk seed has been created.
- [ ] A second non-pilot text case has been completed.
- [ ] A verified external authority database sample has been created.

---

## 当前判断 / Current Assessment

V2 已经达到“可维护项目脚手架”的标准，并已经把仓库中既有《坤輿圖說》《地球圖説》文本纳入 V2 主线。它尚未达到“成熟研究项目”的标准，因为还需要从完整 raw source 生成完整 segment JSONL、完成系统 KWIC、人工复核 claims，并安装 CI。

V2 now meets the standard of a maintainable project scaffold and has incorporated the existing repository texts of *Kunyu Tushuo* and *Diqiu Tushuo* into the V2 main line. It has not yet reached the standard of a mature research project, because it still needs full segment JSONL generated from complete raw sources, systematic KWIC, human-reviewed claims, and installed CI.
