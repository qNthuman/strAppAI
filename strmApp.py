import streamlit as st

# Add a title for the app
st.title("📘 AI Study Assistant – JEE & IAT")

# Create a sidebar for page navigation
st.sidebar.title("Navigation")
pages = ["Notes", "DPP Log", "Daily Log", "Mock Test Log", "DPP Dashboard", "Mock Test Analysis", "Daily Study Plan"]
page = st.sidebar.radio("Choose a page", pages)

# Based on the selection, navigate to the appropriate page
if page == "Notes":
    import pages.notes
elif page == "DPP Log":
    import pages.dpp_log
elif page == "Daily Log":
    import pages.daily_log
elif page == "Mock Test Log":
    import pages.mock_log
elif page == "DPP Dashboard":
    import pages.dpp_dashboard
elif page == "Mock Test Analysis":
    import pages.mock_analysis
elif page == "Daily Study Plan":
    import pages.daily_study_plan
