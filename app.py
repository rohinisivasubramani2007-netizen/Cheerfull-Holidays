from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import random  # Added missing import for PNR generation

app = Flask(__name__)

# ================= DATABASE CONNECTION =================
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="tourist"
)
cursor = db.cursor(dictionary=True)

# ================= HOME =================
@app.route('/')
def home():
    return render_template('Home.html')


# ================= CONTACT =================
@app.route('/contact')
def contact():
    return render_template('contact.html')

# ======================= FLIGHT =======================
@app.route('/flight')
def flight():
    return render_template('Flight.html')

@app.route('/flightbook')
def flightbook():
    return render_template('flightbooking.html')

@app.route('/flightreceipt1')
def flightreceipt1():
    return render_template('flight_booking_receipt.html')

@app.route('/flightbooking', methods=['GET', 'POST'])
def flight_booking():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        from_city = request.form['from_city']
        to_city = request.form['to_city']
        travel_date = request.form['travel_date']

        sql = """
        INSERT INTO flight_booking (name, email, from_city, to_city, travel_date)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (name, email, from_city, to_city, travel_date))
        db.commit()

        return redirect(url_for('flight_receipt'))

    return render_template('flightbooking.html')

@app.route('/flight-dashboard')
def flight_dashboard():
    cursor.execute("SELECT * FROM flight_booking")
    data = cursor.fetchall()
    return render_template('flight_booking_receipt.html', data=data)

@app.route('/flight-receipt')
def flight_receipt():
    cursor.execute("SELECT * FROM flight_booking ORDER BY id DESC LIMIT 1")
    data = cursor.fetchone()
    return render_template('flight_booking_receipt.html', data=data)

# ======================= HOTEL =======================
@app.route('/hotel')
def hotel():
    return render_template('Hotel.html')

@app.route('/hotelbook')
def hotelbook():
    return render_template('Hotelbooking.html')

@app.route('/hotelreceipt1')
def hotelreceipt1():
    return render_template('Hotel_booking_receipt.html')

@app.route('/hotelbooking', methods=['GET', 'POST'])
def hotel_booking():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        hotel_name = request.form['hotel_name']
        checkin = request.form['checkin']
        checkout = request.form['checkout']

        sql = """
        INSERT INTO hotel_booking (name, email, hotel_name, checkin, checkout)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (name, email, hotel_name, checkin, checkout))
        db.commit()

        return redirect(url_for('hotel_receipt'))

    return render_template('Hotelbooking.html')

@app.route('/hotel-dashboard')
def hotel_dashboard():
    cursor.execute("SELECT * FROM hotel_booking")
    data = cursor.fetchall()
    return render_template('hotel_booking_dashboard.html', data=data)

@app.route('/hotel-receipt')
def hotel_receipt():
    cursor.execute("SELECT * FROM hotel_booking ORDER BY id DESC LIMIT 1")
    data = cursor.fetchone()
    return render_template('Hotel_booking_receipt.html', data=data)

# ======================= TRAIN =======================
@app.route('/train')
def train():
    return render_template('Train.html')

@app.route('/trainbook')
def trainbook():
    return render_template('Trainbooking.html')

@app.route('/trainreceipt1')
def trainreceipt1():
    return render_template('Train_booking_receipt.html')


@app.route('/trainbooking', methods=['GET', 'POST'])
def train_booking():
    if request.method == 'POST':
        from_city = request.form['from_city']
        to_city = request.form['to_city']
        journey_date = request.form['journey_date']
        train_class = request.form['train_class']
        passenger_name = request.form['passenger_name']
        age = request.form['age']
        gender = request.form['gender']
        phone_number = request.form['phone_number']
        email = request.form['email']
        person = request.form['person']
        total_amount = request.form['total_amount']

        # FIX: Added 'gender' to the columns list to match the 11 %s placeholders and 11 variables
        sql = """
        INSERT INTO train_booking (from_city, to_city, journey_date, train_class, passenger_name, age, gender, phone_number, email, person, total_amount)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (from_city, to_city, journey_date, train_class, passenger_name, age, gender, phone_number, email, person, total_amount))
        db.commit()
        
        return redirect(url_for('train_receipt'))

    return render_template('Trainbooking.html')


@app.route('/train-dashboard')
def train_dashboard():
    cursor.execute("SELECT * FROM train_booking")
    data = cursor.fetchall()
    return render_template('train_booking_dashboard.html', data=data)

@app.route('/train-receipt')
def train_receipt():

    cursor.execute("""
        SELECT from_city, to_city, journey_date, train_class, passenger_name, 
               age, gender, phone_number, email, person, total_amount 
        FROM train_booking ORDER BY id DESC LIMIT 1
    """)
    row = cursor.fetchone()
    
    if row:
        data = {
            'pnr': f"PNR{random.randint(100000, 999999)}", # Generate PNR in backend
            'from_city': row['from_city'],
            'to_city': row['to_city'],
            'journey_date': row['journey_date'],
            'train_class': row['train_class'],
            'passenger_name': row['passenger_name'],
            'age': row['age'],
            'gender': row['gender'],
            'phone_number': row['phone_number'],
            'email': row['email'],
            'person': row['person'],
            'ticket_amount': row['total_amount']
        }
    else:
        data = {}
        
    return render_template('Train_booking_receipt.html', data=data)

# ================= RUN =================
if __name__ == '__main__':
    app.run()
