# Hướng Dẫn Sử Dụng Nhanh

## 🚀 Cách Chạy

### Cách 1: Chạy với Menu (Khuyến nghị)

Chỉ cần gõ:
```bash
run.bat
```

Sẽ hiển thị menu:
```
===============================================================================
                           CHỌN CHỨC NĂNG
===============================================================================

  1. Train models mới và lưu (khuyến nghị lần đầu)
  2. Load models đã lưu (nhanh hơn)
  3. Train models mới không lưu
  4. Tạo Dashboard (cần có models đã train)
  5. Thoát

===============================================================================

Nhập lựa chọn (1-5):
```

### Cách 2: Chạy với Tham Số

```bash
# Train và lưu models (lần đầu tiên)
run.bat --save

# Load models đã lưu (lần sau - nhanh hơn)
run.bat --load

# Tạo dashboard
run.bat --dashboard
```

---

## ⏱️ Thời Gian Chạy

| Chế độ | Thời gian | Ghi chú |
|--------|-----------|---------|
| **Train mới** | ~8-10 phút | Lần đầu tiên |
| **Load models** | ~45 giây | Đã có models |
| **Dashboard** | ~1 phút | Sau khi train |

---

## 📊 Kết Quả Mẫu

```
================================================================================
                    BẢNG SO SÁNH KẾT QUẢ
================================================================================
Model                     Accuracy     F1 Score     AUC          Time (s)
--------------------------------------------------------------------------------
Logistic Regression       0.9518       0.9518       0.9886       27.48
XGBoost                   0.9943       0.9943       0.9998       13.66
================================================================================

✓ MODEL TỐT NHẤT: XGBoost
  - Accuracy: 0.9943
  - F1 Score: 0.9943
  - Training Time: 13.66s
```

---

## 🎯 Workflow Khuyến Nghị

### Lần Đầu Tiên:
1. Chạy `run.bat`
2. Chọn `1` (Train và lưu models)
3. Đợi ~8-10 phút
4. Models được lưu vào `spark_models/`

### Lần Sau:
1. Chạy `run.bat`
2. Chọn `2` (Load models)
3. Chỉ mất ~45 giây

### Xem Dashboard:
1. Chạy `run.bat`
2. Chọn `4` (Tạo dashboard)
3. Mở `dashboard.html` trong trình duyệt

---

## 📁 Cấu Trúc Models

Sau khi train, các models được lưu trong:
```
spark_models/
├── pipeline_model/        # Preprocessing pipeline
├── logistic_regression/   # Logistic Regression model
└── xgboost/              # XGBoost model
```

Bạn có thể xóa thư mục `spark_models/` để train lại từ đầu.

---

## ❓ FAQ

### Q: Models bị lỗi, muốn train lại?
**A:** Xóa thư mục `spark_models/` và chạy lại với option 1

### Q: Tại sao Load models nhanh hơn?
**A:** Vì không cần train lại, chỉ load và evaluate

### Q: Dashboard không hiển thị đúng dữ liệu?
**A:** Chạy lại option 4 để tạo lại file `results.json`

### Q: Có thể dừng giữa chừng không?
**A:** Có, nhấn `Ctrl+C` để dừng. Models chỉ được lưu khi hoàn tất.

---

## 🔧 Troubleshooting

### Lỗi: "Virtual environment Python 3.11 chưa được cài đặt"
```bash
setup_python311.bat
```

### Lỗi: "HADOOP_HOME is not set"
```bash
install_hadoop.bat
```

### Lỗi: "No module named 'xgboost'"
```bash
venv311\Scripts\pip.exe install xgboost
```

---

## 💡 Tips

- ✅ Lần đầu chạy: Chọn option 1 (Train và lưu)
- ✅ Lần sau: Chọn option 2 (Load models) để tiết kiệm thời gian
- ✅ Muốn xem trực quan: Chọn option 4 (Dashboard)
- ✅ Ctrl+C để dừng bất cứ lúc nào
