import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
import numpy  # type: ignore
from keras.models import load_model  # type: ignore

# Tải model đã huấn luyện
model = load_model('my_model.h5')

# Danh sách các loại biển báo
# classes = {
#     1: 'Speed limit (20km/h)', 2: 'Speed limit (30km/h)', 3: 'Speed limit (50km/h)', 4: 'Speed limit (60km/h)',
#     5: 'Speed limit (70km/h)', 6: 'Speed limit (80km/h)', 7: 'End of speed limit (80km/h)', 8: 'Speed limit (100km/h)',
#     9: 'Speed limit (120km/h)', 10: 'No passing', 11: 'No passing veh over 3.5 tons',
#     12: 'Right-of-way at intersection', 13: 'Priority road', 14: 'Yield', 15: 'Stop', 16: 'No vehicles',
#     17: 'Veh > 3.5 tons prohibited', 18: 'No entry', 19: 'General caution', 20: 'Dangerous curve left',
#     21: 'Dangerous curve right', 22: 'Double curve', 23: 'Bumpy road', 24: 'Slippery road',
#     25: 'Road narrows on the right', 26: 'Road work', 27: 'Traffic signals', 28: 'Pedestrians',
#     29: 'Children crossing', 30: 'Bicycles crossing', 31: 'Beware of ice/snow', 32: 'Wild animals crossing',
#     33: 'End speed + passing limits', 34: 'Turn right ahead', 35: 'Turn left ahead', 36: 'Ahead only',
#     37: 'Go straight or right', 38: 'Go straight or left', 39: 'Keep right', 40: 'Keep left',
#     41: 'Roundabout mandatory', 42: 'End of no passing', 43: 'End no passing veh > 3.5 tons'
# }
classes = {
    1: 'Giới hạn tốc độ (20km/h)', 
    2: 'Giới hạn tốc độ (30km/h)', 
    3: 'Giới hạn tốc độ (50km/h)', 
    4: 'Giới hạn tốc độ (60km/h)', 
    5: 'Giới hạn tốc độ (70km/h)', 
    6: 'Giới hạn tốc độ (80km/h)', 
    7: 'Hết giới hạn tốc độ (80km/h)', 
    8: 'Giới hạn tốc độ (100km/h)', 
    9: 'Giới hạn tốc độ (120km/h)', 
    10: 'Cấm vượt', 
    11: 'Cấm vượt phương tiện trên 3.5 tấn',
    12: 'Nhường đường tại giao lộ', 
    13: 'Đường ưu tiên', 
    14: 'Nhường', 
    15: 'Dừng lại', 
    16: 'Cấm xe cộ', 
    17: 'Cấm xe > 3.5 tấn', 
    18: 'Cấm vào', 
    19: 'Cảnh báo chung', 
    20: 'Khúc cua nguy hiểm bên trái', 
    21: 'Khúc cua nguy hiểm bên phải', 
    22: 'Khúc cua đôi', 
    23: 'Đường gồ ghề', 
    24: 'Đường trơn', 
    25: 'Đoạn đường thu hẹp bên phải', 
    26: 'Công trường thi công', 
    27: 'Đèn tín hiệu giao thông', 
    28: 'Người đi bộ', 
    29: 'Trẻ em qua đường', 
    30: 'Xe đạp qua đường', 
    31: 'Cảnh báo băng tuyết', 
    32: 'Động vật hoang dã qua đường', 
    33: 'Hết giới hạn tốc độ + cấm vượt', 
    34: 'Rẽ phải phía trước', 
    35: 'Rẽ trái phía trước', 
    36: 'Chỉ đi thẳng', 
    37: 'Đi thẳng hoặc rẽ phải', 
    38: 'Đi thẳng hoặc rẽ trái', 
    39: 'Giữ phải', 
    40: 'Giữ trái', 
    41: 'Vòng xuyến bắt buộc', 
    42: 'Hết cấm vượt', 
    43: 'Hết cấm vượt phương tiện > 3.5 tấn'
}


# Giao diện chính
top = tk.Tk()
top.geometry('800x600')
top.title('Nhận dạng biển báo giao thông')
top.configure(background='#ffffff')

label = Label(top, background='#ffffff', font=('arial', 15, 'bold'))
sign_image = Label(top)

# Hàm xử lý nhiều ảnh
def classify_multiple(file_paths):
    for file_path in file_paths:
        image = Image.open(file_path)
        image = image.resize((30, 30))
        image = numpy.expand_dims(image, axis=0)
        image = numpy.array(image)

        pred_probabilities = model.predict(image)[0]
        pred = pred_probabilities.argmax(axis=-1)
        sign = classes[pred + 1]

        print(f"{file_path}: {sign}")

        # Hiển thị ảnh và kết quả
        uploaded = Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width() / 2.25), (top.winfo_height() / 2.25)))
        im = ImageTk.PhotoImage(uploaded)

        sign_image.configure(image=im)
        sign_image.image = im
        label.configure(foreground='#011638', text=sign)

        top.update()
        top.after(2000)  # Hiển thị 2 giây mỗi ảnh

# Nút upload nhiều ảnh
def upload_images():
    try:
        file_paths = filedialog.askopenfilenames()
        if file_paths:
            classify_multiple(file_paths)
    except:
        pass

# Nút chọn ảnh
upload = Button(top, text="Upload images", command=upload_images, padx=10, pady=5)
upload.configure(background='#c71b20', foreground='white', font=('arial', 10, 'bold'))

# Các thành phần giao diện
upload.pack(side=BOTTOM, pady=50)
sign_image.pack(side=BOTTOM, expand=True)
label.pack(side=BOTTOM, expand=True)

heading = Label(top, text="Nhận dạng biển báo giao thông", pady=10, font=('arial', 20, 'bold'),
                background='#ffffff', foreground='#364156')
heading1 = Label(top, text="Môn Học: Thị Giác Máy Tính và Ứng Dụng", pady=10, font=('arial', 20, 'bold'),
                 background='#ffffff', foreground='#364156')
heading2 = Label(top, text="Danh sách thành viên nhóm", pady=5, font=('arial', 20, 'bold'),
                 background='#ffffff', foreground='#364156')
heading3 = Label(top, text="Lê Minh Đăng MSSV: 21080991", pady=5, font=('arial', 20, 'bold'),
                 background='#ffffff', foreground='#364156')
heading4 = Label(top, text="Võ Hoàng Phi MSSV: 21038411", pady=5, font=('arial', 20, 'bold'),
                 background='#ffffff', foreground='#364156')

heading.pack()
heading1.pack()
heading2.pack()
heading3.pack()
heading4.pack()

# Bắt đầu giao diện
top.mainloop()


# code hoàn chỉnhss