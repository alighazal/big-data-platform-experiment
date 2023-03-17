import uuid
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class Journy(Model):
    __keyspace__ = "cqlengine"
    __table_name__ = "jounrys_2"
    uuid = columns.UUID(partition_key=True, default=uuid.uuid4)
    VendorID = columns.Integer()
    tpep_pickup_datetime = columns.DateTime()
    tpep_dropoff_datetime = columns.DateTime()
    passenger_count = columns.Float()
    trip_distance = columns.Float()
    RatecodeID = columns.Float()
    store_and_fwd_flag = columns.Text()
    PULocationID = columns.Integer(primary_key=True)
    DOLocationID = columns.Integer(partition_key=True)
    payment_type = columns.Integer()
    fare_amount = columns.Float()
    extra = columns.Float()
    mta_tax = columns.Float()
    tip_amount = columns.Float()
    tolls_amount = columns.Float()
    improvement_surcharge = columns.Float()
    total_amount = columns.Float()
    congestion_surcharge = columns.Float()
    airport_fee = columns.Float()
