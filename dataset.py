from sklearn.datasets import load_breast_cancer
import pandas as pd

# بارگذاری دیتاست
data = load_breast_cancer()

# تبدیل داده‌ها به DataFrame
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target  # اضافه کردن ستون برچسب‌ها (خوش‌خیم یا بدخیم)

# نمایش ستون‌ها برای بررسی
print("ستون‌های دیتافریم:")
print(df.columns)

# نمایش چند نمونه از داده‌ها
print("\nنمونه‌ای از داده‌ها:")
print(df.head())

# ذخیره به فایل CSV
csv_file_path = "breast_cancer_dataset.csv"  # مسیر و نام فایل CSV
df.to_csv(csv_file_path, index=False)


