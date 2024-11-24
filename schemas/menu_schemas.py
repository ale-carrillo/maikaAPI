from marshmallow import fields, validates, ValidationError

class MenuSchema:
    meal = fields.String(required=True)
    description = fields.String(required=True)
    price = fields.Integer(required=True)

    @validates('meal')
    def validate_meal(self, value):
        if len(value) < 5:
            raise ValidationError("meal must be at least 5 character long.")

    @validates('description')
    def validate_description(self, value):
        if len(value) < 5:
            raise ValidationError("Description must be at least 5 character long.")
    
    @validates('price')
    def validate_price(self, value):
        try:
            if int(value) < 0:
                raise ValidationError("Price must be a non-negative integer.")
        except:
            raise ValidationError("Price must be a non-negative integer.")
        
    @validates('image')
    def validate_image(self, value):
        if not value:
            raise ValidationError("Image must be a base-64-image string.")
        
        
if __name__ == "__main__":
    from logger.logger_base import Logger

    logger = Logger()
    schema = MenuSchema()

    schema.validate_meal('dasdasd')

    try:
        schema.validate_description('d')
    except ValidationError as e:
        logger.error(f'An error has ocurred: {e}')
