from flask import jsonify
from logger.logger_base import Logger

# Service for managing inventory
class InventoryService:
    def __init__(self, db_conn):
        self.logger = Logger()
        self.db_conn = db_conn

    # Getting all the inventories
    def get_all_inventories(self):
        try:
            # Reading
            inventories = list(self.db_conn.db.inventories.find())
            return inventories
        except Exception as e:
            self.logger.error(f'Error fetching all inventories from the database: {e}')
            return jsonify({ 'error': f'Error fetching all inventories from the database: {e}' }), 500
    
    # Adding an inventory
    def add_inventory(self, new_inventory):
        try:
            # Calculating next id
            last_inventory = self.db_conn.db.inventories.find_one(sort=[('_id', -1)])
            next_id = (last_inventory['_id'] + 1 if last_inventory else 1)
            new_inventory["_id"] = next_id
            # Adding
            self.db_conn.db.inventories.insert_one(new_inventory)
            return new_inventory
        except Exception as e:
            self.logger.error(f'Error creating the new inventory: {e}')
            return jsonify({ 'error': f'Error creating the new inventory: {e}' }), 500
        
    # Getting an inventory by id
    def get_inventory_by_id(self, inventory_id):
        try:
            inventory = self.db_conn.db.inventories.find_one({'_id': inventory_id})
            return inventory
        except Exception as e:
            self.logger.error(f'Error fetching the inventory id from the database: {e}')
            return jsonify({'error': f'Error fetching the inventory id from the database: {e}'}), 500
        
    # Updating an inventory
    def update_inventory(self, inventory_id, inventory):
        try:
            update_inventory = self.get_inventory_by_id(inventory_id)

            if update_inventory:
                updated_inventory = self.db_conn.db.inventories.update_one({'_id': inventory_id}, {'$set': inventory})
                if updated_inventory.modified_count > 0:
                    return inventory
                else:
                    return 'The inventory is already up-to-date'
            else:
                return None
        except Exception as e:
            self.logger.error(f'Error updating the inventory: {e}')
            return jsonify({'error': f'Error updating the inventory: {e}'}), 500
        
    def update_inventory_existence(self, inventory_id, existence):
        try:
            update_inventory = self.get_inventory_by_id(inventory_id)

            # Just update the existence for inventory
            if update_inventory:
                updated_inventory = self.db_conn.db.inventories.update_one({'_id': inventory_id}, {'$set': {'existence': existence}})
                if updated_inventory.modified_count > 0:
                    self.logger.info("INCIO")
                    update_inventory["existence"] = existence
                    return update_inventory
                else:
                    return 'The inventory existence is already up-to-date'
            else:
                return None
        except Exception as e:
            self.logger.error(f'Error updating the inventory existence: {e}')
            return jsonify({'error': f'Error updating the inventory existence: {e}'}), 500
    
    # Deleting inventory
    def delete_inventory(self, inventory_id):
        try:
            deleted_inventory = self.get_inventory_by_id(inventory_id)

            if deleted_inventory:
                self.db_conn.db.inventories.delete_one({'_id': inventory_id})            
                return deleted_inventory
            else:
                return None            
        except Exception as e:
            self.logger.error(f'Error deleting the inventory data: {e}')
            return jsonify({'error': f'Error deleting the inventory: {e}'}), 500

# Test
if __name__ == '__main__':
    from models.inventory_model import InventoryModel

    logger = Logger()
    db_conn = InventoryModel()
    inventory_service = InventoryService(db_conn)

    try:
        db_conn.connect_to_database()
        inventories = inventory_service.get_all_inventories()
        logger.info(f'Inventories fetched: {inventories}')

        # Add inventory
        new_inventory = inventory_service.add_inventory({'name': 'Corn', 'unit': 'kg', 'existence': 19, 'image': 'Some image test.'})
        logger.info(f'New inventory added: {new_inventory}')
        
        inventories = inventory_service.get_all_inventories()
        logger.info(f'Inventories fetched: {inventories}')

        # Get inventory by ID
        inventory = inventory_service.get_inventory_by_id(1)
        logger.info(f'Inventory fetched: {inventory}')

        # Update inventory
        new_inventory = inventory_service.update_inventory(1, {'name': 'Corn updated for testing', 'unit': 'kg', 'existence': 32, 'image': 'Some image test.'})
        logger.info(f'Inventory updated: {new_inventory}')
        
        inventories = inventory_service.get_all_inventories()
        logger.info(f'Inventories fetched: {inventories}')

        # Delete inventory by ID
        inventory = inventory_service.delete_inventory(1)
        logger.info(f'Inventory deleted: {inventory}')
    except Exception as e:
        logger.error(f'An error has ocurred: {e}')
    finally:
        db_conn.close_connection()
        logger.info('Connection to database was succesfully closed.')
