from django.forms import Form, CharField, IntegerField


class InventoryPositionStockQuantityCommentForm(Form):
    stock = IntegerField(label='quantity')
    comment = CharField(label='comment', max_length=100, required=False)

