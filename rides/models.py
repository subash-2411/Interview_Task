# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Admin(models.Model):
    username = models.CharField(unique=True)
    email = models.CharField(unique=True)
    password_hash = models.CharField()
    last_login = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Admin'


class Bookingpassengers(models.Model):
    booking = models.ForeignKey('Bookings', models.DO_NOTHING)
    passenger_name = models.CharField()
    passenger_age = models.IntegerField()
    passenger_gender = models.CharField()
    seat_number = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'BookingPassengers'


class Bookings(models.Model):
    travel_plan = models.ForeignKey('Travelplans', models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    total_fare = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    passenger_name = models.CharField(blank=True, null=True)
    passenger_age = models.IntegerField(blank=True, null=True)
    passenger_gender = models.CharField(blank=True, null=True)
    passenger_phone = models.CharField(blank=True, null=True)
    passenger_email = models.CharField(blank=True, null=True)
    status = models.CharField(blank=True, null=True)
    created_at = models.TextField(blank=True, null=True)  # This field type is a guess.
    route_json = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Bookings'


class Busbookings(models.Model):
    booking = models.ForeignKey(Bookings, models.DO_NOTHING)
    bus_number = models.CharField()
    operator_name = models.CharField()
    seat_number = models.CharField()
    departure_time = models.TextField()
    arrival_time = models.TextField()
    fare = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float

    class Meta:
        managed = False
        db_table = 'BusBookings'


class Cancellations(models.Model):
    booking = models.ForeignKey(Bookings, models.DO_NOTHING)
    cancellation_id = models.CharField(unique=True)
    reason = models.TextField(blank=True, null=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    status = models.CharField(blank=True, null=True)
    created_at = models.TextField(blank=True, null=True)  # This field type is a guess.
    refund_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Cancellations'


class Drivers(models.Model):
    name = models.CharField()
    phone = models.CharField(unique=True)
    license_number = models.CharField(unique=True)
    password_hash = models.CharField(blank=True, null=True)
    is_online = models.IntegerField(blank=True, null=True)
    rating = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    balance = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    status = models.CharField(blank=True, null=True)
    created_at = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Drivers'


class Emergencyalerts(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    booking = models.ForeignKey(Bookings, models.DO_NOTHING, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    longitude = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    status = models.CharField(blank=True, null=True)
    created_at = models.TextField(blank=True, null=True)  # This field type is a guess.
    emergency_type = models.CharField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'EmergencyAlerts'


class Emergencycontacts(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    name = models.CharField()
    phone = models.CharField()
    relationship = models.CharField()
    is_active = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'EmergencyContacts'


class Favoritelocations(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    label = models.CharField()
    address = models.CharField()
    latitude = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    longitude = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float

    class Meta:
        managed = False
        db_table = 'FavoriteLocations'


class Flightbookings(models.Model):
    booking = models.ForeignKey(Bookings, models.DO_NOTHING)
    flight_number = models.CharField()
    airline_name = models.CharField()
    seat_number = models.CharField()
    gate = models.CharField()
    departure_time = models.TextField()
    arrival_time = models.TextField()
    fare = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float

    class Meta:
        managed = False
        db_table = 'FlightBookings'


class Notifications(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    title = models.CharField()
    message = models.TextField()
    is_read = models.IntegerField(blank=True, null=True)
    notification_type = models.CharField()
    created_at = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Notifications'


class Payments(models.Model):
    booking = models.ForeignKey(Bookings, models.DO_NOTHING)
    razorpay_order_id = models.CharField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    status = models.CharField(blank=True, null=True)
    created_at = models.TextField(blank=True, null=True)  # This field type is a guess.
    method = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Payments'


class Ridebookings(models.Model):
    booking = models.ForeignKey(Bookings, models.DO_NOTHING)
    driver = models.ForeignKey(Drivers, models.DO_NOTHING, blank=True, null=True)
    vehicle_type = models.CharField()
    fare = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    otp = models.CharField()
    status = models.CharField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    leg_type = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'RideBookings'


class Ridetracking(models.Model):
    booking_id = models.IntegerField()
    driver_id = models.IntegerField()
    current_leg = models.CharField(blank=True, null=True)
    status = models.CharField(blank=True, null=True)
    driver_location_lat = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    driver_location_lng = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    otp = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'RideTracking'


class Tickets(models.Model):
    booking = models.ForeignKey(Bookings, models.DO_NOTHING)
    ticket_file_path = models.CharField()
    qr_code_path = models.CharField()
    generated_at = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Tickets'


class Trainbookings(models.Model):
    booking = models.ForeignKey(Bookings, models.DO_NOTHING)
    train_number = models.CharField()
    train_name = models.CharField()
    coach_number = models.CharField()
    seat_number = models.CharField()
    departure_time = models.TextField()
    arrival_time = models.TextField()
    fare = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float

    class Meta:
        managed = False
        db_table = 'TrainBookings'


class Transactions(models.Model):
    payment = models.ForeignKey(Payments, models.DO_NOTHING)
    transaction_id = models.CharField(unique=True)
    method = models.CharField()
    status = models.CharField(blank=True, null=True)
    created_at = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Transactions'


class Travelhistory(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    booking = models.ForeignKey(Bookings, models.DO_NOTHING)
    travel_date = models.DateField()
    source = models.CharField()
    destination = models.CharField()
    fare = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    status = models.CharField()

    class Meta:
        managed = False
        db_table = 'TravelHistory'


class Travelplans(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    source = models.CharField()
    destination = models.CharField()
    travel_date = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    search_time = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'TravelPlans'


class Triptracking(models.Model):
    booking = models.OneToOneField(Bookings, models.DO_NOTHING, primary_key=True)
    current_latitude = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    current_longitude = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    current_leg = models.CharField()
    eta_minutes = models.IntegerField()
    status = models.CharField()
    updated_at = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'TripTracking'


class Userprofiles(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING, primary_key=True)
    full_name = models.CharField()
    avatar_url = models.CharField(blank=True, null=True)
    default_budget = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    default_first_mile = models.CharField(blank=True, null=True)
    default_last_mile = models.CharField(blank=True, null=True)
    preferred_mode = models.CharField(blank=True, null=True)
    status_emoji = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'UserProfiles'


class Users(models.Model):
    email = models.CharField(unique=True, blank=True, null=True)
    phone = models.CharField(unique=True)
    password_hash = models.CharField(blank=True, null=True)
    status = models.CharField(blank=True, null=True)
    created_at = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Users'


class Vehicles(models.Model):
    driver = models.OneToOneField(Drivers, models.DO_NOTHING, primary_key=True)
    vehicle_type = models.CharField()
    vehicle_number = models.CharField(unique=True)
    vehicle_model = models.CharField()

    class Meta:
        managed = False
        db_table = 'Vehicles'
