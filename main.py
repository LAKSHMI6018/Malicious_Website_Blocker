import tkinter as tk
from tkinter import messagebox
import random
import string
import os
import time
import datetime
import smtplib
import requests
from email.message import EmailMessage

last_scanned_site = ""
last_scan_status = ""

HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
API_KEY = "113dc6883812b8f076fa6742e75734bd021976a58ebd9849359836fbb3586aa7"
def save_log(website, status, reason):
    with open("website_logs.txt", "a") as file:
        time = datetime.datetime.now()
        file.write(
            f"Date: {time}\n"
            f"Website: {website}\n"
            f"Status: {status}\n"
            f"Reason: {reason}\n"
            "----------------------\n"
        )
def send_email(receiver_email, password):

    sender_email = "lakshmi801929@gmail.com"

    app_password = "deuc mccp euix ihtn"

    msg = EmailMessage()

    msg["Subject"] = "Website Blocker Password"

    msg["From"] = sender_email
    msg["To"] = receiver_email

    msg.set_content(
f"""
Hello,

Your verification password is:

{password}

Use this password to continue.

Thank you.
"""
    )

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)

        return True

    except Exception as e:
        messagebox.showerror("Email Error", str(e))
        return False
def email_registered(email):
    try:
        with open("registered_emails.txt", "r") as file:
            emails = file.read().splitlines()

        return email in emails

    except FileNotFoundError:
        return False

# ---------------- VIRUSTOTAL API ----------------

def check_url_virustotal(url):

    headers = {
        "x-apikey": API_KEY
    }

    submit_url = "https://www.virustotal.com/api/v3/urls"

    try:
        response = requests.post(
            submit_url,
            headers=headers,
            data={"url": url}
        )

        if response.status_code != 200:
            return None

        analysis_id = response.json()["data"]["id"]

        time.sleep(3)

        report = requests.get(
            f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
            headers=headers
        )

        return report.json()

    except Exception as e:
        print(e)
        return None
    
def save_log(website, status, detections, reason):

    with open("logs.txt", "a") as file:

        file.write(
            f"""
==================================
Date : {datetime.datetime.now()}

Website : {website}

Status : {status}

Detections : {detections}

Reason : {reason}

==================================

"""
        )

# ---------------- REGISTER EMAIL ----------------

def register_window():

    w=tk.Toplevel(root)
    w.title("Register Email")
    w.geometry("400x250")
    w.configure(bg="black")

    tk.Label(w,text="REGISTER EMAIL",
             fg="#00FF00",
             bg="black",
             font=("Consolas",18,"bold")).pack(pady=10)


    email=tk.Entry(w,width=35)
    email.pack(pady=10)


    def save():

        mail=email.get()

        if mail=="":

            messagebox.showerror("Error","Enter Email")
            return


        with open("registered_emails.txt","a") as f:
            f.write(mail+"\n")


        messagebox.showinfo(
            "Success",
            "Email Registered Successfully"
        )



    tk.Button(
        w,
        text="REGISTER",
        command=save,
        bg="green",
        fg="white"
    ).pack(pady=20)



# ---------------- GENERATE PASSWORD ----------------


def generate_password():

    w = tk.Toplevel(root)
    w.title("Generate Password")
    w.geometry("400x250")
    w.configure(bg="black")

    tk.Label(
        w,
        text="REGISTERED EMAIL",
        fg="#00FF00",
        bg="black",
        font=("Consolas", 16)
    ).pack(pady=10)

    email_entry = tk.Entry(w, width=35)
    email_entry.pack(pady=10)

    def create_password():

        email = email_entry.get()

        if not email_registered(email):
            messagebox.showerror(
                "Error",
                "Email is not registered"
            )
            return

        password = "".join(
            random.choice(string.ascii_letters + string.digits)
            for i in range(8)
        )

        with open("passwords.txt", "w") as file:
            file.write(password)

        if send_email(email, password):

            messagebox.showinfo(
                "Success",
                "Password Sent Successfully"
            )

    tk.Button(
        w,
        text="GENERATE",
        command=create_password,
        bg="green",
        fg="white"
    ).pack(pady=20)




