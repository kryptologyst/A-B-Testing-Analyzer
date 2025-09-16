# A/B Testing Analyzer

A comprehensive statistical analysis tool for A/B testing experiments with an interactive web interface. This tool helps you evaluate whether two variants (A and B) have significantly different performance using proper statistical methods.

## Features

- **Statistical Analysis**: Two-proportion z-tests, t-tests for continuous metrics, confidence intervals
- **Interactive Web UI**: Built with Streamlit for easy data input and visualization
- **Sample Size Calculator**: Determine required sample sizes for your experiments
- **Mock Database**: Pre-loaded sample experiments for testing and learning
- **Data Upload**: Support for custom CSV data uploads
- **Comprehensive Reporting**: Detailed statistical reports with interpretations
- **Visualizations**: Interactive charts using Plotly

## Quick Start

### Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd 0060_A_B_testing_analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

#### Web Interface (Recommended)
```bash
streamlit run app.py
```

#### Command Line Usage
```python
from ab_analyzer import ABTestAnalyzer

# Initialize analyzer
analyzer = ABTestAnalyzer()

# Analyze conversion rates
results = analyzer.analyze_proportions(
    control_conversions=120,
    control_visitors=2400,
    test_conversions=150,
    test_visitors=2300
)

# Print results
print(analyzer.get_summary_report())
```

## Project Structure

```
0060_A_B_testing_analyzer/
├── app.py                 # Streamlit web interface
├── ab_analyzer.py         # Core analysis engine
├── mock_database.py       # Sample data generator
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore           # Git ignore rules
└── 0060.py              # Original simple implementation
```

## Usage Examples

### 1. Quick Analysis
Use the web interface to quickly analyze your A/B test results:
- Enter control and test group data
- Set significance level
- Get instant statistical analysis

### 2. Sample Experiments
Explore pre-loaded experiments:
- E-commerce checkout button color test
- Email subject line optimization
- Landing page layout comparison
- Pricing strategy analysis
- Mobile app onboarding flow

### 3. Custom Data Upload
Upload your own CSV files with columns for:
- Variant (control/test)
- Conversion (0/1)
- User ID (optional)

### 4. Sample Size Planning
Calculate required sample sizes before running experiments:
- Set baseline conversion rate
- Define minimum detectable effect
- Choose significance level and power
- Get sample size recommendations

## Statistical Methods

### Two-Proportion Z-Test
- Compares conversion rates between two groups
- Calculates z-statistic and p-value
- Provides confidence intervals
- Determines statistical significance

### Continuous Metrics Analysis
- T-tests for comparing means
- Effect size calculation (Cohen's d)
- Confidence intervals for differences

### Power Analysis
- Statistical power calculation
- Sample size determination
- Effect size estimation

## Key Metrics Explained

- **Conversion Rate**: Percentage of visitors who completed the desired action
- **Relative Lift**: Percentage improvement of test vs control
- **P-value**: Probability of observing results if no real difference exists
- **Confidence Interval**: Range of plausible values for the true difference
- **Statistical Power**: Probability of detecting a real effect if it exists

## Best Practices

1. **Pre-experiment Planning**:
   - Define success metrics clearly
   - Calculate required sample size
   - Set significance level (typically 0.05)

2. **During Experiment**:
   - Avoid peeking at results too frequently
   - Ensure random assignment
   - Monitor for external factors

3. **Post-experiment Analysis**:
   - Check statistical assumptions
   - Consider practical significance
   - Account for multiple comparisons

## API Reference

### ABTestAnalyzer Class

#### `analyze_proportions(control_conversions, control_visitors, test_conversions, test_visitors, alpha=0.05)`
Analyze conversion rate differences using two-proportion z-test.

**Parameters:**
- `control_conversions` (int): Number of conversions in control group
- `control_visitors` (int): Total visitors in control group  
- `test_conversions` (int): Number of conversions in test group
- `test_visitors` (int): Total visitors in test group
- `alpha` (float): Significance level (default 0.05)

**Returns:** Dictionary with analysis results

#### `analyze_continuous(control_values, test_values, alpha=0.05)`
Analyze continuous metrics using t-test.

#### `sample_size_calculator(baseline_rate, minimum_detectable_effect, alpha=0.05, power=0.8)`
Calculate required sample size for experiment.

#### `get_summary_report()`
Generate formatted text report of analysis results.

## Dependencies

- **streamlit**: Web interface framework
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **scipy**: Statistical functions
- **statsmodels**: Advanced statistical models
- **matplotlib**: Basic plotting
- **plotly**: Interactive visualizations
- **seaborn**: Statistical data visualization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For questions or issues:
1. Check the documentation above
2. Review sample experiments in the web interface
3. Open an issue on GitHub

## Roadmap

- [ ] Bayesian A/B testing methods
- [ ] Multi-variant testing (A/B/C/D)
- [ ] Sequential testing capabilities
- [ ] Integration with popular analytics platforms
- [ ] Advanced visualization options
- [ ] Automated experiment monitoring

---

**Note**: This tool is for educational and analysis purposes. Always validate results with domain expertise and consider business context when making decisions based on A/B test results.
# A-B-Testing-Analyzer
