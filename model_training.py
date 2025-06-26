# === Constants ===
dataset_path = 'dataset'     # Dataset folder
feedback_path = 'feedback_folder'   # Feedback folder
img_size = (224, 224)        # MobileNetV2 default input size
batch_size = 32
epochs = 15  # Tune based on overfitting/underfitting

def retrain_model():
    import os
    import shutil
    import tempfile
    import tensorflow as tf
    from tensorflow.keras.preprocessing.image import ImageDataGenerator # type: ignore
    from tensorflow.keras.applications import MobileNetV2 # type: ignore
    from tensorflow.keras import layers, models # type: ignore

    # === Step 1: Merge dataset and feedback ===
    def merge_datasets(original_path, feedback_path, screenshots_path):
        temp_dir = tempfile.mkdtemp()
        print(f"[INFO] Merging datasets into temp folder: {temp_dir}")

        # Define the final class folders
        class_map = {
            'Harassment': [
                os.path.join(original_path, 'Harassment'),
                os.path.join(feedback_path, 'false_negative'),
                screenshots_path
            ],
            'NoHarassment': [
                os.path.join(original_path, 'NoHarassment'),
                os.path.join(feedback_path, 'false_positive')
            ]
        }

        for class_name, source_folders in class_map.items():
            dest_dir = os.path.join(temp_dir, class_name)
            os.makedirs(dest_dir, exist_ok=True)

            for folder in source_folders:
                if not os.path.exists(folder):
                    continue
                for img_file in os.listdir(folder):
                    src_img = os.path.join(folder, img_file)
                    dest_img = os.path.join(dest_dir, img_file)
                    if os.path.isfile(src_img):
                        shutil.copy2(src_img, dest_img)

        return temp_dir



    merged_data_path = merge_datasets(dataset_path, feedback_path, screenshots_path='screenshots_folder')


    # === Step 2: Prepare ImageDataGenerators ===
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2,
        rotation_range=20,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    val_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2
    )

    train_data = train_datagen.flow_from_directory(
        merged_data_path,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='training'
    )

    val_data = val_datagen.flow_from_directory(
        merged_data_path,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation'
    )

    num_classes = train_data.num_classes

    # === Step 3: Build Model with MobileNetV2 ===
    base_model = MobileNetV2(
        input_shape=(img_size[0], img_size[1], 3),
        include_top=False,
        weights='imagenet'
    )
    base_model.trainable = False  # Freeze base for transfer learning

    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(128, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation='softmax')
    ])

    # === Step 4: Compile & Train ===
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    model.fit(train_data, validation_data=val_data, epochs=epochs)

    # === Step 5: Save Model ===
    model.save("mobilenetv2_with_feedback.h5")
    print("[INFO] Model saved as 'mobilenetv2_with_feedback.h5'")

    # Cleanup merged temp dir
    shutil.rmtree(merged_data_path)
    print("[INFO] Temporary merged dataset folder removed.")

# Uncomment to run
# retrain_model()