# ---------------- SCAN WEBSITE ----------------

def scan_website():

    w = tk.Toplevel(root)
    w.title("Website Scanner")
    w.geometry("500x450")
    w.configure(bg="black")

    tk.Label(
        w,
        text="ENTER WEBSITE URL",
        fg="#00FF00",
        bg="black"
    ).pack(pady=10)

    url = tk.Entry(w, width=40)
    url.pack(pady=5)

    status_label = tk.Label(
        w,
        text="Status : Waiting...",
        fg="yellow",
        bg="black",
        font=("Arial", 12, "bold")
    )
    status_label.pack(pady=10)

    detection_label = tk.Label(
        w,
        text="Detections : -",
        fg="white",
        bg="black",
        font=("Arial", 12)
    )
    detection_label.pack()

    reason_label = tk.Label(
        w,
        text="Reason : -",
        fg="white",
        bg="black",
        font=("Arial", 12)
    )
    reason_label.pack()

    recommendation_label = tk.Label(
        w,
        text="Recommendation : -",
        fg="cyan",
        bg="black",
        font=("Arial", 12, "bold")
    )
    recommendation_label.pack(pady=10)

    def scan():

        website = url.get().strip()
        global last_scanned_site, last_scan_status

        if website == "":
            messagebox.showerror(
                "Error",
                "Enter Website URL"
            )
            return

        result = check_url_virustotal(website)

        if result is None:

            status_label.config(
                text="Status : ERROR"
            )

            detection_label.config(
                text="Detections : -"
            )

            reason_label.config(
                text="Reason : Internet/API Error"
            )

            recommendation_label.config(
                text="Recommendation : Try Again Later"
            )

            return

        stats = result["data"]["attributes"]["stats"]

        malicious = stats["malicious"]
        suspicious = stats["suspicious"]

        if malicious > 0 or suspicious > 0:
            last_scanned_site = website
            last_scan_status = "MALICIOUS"

            status_label.config(
                text="Status : MALICIOUS"
            )

            detection_label.config(
                text=f"Detections : {malicious + suspicious}"
            )

            reason_label.config(
                text="Reason : Detected by VirusTotal"
            )

            recommendation_label.config(
                text="Recommendation : Block this website"
            )

            save_log(
                website,
                "MALICIOUS",
                malicious + suspicious,
                "Detected by VirusTotal"
            )

        else:
            last_scanned_site = website
            last_scan_status = "SAFE"

            status_label.config(
                text="Status : SAFE"
            )

            detection_label.config(
                text="Detections : 0"
            )

            reason_label.config(
                text="Reason : No Threat Found"
            )

            recommendation_label.config(
                text="Recommendation : Safe to access"
            )

            save_log(
                website,
                "SAFE",
                0,
                "No Threat Found"
            )

    tk.Button(
        w,
        text="SCAN",
        command=scan,
        bg="green",
        fg="white",
        width=15
    ).pack(pady=20)    

  

# ---------------- BLOCK WEBSITE ----------------

