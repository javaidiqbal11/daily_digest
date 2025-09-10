import os
import random
import shutil
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img, array_to_img

THRESHOLD = 20000  # per class limit
IMG_SIZE = (224, 224)  # resize target for normalization


def save_normalized_image(img_path, save_path):
    """Load, resize, normalize, and save image."""
    img = load_img(img_path, target_size=IMG_SIZE)
    x = img_to_array(img) / 255.0  # normalize to [0, 1]
    img = array_to_img(x)          # convert back to image
    img.save(save_path)


def balance_dataset(input_dir, output_dir, threshold=THRESHOLD):
    """
    Balances dataset classes by downsampling or upsampling each class
    to exactly `threshold` images. Normalizes images before saving.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    datagen = ImageDataGenerator(
        rotation_range=30,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode="nearest"
    )

    for class_name in os.listdir(input_dir):
        class_path = os.path.join(input_dir, class_name)
        if not os.path.isdir(class_path):
            continue

        output_class_path = os.path.join(output_dir, class_name)
        os.makedirs(output_class_path, exist_ok=True)

        images = os.listdir(class_path)
        num_images = len(images)

        print(f"\nProcessing class: {class_name} ({num_images} images)")

        # ---------------- Downsampling ----------------
        if num_images > threshold:
            selected_images = random.sample(images, threshold)
            for img in selected_images:
                src = os.path.join(class_path, img)
                dst = os.path.join(output_class_path, img)
                save_normalized_image(src, dst)
            print(f"✔ Downsampled {class_name} to {threshold} normalized images.")

        # ---------------- Upsampling ----------------
        elif num_images < threshold:
            # Copy & normalize all available images first
            for img in images:
                src = os.path.join(class_path, img)
                dst = os.path.join(output_class_path, img)
                save_normalized_image(src, dst)

            img_index = 0
            while len(os.listdir(output_class_path)) < threshold:
                img_name = images[img_index % num_images]
                img_path = os.path.join(class_path, img_name)

                try:
                    img = load_img(img_path, target_size=IMG_SIZE)
                    x = img_to_array(img) / 255.0  # normalize
                    x = x.reshape((1,) + x.shape)

                    prefix = os.path.splitext(img_name)[0]
                    save_prefix = f"{prefix}_aug"

                    for batch in datagen.flow(
                        x, batch_size=1,
                        save_to_dir=output_class_path,
                        save_prefix=save_prefix,
                        save_format="jpg"
                    ):
                        if len(os.listdir(output_class_path)) >= threshold:
                            break
                except Exception as e:
                    print(f"⚠ Error processing {img_name}: {e}")

                img_index += 1

            print(f"✔ Upsampled {class_name} to {threshold} normalized images.")

        # ---------------- Exact case ----------------
        else:
            for img in images:
                src = os.path.join(class_path, img)
                dst = os.path.join(output_class_path, img)
                save_normalized_image(src, dst)
            print(f"✔ {class_name} already has {threshold} images. Normalized and copied.")


def main():
    # 👉 set your input and output dataset folders here
    input_dir = "C:/Users/Administrator/Downloads/daily_digest/image-normalize/dataset"
    output_dir = "C:/Users/Administrator/Downloads/daily_digest/image-normalize/dataset_balanced"
    threshold = 20000

    balance_dataset(input_dir, output_dir, threshold)


if __name__ == "__main__":
    main()

