from marshmallow import Schema, fields, validates, ValidationError
from logger.logger_base import Logger

class ItemSchema(Schema):
    name = fields.Str(required=True)
    quantity = fields.Int(required=True)
    price = fields.Float(required=True)

class PaymentSchema(Schema):
    name = fields.String(required=True)
    table = fields.Integer(required=True)
    order_id = fields.Integer(required=True)
    total = fields.Float(required=True)
    rfc = fields.String(required=True)
    payment_type = fields.String(required=True)
    dishes = fields.List(fields.Nested(ItemSchema), required=True)


    @validates('rfc')
    def validate_rfc(self, value):
        if len(value) != 13 or not value.isalnum():
            raise ValidationError('The RFC must have exactly 13 alphanumeric characters.')

    @validates('table')
    def validate_table(self, value):
        if not isinstance(value, int) or value < 1:
            raise ValidationError('The table must be an integer greater than 0.')

    @validates('order_id')
    def validate_order_id(self, value):
        if not isinstance(value, int) or value < 1:
            raise ValidationError('The order ID must be an integer greater than 0.')

    @validates('total')
    def validate_total(self, value):
        if not isinstance(value, int) or value < 1:
            raise ValidationError('The total must be an integer greater than 0.')

    @validates('payment_type')
    def validate_payment_type(self, value):
        if not value:
            raise ValidationError('The payment type cannot be empty.')

    @validates('dishes')
    def validate_dishes(self, value):
        if not value or len(value) == 0:
            raise ValidationError('The dishes field must contain at least one dish.')

if __name__ == '__main__':
    schema = PaymentSchema()
    payment_data = {
        "_id": 311,
        "name": "BHBHB DWUB",
        "table": 4,
        "dishes": [
            {
                "name": "Caesar Salad",
                "price": 12,
                "quantity": 1
            },
            {
                "name": "Spaghetti Carbonara",
                "price": 18,
                "quantity": 1
            }
        ],
        "total": 0,  
        "rfc": "ABCD123456XYZ",  
        "payment_type": "Credit Card"
    }

    try:
        validated_data = schema.load(payment_data)
        print("Validated data:", validated_data)
    except ValidationError as e:
        print("Validation errors:", e.messages)
