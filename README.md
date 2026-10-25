# 衣冠之间

## 汉服的历史、结构与日常

《衣着有名》的独立姊妹篇，面向希望系统认识汉服的兴趣读者。全书新编，以先秦至当代的历史为主线，再深入衣物结构、材料工艺、制度场景、实物阅读与现实穿用。

当前阅读站版本包含26章、3个附录、52幅不同配图。本轮新增23张照片级AI教学图，其中22张含成年模特穿着，1张为收纳护理场景；配合原有15张文物或历史图像、12幅结构图与2幅AI插画。18张新增图采用有具体来源的有限复原／类型试制，5张明确为现代观察实验。它们不是真人实拍，不充当史料，不冒称馆方认证复原。此前离线版的页数与字数不代表此次在线增补版。

[在线阅读](https://yzyexp.github.io/Learn-Hanfu/) · [上身图鉴](https://yzyexp.github.io/Learn-Hanfu/gallery.html)

## 阅读路线

- 历史线：第3—12章，先秦、秦汉、魏晋南北朝、隋唐五代、宋辽金元、明清至近代。
- 结构与工艺线：第2、13—20章，领襟袖身、裙片围合、袍服、内衣与裤、冠履、织染、礼制及制作。
- 案例与实践线：第21—26章，具体馆藏、当代汉服、尺寸系结、护理、比较与观察记录。
- 附录：时间坐标、词汇索引、图像来源与阅读资料。

完整目录与稳定阅读顺序由 [book.json](book.json) 管理。所有正文在 `chapters/` 与 `appendices/`，图片使用相对路径；后续阅读站可以直接消费同一清单，不必复制正文。

## 分章阅读

<!-- book-toc:start -->
- [1 · 看衣冠，也看证据](chapters/01-reading-evidence.md)
- [2 · 衣服怎样构成：领、襟、袖、身与裳](chapters/02-clothing-anatomy.md)
- [3 · 先秦：衣裳、礼制与楚地衣物](chapters/03-pre-qin.md)
- [4 · 秦汉：袍服、曲裾与丝织衣物](chapters/04-qin-han.md)
- [5 · 魏晋南北朝：宽衣、小袖与跨地域交流](chapters/05-wei-jin.md)
- [6 · 隋唐五代女服：襦、裙、半臂与帔帛](chapters/06-sui-tang-women.md)
- [7 · 隋唐男子与骑行衣着：圆领袍、幞头和靴](chapters/07-tang-men.md)
- [8 · 两宋：褙子、衫、裙与城市生活](chapters/08-song.md)
- [9 · 辽金元：并存的衣冠与服饰交流](chapters/09-liao-jin-yuan.md)
- [10 · 明代女服：衫袄、比甲、披风与裙](chapters/10-ming-women.md)
- [11 · 明代男服：袍衫、道袍、直身与曳撒](chapters/11-ming-men.md)
- [12 · 清代至近代：变革、延续与服饰记忆](chapters/12-qing-modern.md)
- [13 · 裙的结构：裙片、褶裥、裙门与围合](chapters/13-skirts.md)
- [14 · 袍服比较：结构、开衩与内外层](chapters/14-robes.md)
- [15 · 内衣与裤：衣着系统中不显眼的部分](chapters/15-underlayers-trousers.md)
- [16 · 冠巾、发式与足衣：从头到脚看整体](chapters/16-head-foot.md)
- [17 · 丝麻棉毛：材料、织物与身体感受](chapters/17-textiles.md)
- [18 · 染色、纹样与装饰工艺](chapters/18-color-pattern.md)
- [19 · 身份、场合与制度：礼服、常服和婚服](chapters/19-ritual-status.md)
- [20 · 从布到衣：裁剪、缝合与复原](chapters/20-making.md)
- [21 · 走进博物馆：八组实物与图像细读](chapters/21-museum-cases.md)
- [22 · 当代汉服：重建、商品与日常穿用](chapters/22-contemporary.md)
- [23 · 穿着实践：尺寸、层次、系结与活动](chapters/23-wearing.md)
- [24 · 清洁、收纳与长期保存](chapters/24-care.md)
- [25 · 相邻传统与跨文化比较](chapters/25-comparison.md)
- [26 · 建立自己的衣冠观察记录](chapters/26-observation.md)

- [附录A · 时间坐标与并行的历史](appendices/a-timeline.md)
- [附录B · 衣冠观察词汇](appendices/b-glossary.md)
- [附录C · 图像来源与阅读资料](appendices/c-image-credits.md)
<!-- book-toc:end -->

## 文件

- `chapters/`：26章可编辑Markdown主稿。
- `appendices/`：时间坐标、词汇、图像来源。
- `assets/images/`：15张文物或历史图像照片、12幅原创教学图、2幅AI教学插画、23张新增照片级教学图。
- `assets/fonts/`：内嵌字体子集及OFL许可。
- `references/`：来源目录、图像权利、图注与插入记录。
- `scripts/`：图解、字体准备、PDF与EPUB构建、完整性验证。
- `editorial/`：编写计划、审校与生成插画记录，不进入读者正文。
- `output/`：构建结果，未纳入Git。包含全书PDF、26份章节PDF、EPUB和合并Markdown。

## 构建

Python 3.10以上；项目已附嵌入字体，无须安装系统中文字库、浏览器、Pandoc或TeX。

```bash
python -m pip install -r requirements.txt
python scripts/build_book.py --format check
python scripts/build_book.py --format all
```

完整性检查另安装`requirements-checks.txt`后运行`python scripts/validate_book.py`。

只导出一种格式：

```bash
python scripts/build_book.py --format epub
python scripts/build_book.py --format pdf
```

教学图可用附带字体重新绘制：

```bash
python scripts/draw_diagrams.py
```

图像已经入稿，日常构建不需要重新插图。`integrate_images.py`用于维护选图清单；已有引用不会重复插入。新增字符超出当前字体子集时，安装`requirements-fonts.txt`中的可选依赖，再运行`prepare_font.py`。该脚本默认从Noto官方仓库下载原字体，亦接受`--source`指向已取得的字体；普通构建不联网下载字体。

## 资料与图像

120个不同的来源URL集中于`references/source-catalog.json`，正文与独立章节保留事实附近的链接。原图题名、年代、编号、机构、许可状态、观察范围与下载校验见`references/image-evidence.json`。

10张海外馆藏图有Public Domain或CC0标记；5张中国博物馆官方图仅用于相应藏品的必要教学评述引用，保留署名和水印，未标作开放授权。不要把全部素材目录一概当成可自由再发布的图片包。原始权利不随本工程改变，完整说明见附录C。

生成插画只辅助外观阅读，不提供历史证据；12幅结构图为概念教学图，不是某件出土衣物的精确纸样。所有章节都区分观察、机构说明与推测。

## 版本

新书根提交仅含零字节README；随后分别加入范围、正文、配图、审校和构建。工程包附`history.bundle`可恢复Git历史：

```bash
git clone history.bundle Hanfu-Atlas-restored
```

网站源码位于 `site/`，与 PDF／EPUB 共用上述分章主稿；生成的 HTML 位于忽略入 Git 的 `build/site/`。

## 在线阅读与 GitHub Pages

阅读站地址：https://yzyexp.github.io/Learn-Hanfu/ 。

网站从 `book.json`、原有分章 Markdown 和图片独立构建，包含总目录、前后章导航、本篇目录、图像来源与下载页；不复制另一份正文。只需轻量 Markdown 依赖：

```bash
python -m pip install -r site/requirements.txt
python site/build.py
python -m http.server --directory build/site 8000
```

构建会校验32个页面的全部站内目标、52幅图片及替代文本；新增上身图鉴逐张列出依据、限制和正文入口。`.github/workflows/pages.yml` 在主分支内容更新后构建并发布，PR 仅构建。首次需要在仓库 Settings → Pages 将 Source 设置为 GitHub Actions。网站 CI 不安装整书导出依赖，不生成 PDF／EPUB；如获准提供公共电子书下载，可将单独构建且已审核的固定产物放入 `downloads/`；无此目录时网站明确显示电子书尚未附加，不生成断链。下载不授予馆藏图新的使用权。
