import streamlit as st
from utils.image_generation import generate_image
import os

st.set_page_config(
    page_title="DecorAIze",
    page_icon="🛋️",
    layout="wide"
)

st.title('DecorAIze: Your AI Interior Designer')

interior_styles = [
    'Indian', 'Minimal', 'Contemporary', 'Traditional', 'Art Deco', 'Scandinavian',
    'Industrial', 'Mid-Century Modern', 'Bohemian', 'Rustic', 'Shabby Chic', 'Hollywood Glam',
    'Coastal', 'French Country', 'Eclectic', 'Victorian', 'Baroque', 'Rococo', 'Gothic', 'Bauhaus',
    'Modern', 'Country', 'Zen', 'Retro', 'Mediterranean', 'Tropical', 'Asian', 'Craftsman', 'Farmhouse', 'Art Nouveau'
]

def main():
    room_type = st.selectbox("Enter the room type", options=['', 'Living Room', 'Bedroom', 'Kitchen', 'Bathroom', 'Dining Room'])
    style_type = st.selectbox("Enter the room style", options=['', *interior_styles])
    objects = st.text_input("Enter or Select the objects to be placed in room", placeholder="e.g., sofa, coffee table, rug")
    extra_details = st.text_area("Additional Details (Optional)", placeholder="e.g., use light pastel colors, wooden flooring")

    st.markdown("### Optional: Enter Room Dimensions (in feet/meters)")
    col1, col2, col3 = st.columns(3)
    with col1:
        length = st.number_input("Length", min_value=0.0, format="%.2f")
    with col2:
        width = st.number_input("Width", min_value=0.0, format="%.2f")
    with col3:
        height = st.number_input("Height", min_value=0.0, format="%.2f")

    if st.button('Generate Interior Design'):
        if not room_type or not style_type or not objects:
            st.warning("Please make sure to fill in all the required fields.")
        else:
            # Build dimension info
            dimension_info = ""
            if length and width:
                dimension_info += f" The room dimensions are {length}x{width} feet"
                if height:
                    dimension_info += f" with a height of {height} feet."
                else:
                    dimension_info += "."

            prompt = f"Generate an interior design for a {style_type} {room_type} with {objects}. Extra details: {extra_details}.{dimension_info}"

            st.write("Prompt used for generation:")
            st.code(prompt)

            with st.spinner("Generating your interior design..."):
                success = generate_image(
                    style=style_type,
                    room_type=room_type,
                    object_input=objects,
                    details=f"{extra_details}{dimension_info}"
                )

                image_path = os.path.abspath('./src/static/generated_image.png')

                if os.path.exists(image_path):
                    if success:
                        st.success("✅ Image successfully generated!")
                    else:
                        st.warning("⚠️ Showing placeholder image (API failed)")
                    st.image(image_path, width=800)

                else:
                    st.error("❌ Image generation failed completely")

if __name__ == '__main__':
    main()
