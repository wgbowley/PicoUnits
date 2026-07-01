from picounits import FREQUENCY, KILO


scale = 10 * KILO 
value = scale * FREQUENCY

print(f"Scale: {scale}")
print(f"Value: {value:.3f}")