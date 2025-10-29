from PIL import Image, ImageOps #pillow for image converting
import os
import mimetypes

ATTACHMENTS_DIR = "benchmark/attachments/"

def process_image_file(filename: str, operation: str = "info", **kwargs):

    """
    Processes various image files (.jpg, .png, .jpeg, etc.) located in the benchmark/attachments/ directory.

    If the file is not an image, it will return an error message telling the agent 
    that only image files are supported.

    Supported operations:
        - "info": return image metadata (format, size, mode)
        - "resize": resize image (requires width and height kwargs)
        - "rotate": rotate image (requires degrees kwarg)
        - "grayscale": convert to grayscale
        - "flip": flip image horizontally or vertically (direction="horizontal"/"vertical")

    Args:
        filename: The name of the image file to process ("photo.png").
        operation: The action to perform (default: "info").
        kwargs: Additional parameters required for specific operations (e.g., width, height, degrees, direction).

    Returns:
        A dictionary containing image metadata and the processed filename, or an error message if the operation fails.
    """

    file_path = os.path.join(ATTACHMENTS_DIR, filename)

    if not os.path.exists(file_path):
        return f"Error: File '{filename}' not found."

    mimetype, _ = mimetypes.guess_type(file_path)
    if not mimetype or not mimetype.startswith("image/"):
        return f"Error: '{filename}' is not an image file."

    try:
        with Image.open(file_path) as img:
            img_info = {"filename": filename, "format": img.format, "size": img.size, "mode": img.mode}
            
            ops = operation.lower().split()
            for op in ops:
                if op == "info":
                    continue
                elif op == "flip":
                    direction = kwargs.get("direction", "horizontal")
                    if direction == "horizontal":
                        img = img.transpose(Image.FLIP_LEFT_RIGHT)
                    elif direction == "vertical":
                        img = img.transpose(Image.FLIP_TOP_BOTTOM)
                    else:
                        return "Error: 'flip' direction must be 'horizontal' or 'vertical'."
                elif op == "resize":
                    width = kwargs.get("width")
                    height = kwargs.get("height")
                    if width is None or height is None:
                        return "Error: 'resize' requires width and height arguments."
                    img = img.resize((width, height))
                elif op == "rotate":
                    degrees = kwargs.get("degrees", 90)
                    img = img.rotate(degrees, expand=True)
                elif op == "grayscale":
                    img = ImageOps.grayscale(img)
                else:
                    return f"Error: Unsupported operation '{op}'"

            new_name = f"processed_{filename}"
            img.save(os.path.join(ATTACHMENTS_DIR, new_name))

            if ops == ["info"]:
                return img_info
            return {"info": img_info, "processed_file": new_name}
    except Exception as e:
        return f"Error processing image '{filename}': {str(e)}"
