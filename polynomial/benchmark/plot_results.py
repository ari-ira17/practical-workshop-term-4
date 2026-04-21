import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("benchmark/results.csv")

plt.figure(figsize=(10, 6))
plt.bar(df["Подход"], df["Mean"], color=['#e74c3c', '#3498db', '#2ecc71', '#f1c40f'], edgecolor='black')

plt.title('Сравнение производительности (среднее время 100к вызовов)')
plt.ylabel('Время (секунды)')
plt.grid(axis='y', linestyle='--', alpha=0.7)

for i, v in enumerate(df["Mean"]):
    plt.text(i, v + (max(df["Mean"])*0.02), f"{v:.4f}s", ha='center', fontweight='bold')

plt.savefig("benchmark/performance_plot.png")
print("График сохранен в benchmark/performance_plot.png")
