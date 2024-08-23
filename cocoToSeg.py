# Program to convert coco json to segmentation mask

import json
from PIL import Image, ImageDraw
import os

class Conversion:
    def __init__(self, json_path, output_folder, image_width, image_height):
        self.json_path = json_path
        self.output_folder = output_folder
        self.image_width = image_width
        self.image_height = image_height
        
    def read_coco_annotations(self):
        with open(self.json_path, 'r') as f:
            coco_data = json.load(f)
        
        # Access annotations and categories
        annotations = coco_data.get('annotations', [])
        categories = coco_data.get('categories', [])

        # Create a mapping from category_id to category name
        category_mapping = {category['id']: category['name'] for category in categories}

        # Process annotations
        for annotation in annotations:
            image_id = annotation.get('image_id')
            category_id = annotation.get('category_id')
            segmentation = annotation.get('segmentation')  # list of polygon coordinates
            
            # Access category name using the mapping
            category_name = category_mapping.get(category_id)

            # Create an empty mask image with image dimensions
            mask_image = Image.new('L', (self.image_width, self.image_height), 0)

            # Draw the segmentation mask on the image
            ImageDraw.Draw(mask_image).polygon(segmentation[0], outline=255, fill=255)

            # Save the mask image
            output_path = os.path.join(self.output_folder, f"mask_{image_id}_{category_name}.png")
            mask_image.save(output_path)


# Example usage:
json_path = 'filePath/to/coco.json'
output_folder = 'output_masks'
image_width = 512
image_height = 512

converter = Conversion(json_path, output_folder, image_width, image_height)
converter.read_coco_annotations()


