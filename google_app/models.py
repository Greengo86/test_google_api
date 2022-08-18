from django.db import models


class Order(models.Model):
    number = models.IntegerField(verbose_name='number')
    order_number = models.IntegerField(verbose_name='Order number', unique=True, db_index=True)
    price_dollars = models.IntegerField(verbose_name='Price in Dollars')
    price_rubles = models.IntegerField(verbose_name='Price in Rubles')
    delivery_time = models.CharField(verbose_name='End time to delivery order', max_length=10)

    def __str__(self):
        return self.order_number

    @classmethod
    def bulk_create_orders(cls, uniques: list[str], data: list[dict]):
        """
        Multiple insert
        """
        data_dict, select = {}, None
        for entry in data:
            sub_entry, key = {}, ''
            for uniq in uniques:
                sub_entry[uniq] = entry[uniq]
                key += str(entry[uniq])
            data_dict[key] = entry

            if not select:
                select = models.Q(**sub_entry)
                continue
            select |= models.Q(**sub_entry)

        records = cls.objects.filter(select).values('pk', *uniques)
        existing = {}
        for rec in records:
            key = ''
            for uniq in uniques:
                key += str(rec[uniq])
            existing[key] = rec

        # Split new objects from existing ones
        to_create = []
        for key, entry in data_dict.items():
            obj = cls(**entry)
            if key not in existing:
                to_create.append(obj)
                continue
            obj.pk = existing[key]['pk']

        cls.objects.bulk_create(to_create, batch_size=1000)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
