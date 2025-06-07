# Jorge Adrian de la Garza Flores - A00838816
# TASK --- Determine which variables are shared among different threads. --- TASK
# baskets: shared resource for produced items
# brands: shared resource for item types
# orders: shared resource for production orders

# TASK ---- Detect possible concucrrent problems that may arise from this implementation. --- TASK
# There is a race condition when a consumer tries to access a basket that is being modified by a producer.
# Multiple producers can modify the same basket at the same time, leading to inconsistent data.
# The consumer may try to consume items from a basket that is currently being modified by a producer.
# No locks are used to protect shared resources, which can lead to data corruption.

# Solution: Use a threading event to signal when a basket is ready for consumption.
# A lock was added for each brand to ensure that only one thread can access a basket at a time.
# A final stop was added to the consumer thread to allow it to finish processing after all producers have finished.



import threading, time, random

# Shared resources: brands of items, empty baskets
brands = ['a', 'b', 'c', 'd', 'e']
baskets = dict(zip(brands, [[] for _ in brands]))
# Added locks to fix concurrency issues by ensuring that only one thread can access a basket at a time
locks = dict(zip(brands, [threading.Lock() for _ in brands]))

# A simple class simulating a product
class ProductClass:
    def __init__(self, brand):
        self.brand = brand
        time.sleep(random.random() / 10)   # Simulating production time

# Class implementing the consumer
class ConsumerThread(threading.Thread):
    def __init__(self, timeout = 0):
        super().__init__()
        self.timeout = timeout
        self.stop_event = threading.Event()     # Stop thread after timeout
        self.inventory = dict(zip(['a', 'b', 'c', 'd', 'e'], [0] * 5))  # Initialize inventory

    def run(self):
        print("Consumer starting...")
        # Consuming data. An inventory of the total produced items should be stored after concluding
        end_time = time.time() + self.timeout
        keys = ['a', 'b', 'c', 'd', 'e']
        while not self.stop_event.is_set() or any(baskets[key] for key in keys):
            for key in keys:
                # Locking the basket to ensure only one consumer accesses it at a time
                with locks[key]:
                # Verifying if products of type key have been produced
                    if baskets[key]:
                        value = len(baskets[key])
                        print(f"Consumed:\t{key} -> {value}")
                        # Products are taken and inventory updated
                        baskets[key].clear()
                        self.inventory[key] += value
                    time.sleep(random.random())  # Simulate time-consuming processing randomly
        print("Consumer terminating...")

    def stop(self):
        self.stop_event.set()

if __name__ == '__main__':
    # Function to be executed by producer threads.
    # Input: an order with the type and number of products to produce 
    def data_producer(order_num):
        order = orders[order_num]
        for key in order:
            value = order[key]
            # Lock the basket so that only one producer can modify it at a time
            with locks[key]:
                baskets[key].extend([ProductClass(key) for _ in range(value)])
                print(f"Producer {order_num}:\t{key} -> {value}")


    # Generating orders randomly for each producer
    nproducers = 3
    orders = []
    for i in range(nproducers):
        # randomly select a number of brands
        n = random.randint(2, 4)
        keys = random.sample(brands, n)
        orders.append(dict(zip(keys, [random.randint(1, 10) for _ in range(n)])))

    # Executing producers
    producers = [threading.Thread(target=data_producer, args=(i, )) for i in range(nproducers)]
    [thread.start() for thread in producers]

    # Executing consumer, and waiting for all threads to conclude
    consumer = ConsumerThread(timeout=10)
    consumer.start()
    [thread.join() for thread in producers]
    consumer.stop() # Signal consumer to stop to allow it to finish processing
    consumer.join()

    print('Final result: {}'.format(consumer.inventory))