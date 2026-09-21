import streamlit as st
from PIL import Image
from transformers import pipeline

st.set_page_config(
    page_title="AI-ECE Vision",
    page_icon="🔬",
    layout="centered"
)

# ECE component knowledge base
component_info = {
    "a resistor": {
        "name": "Resistor",
        "function": "Limits or controls the flow of electric current.",
        "working": "A resistor produces a voltage drop according to the current flowing through it and its resistance.",
        "applications": "Voltage dividers, current limiting, biasing circuits, filters, and LED protection.",
        "concepts": "Ohm's Law, voltage division, current division, power dissipation"
    },

    "a capacitor": {
        "name": "Capacitor",
        "function": "Stores electrical energy in an electric field.",
        "working": "A capacitor stores charge between two conductive plates separated by an insulating material.",
        "applications": "Filtering, coupling, decoupling, timing circuits, and energy storage.",
        "concepts": "Capacitance, RC circuits, charging and discharging"
    },

    "an LED": {
        "name": "LED",
        "function": "Produces light when current flows through it in the forward direction.",
        "working": "An LED emits light when electrons and holes recombine inside the semiconductor junction.",
        "applications": "Indicators, displays, lighting, communication, and optical sensing.",
        "concepts": "PN junction, forward bias, semiconductor devices"
    },

    "a diode": {
        "name": "Diode",
        "function": "Allows current to flow mainly in one direction.",
        "working": "A PN junction conducts under forward bias and blocks current under reverse bias.",
        "applications": "Rectifiers, protection circuits, switching, clipping, and voltage regulation.",
        "concepts": "PN junction, forward bias, reverse bias, rectification"
    },

    "a transistor": {
        "name": "Transistor",
        "function": "Acts as an electronic switch or amplifier.",
        "working": "A small input signal controls a larger current through the transistor.",
        "applications": "Amplifiers, digital logic, switching circuits, oscillators, and signal processing.",
        "concepts": "Biasing, amplification, switching, semiconductor devices"
    },

    "an integrated circuit": {
        "name": "Integrated Circuit (IC)",
        "function": "Contains multiple electronic components fabricated on a single semiconductor chip.",
        "working": "Transistors and other components are interconnected on a chip to perform a specific electronic function.",
        "applications": "Microcontrollers, processors, amplifiers, sensors, communication systems, and digital electronics.",
        "concepts": "VLSI, CMOS, digital logic, semiconductor fabrication"
    },

    "a breadboard": {
        "name": "Breadboard",
        "function": "Provides a temporary platform for building and testing electronic circuits.",
        "working": "Internal metal contacts electrically connect components inserted into the breadboard holes.",
        "applications": "Prototyping, laboratory experiments, circuit testing, and student projects.",
        "concepts": "Circuit prototyping, connections, electronic experimentation"
    },

    "an electronic circuit": {
        "name": "Electronic Circuit",
        "function": "Combines electronic components to perform a desired electrical function.",
        "working": "Components interact through electrical connections to process, control, or transfer signals and power.",
        "applications": "Consumer electronics, communication systems, control systems, computers, and embedded systems.",
        "concepts": "Circuit analysis, voltage, current, power, signals"
    }
}


@st.cache_resource
def load_model():
    return pipeline(
        "zero-shot-image-classification",
        model="openai/clip-vit-base-patch32"
    )


st.title("🔬 AI-ECE Vision")
st.subheader("AI-Powered Intelligent Electronics Lab Assistant")

st.write(
    "Upload an image of an electronic component and "
    "AI-ECE Vision will identify it and provide ECE-related information."
)

uploaded_file = st.file_uploader(
    "Upload an electronic component image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    st.image(
        image,
        caption="Uploaded Component",
        width="stretch"
    )

    with st.spinner("Analyzing component with AI..."):

        classifier = load_model()

        labels = list(component_info.keys())

        results = classifier(
            image,
            candidate_labels=labels
        )

    best_result = results[0]

    component_key = best_result["label"]
    confidence = best_result["score"] * 100

    information = component_info[component_key]

    st.success("AI analysis completed!")

    st.subheader("🔎 Identified Component")

    st.write(f"### {information['name']}")

    st.write(
        f"**AI confidence:** {confidence:.2f}%"
    )

    st.subheader("⚡ Function")

    st.write(information["function"])

    st.subheader("⚙️ Working Principle")

    st.write(information["working"])

    st.subheader("📌 Applications")

    st.write(information["applications"])

    st.subheader("📚 Related ECE Concepts")

    st.write(information["concepts"])

    st.subheader("📊 Other Possibilities")

    for result in results[1:4]:

        st.write(
            f"{result['label'].title()} — "
            f"{result['score'] * 100:.2f}%"
        )

else:

    st.info("Please upload an electronic component image to begin.")