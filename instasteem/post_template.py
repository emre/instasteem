def get_images(images):
    content = ""
    for image_url in images:
        content += f"![image]({image_url})\n***\n"
    return content

def get_body(images, location, description, url, upload_date,
             include_metadata=False):
    content = f"{description}\n***\n"
    content += get_images(images)
    if include_metadata:
        content += f"|Location|{location}|\n|----------------|---|\n|" \
                   f"Instagram Post|{url}|\n"\
                   f"Upload Date|{upload_date}|\n"
    return content