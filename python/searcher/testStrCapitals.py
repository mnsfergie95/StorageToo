from decimal import Decimal, ROUND_HALF_UP
price = float(70.00)
partialPmt = Decimal(price*15/30)
rounded_amount = partialPmt.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
print("partial pmt is ", rounded_amount)