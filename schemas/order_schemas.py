from marshmallow import Schema, fields, validates, ValidationError
import re

class OrderSchema(Schema):
    # Fields with validation
    name = fields.String(required=True)
    table = fields.Integer(required=True)
    dishes = fields.List(fields.Dict(), required=True)

    @validates('name')
    def validate_name(self, value):
        # Check that the name contains at least two words (first and last name)
        if len(value.split()) < 2:
            raise ValidationError('The name must include both first and last name.')
        if not re.match(r"^[a-zA-Z ]+$", value):
            raise ValidationError('The name must only contain alphabetic characters and spaces.')
        
    @validates('table')
    def validate_table(self, value):
        if value <= 0:
            raise ValidationError('The table number must be greater than 0.')
        if value >= 100:
            raise ValidationError('The table number must be less than 100.')

    @validates('dishes')
    def validate_dishes(self, value):
        # Check if the list of dishes is not empty
        if not value:
            raise ValidationError('The order must include at least one dish.')

        for dish in value:
            # Validate that each dish has a valid name
            if 'name' not in dish or not dish['name']:
                raise ValidationError('Each dish must have a valid name.')
            # Validate that the price of the dish is greater than 0
            if 'price' not in dish or dish['price'] <= 0:
                raise ValidationError('The price of each dish must be greater than 0.')
            # Validate that the quantity of the dish is greater than 0
            if 'quantity' not in dish or dish['quantity'] <= 0:
                raise ValidationError('The quantity of each dish must be greater than 0.')


