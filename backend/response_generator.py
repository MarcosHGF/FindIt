from custom_utils import infer_region

def generate_response_with_context(object_name, detected_objects):
    target_object = None
    nearby_objects = []

    # Find the mentioned object
    for obj in detected_objects:
        if obj["name"] == object_name:
            target_object = obj
            break

    if not target_object:
        return f"I couldn't find your {object_name} in the image."

    # Find nearby objects
    nearby_objects = target_object.get("nearby", [])

    # Infer region
    region = infer_region(target_object["position"])

    # Generate response
    if nearby_objects:
        nearby_text = ", ".join(nearby_objects)
        return f"Your {object_name} is in the {region}, near the {nearby_text}."
    else:
        return f"Your {object_name} is in the {region}."