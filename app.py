"""
Streamlit Web UI for A/B Testing Analyzer
Interactive dashboard for analyzing A/B test results
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ab_analyzer import ABTestAnalyzer
from mock_database import MockABDatabase, get_sample_experiment, list_available_experiments

# Page configuration
st.set_page_config(
    page_title="A/B Testing Analyzer",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = ABTestAnalyzer()
if 'mock_db' not in st.session_state:
    st.session_state.mock_db = MockABDatabase()

def main():
    st.title("🧪 A/B Testing Analyzer")
    st.markdown("**Comprehensive statistical analysis for your A/B testing experiments**")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    analysis_type = st.sidebar.selectbox(
        "Choose Analysis Type",
        ["Quick Analysis", "Sample Experiments", "Custom Data Upload", "Sample Size Calculator"]
    )
    
    if analysis_type == "Quick Analysis":
        quick_analysis_page()
    elif analysis_type == "Sample Experiments":
        sample_experiments_page()
    elif analysis_type == "Custom Data Upload":
        custom_data_page()
    elif analysis_type == "Sample Size Calculator":
        sample_size_page()

def quick_analysis_page():
    st.header("Quick A/B Test Analysis")
    st.markdown("Enter your experiment data for instant statistical analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Control Group (A)")
        control_visitors = st.number_input("Total Visitors (Control)", min_value=1, value=2400, step=1)
        control_conversions = st.number_input("Conversions (Control)", min_value=0, value=120, step=1, max_value=control_visitors)
        
    with col2:
        st.subheader("Test Group (B)")
        test_visitors = st.number_input("Total Visitors (Test)", min_value=1, value=2300, step=1)
        test_conversions = st.number_input("Conversions (Test)", min_value=0, value=150, step=1, max_value=test_visitors)
    
    # Analysis settings
    st.subheader("Analysis Settings")
    alpha = st.slider("Significance Level (α)", min_value=0.01, max_value=0.10, value=0.05, step=0.01)
    
    if st.button("Analyze Results", type="primary"):
        try:
            results = st.session_state.analyzer.analyze_proportions(
                control_conversions, control_visitors,
                test_conversions, test_visitors,
                alpha
            )
            
            display_results(results)
            
        except ValueError as e:
            st.error(f"Error: {e}")

def sample_experiments_page():
    st.header("Sample Experiments")
    st.markdown("Explore pre-loaded A/B test experiments with realistic data")
    
    # Get experiment list
    experiments = list_available_experiments()
    
    # Create experiment selector
    exp_options = {exp['name']: exp['id'] for exp in experiments}
    selected_exp_name = st.selectbox("Choose an experiment:", list(exp_options.keys()))
    selected_exp_id = exp_options[selected_exp_name]
    
    # Get experiment data
    exp_data = get_sample_experiment(selected_exp_id)
    
    if exp_data:
        # Display experiment info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Status", exp_data['status'].title())
        with col2:
            st.metric("Start Date", exp_data['start_date'])
        with col3:
            st.metric("End Date", exp_data['end_date'])
        
        st.markdown(f"**Description:** {exp_data['description']}")
        
        # Display experiment data
        st.subheader("Experiment Data")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Control Group**")
            st.write(f"Name: {exp_data['control']['name']}")
            st.write(f"Visitors: {exp_data['control']['visitors']:,}")
            st.write(f"Conversions: {exp_data['control']['conversions']:,}")
            st.write(f"Rate: {exp_data['control']['conversion_rate']:.2%}")
            
        with col2:
            st.markdown("**Test Group**")
            st.write(f"Name: {exp_data['test']['name']}")
            st.write(f"Visitors: {exp_data['test']['visitors']:,}")
            st.write(f"Conversions: {exp_data['test']['conversions']:,}")
            st.write(f"Rate: {exp_data['test']['conversion_rate']:.2%}")
        
        # Analyze button
        if st.button("Analyze This Experiment", type="primary"):
            results = st.session_state.analyzer.analyze_proportions(
                exp_data['control']['conversions'],
                exp_data['control']['visitors'],
                exp_data['test']['conversions'],
                exp_data['test']['visitors']
            )
            
            display_results(results, exp_data)

def custom_data_page():
    st.header("Custom Data Upload")
    st.markdown("Upload your own A/B test data for analysis")
    
    # File upload
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.subheader("Data Preview")
            st.dataframe(df.head())
            
            # Column mapping
            st.subheader("Column Mapping")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                variant_col = st.selectbox("Variant Column", df.columns)
            with col2:
                conversion_col = st.selectbox("Conversion Column", df.columns)
            with col3:
                user_id_col = st.selectbox("User ID Column (optional)", ["None"] + list(df.columns))
            
            # Variant values
            unique_variants = df[variant_col].unique()
            if len(unique_variants) == 2:
                control_variant = st.selectbox("Control Variant", unique_variants)
                test_variant = [v for v in unique_variants if v != control_variant][0]
                
                if st.button("Analyze Uploaded Data", type="primary"):
                    # Process data
                    control_data = df[df[variant_col] == control_variant]
                    test_data = df[df[variant_col] == test_variant]
                    
                    control_visitors = len(control_data)
                    control_conversions = control_data[conversion_col].sum()
                    test_visitors = len(test_data)
                    test_conversions = test_data[conversion_col].sum()
                    
                    results = st.session_state.analyzer.analyze_proportions(
                        control_conversions, control_visitors,
                        test_conversions, test_visitors
                    )
                    
                    display_results(results)
            else:
                st.error("Please ensure your data has exactly 2 variants")
                
        except Exception as e:
            st.error(f"Error processing file: {e}")

def sample_size_page():
    st.header("Sample Size Calculator")
    st.markdown("Calculate the required sample size for your A/B test")
    
    col1, col2 = st.columns(2)
    
    with col1:
        baseline_rate = st.number_input("Baseline Conversion Rate", min_value=0.001, max_value=0.999, value=0.05, step=0.001, format="%.3f")
        min_effect = st.number_input("Minimum Detectable Effect", min_value=0.001, max_value=0.5, value=0.01, step=0.001, format="%.3f")
        
    with col2:
        alpha = st.number_input("Significance Level (α)", min_value=0.01, max_value=0.10, value=0.05, step=0.01)
        power = st.number_input("Statistical Power", min_value=0.70, max_value=0.99, value=0.80, step=0.01)
    
    if st.button("Calculate Sample Size", type="primary"):
        sample_size_results = st.session_state.analyzer.sample_size_calculator(
            baseline_rate, min_effect, alpha, power
        )
        
        st.subheader("Sample Size Results")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Per Group", f"{sample_size_results['sample_size_per_group']:,}")
        with col2:
            st.metric("Total Sample", f"{sample_size_results['total_sample_size']:,}")
        with col3:
            st.metric("Effect Size", f"{sample_size_results['effect_size']:.4f}")
        
        # Display assumptions
        st.subheader("Assumptions")
        st.write(f"- Baseline conversion rate: {baseline_rate:.1%}")
        st.write(f"- Expected test conversion rate: {sample_size_results['test_rate']:.1%}")
        st.write(f"- Minimum detectable effect: {min_effect:.1%}")
        st.write(f"- Significance level: {alpha:.1%}")
        st.write(f"- Statistical power: {power:.1%}")

def display_results(results, exp_data=None):
    """Display analysis results with visualizations"""
    
    st.subheader("📊 Analysis Results")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Control Rate", 
            f"{results['control_rate']:.2%}",
            f"{results['conversions']['control']}/{results['sample_sizes']['control']}"
        )
    
    with col2:
        st.metric(
            "Test Rate", 
            f"{results['test_rate']:.2%}",
            f"{results['conversions']['test']}/{results['sample_sizes']['test']}"
        )
    
    with col3:
        delta_color = "normal" if not results['is_significant'] else ("inverse" if results['difference'] < 0 else "normal")
        st.metric(
            "Relative Lift", 
            f"{results['relative_lift_percent']:+.2f}%",
            delta=f"{results['difference']:+.4f}",
            delta_color=delta_color
        )
    
    with col4:
        significance_color = "🟢" if results['is_significant'] else "🔴"
        st.metric(
            "P-value", 
            f"{results['p_value']:.4f}",
            f"{significance_color} {'Significant' if results['is_significant'] else 'Not Significant'}"
        )
    
    # Statistical details
    st.subheader("Statistical Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Test Statistics:**")
        st.write(f"- Z-statistic: {results['z_statistic']:.4f}")
        st.write(f"- P-value: {results['p_value']:.4f}")
        st.write(f"- Significance level: {results['alpha']:.3f}")
        st.write(f"- Statistical power: {results['statistical_power']:.3f}")
    
    with col2:
        st.write("**Confidence Interval (95%):**")
        ci_lower, ci_upper = results['confidence_interval']
        st.write(f"- Lower bound: {ci_lower:.4f}")
        st.write(f"- Upper bound: {ci_upper:.4f}")
        st.write(f"- Contains zero: {'Yes' if ci_lower <= 0 <= ci_upper else 'No'}")
    
    # Interpretation
    st.subheader("Interpretation")
    
    if results['is_significant']:
        if results['difference'] > 0:
            st.success(f"✅ **Significant Improvement**: {results['interpretation']}")
        else:
            st.error(f"❌ **Significant Decline**: {results['interpretation']}")
    else:
        st.warning(f"⚠️ **No Significant Difference**: {results['interpretation']}")
    
    # Visualizations
    st.subheader("Visualizations")
    
    # Conversion rate comparison
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Conversion Rate Comparison', 'Confidence Interval'),
        specs=[[{"type": "bar"}, {"type": "scatter"}]]
    )
    
    # Bar chart
    fig.add_trace(
        go.Bar(
            x=['Control', 'Test'],
            y=[results['control_rate'], results['test_rate']],
            marker_color=['#1f77b4', '#ff7f0e'],
            text=[f"{results['control_rate']:.2%}", f"{results['test_rate']:.2%}"],
            textposition='auto',
            name='Conversion Rate'
        ),
        row=1, col=1
    )
    
    # Confidence interval
    ci_lower, ci_upper = results['confidence_interval']
    fig.add_trace(
        go.Scatter(
            x=[results['difference']],
            y=[0],
            error_x=dict(
                type='data',
                symmetric=False,
                array=[ci_upper - results['difference']],
                arrayminus=[results['difference'] - ci_lower]
            ),
            mode='markers',
            marker=dict(size=10, color='red'),
            name='Difference'
        ),
        row=1, col=2
    )
    
    # Add vertical line at zero
    fig.add_vline(x=0, line_dash="dash", line_color="gray", row=1, col=2)
    
    fig.update_layout(height=400, showlegend=False)
    fig.update_xaxes(title_text="Variant", row=1, col=1)
    fig.update_yaxes(title_text="Conversion Rate", row=1, col=1)
    fig.update_xaxes(title_text="Difference in Conversion Rate", row=1, col=2)
    fig.update_yaxes(title_text="", showticklabels=False, row=1, col=2)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Summary report
    with st.expander("📋 Detailed Report"):
        st.text(st.session_state.analyzer.get_summary_report())

if __name__ == "__main__":
    main()
