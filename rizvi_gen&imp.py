import os
import random

def extract_subject_impression_class(filename):
    """Extract subject ID, impression number, and class number from filename."""
    parts = filename.split("_")
    if len(parts) < 3:
        return None, None, None  # Invalid filename format

    subject_id = parts[0]  # Subject ID (before the first "_")
    impression = parts[1]  # Impression (e.g., "imp1")
    class_num = parts[-1].split(".")[0]  # Class number (between last "_" and ".")

    return subject_id, impression, class_num


def generate_genuine_pairs(main_folder):
    """Generate genuine pairs: Same subject, same class, different impressions."""
    genuine_pairs = []
    file_dict = {}

    # Organizing images by (subject, class)
    for filename in os.listdir(main_folder):
        if filename.endswith((".jpg", ".JPG", ".png", ".PNG")):
            subject_id, impression, class_num = extract_subject_impression_class(filename)
            if not subject_id or not impression or not class_num:
                continue  # Skip invalid filenames

            key = (subject_id, class_num)  # Grouping based on (subject, class)
            if key not in file_dict:
                file_dict[key] = []
            file_dict[key].append(filename)

    # Creating genuine pairs
    for key, files in file_dict.items():
        if len(files) > 1:
            for i in range(len(files)):
                for j in range(i + 1, len(files)):
                    file1 = os.path.join(main_folder, files[i])
                    file2 = os.path.join(main_folder, files[j])
                    genuine_pairs.append(f"{file1} {file2}")

    print(f"Generated {len(genuine_pairs)} genuine pairs.")
    return genuine_pairs


def generate_imposter_pairs(main_folder, max_comparisons=1000000):
    """Generate imposter pairs: Different subjects, any class."""
    imposter_pairs = set()
    image_files = []

    # Collect all image files with extracted details
    for filename in os.listdir(main_folder):
        if filename.endswith((".jpg", ".JPG", ".png", ".dat")):
            subject_id, impression, class_num = extract_subject_impression_class(filename)
            if subject_id and class_num:
                image_files.append((subject_id, class_num, impression, filename))

    if len(image_files) < 2:
        raise ValueError("Not enough images to create imposter pairs!")

    # Randomly sample pairs from different subjects
    while len(imposter_pairs) < max_comparisons:
        img1, img2 = random.sample(image_files, 2)

        subject1, class1, impression1, file1 = img1
        subject2, class2, impression2, file2 = img2

        # Ensure different subjects
        if subject1 != subject2:
            pair_str = f"{os.path.join(main_folder, file1)} {os.path.join(main_folder, file2)}"
            imposter_pairs.add(pair_str)

    print(f"Generated {len(imposter_pairs)} imposter pairs.")
    return list(imposter_pairs)


# Paths
main_folder = "/media/abbas/New_Drive/contactless_Fingerprint/verifinger/Neurotec_Biometric_12_3_SDK/Tutorials/Biometrics/CPP/VerifyFingerCPP/rizvi/Sample_images"
index_location = "/media/abbas/New_Drive/contactless_Fingerprint/verifinger/Neurotec_Biometric_12_3_SDK/Tutorials/Biometrics/CPP/VerifyFingerCPP/rizvi/"

# Generate pairs
genuine_pairs = generate_genuine_pairs(main_folder)
imposter_pairs = generate_imposter_pairs(main_folder, max_comparisons=1000)

# Write Genuine Pairs to File
genuine_file_path = os.path.join(index_location, 'genuine_pairs.txt')
with open(genuine_file_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(genuine_pairs))
print(f"Stored {len(genuine_pairs)} genuine pairs in {genuine_file_path}")

# Write Imposter Pairs to File
imposter_file_path = os.path.join(index_location, 'imposter_pairs.txt')
with open(imposter_file_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(imposter_pairs))
print(f"Stored {len(imposter_pairs)} imposter pairs in {imposter_file_path}")
