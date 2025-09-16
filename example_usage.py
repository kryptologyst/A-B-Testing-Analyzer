"""
Example Usage of A/B Testing Analyzer
Demonstrates various ways to use the analyzer
"""

from ab_analyzer import ABTestAnalyzer
from mock_database import get_sample_experiment, list_available_experiments

def example_basic_analysis():
    """Basic conversion rate analysis example"""
    print("=== Basic A/B Test Analysis ===")
    
    # Initialize analyzer
    analyzer = ABTestAnalyzer()
    
    # Sample data: testing checkout button colors
    control_conversions = 120
    control_visitors = 2400
    test_conversions = 150
    test_visitors = 2300
    
    # Run analysis
    results = analyzer.analyze_proportions(
        control_conversions, control_visitors,
        test_conversions, test_visitors
    )
    
    # Print summary
    print(analyzer.get_summary_report())
    print("\n" + "="*50 + "\n")

def example_sample_size_calculation():
    """Sample size calculation example"""
    print("=== Sample Size Calculator ===")
    
    analyzer = ABTestAnalyzer()
    
    # Calculate required sample size
    sample_size = analyzer.sample_size_calculator(
        baseline_rate=0.05,  # 5% baseline conversion
        minimum_detectable_effect=0.01,  # Want to detect 1% improvement
        alpha=0.05,  # 5% significance level
        power=0.80   # 80% power
    )
    
    print(f"Baseline conversion rate: {sample_size['baseline_rate']:.1%}")
    print(f"Expected test conversion rate: {sample_size['test_rate']:.1%}")
    print(f"Minimum detectable effect: {sample_size['minimum_detectable_effect']:.1%}")
    print(f"Required sample size per group: {sample_size['sample_size_per_group']:,}")
    print(f"Total required sample size: {sample_size['total_sample_size']:,}")
    print("\n" + "="*50 + "\n")

def example_continuous_metrics():
    """Continuous metrics analysis example"""
    print("=== Continuous Metrics Analysis ===")
    
    analyzer = ABTestAnalyzer()
    
    # Sample revenue data
    control_revenue = [25.50, 30.20, 15.75, 45.00, 22.30, 35.80, 28.90, 19.60, 42.10, 31.25]
    test_revenue = [28.75, 33.40, 18.90, 48.20, 25.60, 38.95, 32.15, 22.80, 45.30, 34.50]
    
    # Analyze continuous data
    results = analyzer.analyze_continuous(control_revenue, test_revenue)
    
    print(f"Control group mean: ${results['control_mean']:.2f}")
    print(f"Test group mean: ${results['test_mean']:.2f}")
    print(f"Difference: ${results['difference']:.2f}")
    print(f"P-value: {results['p_value']:.4f}")
    print(f"Statistical significance: {results['is_significant']}")
    print(f"Cohen's d (effect size): {results['cohens_d']:.3f}")
    print(f"Interpretation: {results['interpretation']}")
    print("\n" + "="*50 + "\n")

def example_sample_experiments():
    """Demonstrate using sample experiments"""
    print("=== Sample Experiments ===")
    
    # List available experiments
    experiments = list_available_experiments()
    print("Available sample experiments:")
    for exp in experiments:
        print(f"- {exp['name']} ({exp['status']})")
    
    print("\nAnalyzing checkout button experiment:")
    
    # Get specific experiment
    exp_data = get_sample_experiment('checkout_button_color')
    
    # Analyze the experiment
    analyzer = ABTestAnalyzer()
    results = analyzer.analyze_proportions(
        exp_data['control']['conversions'],
        exp_data['control']['visitors'],
        exp_data['test']['conversions'],
        exp_data['test']['visitors']
    )
    
    print(f"\nExperiment: {exp_data['name']}")
    print(f"Description: {exp_data['description']}")
    print(f"Control: {exp_data['control']['name']} - {exp_data['control']['conversion_rate']:.2%}")
    print(f"Test: {exp_data['test']['name']} - {exp_data['test']['conversion_rate']:.2%}")
    print(f"Result: {results['interpretation']}")
    print("\n" + "="*50 + "\n")

def main():
    """Run all examples"""
    print("A/B Testing Analyzer - Example Usage\n")
    
    example_basic_analysis()
    example_sample_size_calculation()
    example_continuous_metrics()
    example_sample_experiments()
    
    print("Examples completed! Try running 'streamlit run app.py' for the web interface.")

if __name__ == "__main__":
    main()
