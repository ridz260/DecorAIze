import streamlit as st
from utils.image_generation import generate_image


st.title('DecorAIze: Your AI Interior Designer')

interior_styles = [
    'Indian', 'Minimal', 'Contemporary', 'Traditional', 'Art Deco', 'Scandinavian',
    'Industrial', 'Mid-Century Modern', 'Bohemian', 'Rustic', 'Shabby Chic', 'Hollywood Glam',
    'Coastal', 'French Country', 'Eclectic', 'Victorian', 'Baroque', 'Rococo', 'Gothic', 'Bauhaus',
    'Modern', 'Country', 'Zen', 'Retro', 'Mediterranean', 'Tropical', 'Asian', 'Craftsman', 'Farmhouse', 'Art Nouveau'
]


def main():

    room_type = st.selectbox(label = "Enter the room type", options = ['', 'Living Room', 'Bedroom', 'Kitchen', 'Bathroom', 'Dining Room'])
    style_type = st.selectbox(label = "Enter the room style", options = ['', *interior_styles])
    objects = st.text_input(label = "Enter or Select the objects to be placed in room", help='Example: sofa, Coffee Table, etc.')
    extra_details = st.text_area(label = "Additional Details (e.g., colors, material) (Optional)")

    if st.button('Generate Interior Design'):
        prompt = f"Generate an interior design for {style_type}, {room_type} with {objects}. Extra details include {extra_details}"

        generate_image(style=style_type, room_type=room_type, object_input=objects, details=extra_details)

        st.image(image='./src/static/generated_image.png', width = 1280)

if __name__ == '__main__':
    main()
