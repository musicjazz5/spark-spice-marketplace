# Contributing to spark-spice

感謝您對 spark-spice 的興趣！這份文件說明如何貢獻。

## 行為準則 (Code of Conduct)

本專案採用 Contributor Covenant 行為準則。參與即表示同意遵守準則。

## 貢獻方式

### 報告錯誤 (Bug Reports)

提交 Issue 時包含：
- ✓ spark-spice 版本
- ✓ 複製步驟
- ✓ 預期行為
- ✓ 實際行為
- ✓ 系統信息（OS, Python version, etc.)

### 提交改進 (Enhancement Requests)

描述：
- ✓ 目前的限制
- ✓ 建議的功能
- ✓ 為什麼這有幫助
- ✓ 可能的實施方式

### 代碼貢獻 (Pull Requests)

1. **Fork** 本倉庫
2. **建立分支** (`git checkout -b feature/amazing-feature`)
3. **提交改動** (`git commit -m 'Add amazing feature'`)
4. **推送分支** (`git push origin feature/amazing-feature`)
5. **開啟 Pull Request**

#### PR 提交清單

- [ ] 代碼遵循專案風格指南
- [ ] 已添加適當的文檔
- [ ] 已添加或更新測試
- [ ] 所有測試通過
- [ ] 沒有添加新的警告
- [ ] 更新了 CHANGELOG.md

## 開發設定

### 環境要求
```bash
Python 3.8+
anthropic SDK >= 0.28.0
pytest >= 7.0.0
```

### 本機開發

```bash
# Clone 倉庫
git clone https://github.com/musicjazz5/spark-spice-marketplace.git
cd spark-spice-marketplace

# 建立虛擬環境
python3 -m venv venv
source venv/bin/activate

# 安裝依賴
pip install -r requirements.txt

# 運行測試
pytest tests/

# 運行範例
python examples/basic_design.py
```

## 測試

所有提交必須通過測試：

```bash
# 運行所有測試
pytest tests/ -v

# 檢查覆蓋率
pytest --cov=src tests/

# 檢查代碼風格
flake8 src/
black --check src/
```

## 提交信息指南

使用清晰、簡潔的提交信息：

```
[Type] Brief description

Detailed explanation if needed.

- Point 1
- Point 2

Co-Authored-By: Name <email@example.com>
```

### 提交類型 (Commit Types)

- `feat:` 新功能
- `fix:` 錯誤修復
- `docs:` 文檔更新
- `style:` 代碼風格
- `refactor:` 重構
- `test:` 測試
- `perf:` 性能改進

## 版本編號 (Versioning)

使用語義版本 (SemVer)：`MAJOR.MINOR.PATCH`

- **MAJOR**: 不兼容的 API 變化
- **MINOR**: 向後兼容的新功能
- **PATCH**: 向後兼容的錯誤修復

## 文檔

- 在代碼中添加文檔字符串
- 更新 README 中的相關部分
- 保持 CHANGELOG.md 最新

## 聯絡

- **Issues**: GitHub Issues (公開討論)
- **Email**: musicjazz5@gmail.com (私密詢問)
- **Discussions**: GitHub Discussions (設計提案)

## 商業合作

對於商業授權、合作或定制開發：
📧 musicjazz5@gmail.com

---

感謝您的貢獻！🙏
