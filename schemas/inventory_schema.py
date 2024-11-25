from marshmallow import fields, validates, ValidationError

# Schema for inventory
class InventorySchema:
    name = fields.String(required=True)
    unit = fields.String(required=True)
    existence = fields.Integer(required=True)
    image = fields.String(required=True)

    # Validating name
    @validates('name')
    def validate_name(self, value):
        if not value:
            raise ValidationError("Name must be a non-empty string.")

    # Validating unit
    @validates('unit')
    def validate_unit(self, value):
        if not value:
            raise ValidationError("Unit must be a non-empty string.")

    # Validating existence
    @validates('existence')
    def validate_existence(self, value):
        try:
            if int(value) < 0:
                raise ValidationError("Existence must be a non-negative integer.")
        except:
            raise ValidationError("Existence must be a non-negative integer.")

    # Validating image
    @validates('image')
    def validate_image(self, value):
        if not value:
            raise ValidationError("Image must be a base-64-image string.")


# Test
if __name__ == "__main__":
    from logger.logger_base import Logger

    logger = Logger()
    schema = InventorySchema()


    try:
        schema.validate_name('Corn')
        schema.validate_unit('Kg')
        schema.validate_existence(5)
        schema.validate_image('SOME IMAGE IN BASE 64')
    except ValidationError as e:
        logger.error(f'An error has ocurred: {e}')
