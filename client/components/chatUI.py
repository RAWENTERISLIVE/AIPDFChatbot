import streamlit as st
from utils.api import ask_question, get_available_models


def render_chat():
    st.subheader("💬 Chat with your documents")
    
    # Model selection and settings in sidebar
    with st.sidebar:
        st.markdown("### 🤖 AI Model Settings")
        
        models_info = get_available_models() # This should call the renamed endpoint if api.py is also changed
        
        if models_info:
            available_models = models_info.get("available_models", {})
            # The default_model is now dynamically set by the server based on priority
            default_model_id_from_server = models_info.get("default_model", None)
            
            model_options = {}
            for model_id, model_data in available_models.items():
                display_name = f"{model_data.get('performance', 'N/A')} {model_data.get('name', model_id)}"
                model_options[display_name] = model_id
            
            # Determine the index for the default model in the selectbox
            default_selection_index = 0
            if default_model_id_from_server and default_model_id_from_server in model_options.values():
                default_selection_index = list(model_options.values()).index(default_model_id_from_server)
            elif model_options: # Fallback to the first model if default isn't found
                default_selection_index = 0

            selected_model_display = st.selectbox(
                "Select AI Model:",
                options=list(model_options.keys()),
                index=default_selection_index,
                help="Choose the Gemini model for answering questions. The list is updated by the server."
            )
            selected_model = model_options.get(selected_model_display) if selected_model_display else None
            
            if selected_model and selected_model in available_models:
                model_info = available_models[selected_model]
                st.markdown(f"**Description:** {model_info.get('description', 'N/A')}")
                st.markdown(f"**Best for:** {', '.join(model_info.get('best_for', []))}")
                st.markdown(f"**Release:** {model_info.get('release', 'N/A')}")
                st.markdown(f"**Priority:** {model_info.get('priority', 'N/A')}") # Display priority
            
            st.markdown("---")
            
            temperature = st.slider(
                "Response Creativity:",
                min_value=0.0, max_value=1.0, value=0.1, step=0.1,
                help="Lower values = more precise, Higher values = more creative"
            )
            
            st.session_state.selected_model = selected_model
            st.session_state.temperature = temperature
            
        else:
            st.warning("Could not load model information from the server.")
            st.session_state.selected_model = None
            st.session_state.temperature = 0.1

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).markdown(msg["content"])

    user_input = st.chat_input("Type your question here...")
    if user_input:
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        model_to_request = getattr(st.session_state, 'selected_model', None)
        temp_to_request = getattr(st.session_state, 'temperature', 0.1)
        
        # Display spinner with the model the user *selected* or *default*
        # The actual model used will be confirmed by the server response
        spinner_model_name = "default model"
        if model_to_request and model_to_request in available_models:
            spinner_model_name = available_models[model_to_request].get('name', model_to_request)
        elif default_model_id_from_server and default_model_id_from_server in available_models:
            spinner_model_name = available_models[default_model_id_from_server].get('name', default_model_id_from_server)

        with st.chat_message("assistant"):
            with st.spinner(f"🤖 Thinking with {spinner_model_name}..."):
                response = ask_question(user_input, model_name=model_to_request, temperature=temp_to_request)
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer", "Sorry, I couldn't find an answer.")
                sources = data.get("source_documents", [])  # This now contains source filenames as strings
                actual_model_used = data.get("actual_model_used", "N/A")
                requested_model = data.get("requested_model", "N/A")
                status_message = data.get("status_message")
                
                # Display status message from server (e.g., fallback notification)
                if status_message:
                    st.info(status_message) # Use st.info, st.warning, or st.success as appropriate
                
                st.markdown(answer)
                if sources:
                    st.markdown("--- ")
                    st.markdown("📄 **Sources:**")
                    for source_file in sources:
                        # sources is now a list of filename strings
                        st.markdown(f"- `{source_file}`")
                
                # Optionally, add model info to the message for clarity, if desired
                # st.caption(f"Answered using: {actual_model_used} (Requested: {requested_model})")

                st.session_state.messages.append({"role": "assistant", "content": answer})
            
            elif response.status_code == 503: # Handle "All models unavailable"
                data = response.json()
                error_msg = data.get("error", "The AI service is currently unavailable. Please try again later.")
                st.error(f"🚨 {error_msg}")
                st.session_state.messages.append({"role": "assistant", "content": f"Error: {error_msg}"})
            else:
                try:
                    error_data = response.json()
                    error_msg = error_data.get("error", response.text) 
                except ValueError: # If response is not JSON
                    error_msg = response.text
                st.error(f"⚠️ Error: {error_msg} (Status: {response.status_code})")
                st.session_state.messages.append({"role": "assistant", "content": f"Error: {error_msg}"})
