import random
import string

characters = string.ascii_letters + string.digits + string.punctuation
random_combination = ''.join(random.choices(characters, k=10))

print(random_combination)
