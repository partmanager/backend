import logging
from django.db.models import Sum
from celery import shared_task
from .models import Assembly, Rework
from inventory.models import InventoryPosition, InventoryReservation
from inventory.utils import reserve_quantity


logger = logging.getLogger('projects')


# @shared_task
# def reserve_assembly_parts(assembly: Assembly):
#     for item in assembly.assembly_item_set.all():
#         reserved = item.inventoryreservation_set.all.aggregate(Sum('quantity'))['quantity_sum'] or 0
#         required = item.quantity + item.quantity_correction - reserved
#         reserve_parts(item.part, item.manufacturer_order_number, required, assembly)
#
#
# def reserve_parts(part, mon, required, assembly):
#     if mon is not None:
#         position = mon.inventoryposition_set.filter(stock__gte=required).order_by('-invoice__invoice_date').first()
#         if position:
#             reserve_quantity(position, assembly, required)
#     elif part is not None:
#         position = InventoryPosition.objects.filter(part__part=part, stock__gte=required).order_by('-invoice__invoice_date').first()
#         if position:
#             reserve_quantity(position, assembly, required)


def close_rework(rework_id):
    rework = Rework.objects.get(id=rework_id)
    if rework.closed is False:
        for reservation in InventoryReservation.objects.filter(assembly__rework=rework_id).all():
            comment = f"Used for {reservation.assembly.designator} in {reservation.assembly.assembly.project_version.project.name}, {reservation.assembly.assembly.project_version.name} SN: {reservation.assembly.assembly.serial_number}"
            print(comment)
            inventory = reservation.inventory
            inventory.stock -= reservation.quantity
            inventory.save_with_history(comment=comment, user_id=None)
        rework.closed = True
        rework.save()






