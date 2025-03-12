from flask import Flask, request, jsonify, render_template
from dynamsoft_barcode_reader_bundle import *
import os
import logging
import io

secret_key = os.getenv("DYNAMSOFT_LICENSE")

app = Flask(__name__)

# Accept data up to 100MB
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
app.config['DEBUG'] = True
app.config['TIMEOUT'] = 300

app.logger.setLevel(logging.DEBUG)

# Create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Create formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# Add the handler to the app's logger
app.logger.addHandler(ch)

# Initialize Dynamsoft License
errorCode, errorMsg = LicenseManager.init_license(secret_key)

if errorCode != EnumErrorCode.EC_OK and errorCode != EnumErrorCode.EC_LICENSE_CACHE_USED:
    raise Exception(f"License initialization failed: {errorMsg}")

cvr = CaptureVisionRouter()

DL_ABBR_DES_MAP = {
        "DCA": "Jurisdiction-specific vehicle class",
        "DBA": "Expiry Date",
        "DCS": "Last Name",
        "DAC": "First Name",
        "DBD": "Issue Date",
        "DBB": "Birth Date",
        "DBC": "Gender",
        "DAY": "Eye Color",
        "DAU": "Height",
        "DAG": "Street",
        "DAI": "City",
        "DAJ": "State",
        "DAK": "Zip",
        "DAQ": "License Number",
        "DCF": "Document Discriminator",
        "DCG": "Issue Country",
        "DAH": "Street 2",
        "DAZ": "Hair Color",
        "DCI": "Place of birth",
        "DCJ": "Audit information",
        "DCK": "Inventory Control Number",
        "DBN": "Alias / AKA Family Name",
        "DBG": "Alias / AKA Given Name",
        "DBS": "Alias / AKA Suffix Name",
        "DCU": "Name Suffix",
        "DCE": "Physical Description Weight Range",
        "DCL": "Race / Ethnicity",
        "DCM": "Standard vehicle classification",
        "DCN": "Standard endorsement code",
        "DCO": "Standard restriction code",
        "DCP": "Jurisdiction-specific vehicle classification description",
        "DCQ": "Jurisdiction-specific endorsement code description",
        "DCR": "Jurisdiction-specific restriction code description",
        "DDA": "Compliance Type",
        "DDB": "Card Revision Date",
        "DDC": "HazMat Endorsement Expiration Date",
        "DDD": "Limited Duration Document Indicator",
        "DAW": "Weight(pounds)",
        "DAX": "Weight(kilograms)",
        "DDH": "Under 18 Until",
        "DDI": "Under 19 Until",
        "DDJ": "Under 21 Until",
        "DDK": "Organ Donor Indicator",
        "DDL": "Veteran Indicator",
        "DAA": "Customer Full Name",
        "DAB": "Customer Last Name",
        "DAE": "Name Suffix",
        "DAF": "Name Prefix",
        "DAL": "Residence Street Address1",
        "DAM": "Residence Street Address2",
        "DAN": "Residence City",
        "DAO": "Residence Jurisdiction Code",
        "DAR": "License Classification Code",
        "DAS": "License Restriction Code",
        "DAT": "License Endorsements Code",
        "DAV": "Height in CM",
        "DBE": "Issue Timestamp",
        "DBF": "Number of Duplicates",
        "DBH": "Organ Donor",
        "DBI": "Non-Resident Indicator",
        "DBJ": "Unique Customer Identifier",
        "DBK": "Social Security Number",
        "DBM": "Social Security Number",
        "DCH": "Federal Commercial Vehicle Codes",
        "DBR": "Name Suffix",
        "PAA": "Permit Classification Code",
        "PAB": "Permit Expiration Date",
        "PAC": "Permit Identifier",
        "PAD": "Permit Issue Date",
        "PAE": "Permit Restriction Code",
        "PAF": "Permit Endorsement Code",
        "ZVA": "Court Restriction Code",
        "DAD": "Middle Name"
    }

def parse_driver_license(txt):
    lines = txt.split("\n")
    abbrs = set(DL_ABBR_DES_MAP.keys())
    parsed_data = {}

    for i, line in enumerate(lines):
        if i == 1:
            abbr = "DAQ"
            content = line[line.index(abbr) + 3:].strip() if abbr in line else line.strip()
        else:
            abbr = line[:3]
            content = line[3:].strip()

        if abbr in abbrs:
            parsed_data[DL_ABBR_DES_MAP[abbr]] = content 

    return parsed_data

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan_barcode():
    if request.data is None:
        return jsonify({"error": "No file uploaded"}), 422

    result = cvr.capture(request.data, EnumPresetTemplate.PT_READ_BARCODES)
    
    if result.get_error_code() != EnumErrorCode.EC_OK:
        return jsonify({"error": result.get_error_string()}), 422

    barcode_result = result.get_decoded_barcodes_result()
    if barcode_result is None or barcode_result.get_items() == 0:
        return jsonify({"error": "No barcodes found"}), 404

    items = barcode_result.get_items()
    
    has_valid_pdf417 = any(item.get_format_string() == "PDF417" and item.get_text().strip() for item in items)

    if has_valid_pdf417:
        barcodes = [{"type": item.get_format_string(), "text": {"raw": item.get_text(), "parsed": parse_driver_license(item.get_text())}} for item in items]
        return jsonify({"barcodes": barcodes})
    else:
        return jsonify({"error": "Scanned but no PDF417"}), 422


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run on port 5000

