from marshmallow import Schema, fields, validates, ValidationError
from datetime import datetime


class StaffSchema(Schema):
    name = fields.String(required=True)
    title = fields.String(required=True)
    email = fields.Email(required=True)
    salary = fields.Float(required=True)
    birthday = fields.String(required=True)
    status = fields.Boolean(required=True)
    avatar = fields.String(required=True)

    @validates('name')
    def validate_name(self, value):
        if not value or not value.strip():
            raise ValidationError("Name must be a non-empty string.")
        if len(value) > 50:
            raise ValidationError("Name must not exceed 50 characters.")

    @validates('title')
    def validate_title(self, value):
        if not value or not value.strip():
            raise ValidationError("Title must be a non-empty string.")
        if len(value) > 100:
            raise ValidationError("Title must not exceed 100 characters.")

    @validates('email')
    def validate_email(self, value):
        if not value:
            raise ValidationError("Email must be provided.")
        if len(value) > 100:
            raise ValidationError("Email must not exceed 100 characters.")

    @validates('salary')
    def validate_salary(self, value):
        if value < 0:
            raise ValidationError("Salary must be a non-negative number.")
        if value > 1_000_000:
            raise ValidationError("Salary seems unrealistic (over 1 million).")

    @validates('birthday')
    def validate_birthday(self, value):
        try:
            if  len(value)<1:
                raise ValidationError("Birthday cannot be in the future.")
        except Exception as e:
            raise ValidationError(f"Invalid date format for birthday: {e}")

    @validates('status')
    def validate_status(self, value):
        if not isinstance(value, bool):
            raise ValidationError("Status must be a boolean value.")

    @validates('avatar')
    def validate_avatar(self, value):
        if not value or not value.strip():
            raise ValidationError("Avatar must be a non-empty base-64 encoded string.")
        if not value.startswith("data:image/"):
            raise ValidationError("Avatar must be a valid base-64 image string.")

# Example usage
if __name__ == "__main__":
    from marshmallow import ValidationError

    schema = StaffSchema()

    try:
        data = {
            "name": "John Doe",
            "title": "Manager",
            "email": "john.doe@example.com",
            "salary": 75000.0,
            "birthday": "1985-06-15",
            "status": True,
            "avatar": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAA..."
        }
        schema.load(data)
        print("Validation passed.")
    except ValidationError as e:
        print(f"Validation errors: {e.messages}")
