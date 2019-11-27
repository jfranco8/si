
# drop db -U alumnodb si1
# createdb -U alumnodb si1
#
# cat dump_v1.sql | psql -U alumnodb si1
# cat actualiza.sql | psql -U alumnodb si1
# cat getTopVentas.sql | psql -U alumnodb si1
# cat getTopMonths.sql | psql -U alumnodb si1
# cat setOrderAmount.sql | psql -U alumnodb si1
# cat setPrice.sql | psql -U alumnodb si1
# cat updInventory.sql | psql -U alumnodb si1
# cat updOrders.sql | psql -U alumnodb si1


# drop db -U alumnodb -h localhost si1
# createdb -U alumnodb -h localhost si1

cat dump_v1.3.sql | psql -U alumnodb -h localhost si1
cat actualiza.sql | psql -U alumnodb -h localhost si1
cat getTopVentas.sql | psql -U alumnodb -h localhost si1
cat getTopMonths.sql | psql -U alumnodb -h localhost si1
cat setOrderAmount.sql | psql -U alumnodb -h localhost si1
cat setPrice.sql | psql -U alumnodb -h localhost si1
cat updInventory.sql | psql -U alumnodb -h localhost si1
cat updOrders.sql | psql -U alumnodb -h localhost si1
