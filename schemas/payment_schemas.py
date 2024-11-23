from marshmallow import Schema, fields, validates, ValidationError
from logger.logger_base import Logger

# Definimos el esquema PaymentSchema con las validaciones
class PaymentSchema(Schema):
    mesa = fields.Integer(required=True)
    numero_de_orden = fields.Integer(required=True)
    rfc = fields.String(required=True)

    @validates('name')
    def validate_name(self, value):
        if len(value) < 1 or not value.isalnum():
            raise ValidationError('El RFC debe tener 13 caracteres alfanuméricos.')
        
    @validates('rfc')
    def validate_rfc(self, value):
        if len(value) != 13 or not value.isalnum():
            raise ValidationError('El RFC debe tener 13 caracteres alfanuméricos.')
    
    
    @validates('mesa')
    def validate_table(self, value):
        if not isinstance(value, int) or value < 1:
            raise ValidationError('La mesa debe ser un número entero mayor que 0.')

    @validates('numero_de_orden')
    def validate_order_number(self, value):
        if not isinstance(value, int) or value < 1:
            raise ValidationError('El número de orden debe ser un número entero mayor que 0.')


# Prueba de validación
if __name__ == '__main__':
    logger = Logger()  # Instanciamos el logger
    schema = PaymentSchema()  # Creamos la instancia del esquema

    # Datos de prueba con campos inválidos
    new_payment = {
        'name': "HOOOLLL",
        'mesa': 3,  # Mesa inválida (debe ser mayor a 0)
        'numero_de_orden': 12345,  # Número de orden válido
        'rfc': 'INVALIDRFCGHA'  # RFC inválido (debe tener 13 caracteres alfanuméricos)
    }

    try:
        # Intentamos cargar los datos y validar
        schema.load(new_payment)  # Esto valida el nuevo pago con el esquema
        print("El pago es válido.")  # Si no se lanza ninguna excepción, se imprime que es válido

    except ValidationError as e:
        # Si hay un error de validación, lo capturamos y lo mostramos
        logger.error(f'An error has occurred: {e.messages}')  # Mostramos el error con los mensajes de validación
