from flask import Flask, request, jsonify
import uuid
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Log format
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)

logger = logging.getLogger(__name__)

app = Flask(__name__)

# In-memory storage for receipt ids and their points
receipts_cache = {}


def check_request_data(data):
    expected_keys = ['retailer', 'purchaseDate', 'purchaseTime', 'items', 'total']
    all_ok = bool(not data or not all(key in data for key in expected_keys))
    logger.debug(f"Request check, any issues found: {all_ok}")
    return all_ok


def generate_receipt_id():
    return str(uuid.uuid4())


@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    request_data = request.get_json()

    # Validate the receipt data
    if check_request_data(request_data):
        return jsonify({"error": "The receipt is invalid."}), 400

    # Generate a unique ID for the receipt
    receipt_id = generate_receipt_id()

    logger.info(f"Generated receipt ID: {receipt_id}")

    # Calculate points based on the rules
    points = calculate_points(request_data)
    receipts_cache[receipt_id] = points
    logger.info(f"Stored receipt-ID: {receipt_id} and points: {points} in memory")

    return jsonify({"receipt_id": receipt_id}), 200

@app.route('/health',methods=['GET'])
def health_check():
    logger.debug("Received health check request")
    return jsonify({"status":"OK"}), 200


@app.route('/receipts/<string:receipt_id>/points', methods=['GET'])
def get_points(receipt_id):
    logger.debug(f"Received request to get points for receipt ID: {receipt_id}")

    if receipt_id not in receipts_cache:
        msg = f"No receipt found for ID: {receipt_id}"
        logger.error(msg)
        return jsonify({"error": msg}), 404

    points = receipts_cache[receipt_id]
    logger.debug(f"Returning points for receipt ID {receipt_id}: {points}")

    return jsonify({"points": points}), 200


def calculate_points(receipt):
    logger.info("Calculating points for receipt")

    points = 0

    # Rule 1: One point for every alphanumeric character in the retailer name.
    points += sum(c.isalnum() for c in receipt['retailer'])
    logger.debug(f"Retailer name points: {points}")

    # Rule 2: 50 points if the total is a round dollar amount with no cents.
    total = float(receipt['total'])
    if total == int(total):
        points += 50
        logger.debug("Added 50 points for round dollar amount")

    # Rule 3: 25 points if the total is a multiple of 0.25.
    if total % 0.25 == 0:
        points += 25
        logger.debug("Added 25 points for multiple of 0.25")

    # Rule 4: 5 points for every two items on the receipt.
    points += (len(receipt['items']) // 2) * 5
    logger.debug(f"Points for every two items: {points}")

    # Rule 5: If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2
    # and round up to the nearest integer.
    for item in receipt['items']:
        description = item['shortDescription'].strip()
        if len(description) % 3 == 0:
            price = float(item['price'])
            points += round(price * 0.2 + 0.5)
            logger.debug(f"Points {points} after item: '{description}'")

    # Rule 6: 6 points if the day in the purchase date is odd.
    purchase_date = datetime.strptime(receipt['purchaseDate'], "%Y-%m-%d")
    if purchase_date.day % 2 != 0:
        points += 6
    logger.debug(f"Points: {points} after checking date: {purchase_date.day}")

    # Rule 7: 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    two_pm = datetime.strptime("14:00", "%H:%M").time()
    four_pm = datetime.strptime("16:00", "%H:%M").time()
    purchase_time = datetime.strptime(receipt['purchaseTime'], "%H:%M").time()
    if two_pm < purchase_time < four_pm:
        points += 10
    logger.debug(f"Points: {points} after checking time: {purchase_time}")

    return points


if __name__ == '__main__':
    #app.debug = True
    app.run(host='0.0.0.0', port=3000)
