import streamlit as st
from abc import ABC, abstractmethod

# Base class for all UI components
class UIComponent(ABC):
    def __init__(self, title):
        self.title = title
        self._state = {}
    
    @abstractmethod
    def render(self):
        pass
    
    def update_state(self, key, value):
        self._state[key] = value
    
    def get_state(self, key):
        return self._state.get(key)

# Concrete implementation of a form component
class FormComponent(UIComponent):
    def __init__(self, title, fields):
        super().__init__(title)
        self.fields = fields
    
    def render(self):
        with st.form(key=self.title.lower().replace(" ", "_")):
            st.subheader(self.title)
            
            for field in self.fields:
                if field["type"] == "text":
                    self._state[field["name"]] = st.text_input(
                        field["label"], 
                        value=self.get_state(field["name"]) or ""
                    )
                elif field["type"] == "number":
                    self._state[field["name"]] = st.number_input(
                        field["label"],
                        value=self.get_state(field["name"]) or 0
                    )
                elif field["type"] == "select":
                    self._state[field["name"]] = st.selectbox(
                        field["label"],
                        options=field["options"],
                        index=field["options"].index(self.get_state(field["name"])) 
                        if self.get_state(field["name"]) in field["options"] else 0
                    )
            
            submitted = st.form_submit_button("Submit")
            if submitted:
                st.success("Form submitted successfully!")
                st.json(self._state)

# App class to compose and manage components
class OOPStreamlitApp:
    def __init__(self):
        self.components = []
    
    def add_component(self, component):
        self.components.append(component)
    
    def run(self):
        st.set_page_config(page_title="OOP Streamlit Demo", layout="wide")
        st.title("Object-Oriented Programming with Streamlit")
        
        for component in self.components:
            component.render()

# Example usage
if __name__ == "__main__":
    app = OOPStreamlitApp()
    
    # Create a registration form
    registration_fields = [
        {"name": "username", "label": "Username", "type": "text"},
        {"name": "email", "label": "Email", "type": "text"},
        {"name": "age", "label": "Age", "type": "number"},
        {"name": "gender", "label": "Gender", "type": "select", 
         "options": ["Male", "Female", "Other", "Prefer not to say"]}
    ]
    registration_form = FormComponent("Registration Form", registration_fields)
    
    # Create a survey form
    survey_fields = [
        {"name": "satisfaction", "label": "Satisfaction Level", "type": "select",
         "options": ["Very Satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very Dissatisfied"]},
        {"name": "feedback", "label": "Your Feedback", "type": "text"}
    ]
    survey_form = FormComponent("Customer Survey", survey_fields)
    
    # Add components to the app
    app.add_component(registration_form)
    app.add_component(survey_form)
    
    # Run the app
    app.run()

    import streamlit as st
import re

class AuthenticatedComponent(UIComponent):
    def __init__(self, title, required_roles=None):
        super().__init__(title)
        self._required_roles = required_roles or []
        self.__auth_token = None  # Private variable
    
    def set_auth_token(self, token):
        # Basic validation
        if not isinstance(token, str) or len(token) < 10:
            raise ValueError("Invalid token format")
        self.__auth_token = token
    
    def _validate_role(self, user_roles):
        """Protected method for role validation"""
        return any(role in self._required_roles for role in user_roles)
    
    def render(self):
        if not self.__auth_token:
            st.error("Authentication required")
            return
        
        # In a real app, you would validate the token here
        user_roles = ["admin"]  # Simulated roles
        
        if self._required_roles and not self._validate_role(user_roles):
            st.error("Insufficient permissions")
            return
        
        st.success(f"Authenticated as {', '.join(user_roles)}")
        self._render_authenticated_content()
    
    @abstractmethod
    def _render_authenticated_content(self):
        pass

class AdminDashboard(AuthenticatedComponent):
    def __init__(self):
        super().__init__("Admin Dashboard", required_roles=["admin"])
    
    def _render_authenticated_content(self):
        st.title("Admin Dashboard")
        st.write("Sensitive admin operations go here")
        
        if st.button("Delete All Data (Danger)"):
            st.error("This would delete all data in a real app")

