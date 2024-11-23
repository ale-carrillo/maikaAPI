from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from logger.logger_base import Logger
from services.payment_services import PaymentService  # Asegúrate de que importes el servicio adecuado
from schemas.payment_schemas import PaymentSchema  # Importa el esquema de validación

class PaymentRoutes(Blueprint):
    def __init__(self, payment_service, payment_schema):
        super().__init__('payment', __name__)
        self.payment_service = payment_service
        self.payment_schema = payment_schema
        self.register_routes()
        self.logger = Logger()

    def register_routes(self):
        self.route('/api/v1/payments', methods=['POST'])(self.add_payment)

    def add_payment(self):
        try:
            # Obtener los datos del cuerpo de la solicitud
            request_data = request.json
            if not request_data:
                return jsonify({'error': 'Invalid data'}), 400

            # Extraer datos de la solicitud
            name = request_data.get('name')
            user_id = request_data.get('user_id')
            items = request_data.get('items', [])

            # Validar los datos de la solicitud con el esquema
            try:
                self.payment_schema.validate_name(name)
                self.payment_schema.validate_user_id(user_id)
                self.payment_schema.validate_items(items)
            except ValidationError as e:
                return jsonify({'error': f'Invalid data: {e}'}), 400

            # Calcular el total de la orden
            total = self.payment_service.calculate_total_price(items)

            # Crear el nuevo pago (incluyendo el total calculado)
            new_payment = {
                'name': name,
                'user_id': user_id,
                'items': items,
                'total_price': total  # Agregamos el total calculado
            }

            # Llamar al servicio para añadir el nuevo pago
            created_payment = self.payment_service.add_payment(new_payment)

            # Registrar en el log y devolver la respuesta
            self.logger.info(f'New Payment Created: {created_payment}')
            return jsonify(created_payment), 201

        except Exception as e:
            self.logger.error(f'Error adding a new payment: {e}')
            return jsonify({'error': f'An error occurred: {e}'}), 500
