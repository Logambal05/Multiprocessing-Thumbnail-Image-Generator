import os
from PIL import Image
from io import BytesIO
from multiprocessing import Process, Queue


def producer(queue, image_dir):
    for file_name in os.listdir(image_dir):
        if file_name.lower().endswith((".jpg", ".jpeg", ".png")):
            path = os.path.join(image_dir, file_name)
            img = Image.open(path)
            img.thumbnail((800, 800))
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            buffer = BytesIO()
            img.save(buffer, format="JPEG")
            queue.put((file_name, buffer.getvalue()))
    queue.put(None)


def consumer(queue, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    while True:
        item = queue.get()
        if item is None:
            break
        file_name, img_bytes = item
        img = Image.open(BytesIO(img_bytes))
        save_path = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}-thumbnail.jpg")
        img.save(save_path)


def start_processing(input_dir, output_dir):
    main_queue = Queue()
    producer_queue = Process(target=producer, args=(main_queue, input_dir))
    consumer_queue = Process(target=consumer, args=(main_queue, output_dir))
    producer_queue.start()
    consumer_queue.start()
    producer_queue.join()
    consumer_queue.join()


if __name__ == '__main__':
    start_processing("producer", "consumer")
