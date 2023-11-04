from tkinter import *
import requests
import smtplib
from tkinter import messagebox
import os

news_url = "https://newsapi.org/v2/everything"
news_api_key = os.environ["API_KEY"]


def question_button_clicked():
    messagebox.showinfo(title="How to use:",
                        message="1. Enter valid company name.\n2. After that click on send me mail.\n3. It will send "
                                "you Top 3 news of the Company.")


def send_mail():
    user_popup_ask = messagebox.askokcancel(title="Send Mail",
                                            message="Finally send mail?\nThis action can't be rolled back!")
    if user_popup_ask:

        company_name = company_name_entry.get()

        news_parameters = {
            "q": company_name,
            "sortBy": "popularity",
            "apikey": news_api_key
        }

        response_news = requests.get(url=news_url, params=news_parameters)
        response_news.raise_for_status()
        news_articles = response_news.json()["articles"]

        articles = []

        for index in range(3):
            article = f"Headline: {news_articles[index]['title']}\n\nDescription: {news_articles[index]['description']}\n\n"
            articles.append(article)

        news1 = articles[0]
        news2 = articles[1]
        news3 = articles[2]

        message = f"1. {news1}\n2. {news2}\n3. {news3}"

        subject = f"Subject:{company_name} News"
        message = message.encode('utf-8')

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_mail, password=my_pass)
            connection.sendmail(from_addr=my_mail, to_addrs=receiver_mail,
                                msg=subject.encode('utf-8') + b'\n\n' + message)
        print("Mail sent successfully!")


my_mail = os.environ["MY_EMAIL"]
my_pass = os.environ["MY_PASS"]

receiver_mail = "Email where you want to get news"

window = Tk()
window.config(pady=40, padx=30)
window.title("Stock Market News GUI")
window.minsize(width=840, height=400)

image_canvas = Canvas(width=320, height=158)
image_canvas.grid(row=1, column=1)

stock_market_news_label = Label(text="Stock-Market News", width=17, font=("Arial", 20, 'bold'), bg="#2c3e50",
                                fg="#ecf0f1")
stock_market_news_label.grid(row=0, column=1, pady=30)

company_name_label = Label(text="Company Name: ", font=("Arial", 10))
company_name_label.grid(row=2, column=0)

company_name_entry = Entry(width=30)
company_name_entry.grid(row=2, column=1, pady=30)

img = PhotoImage(file="Newslogo.png")

image_canvas.create_image(160, 79, image=img)

question_button = Button(text="❓", command=question_button_clicked, fg="white", bg="#687EFF")
question_button.grid(row=2, column=3)

send_me_mail = Button(text="Send Me Mail", font=("Arial", 12), width=20, command=send_mail, fg="white", bg="#27ae60")
send_me_mail.grid(row=3, column=1)

window.mainloop()
