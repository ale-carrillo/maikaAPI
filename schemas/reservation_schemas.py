from datetime import datetime
from marshmallow import Schema, fields, validates, ValidationError

class ReservationSchema(Schema):
    date = fields.String(required=True)
    people = fields.Integer(required=True)
    t_reservation = fields.String(required=True)
    name = fields.String(required=True)
    last_name = fields.String(required=True)
    phone = fields.Integer(required=True)
    email = fields.String(required=True)
    special = fields.String(required=False)

    @validates('date')
    def validate_date(self, value):
        if not value:
            raise ValidationError("Date must be in the format 'DD MMM YYYY HH:MM'")

    @validates('people')
    def validate_people(self, value):
        try:
            if int(value) < 0:
                raise ValidationError("Existence must be a non-negative integer.")
        except:
            raise ValidationError("Existence must be a non-negative integer.")

    @validates('t_reservation')
    def validate_t_reservation(self, value):
        if not value:
            raise ValidationError("Reservation type must not be empty.")

    @validates('name')
    def validate_name(self, value):
        if not value:
            raise ValidationError("Name must not be empty.")

    @validates('last_name')
    def validate_last_name(self, value):
        if not value:
            raise ValidationError("Last name must not be empty.")

    @validates('phone')
    def validate_phone(self, value):
        if len(str(value)) != 10:
            raise ValidationError("Phone must be exactly 10 digits long.")

    @validates('special')
    def validate_special(self, value):
        if value and len(value) > 255:
            raise ValidationError("Special instructions must not exceed 255 characters.")

    def validate_email(self, value):
        if not value:
            raise ValidationError("Email must not be empty.")

if __name__ == "__main__":
    from logger.logger_base import Logger

    logger = Logger()
    schema = ReservationSchema()

    try:
        schema.validate_date(test_data['date'])
        schema.validate_people(test_data['people'])
        schema.validate_t_reservation(test_data['t_reservation'])
        schema.validate_name(test_data['name'])
        schema.validate_last_name(test_data['last_name'])
        schema.validate_phone(test_data['phone'])
        schema.validate_email(test_data['email'])
        schema.validate_special(test_data['special'])
        logger.info("All fields passed validation.")
    except ValidationError as e:
        logger.error(f"An error has occurred: {e}")
