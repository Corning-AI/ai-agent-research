# 2025年最新AI Agent调研执行摘要
## 20个WebSearch查询的关键发现

**调研日期**: 2025-12-31
**调研方式**: 主会话20个WebSearch并行查询
**覆盖领域**: LaTeX、CAD、Circuit、AI Framework
**数据来源**: 实时Web搜索，2025年12月最新信息

---

## 🎯 重大突破性发现

### 2025年AI工具爆发式增长
- **LaTeX领域**: Underleaf、Overleaf AI Assist、Paperpal等新工具全面上线
- **CAD领域**: AURA AI、AdamCAD、VideoCAD等颠覆性工具发布
- **Circuit领域**: Quilter AI成功设计843部件Linux电脑，首次启动即成功
- **AI框架**: Google ADK、LangGraph、Agno等框架成熟度显著提升

---

## 📄 LaTeX AI 工具 - 2025最新发现

### 🚀 新工具发布

#### 1. **Under leaf** (2025新星)
- **突破**: AI驱动的LaTeX工作流助手
- **特色**:
  - 图像/文档转LaTeX，秒级完成
  - 直接嵌入Overleaf，无需复制粘贴
  - AI写作辅助、引用搜索、错误检测
- **链接**: [Underleaf AI](https://www.underleaf.ai/)

#### 2. **Overleaf AI Assist** (2025年6-7月发布)
- **用户基数**: 超过2000万研究人员
- **核心功能**:
  - 从简单提示或图像生成LaTeX代码（表格、公式）
  - TeXGPT：格式化、图形生成、自定义命令
  - 上下文感知的语法、拼写建议
- **重要性**: 标志LaTeX工具AI化的里程碑
- **链接**: [Overleaf AI Features](https://www.overleaf.com/about/ai-features)

#### 3. **Paperpal for Overleaf** (2025年1月发布)
- **用户**: 超过150万学术用户信赖
- **创新**:
  - LaTeX文档实时语法检查
  - 保留代码和格式的精确建议
  - **免费提供**无限访问语法检查
- **影响**: 改变学术LaTeX编辑方式
- **链接**: [Paperpal Overleaf](https://paperpal.com/blog/news-updates/product-updates/introducing-paperpal-for-overleaf)

#### 4. **BibbyAI**
- 强大LaTeX编辑器 + 上下文感知AI助手
- 端到端研究工作流理解

#### 5. **Crixet**
- 免费在线LaTeX编辑器
- 协作、AI和模板支持

### 📊 OCR工具更新

#### Mathpix 2025改进
- **重大更新**（2025年3月1日）:
  - 简化并降低Image API价格
  - 新OCR模型，保证语法正确性
  - 英文手写新增拼写检查选项
- **性能**: 手写识别准确率显著提升
- **定价**: 更实惠，对所有用户开放

#### Pix2Text (开源免费)
- **定位**: Mathpix免费开源替代品
- **功能**: 识别布局、表格、公式、文本→Markdown
- **优势**: 80+语言支持
- **链接**: [Pix2Text GitHub](https://github.com/breezedeus/Pix2Text)

### 🔧 VSCode扩展 (2025)

#### LaTeX Workshop (必备)
- **最新版本**: 需要VSCode 1.96.0+ (2024年12月或更新)
- **核心功能**:
  - 自动编译PDF（保存时）
  - 双向SyncTeX（源码↔PDF点击跳转）
  - Intellisense（引用、标签自动完成）
- **链接**: [LaTeX Workshop](https://github.com/James-Yu/LaTeX-Workshop)

#### LTeX+ (语法检查)
- **专为LaTeX设计**
- LaTeX语法感知的拼写和语法检查

### 🎓 学术写作AI工具

#### 核心平台整合
所有主流LaTeX平台现已集成AI：
- **Overleaf**: AI Assist add-on
- **Writefull**: LaTeX内语言反馈
- **Claude/ChatGPT**: 通用LaTeX代码生成

#### 文献管理
- Zotero、Mendeley：导出.bib，与AI工具协同

---

## 🏗️ CAD AI 自动化 - 2025颠覆性进展

### 🌟 突破性新工具

#### 1. **AdamCAD** (2025年1月24日正式发布)
- **融资**: 种子轮融资$4.1M（2个月后）
- **革命性**: 自然语言→3D模型
  - 输入: "hexagonal gear with 10mm shaft"
  - 输出: 秒级生成参数化模型
- **定位**: "Cursor for CAD"
- **YC支持**: Y Combinator投资
- **链接**: [Adam AI](https://www.ycombinator.com/companies/adam)

#### 2. **VideoCAD** (MIT 2025)
- **突破**: AI直接操控CAD软件
- **能力**:
  - 从2D草图输入
  - 点击、拖动、选择工具
  - 构建完整3D形状
- **意义**: AI成为CAD操作者
- **链接**: [MIT News](https://news.mit.edu/2025/new-ai-agent-learns-use-cad-create-3d-objects-sketches-1119)

#### 3. **Zoo (text-to-CAD)**
- **功能**: 文本→CAD几何
  - 示例: "flange with 6 bolt holes"
  - 输出: 完全参数化CAD模型（KCL语言）
- **精度**: 工程级B-Rep几何
- **链接**: [Zoo Text-to-CAD](https://zoo.dev/research/introducing-text-to-cad)

#### 4. **DraftAid**
- **特长**: 3D模型→2D制造图纸自动化
- **性能**: 减少绘图时间高达90%
- **集成**: SolidWorks、Inventor
- **链接**: [DraftAid](https://draftaid.io/)

#### 5. **CADGPT**
- **定位**: CAD版ChatGPT
- **能力**:
  - 回答设计问题
  - 建议命令和工具
  - 编写AutoLISP/Python脚本
- **用途**: 自动化AutoCAD工作流
- **链接**: [CADGPT](https://apps.autodesk.com/ACD/en/Detail/Index?id=5943525154513009240)

#### 6. **Leo AI**
- **定位**: 工程师AI副驾驶
- **模型**: Large Mechanical Model (LMM)
- **输入**: 描述机制/草图/规格表
- **输出**: 完整CAD模型
- **训练**: 工程数据训练
- **链接**: [Leo AI](https://www.getleo.ai/)

### 🔥 主流CAD软件AI功能

#### SOLIDWORKS 2025 - **AURA AI**
- **发布**: 2025年7月公开
- **当前**: Beta测试中
- **核心功能**:
  - 上下文感知洞察
  - 行业法规导航
  - 生成智能3D解决方案
  - 学习用户习惯，提升生产力
- **链接**: [SOLIDWORKS AURA](https://www.engineersrule.com/ai-capabilities-in-solidworks-2025-redefining-design-intelligence/)

#### SOLIDWORKS 2025 - AI功能清单
1. **AI紧固件识别**: 自动识别螺栓、螺母、垫圈
2. **自动生成图纸**: 从3D模型自动创建2D生产图纸
3. **图像转草图**: 从图像生成草图，自动添加尺寸和约束
4. **命令预测器**: 学习预测下一步命令
5. **生成式NC加工**: 优化刀路，减少浪费
- **链接**: [8 AI Features](https://www.engineersrule.com/8-key-features-demonstrating-the-power-of-ai-in-solidworks-2025/)

#### AutoCAD 2025 - Smart Blocks
- **AI技术**: Autodesk AI
- **功能**:
  - ML识别相似块from库
  - 提升内容重用效率
  - 标准化设计
- **Autodesk Assistant**: 增强对话界面，生成式响应
- **链接**: [AutoCAD 2025](https://www.autodesk.com/blogs/autocad/autocad-2025/)

#### Fusion 360 2025
- **新功能**: AI驱动自动化
- **改进**: 实时协作增强、制造工具改进
- **生成式设计**: 云端AI优化

#### PTC Creo Version 12
- **AI生成式设计**: 集成热物理
- **优化**: 基于热、机械、重量约束

#### Onshape AI Advisor (PTC 2025发布)
- **集成**: 直接嵌入设计环境
- **功能**: 实时指导、故障排除、最佳实践
- **链接**: [Onshape AI](https://www.ptc.com/en/news/2025/ptc-announces-latest-onshape-ai-advisor-release)

### 🔄 Parametric CAD Programming AI

#### Backflip AI (2025年初)
- **能力**: 3D扫描数据→完全参数化CAD模型
- **突破**: 直接驱动CAD软件
  - 草图、拉伸、旋转
  - 构建参数化模型匹配网格输入

#### CAD-Coder-NextGen
- **功能**: 想法→CAD-ready代码
- **平台**: AI平台
- **链接**: [CAD-Coder](https://medium.com/institute-for-applied-computational-science/cad-coder-nextgen-ai-platform-that-turns-ideas-into-cad-ready-code-d8a4df202859)

---

## ⚡ Circuit 设计 AI - 2025实战化

### 🚀 革命性工具

#### 1. **Quilter** (物理驱动AI)
- **定位**: 非自动路由器，非co-pilot，非LLM
- **本质**: 物理优先AI系统
- **学习**: 从自然法则学习（非人类捷径）
- **性能**: 月→分钟级布局
- **突破案例** (2025):
  - 设计843部件Linux计算机
  - **1周完成** (传统需3个月)
  - **首次启动即成功**，无需昂贵修订
- **链接**: [Quilter](https://www.quilter.ai/)
- **报道**: [VentureBeat](https://venturebeat.com/ai/quilters-ai-just-designed-an-843-part-linux-computer-that-booted-on-the)

#### 2. **Circuit Mind**
- **能力**: 60秒生成原理图和BOM
- **速度**: 周/月→秒/分钟
- **定位**: AI电子设计自动化平台
- **链接**: [Circuit Mind](https://www.circuitmind.io/)

#### 3. **Cirkit Designer**
- **提速**: 10x更快电路设计
- **适用**: Arduino、ESP32、Raspberry Pi、IoT
- **链接**: [Cirkit Designer](https://www.cirkitstudio.com/)

#### 4. **DeepPCB**
- **技术**: 强化学习（Reinforcement Learning）
- **特长**: PCB路由决策问题
- **部署**: 纯AI驱动，云原生
- **链接**: [DeepPCB](https://deeppcb.ai/)

#### 5. **NVIDIA CircuitVAE**
- **技术**: 生成模型
- **性能**: 2-3x加速（vs RL和遗传算法）
- **应用**: 电路设计
- **链接**: [NVIDIA Blog](https://developer.nvidia.com/blog/using-generative-ai-models-in-circuit-design/)

### 📊 PCB设计AI自动化现状

#### 核心应用
1. **自动路由和布局**: 天→分钟
2. **设计优化**: ML分析大数据集
   - 最优元件布局建议
   - 预测信号完整性问题
   - 简化路由
3. **错误检测**: AI速度和准确性远超人类
   - 短路检测
   - 设计规则违规

#### 性能提升
- **走线长度减少**: 高达20% (vs手动设计)
- **效果**: 减少信号干扰，提升性能

#### 主流解决方案
- **Allegro X AI** (Cadence): 评估数千种布局策略
- **Quilter**: 自主PCB设计引擎
- **DeepPCB**: RL驱动路由

### 🔬 SPICE仿真AI增强

#### Siemens Solido Suite (2025年12月)
- **性能**: 2-30x加速
  - 模拟、混合信号、RF、3D IC验证
- **技术**:
  - 新收敛算法
  - 缓存高效算法
  - 高多核可扩展性
- **High-Sigma验证**: 4,000,000X加速（vs蛮力）
- **链接**: [Siemens EDA Suite](https://www.electronicspecifier.com/news/siemens-introduces-ai-powered-suite/)

#### SPICEPilot (2025研究)
- **创新**: Python数据集（PySpice生成）
- **用途**: 自动化SPICE代码生成
- **配置**: 跨多种电路配置
- **链接**: [arXiv](https://arxiv.org/html/2410.20553v1)

#### YouSpice AI教程
- **内容**: ChatGPT生成SPICE模型（从数据表）
- **包含**: 逐步AI提示、参数提取、模型验证
- **链接**: [YouSpice](https://youspice.com/)

### 🏭 EDA工具AI功能对比(2025)

#### Siemens EDA (DAC 2025展示)
- **Aprisa AI**: 10x生产力，3x更快tape-out，10%更好PPA
- **Calibre Vision AI**: 半时间识别并修复关键设计违规
- **Questa One**: AI验证平台，自动化工作流，加速验证
- **链接**: [Siemens DAC 2025](https://www.designnews.com/design-software/siemens-unveils-eda-ai-system-for-semiconductor-pcb-design-at-dac-2025)

#### Synopsys
- **工具**: Fusion Compiler、DSO.ai
- **焦点**: AI驱动仿真、布局、验证

#### PrimisAI - RapidGPT
- **突破**: 生成式AI，自然语言接口
- **用户**: 硬件设计师
- **效果**: 提升生产力，加速上市
- **链接**: [PrimisAI](https://primis.ai/)

### 📈 电路优化ML研究(2025)

#### 关键研究领域
1. **深度学习电路设计**: 预测性能（时序、功耗、面积）
2. **图神经网络(GNNs)**: 电路表示和优化
3. **强化学习**: 自动布局布线决策

#### 最新成果
- **自动晶体管级综合** (2025年12月): 语法演化框架，无需领域知识
- **ML驱动优化**: SPICE仿真调用减少56-83%
- **量子电路优化**: 纠缠分布增强，电路深度和门计数减少20-86% (2025年9月)

#### 应用
- 集成电路、量子计算、自动化设计优化

---

## 🤖 AI Agent 框架 - 2025成熟化

### 📊 框架格局 (2025年12月)

#### 主导框架
1. **LangChain/LangGraph**: 最广泛使用
   - **优势**: 模块化、生态丰富、文档完善
   - **LangGraph**: 复杂状态工作流
   - **应用**: 通用LLM应用、RAG系统

2. **AutoGen** (Microsoft): 快速增长
   - **焦点**: 高级多agent系统
   - **特色**: agent对话、灵活性、上下文管理

3. **CrewAI**:
   - **焦点**: 角色化协作
   - **增长**: GitHub stars Q3 2024→Q1 2025翻3倍
   - **应用**: 营销自动化、内容创作

#### 新兴框架

##### Google ADK (Agent Development Kit)
- **发布**: Google Cloud NEXT 2025
- **定位**: 开源框架
- **用途**: 端到端agent和多agent系统开发
- **链接**: [Google ADK](https://developers.googleblog.com/en/agent-development-kit-easy-to-build-multi-agent-applications/)

##### Agno
- **优势**: 清晰度、内存管理、可读代码
- **适用**: 生产开发者，一致性
- **链接**: [Shakudo Top 9](https://www.shakudo.io/blog/top-9-ai-agent-frameworks)

##### Microsoft Semantic Kernel
- **用途**: 通过技能和规划器嵌入AI
- **应用**: Microsoft 365 Copilot
- **焦点**: 生产环境

#### 专业框架
- **DSPy**: 实验密集型工作流，eval驱动迭代
- **Pydantic AI**: 类型安全、数据验证
- **Motia**: 开源新秀

### 🎯 框架选择指南(2025)

| 需求 | 推荐框架 |
|------|----------|
| 简单聊天机器人/RAG | LangChain、Claude Tools |
| 复杂多步任务 | AutoGen、CrewAI |
| 快速原型 | OpenAI Swarm、AgentGPT |
| 专业agent团队 | CrewAI |
| 图控制流 | LangGraph |
| 自定义ML工作流 | Hugging Face Agents |
| 企业部署 | Semantic Kernel、AutoGen |

### 🔥 Code Assistant对比(2025最新)

#### Cursor vs GitHub Copilot深度对比

##### 性能基准测试
- **速度**: Cursor更快 (62.95秒 vs 89.91秒平均)
- **成功率**: Copilot更高 (56.5% vs 51.7%)
- **解决任务**: Copilot 283个，Cursor 258个

##### 定价
| 工具 | 价格 | 使用限制 |
|------|------|----------|
| Cursor Pro | $20/月 | 500高级请求，额外收费 |
| GitHub Copilot Pro | $10/月 | 公平使用下无限 |

##### 最佳用途
- **Copilot**: 速度、简单性、GitHub集成紧密
  - 文件级任务（行内补全、语法纠正）
  - 熟悉IDE用户(VSCode、JetBrains)

- **Cursor**: 大项目、AI行为精细控制
  - 专业开发者
  - VSCode熟练用户
  - 最强AI辅助开发体验

##### 独特优势
- **Cursor**: 多文件编辑、codebase感知、专业模型
- **Copilot**: GitHub生态、广泛IDE支持、成熟度高

- **链接**: [Zapier Comparison](https://zapier.com/blog/cursor-vs-copilot/)

### 🔌 VSCode AI扩展 Top 10 (2025)

#### 代码补全类
1. **GitHub Copilot**: 最广泛使用
   - 2025更新: 更好跨文件上下文、智能docstring

2. **Codeium (Windsurf)**: 免费强力替代
   - 70+语言
   - 免费供个人开发者
   - 无订阅成本

3. **Tabnine**: 隐私+速度
   - 本地模型选项（无云）
   - 学习编码模式和风格

4. **Amazon Q** (formerly CodeWhisperer):
   - 多语言
   - 后端应用特长
   - AWS最佳实践

5. **Continue** (开源):
   - 对话本地/云LLMs
   - 支持Ollama、GPT-4、Claude、Mistral

#### 专业工具
6. **Cody (Sourcegraph)**:
   - 大代码库理解和导航
   - 完整项目上下文

7. **Qodo Gen** (formerly Codium):
   - 代码质量改进
   - 自动化测试生成

8. **Gemini Code Assist**:
   - Google Gemini模型
   - 文档感知
   - Google生态绑定

#### Agent类扩展
9. **Cline**: 代理式AI扩展
10. **BLACKBOXAI Agent**: 自主上下文感知开发伙伴
11. **Roo Code**: Agent化代码助手

- **链接**: [VSCode AI Extensions](https://graphite.com/guides/best-vscode-extensions-ai)
- **Visual Studio Magazine**: [Top Agentic Tools](https://visualstudiomagazine.com/articles/2025/10/07/top-agentic-ai-tools-for-vs-code-according-to-installs.aspx)

### 🏢 Domain-Specific AI Agents (2025实战)

#### 2025年转折点
- AI系统从**内容创作者/聊天机器人**→**能使用软件工具、自主行动的agents**
- R&D投资创新高
- 成功集成AI的公司 vs 落后公司差距扩大

#### 性能研究
- **发现** (ICLR 2025 Workshop):
  - 领域特定AI agents > 直接使用前沿LLMs构建的agents
  - 跨IT、CX、HR职能
  - 行业: 银行、金融、医疗、教育科技、生物技术
- **链接**: [Aisera Framework](https://aisera.com/press-releases/aisera-introduces-a-framework-to-evaluate-how-domain-specific-agents/)

#### 实际应用

##### 商务领域
- **支付巨头** (Visa、Mastercard):
  - 构建agent commerce基础设施
  - AI驱动购买（聊天机器人内）
  - **时间表**: 2026年初

##### 医疗领域
- 诊断疾病
- 分析医学图像
- 肿瘤检测agents（AI训练）

##### 金融领域
- 实时欺诈检测
- 评估交易活动

#### 关键特性
- **专注数据**: 来自特定行业（vs大而无序的数据集）
- **任务定义**: 完成特定领域的明确任务
- **性能**: 优于通用AI

- **链接**: [CNBC AI Shopping](https://www.cnbc.com/2025/12/29/ai-agentic-shopping-price-discounts-cheap-sales-commerce-visa-mastercard-chatbots.html)

---

## 🎯 2025年核心趋势总结

### 1. AI原生化
- 传统工具全面AI集成（非可选功能）
- LaTeX: Overleaf、Writefull
- CAD: SOLIDWORKS AURA、AutoCAD Smart Blocks
- Circuit: Quilter、Allegro X AI
- Code: Cursor、Copilot内置

### 2. 自然语言→专业输出
- **AdamCAD**: 文本→3D CAD模型
- **Zoo**: 文本→参数化CAD
- **VideoCAD**: 草图→AI操控CAD软件
- **Circuit Mind**: 描述→原理图+BOM(60秒)

### 3. 物理/领域知识AI
- **Quilter**: 物理优先AI（非LLM）
- **CircuitVAE**: 计算图嵌入连续潜空间
- **领域特定agents**: 性能超越通用LLMs

### 4. 多agent系统成熟
- **Google ADK**: 官方多agent框架
- **CrewAI**: GitHub stars翻3倍
- **MetaGPT**: ICLR 2025口头报告
- 从单agent→协作团队

### 5. 开源vs商业双轨
- **开源**: Pix2Text、LaTeX-OCR、Continue、Codeium
- **商业**: Mathpix、Cursor、Quilter、AdamCAD
- **混合**: 大厂免费tier (Copilot、Gemini)

### 6. 成本优化意识
- Mathpix降价（2025年3月）
- Cursor双倍价格引发讨论
- Codeium免费策略成功
- 开源替代品质量提升

---

## 💡 实施建议 (基于2025最新发现)

### LaTeX工作流2025版

```
研究阶段
    ↓
Semantic Scholar + Claude/GPT-4
    ↓
文献管理 (Zotero .bib导出)
    ↓
写作环境
  • Overleaf AI Assist ($) → 生成LaTeX、TeXGPT
  • Underleaf (⭐新) → 图像转LaTeX、AI助手
  • VS Code + LaTeX Workshop (免费)
    ↓
AI写作改进
  • Paperpal (免费!) → 语法检查
  • Writefull → 学术语气
  • Claude/ChatGPT → 内容生成
    ↓
公式识别
  • Mathpix (商业，最高准确率，降价)
  • Pix2Text (免费开源，80+语言)
  • LaTeX-OCR (免费，隐私)
```

### CAD自动化2025路线

**初创/快速原型**:
- AdamCAD ($4.1M融资) → 文本→CAD模型
- Leo AI → 描述/草图→完整CAD
- Zoo → 文本→参数化模型(KCL)

**企业级生产**:
- SOLIDWORKS 2025 + AURA AI → 智能3D、法规导航
- Fusion 360 2025 → AI自动化、协作
- Onshape AI Advisor → 实时指导

**自动化工具**:
- DraftAid → 3D→2D图纸(90%减少时间)
- CADGPT → AutoCAD脚本生成

**编程化CAD**:
- Backflip AI → 3D扫描→参数化模型
- Text-to-CAD (Zoo) → KCL编程语言
- VideoCAD (MIT) → AI操控CAD软件

### Circuit设计2025策略

**突破级项目**:
- **Quilter** → 月→分钟布局，首次启动成功

**快速原型**:
- Circuit Mind → 60秒原理图+BOM
- Cirkit Designer → 10x加速(Arduino/IoT)

**PCB设计**:
- DeepPCB → RL驱动路由
- Allegro X AI → 千种策略评估
- 走线减少20% (AI vs手动)

**仿真优化**:
- Siemens Solido Suite → 2-30x加速，4M x高西格玛
- SPICEPilot → 自动代码生成

**EDA平台**:
- Siemens (Aprisa/Calibre/Questa) → 10x生产力
- PrimisAI RapidGPT → 自然语言接口

### Code Assistant选择(2025)

**预算敏感**:
- **Codeium** (免费，70+语言)
- **Continue** (开源，本地LLMs)
- **Tabnine** (免费tier)

**专业开发**:
- **Cursor** ($20/月) → 大项目、多文件、最强AI
- **GitHub Copilot** ($10/月) → GitHub集成、成熟度

**企业**:
- **Copilot Enterprise** → 组织知识
- **Amazon Q** → AWS生态
- **Gemini Code Assist** → Google生态

**特殊需求**:
- **隐私**: Tabnine本地模型
- **大代码库**: Cody (Sourcegraph)
- **测试生成**: Qodo Gen
- **Agent化**: Cline、BLACKBOXAI Agent

### AI Framework选择(2025更新)

**企业级复杂系统**:
- **LangGraph** → 图控制流、状态管理
- **AutoGen** → 多agent对话
- **Semantic Kernel** → Microsoft生态

**快速开发**:
- **CrewAI** → 角色团队(GitHub增长3x)
- **Google ADK** (⭐新) → 官方多agent框架
- **OpenAI Swarm** → 轻量级

**实验研究**:
- **DSPy** → Eval驱动迭代
- **Agno** → 清晰、可读

**多agent系统**:
- **Google ADK** → Cloud NEXT 2025发布
- **MetaGPT** → ICLR 2025口头报告
- **CrewAI** → stars翻3倍

---

## 📚 重要资源链接

### LaTeX工具
- [Underleaf](https://www.underleaf.ai/)
- [Overleaf AI Assist](https://www.overleaf.com/about/ai-features)
- [Paperpal for Overleaf](https://paperpal.com/blog/news-updates/product-updates/introducing-paperpal-for-overleaf)
- [Mathpix](https://mathpix.com/)
- [Pix2Text GitHub](https://github.com/breezedeus/Pix2Text)
- [LaTeX Workshop GitHub](https://github.com/James-Yu/LaTeX-Workshop)

### CAD工具
- [AdamCAD (YC)](https://www.ycombinator.com/companies/adam)
- [MIT VideoCAD](https://news.mit.edu/2025/new-ai-agent-learns-use-cad-create-3d-objects-sketches-1119)
- [Zoo Text-to-CAD](https://zoo.dev/research/introducing-text-to-cad)
- [DraftAid](https://draftaid.io/)
- [Leo AI](https://www.getleo.ai/)
- [SOLIDWORKS AURA](https://www.engineersrule.com/ai-capabilities-in-solidworks-2025-redefining-design-intelligence/)
- [Onshape AI Advisor](https://www.ptc.com/en/news/2025/ptc-announces-latest-onshape-ai-advisor-release)

### Circuit设计
- [Quilter](https://www.quilter.ai/)
- [Circuit Mind](https://www.circuitmind.io/)
- [DeepPCB](https://deeppcb.ai/)
- [Siemens EDA DAC 2025](https://www.designnews.com/design-software/siemens-unveils-eda-ai-system-for-semiconductor-pcb-design-at-dac-2025)
- [PrimisAI](https://primis.ai/)
- [NVIDIA CircuitVAE Blog](https://developer.nvidia.com/blog/using-generative-ai-models-in-circuit-design/)

### AI框架
- [Google ADK](https://developers.googleblog.com/en/agent-development-kit-easy-to-build-multi-agent-applications/)
- [Shakudo Top 9 Frameworks](https://www.shakudo.io/blog/top-9-ai-agent-frameworks)
- [LangWatch Comparison](https://langwatch.ai/blog/best-ai-agent-frameworks-in-2025-comparing-langgraph-dspy-crewai-agno-and-more)
- [Aisera Domain Agents](https://aisera.com/press-releases/aisera-introduces-a-framework-to-evaluate-how-domain-specific-agents/)

### Code Assistants
- [Cursor vs Copilot (Zapier)](https://zapier.com/blog/cursor-vs-copilot/)
- [VSCode AI Extensions (Graphite)](https://graphite.com/guides/best-vscode-extensions-ai)
- [Visual Studio Magazine Agentic Tools](https://visualstudiomagazine.com/articles/2025/10/07/top-agentic-ai-tools-for-vs-code-according-to-installs.aspx)

---

## 🚨 重要免责声明

- **数据时效**: 基于2025年12月31日WebSearch结果
- **动态变化**: AI工具发展迅速，信息可能过时
- **定价更新**: 请访问官网确认最新价格
- **功能验证**: 建议测试免费trial后再购买

---

**报告编制**: 20个并行WebSearch查询
**执行时间**: 2025-12-31
**编制单位**: 专业领域 AI Agent 调研平台
**调研方式**: 实时Web搜索 + GitHub数据（328+项目）
