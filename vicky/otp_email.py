# import random
# import smtplib
# import time


# class OTPManager:
#     def __init__(self, expiry_time=120, cooldown_time=60):
#         self.otp_storage = {}       # {email: (otp, expiry_timestamp)}
#         self.last_request = {}      # {email: last_request_timestamp}
#         self.expiry_time = expiry_time
#         self.cooldown_time = cooldown_time

#     def generate_otp(self, email):
#         """Generate OTP with cooldown"""
#         now = time.time()

#         # Check cooldown
#         if email in self.last_request and (now - self.last_request[email]) < self.cooldown_time:
#             wait_time = int(self.cooldown_time - (now - self.last_request[email]))
#             return None, f"⏳ Cooldown active! Please wait {wait_time} seconds before requesting a new OTP."

#         # Generate OTP
#         otp = str(random.randint(100000, 999999))
#         expiry = now + self.expiry_time
#         self.otp_storage[email] = (otp, expiry)
#         self.last_request[email] = now

#         return otp, f"✅ OTP generated successfully! (Cooldown {self.cooldown_time} sec)"

#     def validate_otp(self, email, entered_otp):
#         """Validate OTP"""
#         if email not in self.otp_storage:
#             return False, "❌ No OTP generated for this email"

#         otp, expiry = self.otp_storage[email]

#         if time.time() > expiry:
#             return False, "⌛ OTP expired"

#         if entered_otp == otp:
#             del self.otp_storage[email]  # remove after success
#             return True, "✅ OTP verified successfully"
#         else:
#             return False, "❌ Invalid OTP"


# def send_email(receiver_email, otp):
#     try:
#         sender_email = "ramgutukade504@gmail.com"
#         sender_password = "ahgmsofxvcrjtllv"  # Gmail App Password

#         subject = "Your OTP Code"
#         body = f"Your OTP is {otp}. It will expire in 2 minutes."

#         message = f"Subject: {subject}\n\n{body}"

#         with smtplib.SMTP("smtp.gmail.com", 587) as server:
#             server.starttls()
#             server.login(sender_email, sender_password)
#             server.sendmail(sender_email, receiver_email, message)

#         print(f"📧 OTP sent successfully to {receiver_email}")
#     except Exception as e:
#         print("❌ Failed to send email:", e)


# # ==============================
# # Example Usage
# # ==============================
# if __name__ == "__main__":
#     otp_manager = OTPManager()

#     email = input("Enter your email address: ")

#     # Try generating OTP
#     otp, msg = otp_manager.generate_otp(email)
#     print(msg)

#     if otp:  # Only send if OTP was generated
#         send_email(email, otp)
#         print(f"⚠️ You cannot request another OTP for {otp_manager.cooldown_time} seconds.\n")

#         user_input = input("Enter the OTP you received in your email: ")
#         success, msg = otp_manager.validate_otp(email, user_input)
#         print(msg)

import random
import smtplib
import time


class OTPManager:
    def __init__(self, expiry_time=120, cooldown_time=30):
        self.otp_storage = {}       # {email: (otp, expiry_timestamp)}
        self.last_request = {}      # {email: last_request_timestamp}
        self.expiry_time = expiry_time
        self.cooldown_time = cooldown_time

    def generate_otp(self, email):
        """Generate OTP with cooldown"""
        now = time.time()

        # Check cooldown
        if email in self.last_request and (now - self.last_request[email]) < self.cooldown_time:
            wait_time = int(self.cooldown_time - (now - self.last_request[email]))
            return None, f"⏳ Cooldown active! Please wait {wait_time} seconds before requesting a new OTP."

        # Generate OTP
        otp = str(random.randint(100000, 999999))
        expiry = now + self.expiry_time
        self.otp_storage[email] = (otp, expiry)
        self.last_request[email] = now

        return otp, f"✅ OTP generated successfully! (Cooldown {self.cooldown_time} sec)"

    def validate_otp(self, email, entered_otp):
        """Validate OTP"""
        if email not in self.otp_storage:
            return False, "❌ No OTP generated for this email"

        otp, expiry = self.otp_storage[email]

        if time.time() > expiry:
            return False, "⌛ OTP expired"

        if entered_otp == otp:
            del self.otp_storage[email]  # remove after success
            return True, "✅ OTP verified successfully"
        else:
            return False, "❌ Invalid OTP"


def send_email(receiver_email, otp):
    try:
        sender_email = "Enter_Your_Email_Id"
        sender_password = "Enter_Your_Gmail_App_Password"  # Gmail App Password

        subject = "Your OTP Code"
        body = f"Your OTP is {otp}. It will expire in 2 minutes."

        message = f"Subject: {subject}\n\n{body}"

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message)

        print(f"📧 OTP sent successfully to {receiver_email}")
    except Exception as e:
        print("❌ Failed to send email:", e)


# ==============================
# Example Usage with Resend Option
# ==============================
if __name__ == "__main__":
    otp_manager = OTPManager()

    email = input("Enter your email address: ")

    while True:
        # Generate and send OTP
        otp, msg = otp_manager.generate_otp(email)
        print(msg)

        if otp:  # Only send if OTP generated
            send_email(email, otp)
            print(f"⚠️ You cannot request another OTP for {otp_manager.cooldown_time} seconds.\n")

        # Ask user for OTP or resend
        user_input = input("Enter the OTP you received (or type 'resend' to get a new one): ").strip()

        if user_input.lower() == "resend":
            continue  # go back to OTP generation

        # Validate OTP
        success, msg = otp_manager.validate_otp(email, user_input)
        print(msg)

        if success:
            break  # Exit loop after success
        else:
            # Ask if they want to try again
            retry = input("Do you want to try again? (yes/no): ").strip().lower()
            if retry != "yes":
                break


