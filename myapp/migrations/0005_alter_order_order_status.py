# Generated by Django 4.1.1 on 2022-11-13 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0004_product_interested"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="order_status",
            field=models.IntegerField(
                choices=[
                    (0, "Order Cancelled"),
                    (1, "Order Placed"),
                    (2, "OrderShipped"),
                    (3, "Order Delivered"),
                ],
                default=1,
            ),
        ),
    ]