# Update the main app to include authentication
class SecureOOPStreamlitApp(OOPStreamlitApp):
    def __init__(self):
        super().__init__()
        self.__secret_key = "complex_secret_key_123"
        # Set page config immediately when class is initialized
        st.set_page_config(page_title="Secure OOP Streamlit Demo", layout="wide")
    
    def run(self):
        # Rest of your code
        if "authenticated" not in st.session_state:
            st.title("Login")  # Now this comes AFTER set_page_config
            # ...
    
    def run(self):
        st.set_page_config(page_title="Secure OOP Streamlit Demo", layout="wide")
        
        # Login form
        if "authenticated" not in st.session_state:
            st.title("Login")
            
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Login")
                
                if submitted:
                    if self._validate_login(username, password):
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
            return
        
        # If authenticated, show the main app
        st.title(f"Welcome, {st.session_state.username}!")
        super().run()

# Example usage
if __name__ == "__main__":
    app = SecureOOPStreamlitApp()
    
    # Add regular components
    survey_fields = [
        {"name": "feedback", "label": "Your Feedback", "type": "text"}
    ]
    survey_form = FormComponent("Customer Survey", survey_fields)
    app.add_component(survey_form)
    
    # Add authenticated component
    admin_dashboard = AdminDashboard()
    admin_dashboard.set_auth_token("valid_token_1234567890")
    app.add_component(admin_dashboard)
    
    # Run the app
    app.run()

    class EnhancedFormComponent(FormComponent):
        def __init__(self, title, fields, description=None, help_texts=None):
            super().__init__(title, fields)
            self.description = description
            self.help_texts = help_texts or {}
            self._validations = {}
    
    def add_validation(self, field_name, validation_fn, error_message):
        if field_name not in self._validations:
            self._validations[field_name] = []
        self._validations[field_name].append((validation_fn, error_message))
    
    def render(self):
        with st.form(key=self.title.lower().replace(" ", "_")):
            st.subheader(self.title)
            
            if self.description:
                st.markdown(self.description)
            
            for field in self.fields:
                help_text = self.help_texts.get(field["name"], "")
                
                if field["type"] == "text":
                    self._state[field["name"]] = st.text_input(
                        field["label"], 
                        value=self.get_state(field["name"]) or "",
                        help=help_text
                    )
                elif field["type"] == "number":
                    self._state[field["name"]] = st.number_input(
                        field["label"],
                        value=self.get_state(field["name"]) or 0,
                        help=help_text
                    )
                elif field["type"] == "select":
                    self._state[field["name"]] = st.selectbox(
                        field["label"],
                        options=field["options"],
                        index=field["options"].index(self.get_state(field["name"])) 
                        if self.get_state(field["name"]) in field["options"] else 0,
                        help=help_text
                    )
            
            submitted = st.form_submit_button("Submit")
            if submitted:
                if self._validate_form():
                    st.success("Form submitted successfully!")
                    st.json(self._state)
    
    def _validate_form(self):
        is_valid = True
        for field_name, validations in self._validations.items():
            field_value = self._state.get(field_name)
            for validation_fn, error_message in validations:
                if not validation_fn(field_value):
                    st.error(f"{field_name}: {error_message}")
                    is_valid = False
        return is_valid

# Example usage in the app
if __name__ == "__main__":
    app = SecureOOPStreamlitApp()
    
    # Create an enhanced registration form with validations
    def validate_email(email):
        return re.match(r"^[^@]+@[^@]+\.[^@]+$", email) is not None
    
    registration_fields = [
        {"name": "username", "label": "Username", "type": "text"},
        {"name": "email", "label": "Email", "type": "text"},
        {"name": "age", "label": "Age", "type": "number"},
    ]
    
    help_texts = {
        "username": "Must be 3-20 characters, letters and numbers only",
        "email": "Must be a valid email address",
        "age": "Must be between 18 and 120"
    }
    
    registration_form = EnhancedFormComponent(
        "Enhanced Registration", 
        registration_fields,
        description="Please fill out all fields carefully.",
        help_texts=help_texts
    )
    
    # Add validations
    registration_form.add_validation(
        "username",
        lambda x: re.match(r"^[a-zA-Z0-9_]{3,20}$", x),
        "Username must be 3-20 characters (letters, numbers, underscores)"
    )
    
    registration_form.add_validation(
        "email",
        validate_email,
        "Please enter a valid email address"
    )
    
    registration_form.add_validation(
        "age",
        lambda x: 18 <= x <= 120,
        "Age must be between 18 and 120"
    )
    
    app.add_component(registration_form)
    app.run()