def block_website():

    w = tk.Toplevel(root)

    w.title("Block Website")
    w.geometry("450x350")
    w.configure(bg="black")

    # DOMAIN LABEL
    tk.Label(
        w,
        text="ENTER DOMAIN",
        fg="#00FF00",
        bg="black",
        font=("Arial", 12)
    ).pack(pady=10)

    domain = tk.Entry(
        w,
        width=40,
        font=("Arial", 12)
    )
    domain.pack()

    # PASSWORD LABEL
    tk.Label(
        w,
        text="ENTER PASSWORD",
        fg="#00FF00",
        bg="black",
        font=("Arial", 12)
    ).pack(pady=10)

    password_entry = tk.Entry(
        w,
        width=40,
        show="*",
        font=("Arial", 12)
    )
    password_entry.pack()

    # ---------------- BLOCK FUNCTION ----------------

    def block():

        global last_scanned_site, last_scan_status

        site = domain.get().strip()

        if site == "":
            messagebox.showerror(
                "Error",
                "Enter Website Domain"
            )
            return
        print("Entered Site :", site)
        print("Scanned Site :", last_scanned_site)
        print("Scan Status  :", last_scan_status)

        # Website must be scanned first
        if site.lower() != last_scanned_site.lower():
            messagebox.showerror(
                "Error",
                "Please scan this website first."
            )
            return

        # Allow only malicious websites
        if last_scan_status != "MALICIOUS":
            messagebox.showerror(
                "Blocked",
                "Only malicious websites can be blocked."
            )
            return

        entered_password = password_entry.get().strip()

        if entered_password == "":
            messagebox.showerror(
                "Error",
                "Enter Password"
            )
            return

        try:
            with open("passwords.txt", "r") as file:
                saved_password = file.read().strip()

        except FileNotFoundError:
            messagebox.showerror(
                "Error",
                "Password file not found"
            )
            return

        if entered_password != saved_password:
            messagebox.showerror(
                "Error",
                "Incorrect Password"
            )
            return

        try:

            # Check if already blocked
            with open(HOSTS_PATH, "r") as file:
                lines = file.readlines()

            for line in lines:
                if line.startswith("127.0.0.1") and site in line:
                    messagebox.showinfo(
                        "Info",
                        "Website is already blocked."
                    )
                    return

            # Block website
            with open(HOSTS_PATH, "a") as file:
                file.write(f"\n127.0.0.1 {site}")
                file.write(f"\n127.0.0.1 www.{site}")

            # Save Log
            save_log(
                site,
                "BLOCKED",
                0,
                "Website blocked successfully"
            )

            messagebox.showinfo(
                "Success",
                f"{site} Blocked Successfully"
            )

            w.destroy()

        except PermissionError:
            messagebox.showerror(
                "Permission Error",
                "Run the program as Administrator."
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    # ---------------- BLOCK BUTTON ----------------

    tk.Button(
        w,
        text="BLOCK WEBSITE",
        command=block,
        bg="red",
        fg="white",
        font=("Arial", 12, "bold"),
        width=20
    ).pack(pady=25)
    




# ---------------- UNBLOCK WEBSITE ----------------

def unblock_website():

    w = tk.Toplevel(root)

    w.title("Unblock Website")
    w.geometry("450x300")
    w.configure(bg="black")


    tk.Label(
        w,
        text="ENTER DOMAIN TO UNBLOCK",
        fg="#00FF00",
        bg="black",
        font=("Arial", 12)
    ).pack(pady=15)


    domain = tk.Entry(
        w,
        width=40,
        font=("Arial", 12)
    )

    domain.pack()



    def unblock():

        site = domain.get().strip()


        if site == "":
            messagebox.showerror(
                "Error",
                "Enter Domain"
            )
            return


        try:

            with open(HOSTS_PATH, "r") as file:
                lines = file.readlines()



            with open(HOSTS_PATH, "w") as file:

                for line in lines:

                    if site not in line:
                        file.write(line)



            messagebox.showinfo(
                "Success",
                site + " Unblocked Successfully"
            )


        except PermissionError:

            messagebox.showerror(
                "Error",
                "Run program as Administrator"
            )



    tk.Button(
        w,
        text="UNBLOCK",
        command=unblock,
        bg="green",
        fg="white",
        font=("Arial", 12)
    ).pack(pady=25)


# ---------------- VIEW BLOCKED WEBSITES ----------------

def view_blocked():

    w = tk.Toplevel(root)

    w.title("Blocked Websites")
    w.geometry("450x350")
    w.configure(bg="black")


    tk.Label(
        w,
        text="BLOCKED WEBSITES",
        fg="#00FF00",
        bg="black",
        font=("Arial",14)
    ).pack(pady=10)


    list_box = tk.Listbox(
        w,
        width=45,
        height=12,
        bg="black",
        fg="#00FF00",
        font=("Arial",12)
    )

    list_box.pack(pady=10)


    try:

        with open(HOSTS_PATH, "r") as file:
            lines = file.readlines()


        count = 1

        for line in lines:

            if line.startswith("127.0.0.1"):

                website = line.replace("127.0.0.1", "").strip()


                if website != "localhost":

                    list_box.insert(
                        tk.END,
                        str(count) + ". " + website
                    )

                    count += 1


    except FileNotFoundError:

        messagebox.showerror(
            "Error",
            "Hosts file not found"
        )

# ---------------- REPORTS ----------------

def reports():

    w = tk.Toplevel(root)

    w.title("Security Reports")
    w.geometry("550x400")
    w.configure(bg="black")

    tk.Label(
        w,
        text="CYBER SECURITY REPORT",
        fg="#00FF00",
        bg="black",
        font=("Consolas",18,"bold")
    ).pack(pady=15)

    total_scans = 0
    safe = 0
    malicious = 0

    try:

        with open("logs.txt","r") as file:

            logs = file.read()

            total_scans = logs.count("Website :")

            safe = logs.count("Status : SAFE")

            malicious = logs.count("Status : MALICIOUS")

    except FileNotFoundError:

        pass

    date = datetime.datetime.now()

    report = f"""

Total Scans          : {total_scans}

Safe Websites        : {safe}

Malicious Websites   : {malicious}

Generated On:

{date}

"""

    tk.Label(

        w,

        text=report,

        fg="#00FF00",

        bg="black",

        justify="left",

        font=("Consolas",13)
    ).pack(pady=20)

# ---------------- VIEW LOGS ----------------

def view_logs():

    w = tk.Toplevel(root)
    w.title("Scan Logs")
    w.geometry("700x500")
    w.configure(bg="black")

    tk.Label(
        w,
        text="SCAN LOGS",
        fg="#00FF00",
        bg="black",
        font=("Consolas", 18, "bold")
    ).pack(pady=10)

    text_box = tk.Text(
        w,
        bg="black",
        fg="#00FF00",
        font=("Consolas", 11),
        wrap="word"
    )

    text_box.pack(fill="both", expand=True, padx=10, pady=10)

    try:
        with open("logs.txt", "r") as file:
            logs = file.read()

        text_box.insert("1.0", logs)

    except FileNotFoundError:
        text_box.insert(
            "1.0",
            "No logs found."
        )

    text_box.config(state="disabled")


# ---------------- PROJECT INFO ----------------


def project_info():

    messagebox.showinfo(
        "Project Info",

"""
Project Name:
Malicious Website Blocker


Features:

✔ URL Scanning
✔ Website Blocking
✔ Host File Protection
✔ Email Authentication
✔ Security Reports


Technology:
Python
Tkinter
VirusTotal API
Windows Host File

"""
    )





# ---------------- MAIN WINDOW ----------------


root=tk.Tk()

root.title(
"Cyber Security Console"
)

root.geometry(
"900x600"
)

root.configure(
bg="black"
)



tk.Label(
root,
text="MALICIOUS WEBSITE BLOCKER",
fg="#00FF00",
bg="black",
font=("Consolas",24,"bold")
).pack(pady=20)



frame=tk.Frame(
root,
bg="black"
)

frame.pack(pady=30)




buttons=[


("📧 REGISTER EMAIL",register_window),

("🔑 GENERATE PASSWORD",generate_password),

("🌐 SCAN WEBSITE",scan_website),

("🚫 BLOCK WEBSITE",block_website),

("🔓 UNBLOCK WEBSITE",unblock_website),

 ("📋 VIEW BLOCKED", view_blocked),


("📊 REPORTS",reports),

("📄 VIEW LOGS", view_logs),

("ℹ PROJECT INFO",project_info),

("❌ EXIT",root.destroy)

]



for i,(text,cmd) in enumerate(buttons):

    tk.Button(

        frame,

        text=text,

        command=cmd,

        width=30,

        height=2,

        bg="black",

        fg="#00FF00",

        font=("Consolas",11,"bold")

    ).grid(
        row=i//2,
        column=i%2,
        padx=20,
        pady=10
    )



tk.Label(

root,

text="STATUS : ONLINE | FIREWALL : ACTIVE",

fg="#00FF00",

bg="black"

).pack(
side="bottom",
fill="x"
)



root.mainloop()