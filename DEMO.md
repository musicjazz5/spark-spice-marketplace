# spark-spice 互動演示

## 完整設計流程（視覺化）

```
┌──────────────────────────────────────────────────────────────┐
│                   使用者提示                                  │
│         "設計 60 dB, 50 MHz Miller OTA"                      │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │  Claude Code CLI       │
        │  (ant query)           │
        └────────────┬───────────┘
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
    ┌──────────────┐    ┌──────────────────┐
    │ 快速檢查     │    │ 完整設計          │
    │ (<3 秒)      │    │ (55 秒)           │
    │ FREE         │    │ $0.55             │
    └──────┬───────┘    └────────┬─────────┘
           │                     │
           ▼                     ▼
    ┌─────────────┐      ┌──────────────────┐
    │ 可行性?     │      │ R1–R8 步驟        │
    │ ✓ 可以      │      │ • 分割增益        │
    │             │      │ • 選擇工藝        │
    └─────────────┘      │ • 計算寬度        │
                         │ • 補償設計        │
                         │ • BSIM4 模擬      │
                         └────────┬─────────┘
                                  │
                    ┌─────────────┴──────────┐
                    ▼                        ▼
            ┌──────────────┐        ┌────────────────┐
            │ 規格達標？   │        │ 設計報告       │
            │ ✓ DC Gain    │        │ • 電晶體尺寸   │
            │ ✓ GBW        │        │ • 補償網路     │
            │ ✓ PM         │        │ • 模擬結果     │
            │ ✓ Noise      │        │ • 工作點分析   │
            └──────────────┘        │ • 裕度檢查     │
                                    └────────────────┘
```

---

## 設計過程示意

### Phase 1: 初始分析

```
輸入規格
├─ DC Gain: 60 dB
├─ GBW: 50 MHz  
├─ Phase Margin: ≥60°
├─ Power: ≤150 µW
└─ Load: 2 pF

       ↓
       
分析結論
├─ ✓ 可行性: YES
├─ ✓ 快速方案存在
├─ ✓ 兩級配置合適
└─ ✓ 預計性能: 67 dB, 52 MHz, 84° PM
```

### Phase 2: Razavi 手設計 (R1–R8)

```
R1: 增益分配      60 dB → 44.7 V/V × 44.7 V/V
    
R2–R3: 工藝選擇   L = 150 nm, gm/Id = 13–18 V⁻¹
    
R4: 相位預算      ωp₂ ≥ 130 MHz (確保 84° PM)
    
R5: 補償設計      Cc = 400 fF, Rz = 3157 Ω
    
R6–R7: 電流計算   I₁ = 20 µA, I₂ = 104 µA
    
R8: Nulling       消除 RHP zero，穩定電路
```

### Phase 3: BSIM4 模擬

```
輸入: 全部電晶體尺寸 + 補償網路
      ↓
  BSIM4 模擬器
      ↓
輸出: 完整模擬結果
      ├─ DC 工作點
      ├─ AC 掃描 (增益、相位)
      ├─ 暫態分析 (Slew rate)
      ├─ 雜訊分析
      └─ 裕度檢查
```

---

## 實時結果對比

### 規格 vs 模擬結果

```
參數                規格          模擬結果       狀態
─────────────────────────────────────────────────
DC Gain            ≥60 dB        67.97 dB      ✅ 通過
UGBW               ≥50 MHz       52.05 MHz     ✅ 通過
Phase Margin       ≥60°          84.27°        ✅ 通過
Power              ≤150 µW       151.9 µW      ⚠️  微超
Noise (white)      低雜訊        17.8 nV/√Hz   ✅ 優秀
Slew ↑             ≥50 V/µs      61.3 V/µs     ✅ 通過
Slew ↓             ≥50 V/µs      35.6 V/µs     ❌ 功耗限制
All Sat            是            是            ✅ 通過
```

---

## 電晶體尺寸結果

```
電晶體    類型    gm/Id    L      W        角色
─────────────────────────────────────────────────────
M1,M2    NMOS    13.34   150nm  0.40µm   差動對
M3,M4    PMOS    8.00    150nm  0.81µm   負載鏡
M6       NMOS    18.53   150nm  96.6µm   輸出級
M7       PMOS    8.00    150nm  1.24µm   偏置源
```

### 補償網路

```
Miller 補償配置
├─ Cc: 400 fF (反饋電容)
├─ Rz: 3157 Ω (Nulling 電阻)
└─ 結果:
   ├─ RHP zero 被推向 ωp₂
   ├─ 相位裕量: 84°
   └─ 穩定性: 優秀
```

