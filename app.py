import cv2
from pyzbar.pyzbar import decode
from flask import Flask, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Set up credentials from the downloaded JSON key file
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("path/to/your/keyfile.json", scope)
client = gspread.authorize(creds)

# Specify the spreadsheet and sheet
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1Zy3x_d4Lrk2v1njIG9LL5-cp3i_a_0PzCVT7Q6NpQls/edit"
spreadsheet = client.open_by_url(spreadsheet_url)
sheet = spreadsheet.get_worksheet(0)  # Assuming data is in the first sheet

@app.route('/scan_qr_code', methods=['GET'])
def scan_qr_code():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        decoded_objects = decode(frame)

        for obj in decoded_objects:
            data = obj.data.decode("utf-8")
            cap.release()
            store_data_in_spreadsheet(data)
            return jsonify({"data": data})

        cv2.imshow("QR Code Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    return jsonify({"data": None})

def store_data_in_spreadsheet(data):
    # Extract data from the QR code
    name, phone = data.split("\n")[0].split(":")[1], data.split("\n")[1].split(":")[1]

    # Append data to the Google Sheets spreadsheet
    sheet.append_row([name, phone])

# if __name__ == "__main__":
#     app.run(debug=True)
