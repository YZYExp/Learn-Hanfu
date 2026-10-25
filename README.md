# 衣冠之间

## 汉服的历史、结构与日常

《衣着有名》的独立姊妹篇，面向希望系统认识汉服的兴趣读者。全书新编，以先秦至当代的历史为主线，再深入衣物结构、材料工艺、制度场景、实物阅读与现实穿用。

本版102页PDF、26章、3个附录，约5.7万汉字（含图注、附录与资料说明），29幅配图。引用邻近事实，PDF提供同页资料链接；历史图像、服装实物、教学示意和生成插画分别标明性质。文字按内容需要展开，不受配图分格数量限制。

## 阅读路线

- 历史线：第3—12章，先秦、秦汉、魏晋南北朝、隋唐五代、宋辽金元、明清至近代。
- 结构与工艺线：第2、13—20章，领襟袖身、裙片围合、袍服、内衣与裤、冠履、织染、礼制及制作。
- 案例与实践线：第21—26章，具体馆藏、当代汉服、尺寸系结、护理、比较与观察记录。
- 附录：时间坐标、词汇索引、图像来源与阅读资料。

完整目录与稳定阅读顺序由 [book.json](book.json) 管理。所有正文在 `chapters/` 与 `appendices/`，图片使用相对路径；后续阅读站可以直接消费同一清单，不必复制正文。

## 文件

- `chapters/`：26章可编辑Markdown主稿。
- `appendices/`：时间坐标、词汇、图像来源。
- `assets/images/`：15张文物或历史图像照片、12幅原创教学图、2幅AI教学插画。
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

118个不同的来源URL集中于`references/source-catalog.json`，正文与独立章节保留事实附近的链接。原图题名、年代、编号、机构、许可状态、观察范围与下载校验见`references/image-evidence.json`。

10张海外馆藏图有Public Domain或CC0标记；5张中国博物馆官方图仅用于相应藏品的必要教学评述引用，保留署名和水印，未标作开放授权。不要把全部素材目录一概当成可自由再发布的图片包。原始权利不随本工程改变，完整说明见附录C。

生成插画只辅助外观阅读，不提供历史证据；12幅结构图为概念教学图，不是某件出土衣物的精确纸样。所有章节都区分观察、机构说明与推测。

## 版本

新书根提交仅含零字节README；随后分别加入范围、正文、配图、审校和构建。工程包附`history.bundle`可恢复Git历史：

```bash
git clone history.bundle Hanfu-Atlas-restored
```

网站源码如后续需要，预留在`site/`；当前交付为书稿、PDF和EPUB，不包含生成的HTML阅读站。
