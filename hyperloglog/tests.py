from algorithm import Hyperloglog

data = ["user_" + str(i) for i in range(1000)]

hll = Hyperloglog(eps=0.02)
estimated = hll.hyperloglog_estimate(data)
print(f"Оценка кардинальности: {estimated}") 