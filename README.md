![Yilong Xiao — 高海拔葡萄园，可复现的田间研究工具](./assets/hero.svg)

在读硕士，西北农林科技大学葡萄酒学院。研究香格里拉高海拔葡萄园的行间生草、叶幕管理与土壤有机碳。

这里放的是研究里真实写下的工具。共同点：能装、能跑、有测试、写明局限；合成数据与公开数据分开标注，网格值不冒充园地实测。多数是给同行复算用的，也适合直接改成本地版本。

**两个不用安装、点开就能用的：**

| 打开 | 是什么 |
|---|---|
| **[藤候 VineWatch →](https://uppercrusteve.github.io/vinewatch/)** | 离线物候（BBCH）记录 PWA。山里没信号也能记，照片在本地压缩，数据只留在这台设备，随时导出 CSV / GeoJSON。手机上试最直观。 |
| **[云岭之上 · 图集 →](https://uppercrusteve.github.io/yunnan-vineyard-atlas/)** | 德钦葡萄园数据图集。同一年的四种面积口径并排展示，不取平均，每条数字都带出处与检索日期。 |

![仓库数据：8 个仓库、457 项测试、8/8 CI 通过，由 Actions 每天生成](./assets/stats.svg)

## 命令行工具

下面几个需要 `git clone` 后安装，三条命令内出结果。全部是 MIT。

| 工具 | 解决什么 | 上手 |
|---|---|---|
| **[splitplot-designer](https://github.com/uppercrusteve/splitplot-designer)** | 裂区试验的随机化、布局图与功效模拟。主区效应用 `block×main` 误差层检验，避免把采样点当重复 | `splitplot power --blocks 4 --effect 0.6` |
| **[aggcarbon](https://github.com/uppercrusteve/aggcarbon)** | 湿筛团聚体的 MWD、GMD、R>0.25、ESM 校正储量、POC/MAOC、LI、CPI/CMI，带块 bootstrap 区间 | `aggcarbon compute examples/aggregates_demo.csv --reference CK -o out` |
| **[vineclim](https://github.com/uppercrusteve/vineclim)** | GDD、Huglin、冷夜、霜冻日历；支持 NASA POWER 拉取与海拔订正，未订正/订正双列对照 | `vineclim compute examples/deqin_power_2015_2025.csv --lat 28.5` |
| **[rusle-terrace](https://github.com/uppercrusteve/rusle-terrace)** | DEM 驱动的坡地葡萄园 RUSLE 筛查：坡度分级、D8 汇流、风险图与汇总；缺米制 CRS 直接报错 | `rusle demo -o out` |
| **[thesis-forge](https://github.com/uppercrusteve/thesis-forge)** | Markdown → A4 学位论文 DOCX：样式、目录域、三线表、图表题注，外加一次格式体检 | `thesis-forge build thesis.md -o thesis.docx` |
| **[citecheck-zh](https://github.com/uppercrusteve/citecheck-zh)** | 中文稿件的引文—文献表一致性检查：悬空引用、孤立文献、编号断档、坏 DOI，定位到行号 | `citecheck check manuscript.md` |

## 做过的事

| 类别 | 具体内容 |
|---|---|
| 试验设计 | 裂区与随机完全区组：处理结构、缓冲行、可复现随机化、误差分层、Monte Carlo 功效与区组数建议 |
| 土壤碳 | 湿筛分级、团聚体稳定性、等效土壤质量校正、POC/MAOC 物理分组、CPI/CMI 与活性指数、按 block 的 bootstrap |
| 气候指标 | GDD、Huglin、冷夜、霜冻日、生长季长度；POWER API 拉取、缺测阈值、气温直减率订正 |
| 空间分析 | rasterio / GDAL 读写、坡度坡向、D8 流向与汇流累积、RUSLE 因子计算、风险分级 |
| 工程 | Python 3.11+、pytest、ruff、类型标注；原生 JavaScript、IndexedDB、Service Worker、PWA 离线缓存 |
| 文档 | OOXML 样式与域、三线表、题注编号；引文核对；Markdown / Pandoc / Quarto 工具链 |

## 几条固定做法

- **公开数据带来源和检索日期**，直链失效也保留标题，不悄悄删。
- **冲突口径并排**：面积、产量、海拔区间有几套说法就放几套，宁可页面难看，不取平均。
- **合成演示只用来跑通流程**，首屏标注；网格气候值与园地实测分开写。
- 每个仓库都有 `docs/methods.md`：公式、单位、假设、文献、已知偏差。

## 这页的维护

头图是手写 SVG，等高线用 SMIL 缓慢流动。下面的数据卡由 [`.github/workflows/stats.yml`](./.github/workflows/stats.yml) 每天 01:30 UTC 抓 GitHub API 与各仓库 CI 结论生成并提交，不靠第三方徽章服务；星标数为实时值，现在还是 0，说明还没被看到。

## 联系

- 问题与建议：在对应仓库开 issue，比私信好归档。
- 复用与改作：MIT，署名即可，不必先问。
- 引用：各仓库附 `CITATION.cff`，GitHub 右侧 “Cite this repository” 可直接取。

<sub>个人研究工具，不代表所在单位。所有示例除注明出处外均为合成数据。</sub>
