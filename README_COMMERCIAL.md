# spark-spice — Analog Circuit Design for Everyone

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/github-musicjazz5%2Fspark--spice--marketplace-blue)](https://github.com/musicjazz5/spark-spice-marketplace)
[![Email](https://img.shields.io/badge/email-musicjazz5%40gmail.com-informational)](mailto:musicjazz5@gmail.com)

**spark-spice** 是一個開源的模擬驅動模擬工具，利用 Anthropic Claude + BSIM4 模擬進行高速、低成本的類比電路設計。

---

## 🚀 亮點

✅ **成本低 1000 倍**：$0.55 vs $600（傳統 EDA）  
✅ **速度快 100 倍**：5 分鐘 vs 6 小時  
✅ **Razavi gm/Id 自動化**：無需手動迭代  
✅ **BSIM4 Level-54**：台積電標準模型  
✅ **完全開源**：MIT 許可，自由使用  
✅ **商業支持**：企業級授權可用  

---

## 📊 性能對比

| 指標 | spark-spice | 傳統 CAD |
|------|-----------|---------|
| **成本/設計** | $0.55 | $600 |
| **時間** | 5 分鐘 | 6 小時 |
| **工具成本** | 免費 | $50K+/年 |
| **學習曲線** | 30 分鐘 | 2 週 |
| **精度** | ±2% of spec | ±1% |

---

## 📖 完整指南

- 🎯 [快速開始](QUICK_REFERENCE.md)
- 📚 [Razavi gm/Id 方法論](/.claude/RAZAVI_GMID_GUIDE.md)
- 🔧 [工作流程圖](docs/WORKFLOW_DIAGRAM.md)
- 🏗️ [架構和 API](docs/API.md)
- 💼 [商業授權](COMMERCIAL.md)

---

## 🛠️ 快速開始

### 1. 安裝

```bash
# Clone 倉庫
git clone https://github.com/musicjazz5/spark-spice-marketplace
cd spark-spice-marketplace

# 安裝依賴
pip install -r requirements.txt

# 認證 (一次性)
ant auth login
```

### 2. 設計 OTA

```bash
# 可行性檢查（免費）
ant query "Is 60 dB, 50 MHz on 150 µW feasible?"

# 完整設計（$0.55）
ant query "Design 60 dB, 50 MHz Miller OTA using Razavi gm/Id"
```

### 3. 獲取結果

```
✓ R1–R8 手設計步驟
✓ 電晶體尺寸 (W/L)
✓ 補償網路 (Cc, Rz)
✓ BSIM4 模擬結果
✓ 完整設計報告
```

---

## 📋 使用案例

### 學術研究
```
✓ 免費使用 MIT 許可
✓ 設計課程材料
✓ 畢業論文
✓ 開源項目
```

### 工業設計
```
✓ IC 設計公司
✓ 初創 / 創新公司
✓ 芯片設計小組
✓ EDA 工具集成
```

### 商業化
```
✓ OEM 嵌入授權
✓ SaaS 訂閱
✓ 企業支持合約
✓ 定制開發服務
```

---

## 🎯 核心功能

### 工具集

| 工具 | 功能 | 時間 |
|------|------|------|
| `explore_design_space` | 快速可行性檢查 | <3s |
| `characterize_device` | gm/Id 掃描 | <5s |
| `recall_designs` | 查詢設計資料庫 | <1s |
| `query_device_table` | 單點設備指標 | <1s |
| `size_analog_block` | 完整 BSIM4 模擬 | 55s |

### 支持的電路

目前：
- ✅ Miller OTA (兩級)
- ✅ Folded-Cascode OTA
- ✅ 五晶體 OTA

計劃中：
- 🔜 低功耗 OTA
- 🔜 寬擺幅 OTA
- 🔜 比較器
- 🔜 放大器

---

## 💰 定價

### 開源（MIT 許可）

```
✓ 完全免費
✓ 自由使用和修改
✓ 社區支持
✓ 無商業保證
```

### 商業許可

```
✓ 企業級支持
✓ 優先錯誤修復
✓ 定制開發
✓ 源代碼訪問

初期：$50K-$500K
年度：$20K-$100K
```

詳見 [商業授權](COMMERCIAL.md)

---

## 🔗 聯絡方式

### 支持和反饋

- **GitHub Issues**: [報告錯誤或請求功能](https://github.com/musicjazz5/spark-spice-marketplace/issues)
- **Email**: musicjazz5@gmail.com
- **Discussions**: [GitHub Discussions](https://github.com/musicjazz5/spark-spice-marketplace/discussions)

### 商業合作

- **企業許可**: businessdev@musicjazz5.com
- **技術諮詢**: support@musicjazz5.com
- **合作機會**: partnerships@musicjazz5.com

---

## 📄 許可

spark-spice 在 MIT 許可下發佈。詳見 [LICENSE](LICENSE) 文件。

商業使用需要商業許可。詳見 [COMMERCIAL.md](COMMERCIAL.md)。

---

## 🤝 貢獻

我們歡迎所有貢獻！請閱讀 [CONTRIBUTING.md](CONTRIBUTING.md) 瞭解如何參與。

---

## 📚 引用

如果您在研究中使用 spark-spice，請引用：

```bibtex
@software{spark-spice-2024,
  author = {musicjazz5},
  title = {spark-spice: Analog Circuit Design with Razavi gm/Id},
  year = {2024},
  url = {https://github.com/musicjazz5/spark-spice-marketplace}
}
```

---

## 🎓 致謝

- Razavi 教科書《CMOS 模擬集成電路設計》
- Anthropic Claude API
- BSIM4 工藝模型
- 開源社區

---

**最後更新**: 2024-10-01  
**版本**: 1.0.0  
**開發者**: musicjazz5  

---

**準備好了嗎？** → [快速開始](QUICK_REFERENCE.md)  
**想了解更多？** → [完整文檔](/.claude/RAZAVI_GMID_GUIDE.md)  
**需要商業授權？** → [聯絡我們](COMMERCIAL.md)