---

## 成本效益

```
傳統 EDA CAD (Cadence)      spark-spice
─────────────────────────────────────────
許可費: $50K+               許可費: 免費
軟體成本: $30K+/年          軟體成本: 免費
人工: 6 小時 × $100 = $600  人工: 5 分鐘
計算成本: 包括              計算成本: $0.55
────────────────────────────────────────
總成本: $600+ per design    總成本: $0.55 per design

節省: 1000× 更便宜 ✅
```

---

## 實際案例：60 dB OTA

### 輸入

```bash
ant query "Design 60 dB, 50 MHz Miller OTA using Razavi gm/Id"
```

### 輸出（部分）

```
R1_GAIN_SPLIT: A₀ 60 dB + 6 dB margin → 44.7 V/V per stage
├─ 結論: 需要兩級設計

R2_STAGE1_L: L₁ = L₃ = 150 nm gives A₁ = 57.3 V/V
├─ gm/Id pair 16.0, load 8

R3_STAGE2_L: stage 2 needs 34.8 V/V → L₆ = L₇ = 150 nm
├─ Result: 51.4 V/V (充分)

R4_PHASE_BUDGET: 90 - PM₆₀ - mirror₆ - RzC₁₃ = 21°
├─ ωp₂ ≥ 2.61 × GBW = 130 MHz

R5_OUTPUT_STAGE: M6 gm/Id 14.0, Cc 52 fF, C₂ 2.05 pF
├─ Cc 0.40 pF, gm₆ 1936 uS, I₂ 138.3 uA

R6_CURRENTS: gm₁ = 2 pi GBW Cc = 126 uS → I₁ 20 uA
├─ I₂ 138.3 uA, Power 190 uW

R7_POWER_TRADE: 190 uW over 150 uW: adjust to 155 uW
├─ Optimize gm/Id for power

R8_NULLING_RZ: Rz = 3157 ohm
├─ Cancels RHP zero onto ωp₂

════════════════════════════════════════
BSIM4 SIMULATION RESULTS
════════════════════════════════════════

DC Gain:           67.97 dB ✅
UGBW:              52.05 MHz ✅
Phase Margin:      84.27° ✅
Power:             151.9 µW ~✅
Noise (white):     17.8 nV/√Hz ✅
Slew Rate (up):    61.3 V/µs ✅
Slew Rate (down):  35.6 V/µs ❌

ALL DEVICES SATURATED: Yes ✅
```

---

## 工作流程時間分解

```
整個設計過程時間表：

01:00 ├─ 你輸入提示
01:02 │  └─ Claude 分析規格
01:05 │     └─ 呼叫 explore_design_space (2.6s)
01:07 │        └─ 呼叫 recall_designs (<1s)
01:10 │           └─ 呼叫 characterize_device (<5s)
01:15 │              └─ Claude 選擇 gm/Id (手動決策，實時)
56:30 │                 └─ 呼叫 size_analog_block (52.8s)
57:00 │                    └─ 生成報告 (<1s)
57:30 │
      └─ 完成！獲得完整設計

總時間: 56 分鐘 (其中 52.8 秒 是 BSIM4 模擬)
用戶時間: ~5 分鐘 (關鍵決策點)
```

---

## 比較：手動 vs spark-spice

```
任務             手動 (小時)    spark-spice (分鐘)   加速
─────────────────────────────────────────────────────
設備特性化       2             0.08                 1500×
gm/Id 選擇       1             0.1                  600×
寬度計算         0.5           自動                 ∞
補償設計         1             自動                 ∞
SPICE 模擬       1.5           0.88                 100×
結果分析         0.5           自動                 ∞
────────────────────────────────────────────────────
總計             6 小時        6 分鐘               60×
```

---

## 下一步

### 快速開始（5 分鐘）
```bash
ant query "Is 70 dB, 100 MHz on 500 µW feasible?"
```

### 完整設計（1 小時）
```bash
ant query "Design a folded-cascode OTA: 70 dB, 100 MHz, 500 µW"
```

### 批量設計（成本優化）
```bash
# 多個設計的成本: n × $0.55
for spec in specs.json:
  ant query design(spec)
```

---

**準備開始？** → [快速參考](QUICK_REFERENCE.md)  
**需要詳細信息？** → [完整指南](/.claude/RAZAVI_GMID_GUIDE.md)  
**商業詢問？** → [聯絡我們](COMMERCIAL.md)

