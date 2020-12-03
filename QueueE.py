import threading
from threading import Semaphore

"""Lab 3 Threaded Video Player
   Stephanie Callejas
   This lab assignment was created with the use of demos provided by the professors. 
   The lab involves first getting the frames from a video. The frames will be enconded and
   then stored into a queue. From the first queue we will be dequeing and decoding the frames
   into a photo and changing the photo from color to gray. The gray photo will be encoded and 
   stored into a second queue. Finally we will dequeue from the second queue each frame, 
   decode it to be a photo and display every 42 milliseconds a gray photo/frame into the
   screen. Important elements of the lab are that 3 threads will be used to concurrently
   process and trasform the frames. Semaphores will be used to avoid processing more than 
   10 frames at the time in each queue. 
"""

#Semaphores help by never going over the given capacity or lower than 0
#acquire() decrements by 1 its internal counter and release() increments by 1
#its internal counter

class QueueE: 
    def __init__(self, capacity = 10):
        self.queue = [] 
        self.capacity = capacity
        self.semaphoreCapacity = threading.Semaphore(capacity)
        self.semaphoreUsed = threading.Semaphore(0)

    #When adding to the queue, we have to check that it doesn't go over the capacity
    #(not going below 0 in the semaphoreCapacity) and updating the number of current
    #items with semaphoreUsed
    def enqueue(self, item):
        self.semaphoreCapacity.acquire()
        self.queue.append(item)
        self.semaphoreUsed.release()

    #When getting items from the queue we have to first check that we have something
    #to obtain (acquire decrements 1, since the semaphore can't go below 0, it has to have
    #an item, if it doesn't it will wait) and then update the capacity by releasing 1 from
    #semaphoreCapacity 
    def dequeue(self):
        self.semaphoreUsed.acquire()
        item = self.queue.pop(0)
        self.semaphoreCapacity.release()
        return item

    #Peek is not used in this lab
    def peek(self):
        return self.queue[0]

