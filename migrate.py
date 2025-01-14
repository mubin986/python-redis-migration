import redis
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Retrieve sensitive data from environment variables
source_host = os.environ.get('SOURCE_HOST')
source_port = int(os.environ.get('SOURCE_PORT', 0))
source_password = os.environ.get('SOURCE_PASSWORD')

dest_host = os.environ.get('DEST_HOST')
dest_port = int(os.environ.get('DEST_PORT', 0))
dest_password = os.environ.get('DEST_PASSWORD')

# Connect to source and destination
source = redis.StrictRedis(host=source_host, port=source_port, password=source_password, decode_responses=False)
destination = redis.StrictRedis(host=dest_host, port=dest_port, password=dest_password, decode_responses=False)

# Get total number of keys for progress estimation
total_keys = source.dbsize()
print(f"Total keys in source: {total_keys}")

processed_keys = 0
cursor = 0

while True:
    cursor, keys = source.scan(cursor=cursor, count=1000)  # Adjust count as needed
    for key in keys:
        try:
            # Serialize the value from the source
            dumped_value = source.dump(key)
            if dumped_value is None:
                continue  # Key might have been deleted between SCAN and DUMP

            # Get remaining TTL in milliseconds
            ttl = source.pttl(key)
            ttl = ttl if ttl and ttl > 0 else 0  # Use 0 if no expiry

            # Restore the key to the destination
            destination.restore(key, ttl, dumped_value, replace=True)
            processed_keys += 1

            # Print progress every 100 keys
            if processed_keys % 100 == 0:
                percentage = (processed_keys / total_keys) * 100 if total_keys else 0
                print(f"Processed {processed_keys} keys out of {total_keys} ({percentage:.2f}%).")

        except Exception as e:
            print(f"Error migrating key {key}: {e}")

    # End loop if scan is complete
    if cursor == 0:
        break

print(f"Migration complete. Total keys processed: {processed_keys}")
