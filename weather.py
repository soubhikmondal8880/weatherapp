from tkinter import *
from tkinter import ttk
import requests
import threading
import time

win = Tk()
win.title("Weather App")
win.geometry("500x600")
win.configure(bg="#c1ede6")  
win.resizable(False, False)


title = Label(win, text="🌤️ Weather App", font=("Helvetica", 26, "bold"), bg="#c1ede6", fg="#1f3b3a")
title.pack(pady=30)


cities = ["Kolkata", "Delhi", "Mumbai", "Chennai", "Bengaluru", "Hyderabad", "Ahmedabad", "Pune", "Jaipur", "Lucknow", "Bhopal"]
city_combo = ttk.Combobox(win, values=cities, font=("Helvetica", 14), state="readonly")
city_combo.set("Select City")
city_combo.pack(pady=10, ipady=5)


info_labels = {}
def create_info_label(text):
    frame = Frame(win, bg="#c1ede6")
    frame.pack(pady=8)
    label_title = Label(frame, text=text, font=("Helvetica", 14, "bold"), bg="#c1ede6", fg="#1f3b3a")
    label_title.pack(side=LEFT, padx=8)
    label_value = Label(frame, text="--", font=("Helvetica", 14), bg="#ffffff", fg="#1f3b3a", width=20, relief=FLAT, bd=1)
    label_value.pack(side=LEFT, padx=8)
    return label_value

info_labels["Climate"] = create_info_label("Climate:")
info_labels["Description"] = create_info_label("Description:")
info_labels["Temperature"] = create_info_label("Temperature:")
info_labels["Pressure"] = create_info_label("Pressure:")


def show_loader():
    loader = Label(win, text="Fetching Data...", font=("Helvetica", 16), bg="#c1ede6", fg="#1f3b3a")
    loader.pack(pady=20)
    return loader

def hide_loader(loader):
    loader.pack_forget()


def change_bg_color(new_color):
    def transition():
        current_color = win.cget('bg')
        for i in range(100):
            blended_color = blend_colors(current_color, new_color, i / 100)
            win.configure(bg=blended_color)
            win.update()
            time.sleep(0.03)

    threading.Thread(target=transition).start()

def blend_colors(color1, color2, blend_factor):
    color1 = win.winfo_rgb(color1)
    color2 = win.winfo_rgb(color2)
    blended = tuple(int(c1 + (c2 - c1) * blend_factor) for c1, c2 in zip(color1, color2))
    return f"#{blended[0]:04x}{blended[1]:04x}{blended[2]:04x}"


def get_weather():
    city = city_combo.get()
    if city == "Select City":
        info_labels["Climate"].config(text="Select a city")
        return

    api_key = "e9c4a73b3b7d34a5997c2b276da03d45"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    loader = show_loader()
    
    def fetch():
        try:
            res = requests.get(url)
            data = res.json()
            if data.get("cod") != 200:
                info_labels["Climate"].config(text="City not found")
                return

            values = {
                "Climate": data["weather"][0]["main"],
                "Description": data["weather"][0]["description"].title(),
                "Temperature": f"{data['main']['temp']} °C",
                "Pressure": f"{data['main']['pressure']} hPa"
            }

            for key in info_labels:
                info_labels[key].config(text=values[key])

            if "Clear" in values["Climate"]:
                change_bg_color("#FFEB3B")  
            elif "Rain" in values["Climate"]:
                change_bg_color("#2196F3") 
            elif "Cloud" in values["Climate"]:
                change_bg_color("#81C784")  
            else:
                change_bg_color("#f8bbd0")  
        except Exception:
            info_labels["Climate"].config(text="Error")
        finally:
            hide_loader(loader)

    threading.Thread(target=fetch).start()


get_button = Button(win, text="Get Weather", font=("Helvetica", 14, "bold"), bg="#0fa3a6", fg="white", activebackground="#0b8c8f", relief=FLAT, command=get_weather)
get_button.pack(pady=30, ipadx=10, ipady=6)

win.mainloop()
