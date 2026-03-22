import time
import random
import matplotlib.pyplot as plt
import sys


# Tăng giới hạn đệ quy để tránh lỗi trường hợp chạy mảng lớn
sys.setrecursionlimit(5000)


# 1. Vét cạn thuần túy - O(n^2)
def brute_force_basic(arr):
   max_sum = -float('inf')
   n = len(arr)
   for i in range(n):
       curr = 0
       for j in range(i, n):
           curr += arr[j]
           if curr > max_sum: max_sum = curr
   return max_sum


# 2. Chia để trị - O(n log n)
def divide_and_conquer(arr, l, h):
   if l == h: return arr[l]
   m = (l + h) // 2
  
   # Hàm tìm tổng xuyên tâm
   def cross(l, m, h):
       sm = 0; left = -float('inf')
       for i in range(m, l-1, -1):
           sm += arr[i]; left = max(left, sm)
       sm = 0; right = -float('inf')
       for i in range(m+1, h+1):
           sm += arr[i]; right = max(right, sm)
       return left + right
      
   return max(divide_and_conquer(arr, l, m),
              divide_and_conquer(arr, m+1, h),
              cross(l, m, h))


# 3. Quy hoạch động (Kadane) - O(n)
def kadane(arr):
   max_so_far = current_max = arr[0]
   for x in arr[1:]:
       current_max = max(x, current_max + x)
       max_so_far = max(max_so_far, current_max)
   return max_so_far


# 4.1 Prefix Sum bản Vét cạn - O(n^2)
def prefix_sum_brute_force(arr):
   n = len(arr)
   P = [0] * (n + 1)
   for i in range(n):
       P[i+1] = P[i] + arr[i]
  
   max_sum = -float('inf')
   for i in range(n):
       for j in range(i, n):
           current_sum = P[j+1] - P[i]
           if current_sum > max_sum:
               max_sum = current_sum
   return max_sum

# 4.2 Prefix Sum - O(n)
def prefix_sum_method(arr):
   min_pre, pre, res = 0, 0, -float('inf')
   for x in arr:
       pre += x
       res = max(res, pre - min_pre)
       min_pre = min(min_pre, pre)
   return res

# --- CHẠY THỬ NGHIỆM ---
# Lưu ý: n không nên quá 2000 vì O(n^2) sẽ ảnh hưởng đến tốc độ chạy
#sizes = [100, 300, 600, 1000, 1500, 2000]
sizes = [100, 500, 1000, 2000, 3000, 4000, 5000]
data = { "Brute Force O(n^2)": [],
        "Divide & Conquer O(n log n)": [],
        "Kadane O(n)": [],
        "Prefix Sum O(n^2)": [],
        "Prefix Sum O(n)": [] }


print("Đang chạy thử nghiệm... vui lòng đợi khoảng 10-20 giây.")


for n in sizes:
   test_arr = [random.randint(-100, 100) for _ in range(n)]
  
   # 1. Đo Brute Force
   s = time.time(); brute_force_basic(test_arr); data["Brute Force O(n^2)"].append(time.time()-s)
  
   # 2. Đo Divide & Conquer
   s = time.time(); divide_and_conquer(test_arr, 0, n-1); data["Divide & Conquer O(n log n)"].append(time.time()-s)
  
   # 3. Đo Kadane
   s = time.time(); kadane(test_arr); data["Kadane O(n)"].append(time.time()-s)
  
   # 4.1 Đo Prefix Sum O(n^2)
   s = time.time(); prefix_sum_brute_force(test_arr); data["Prefix Sum O(n^2)"].append(time.time()-s)
   
   # 4.2 Đo Prefix Sum O(n)
   s = time.time(); prefix_sum_method(test_arr); data["Prefix Sum O(n)"].append(time.time()-s)
  
   print(f"Hoàn thành kích thước n = {n}")


# --- VẼ ĐỒ THỊ ---
plt.figure(figsize=(10, 6))
plt.plot(sizes, data["Brute Force O(n^2)"], 'r-o', label="Brute Force (n^2)")
plt.plot(sizes, data["Prefix Sum O(n^2)"], 'm-s', label="Prefix Sum (n^2)")
plt.plot(sizes, data["Prefix Sum O(n)"], 'y-s', label="Prefix Sum (n)")
plt.plot(sizes, data["Divide & Conquer O(n log n)"], 'g-^', label="Divide & Conquer (n log n)")
plt.plot(sizes, data["Kadane O(n)"], 'b-x', label="Kadane (n)")


plt.title('SO SÁNH THỰC TẾ 4 CHIẾN LƯỢC')
plt.xlabel('Kích thước mảng (n)')
plt.ylabel('Thời gian (giây)')
plt.legend()
plt.grid(True)
plt.show()
