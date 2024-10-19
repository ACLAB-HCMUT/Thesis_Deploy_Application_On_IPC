import customtkinter
from tkcalendar import Calendar

class CalendarView(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        # Tạo lịch và nhúng vào frame của CustomTkinter
        self.calendar = Calendar(self, selectmode='day', year=2024, month=10, day=18)
        self.calendar.pack(pady=20, padx=20)

        # Nút để lấy ngày đã chọn
        self.get_date_button = customtkinter.CTkButton(self, text="Get Date", command=self.get_selected_date)
        self.get_date_button.pack(pady=10)

        # Hiển thị ngày được chọn
        self.selected_date_label = customtkinter.CTkLabel(self, text="")
        self.selected_date_label.pack(pady=10)

    def get_selected_date(self):
        date = self.calendar.get_date()
        self.selected_date_label.configure(text=f"Selected Date: {date}")

# Tạo ứng dụng CustomTkinter
app = customtkinter.CTk()
app.geometry("400x400")
calendar_view = CalendarView(app)
app.mainloop()
