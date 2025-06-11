import streamlit as st
from utils.api import ask_question, get_available_models


def render_chat():
    st.subheader("💬 Chat with your documents")
    
    # Model selection and settings in sidebar
    with st.sidebar:
        st.markdown("### 🤖 AI Model Settings")
        
        # Get available models
        models_info = get_available_models()
        
        if models_info:
            available_models = models_info.get("available_models", {})
            default_model = models_info.get("default_model", "gemini-exp-1206")
            
            # Model selection
            model_options = {}
            for model_id, model_data in available_models.items():
                display_name = f"{model_data['performance']} {model_data['name']}"
                model_options[display_name] = model_id
            
            selected_model_display = st.selectbox(
                "Select AI Model:",
                options=list(model_options.keys()),
                index=list(model_options.values()).index(default_model) if default_model in model_options.values() else 0,
                help="Choose the Gemini model for answering questions"
            )
            selected_model = model_options[selected_model_display]
            
            # Show model description
            if selected_model in available_models:
                model_info = available_models[selected_model]
                st.markdown(f"**Description:** {model_info['description']}")
                st.markdown(f"**Best for:** {', '.join(model_info['best_for'])}")
                st.markdown(f"**Release:** {model_info.get('release', 'N/A')}")
            
            st.markdown("---")
            
            # Temperature control
            temperature = st.slider(
                "Response Creativity:",
                min_value=0.0,
                max_value=1.0,
                value=0.1,
                step=0.1,
                help="Lower values = more precise, Higher values = more creative"
            )
            
            # Store in session state
            st.session_state.selected_model = selected_model
            st.session_state.temperature = temperature
            
        else:
            st.warning("Could not load model information from server")
            st.session_state.selected_model = None
            st.session_state.temperature = 0.1

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Render existing chat history
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).markdown(msg["content"])

    # Input and response
    user_input = st.chat_input("Type your question here...")
    if user_input:
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Show which model is being used
        model_name = getattr(st.session_state, 'selected_model', None)
        temp = getattr(st.session_state, 'temperature', 0.1)
        
        with st.chat_message("assistant"):
            with st.spinner(f"🤖 Thinking with {model_name or 'default model'}..."):
                response = ask_question(user_input, model_name=model_name, temperature=temp)
                
            if response.status_code == 200:
                data = response.json()
                answer = data["response"]
                sources = data.get("sources", [])
                
                st.markdown(answer)
                if sources:
                    st.markdown("📄 **Sources:**")
                    for src in sources:
                        st.markdown(f"- `{src}`")
                        
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                error_msg = f"Error: {response.text}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
