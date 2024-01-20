
import cv2
from pyzbar.pyzbar import decode
import openpyxl
from openpyxl import Workbook

def scan_qr_code_camera():
    cap = cv2.VideoCapture(0) 

    while True:
        ret, frame = cap.read()
        decoded_objects = decode(frame)

        for obj in decoded_objects:
            data = obj.data.decode("utf-8")
            cap.release()
            cv2.destroyAllWindows()
            return data

        cv2.imshow("QR Code Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

def save_to_excel(data, excel_filename="data.xlsx"):
    wb = Workbook()
    sheet = wb.active

    sheet["A1"] = "Name"
    sheet["B1"] = "Phone"

    name, phone = data.split("\n")[0].split(":")[1], data.split("\n")[1].split(":")[1]

    sheet.append([name, phone])

    wb.save(excel_filename)
    print(f"Data saved to {excel_filename}")

if __name__ == "__main__":
    print("Scan QR code with the camera.")
    data = scan_qr_code_camera()
    print("QR Code scanned successfully!")
    
    save_to_excel(data)
