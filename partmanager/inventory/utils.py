from .models import InventoryReservation


def reserve_quantity(inventory_position, assembly, quantity):
    reservation = InventoryReservation(quantity=quantity,
                                       inventory=inventory_position,
                                       assembly=assembly)
    reservation.save()
