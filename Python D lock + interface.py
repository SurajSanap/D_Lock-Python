import tkinter as tk
from PIL import ImageTk, Image
import time

# Global variable to track password visibility
password_visible = False

def hour_min():
    current_time = time.localtime()
    return current_time.tm_hour, current_time.tm_min


def sum_of_digits(num):
    sum_val = 0
    while num != 0:
        x = num % 10
        sum_val += x
        num = num // 10
    return sum_val


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def function2(minute):
    final_prime = 0
    k = 1
    for i in range(950000101, 0, -18):
        if k == minute:
            break
        if i % 10 != 5:
            if sum_of_digits(i) == 16:
                if is_prime(i):
                    final_prime = i
                    k += 1
    return final_prime


def function1(power):
    final_prime = 0
    for i in range(59, 1000000000, 18):
        if i < power:
            continue
        if i % 10 != 5:
            if sum_of_digits(i) == 14:
                if is_prime(i):
                    final_prime = i
                    break
    return final_prime


def my_pow(x, n):
    ans = 1.0
    nn = abs(n)
    while nn:
        if nn % 2:
            ans *= x
            nn -= 1
        else:
            x *= x
            nn //= 2
    if n < 0:
        ans = 1.0 / ans
    return ans


def check(hour, minute, day, month, year):
    sum_val = hour + minute + day + month + year
    power = sum_val % 10
    if power == 0 or power == 1:
        power = 5
    elif power == 2:
        power = 6
    elif power == 3:
        power = 7
    elif power == 4:
        power = 8

    limit = my_pow(10, power)

    temp1 = function1(limit) % 10000 + function1(limit) // 10000
    temp2 = function2(minute) % 10000 + function2(minute) // 10000

    ans = (temp1 + temp2 + year + minute + hour) % 10000
    return ans


def unlock():
    global status_label
    hour, minute = hour_min()
    current_time = time.localtime()
    day = current_time.tm_mday
    month = current_time.tm_mon + 1
    year = current_time.tm_year + 1900

    password = int(password_entry.get())

    if check(hour, minute, day, month, year) == password:
        status_label.config(text="Unlocked", fg="green")
    else:
        status_label.config(text="Incorrect Password", fg="red")


def toggle_password_visibility():
    global password_visible
    password_visible = not password_visible

    if password_visible:
        password_entry.config(show="")
    else:
        password_entry.config(show="*")


def update_timer():
    current_time = time.strftime("%H:%M:%S")
    timer_label.config(text=current_time)
    move_timer_label()
    timer_label.after(1000, update_timer)


def move_timer_label():
    global direction
    x = timer_label.winfo_rootx() + 10
    y = timer_label.winfo_rooty() + 5 * direction
    if y <= 0 or y >= window.winfo_screenheight() - timer_label.winfo_height():
        direction *= -1
    timer_label.place(x=x, y=y)
    timer_label.after(50, move_timer_label)


# Create the main window
window = tk.Tk()
window.title("Password Unlock")

# Load the background image
bg_image = ImageTk.PhotoImage(Image.open("lockimg.jpg"))
image_width = bg_image.width()
image_height = bg_image.height()

# Set the window size to match the background image
window.geometry(f"{image_width}x{image_height}")

# Set the background image as the window background
bg_label = tk.Label(window, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create the password entry widget
password_label = tk.Label(window, text="Enter the password:", font=("semibold", 12), fg="red")
password_label.pack(pady=10)
password_entry = tk.Entry(window, show="*", font=("Arial", 12), fg="blue")
password_entry.pack()

# Create the password visibility toggle button
toggle_button = tk.Button(window, text="Show Password", command=toggle_password_visibility, font=("Arial", 10), fg="blue")
toggle_button.pack(pady=5)

# Create the unlock button
unlock_button = tk.Button(window, text="Unlock", command=unlock, font=("Arial", 10), fg="blue")
unlock_button.pack(pady=5)

# Create the status label
status_label = tk.Label(window, text="", font=("Arial", 20))
status_label.pack()

# Create the timer label
direction = 1  # Direction of the floating animation
timer_label = tk.Label(window, text="", font=("Arial", 25), fg="blue")
timer_label.pack(pady=20)

# Start the timer
update_timer()

# Start the Tkinter event loop
window.mainloop()
